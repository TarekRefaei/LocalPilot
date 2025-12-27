export type ActEvent =
  | { type: 'act:started' }
  | { type: 'act:paused' }
  | { type: 'act:resumed' }
  | { type: 'act:cancelled' }
  | { type: 'act:completed' }
  | { type: 'task:advance'; index: number };
