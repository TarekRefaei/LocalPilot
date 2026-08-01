import type { Task } from './task.entity';
/**
 * Represents an implementation plan.
 *
 * ===============================
 * PLAN CONTRACT — P0 (FROZEN)
 * ===============================
 *
 * Invariants:
 * - A Plan is a deterministic description of file-level changes.
 * - Tasks are executed strictly by ascending orderIndex.
 * - A Plan MAY be invalid while in 'draft' status.
 * - A Plan MUST be approved before it can be executed.
 * - A Plan MUST NOT be modified after approval.
 *
 * Non-goals (future phases):
 * - Workspace awareness (P2)
 * - Auto-repair or intelligence (P3+)
 */
export interface Plan {
  /** Unique plan ID */
  id: string;
  /** Plan title */
  title: string;
  /** Brief description/overview */
  overview: string;
  /** List of tasks to execute */
  tasks: Task[];
  /** Current plan status */
  status: PlanStatus;
}

export type PlanStatus =
  | 'draft'
  | 'approved';
