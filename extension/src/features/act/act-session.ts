import type { ExecutableTask, ActSessionStatus } from './act-types';

export interface ActSession {
  sessionId: string;
  planId: string;
  status: ActSessionStatus;
  currentTaskIndex: number;
  tasks: ExecutableTask[];
  startedAt: number;
  lastUpdatedAt: number;
}
