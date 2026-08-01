/**
 * Represents a single task in a plan.
 *
 * ===============================
 * TASK CONTRACT — P0 (FROZEN)
 * ===============================
 *
 * Invariants:
 * - A Task MUST target exactly one filePath.
 * - A Task MUST have exactly one actionType.
 * - A Task MUST be atomic (one logical change).
 * - Dependencies MUST reference task IDs within the same Plan.
 * - Execution order is defined by orderIndex, not array order.
 */
export interface Task {
  /** Unique task ID */
  id: string;
  /** Order in the plan (0-based, authoritative execution order) */
  orderIndex: number;
  /** Short task title */
  title: string;
  /** Detailed description */
  description: string;
  /** File to create/modify/delete */
  filePath: string;
  /** What action to take */
  actionType: TaskActionType;
  /** Additional details/requirements */
  details: string[];
  /** IDs of tasks this depends on */
  dependencies: string[];
  /** Optional expected hash of target file content before applying patch */
  expectedFileHash?: string;
}

export type TaskActionType = 'create' | 'modify' | 'delete';
