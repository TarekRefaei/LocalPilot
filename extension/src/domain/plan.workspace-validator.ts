import type { Plan } from '../core/entities/plan.entity';
import type { ValidationWarning } from '../features/plan/plan-validator';
import { ValidationCode } from './plan.validation';
import type { WorkspaceSnapshot } from './workspace.snapshot';

export function validatePlanAgainstWorkspace(
  plan: Plan,
  workspace: WorkspaceSnapshot
): ValidationWarning[] {
  const warnings: ValidationWarning[] = [];

  for (const task of plan.tasks) {
    const filePath = task.filePath;

    if (filePath.startsWith('..')) {
      warnings.push({
        code: ValidationCode.PATH_OUTSIDE_WORKSPACE,
        message: `Task ${task.id} targets a path outside the workspace.`,
        taskId: task.id,
      });
      continue;
    }

    const exists = workspace.existingFiles.has(filePath);

    if (task.actionType === 'create' && exists) {
      warnings.push({
        code: ValidationCode.FILE_ALREADY_EXISTS,
        message: `Cannot CREATE '${filePath}' because it already exists.`,
        taskId: task.id,
        suggestion: 'Change actionType to MODIFY.',
      });
    }

    if ((task.actionType === 'modify' || task.actionType === 'delete') && !exists) {
      warnings.push({
        code: ValidationCode.FILE_NOT_FOUND,
        message: `Cannot ${task.actionType.toUpperCase()} '${filePath}' because it does not exist.`,
        taskId: task.id,
      });
    }

    if (
      task.actionType === 'modify' &&
      workspace.indexedFiles.size > 0 &&
      !workspace.indexedFiles.has(filePath)
    ) {
      warnings.push({
        code: ValidationCode.FILE_NOT_INDEXED,
        message: `File '${filePath}' is not indexed; modifications may be unsafe.`,
        taskId: task.id,
      });
    }
  }

  return warnings;
}
