import type { Plan } from '../../core/entities/plan.entity';
import type { Task } from '../../core/entities/task.entity';

export interface ValidationWarning {
  code: string;
  message: string;
  path?: string;
  taskId?: string;
  suggestion?: string;
}

export function validatePlan(plan: Plan | null | undefined): ValidationWarning[] {
  const warnings: ValidationWarning[] = [];
  if (!plan) {
    warnings.push({ code: 'empty_plan', message: 'Plan is empty or could not be parsed.' });
    return warnings;
  }

  if (!Array.isArray(plan.tasks) || plan.tasks.length === 0) {
    warnings.push({ code: 'no_tasks', message: 'Plan has no tasks.' });
    return warnings;
  }

  plan.tasks.forEach((t: Task, idx: number) => {
    if (!t.filePath) {
      warnings.push({
        code: 'missing_file_path',
        message: `Task ${t.id} is missing filePath.`,
        path: `tasks[${idx}].filePath`,
        taskId: t.id,
        suggestion: 'Set filePath to the same file as the previous task.'
      });
    }
    const validActions = ['create', 'modify', 'delete'];
    if (!t.actionType) {
      warnings.push({
        code: 'missing_action_type',
        message: `Task ${t.id} is missing actionType.`,
        path: `tasks[${idx}].actionType`,
        taskId: t.id,
        suggestion: 'Set actionType to create | modify | delete based on intent.'
      });
    } else if (!validActions.includes(t.actionType as any)) {
      warnings.push({
        code: 'invalid_action_type',
        message: `Task ${t.id} has an invalid actionType: ${t.actionType}.`,
        path: `tasks[${idx}].actionType`,
        taskId: t.id,
        suggestion: 'Use a valid actionType, e.g. modify.'
      });
    }
  });

  const order = plan.tasks.map(t => t.orderIndex);
  const sorted = [...order].sort((a, b) => a - b);
  const same = order.every((v, i) => v === sorted[i]);
  if (!same) {
    warnings.push({ code: 'invalid_order', message: 'Task orderIndex values are not in ascending order.' });
  }

  const ids = new Set<string>();
  for (const t of plan.tasks) {
    if (ids.has(t.id)) {
      warnings.push({ code: 'duplicate_task_id', message: `Duplicate task id detected: ${t.id}` });
      break;
    }
    ids.add(t.id);
  }

  return warnings;
}

export function isPlanActReady(plan: Plan | null | undefined, warnings: ValidationWarning[] = []): boolean {
  return !!plan && (warnings?.length ?? 0) === 0;
}
