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
}

export type TaskActionType = 'create' | 'modify' | 'delete';
