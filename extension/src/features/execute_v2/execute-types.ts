export interface BackendExecution {
  execution_id: string;
  plan_id: string;
  status: string;
  current_task_id?: string;
  tasks?: Array<{ task_id: string; title: string }>;
}
