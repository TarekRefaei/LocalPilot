/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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

