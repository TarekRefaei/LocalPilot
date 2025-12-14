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
  /** When the plan was created */
  createdAt: Date;
  /** When the plan was last modified */
  updatedAt: Date;
  /** Current plan status */
  status: PlanStatus;
  /** Original conversation that led to this plan */
  sourceConversationId?: string;
}

export type PlanStatus =
  | 'draft'
  | 'approved'
  | 'executing'
  | 'paused'
  | 'completed'
  | 'cancelled';
