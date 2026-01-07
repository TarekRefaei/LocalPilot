export const TASK_STATUSES = [
  'pending',
  'running',
  'done',
  'failed',
  'skipped',
] as const;

export type TaskStatus = typeof TASK_STATUSES[number];
