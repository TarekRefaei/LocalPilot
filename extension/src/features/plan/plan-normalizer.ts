import { normalizeFilePath } from '../../domain/plan.paths';

export interface PlanLintWarning {
  message: string;
  taskId?: string;
  field?: string;
}

export function normalizePlan(plan: any): {
  plan: any;
  warnings: PlanLintWarning[];
  changed: boolean;
} {
  const warnings: PlanLintWarning[] = [];
  let changed = false;

  if (!plan?.tasks) {
    return { plan, warnings, changed };
  }

  for (const task of plan.tasks) {
    if (!task.filePath) continue;

    const original = task.filePath;
    task.filePath = normalizeFilePath(task.filePath);

    if (original !== task.filePath) {
      warnings.push({
        taskId: task.id,
        field: 'filePath',
        message: `Absolute path normalized to '${task.filePath}'`,
      });
      changed = true;
    }

    // Script file safety hint
    if (task.filePath.endsWith('.py') && task.details) {
      task.details.push(
        'If this file is a script, print results instead of returning them.'
      );
      changed = true;
    }
  }

  return { plan, warnings, changed };
}
