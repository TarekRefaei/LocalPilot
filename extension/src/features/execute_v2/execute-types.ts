import type { ExecutionStatus } from '../../domain/execution.status';

export interface BackendExecution {
  execution_id: string;
  plan_id: string;
  status: ExecutionStatus;
  current_task_id?: string;
  tasks?: Array<{ task_id: string; title: string }>;
}
