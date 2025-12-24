import type { Plan } from '../../core/entities/plan.entity';
import type { Task } from '../../core/entities/task.entity';

export interface ValidationWarning {
  code: string;
  message: string;
  path?: string;
}

export function validatePlan(plan: Plan | null | undefined): ValidationWarning[] {
  const warnings: ValidationWarning[] = [];
  if (!plan) {
    warnings.push({ code: 'EMPTY_PLAN', message: 'Plan is empty or could not be parsed.' });
    return warnings;
  }

  if (!Array.isArray(plan.tasks) || plan.tasks.length === 0) {
    warnings.push({ code: 'NO_TASKS', message: 'Plan has no tasks.' });
    return warnings;
  }

  plan.tasks.forEach((t: Task, idx: number) => {
    if (!t.filePath) warnings.push({ code: 'MISSING_FILE_PATH', message: `Task ${t.id} is missing filePath.`, path: `tasks[${idx}].filePath` });
    if (!t.actionType) warnings.push({ code: 'MISSING_ACTION_TYPE', message: `Task ${t.id} is missing actionType.`, path: `tasks[${idx}].actionType` });
  });

  const order = plan.tasks.map(t => t.orderIndex);
  const sorted = [...order].sort((a, b) => a - b);
  const same = order.every((v, i) => v === sorted[i]);
  if (!same) {
    warnings.push({ code: 'INVALID_ORDER', message: 'Task orderIndex values are not in ascending order.' });
  }

  const ids = new Set<string>();
  for (const t of plan.tasks) {
    if (ids.has(t.id)) {
      warnings.push({ code: 'DUPLICATE_TASK_ID', message: `Duplicate task id detected: ${t.id}` });
      break;
    }
    ids.add(t.id);
  }

  return warnings;
}
