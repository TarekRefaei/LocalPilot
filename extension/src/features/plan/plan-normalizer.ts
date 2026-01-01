import * as path from 'path';

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

    // Windows absolute path
    if (/^[A-Za-z]:[\\/]/.test(task.filePath)) {
      task.filePath = path.basename(task.filePath);
    }

    // Unix absolute path
    if (task.filePath.startsWith('/')) {
      task.filePath = path.basename(task.filePath);
    }

    if (original !== task.filePath) {
      warnings.push({
        taskId: task.id,
        field: 'filePath',
        message: `Absolute path normalized to '${task.filePath}'`,
      });
      changed = true;
    }
  }

  return { plan, warnings, changed };
}
