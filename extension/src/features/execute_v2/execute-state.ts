export interface ExecutionUIState {
  executionId: string;
  planTitle: string;
  status: 'idle' | 'ready' | 'awaiting_human' | 'applied' | 'error';
  currentTask?: string;
  diff?: string;
}

let state: ExecutionUIState | null = null;

export const executionState = {
  set(s: ExecutionUIState) { state = s; },
  get() { return state; },
  clear() { state = null; }
};
