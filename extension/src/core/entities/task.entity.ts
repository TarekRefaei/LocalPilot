/**
 * Represents a single task in a plan
 */
export interface Task {
  /** Unique task ID */
  id: string;
  /** Order in the plan (0-based) */
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
  /** Current task status */
  status: TaskStatus;
  /** Generated code (after code generation) */
  generatedCode?: string;
  /** Diff for modify actions */
  diff?: string;
  /** Error message if failed */
  error?: string;
  /** Execution timestamps */
  startedAt?: Date;
  completedAt?: Date;
}

export type TaskActionType = 'create' | 'modify' | 'delete';

export type TaskStatus =
  | 'pending'
  | 'running'
  | 'awaiting-approval'
  | 'done'
  | 'skipped'
  | 'error';
