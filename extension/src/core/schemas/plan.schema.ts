export interface PlanSchema {
  id: string;
  title: string;
  overview: string;
  status: 'draft';
  tasks: TaskSchema[];
}

export interface TaskSchema {
  id: string;
  orderIndex: number;
  title: string;
  description: string;
  filePath: string;
  actionType: 'create' | 'modify' | 'delete';
  details: string[];
  dependencies: string[];
}
