import type { Plan } from '../core/entities/plan.entity';

/**
 * PLAN CONTRACT GUARD — P0
 *
 * This function enforces hard Plan invariants.
 * It MUST remain stable across versions.
 *
 * NOTE:
 * - This does NOT validate workspace correctness.
 * - This does NOT attempt to repair plans.
 */
export function assertPlanContract(plan: Plan): void {
  if (!plan) {
    throw new Error('Plan contract violation: plan is null or undefined.');
  }

  if (!Array.isArray(plan.tasks)) {
    throw new Error('Plan contract violation: tasks must be an array.');
  }

  for (const task of plan.tasks) {
    if (!task.id) {
      throw new Error('Plan contract violation: task.id is required.');
    }
    if (!task.filePath) {
      throw new Error(`Plan contract violation: task ${task.id} has no filePath.`);
    }
    if (!task.actionType) {
      throw new Error(`Plan contract violation: task ${task.id} has no actionType.`);
    }
  }
}
