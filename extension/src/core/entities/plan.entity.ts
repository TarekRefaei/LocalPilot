import type { Task } from './task.entity';
/**
 * Represents an implementation plan
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
