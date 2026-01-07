export const EXECUTION_STATUSES = [
  'running',
  'paused',
  'completed',
  'failed',
] as const;

export type ExecutionStatus = typeof EXECUTION_STATUSES[number];
