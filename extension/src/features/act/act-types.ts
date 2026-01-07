/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import type { Task } from '../../core/entities/task.entity';
import type { Preview } from './diff-generator';
import type { ExecutionStatus } from '../../domain/execution.status';
import type { TaskStatus } from '../../domain/execution.task-status';

// Legacy mapping notes (Act v1 → canonical):
// - error → failed (session)
// - generated → running (task)
// - applied → done (task)
// ActSessionStatus remains compatible by allowing 'idle' + canonical ExecutionStatus.
export type ActSessionStatus = 'idle' | ExecutionStatus;

// TaskExecutionState now aligns with canonical TaskStatus.
// Legacy mapping preserved by adapters where needed:
// - generated ⇒ running
// - applied ⇒ done
// - error ⇒ failed
export type TaskExecutionState = TaskStatus;

export interface ExecutableTask {
  task: Task;
  state: TaskExecutionState;
  preview?: Preview;
  backupPath?: string;
  error?: string;
  generatedContent?: string;
}

