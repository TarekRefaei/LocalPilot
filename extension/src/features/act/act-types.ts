import type { Task } from '../../core/entities/task.entity';
import type { Preview } from './diff-generator';

export type ActSessionStatus =
  | 'idle'
  | 'running'
  | 'paused'
  | 'completed'
  | 'error';

export type TaskExecutionState =
  | 'pending'
  | 'generated'
  | 'applied'
  | 'skipped'
  | 'error';

export interface ExecutableTask {
  task: Task;
  state: TaskExecutionState;
  preview?: Preview;
  backupPath?: string;
  error?: string;
  generatedContent?: string;
}
