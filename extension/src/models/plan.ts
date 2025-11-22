export type PlanStatus = 'draft' | 'active' | 'completed';

export interface FileRef {
  path: string;
  startLine?: number;
  endLine?: number;
}

export interface AcceptanceCriterion {
  id: string;
  text: string;
  refs?: FileRef[];
  done?: boolean;
}

export interface PlanStep {
  id: string;
  title: string;
  done: boolean;
  order: number;
  children?: PlanStep[];
}

export interface Plan {
  id: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  status: PlanStatus;
  steps: PlanStep[];
  acceptance: AcceptanceCriterion[];
  version: number;
}

export function nowIso(): string {
  return new Date().toISOString();
}

export function createPlan(params: {
  id: string;
  title: string;
  steps?: PlanStep[];
  acceptance?: AcceptanceCriterion[];
}): Plan {
  const createdAt = nowIso();
  return {
    id: params.id,
    title: params.title,
    createdAt,
    updatedAt: createdAt,
    status: 'draft',
    steps: params.steps ?? [],
    acceptance: params.acceptance ?? [],
    version: 2,
  };
}

export function createStep(title: string, order: number): PlanStep {
  return {
    id: String(Date.now()) + '-' + Math.random().toString(36).slice(2, 8),
    title,
    done: false,
    order,
  };
}
