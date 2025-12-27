import type { Plan } from '../../core/entities/plan.entity';

export type ActTaskStatus =
  | 'pending'
  | 'running'
  | 'done'
  | 'failed'
  | 'skipped';

export interface ActTask {
  id: string;
  title: string;
  status: ActTaskStatus;
}

export interface ActSession {
  planId: string;
  planTitle: string;
  tasks: ActTask[];
  currentIndex: number;
}

let session: ActSession | null = null;

export const actState = {
  set(s: ActSession) {
    session = s;
  },
  get() {
    return session;
  },
  // Back-compat: allow legacy service to merge arbitrary fields (e.g., status)
  update(patch: any) {
    if (!session) return;
    session = { ...(session as any), ...(patch as any) } as ActSession;
  },
  // Back-compat: signal if there is any active session
  hasActiveSession(): boolean {
    return !!session;
  },
  updateTask(id: string, status: ActTaskStatus) {
    if (!session) return;
    const t = session.tasks.find(t => t.id === id);
    if (t) t.status = status;
  },
  advance() {
    if (session) session.currentIndex++;
  },
  clear() {
    session = null;
  }
};
