import type { ExecutionStatus } from '../../domain/execution.status';

export interface ExecutionUIState {
  executionId: string;
  planTitle: string;

  /** Backend execution status (authoritative) */
  status: ExecutionStatus;

  currentTaskIndex?: number;
  tasks?: ExecutionTaskUI[];

  /** UI-derived capabilities (NOT backend state) */
  canApply?: boolean;
  canSkip?: boolean;
  isMutating?: boolean;
}

export interface ExecutionTaskUI {
  executionTaskId: string;
  title: string;
  filePath: string;
  actionType: string;
  status: 'pending' | 'running' | 'done' | 'failed' | 'skipped';
  lastDiff?: string;
  error?: string;
}

let state: ExecutionUIState | null = null;

export const executionState = {
  set(s: ExecutionUIState) { state = s; },
  get() { return state; },
  clear() { state = null; }
};
