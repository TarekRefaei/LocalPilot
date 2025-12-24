import type { Plan } from '../../core/entities/plan.entity';
import type { ValidationWarning } from './plan-validator';

export interface PlanState {
  markdown: string | null;
  plan: Plan | null;
  status: 'draft' | 'approved';
  warnings: ValidationWarning[];
}

class PlanStateStore {
  private state: PlanState = {
    markdown: null,
    plan: null,
    status: 'draft',
    warnings: [],
  };

  get(): PlanState {
    return this.state;
  }

  set(partial: Partial<PlanState>) {
    this.state = { ...this.state, ...partial };
  }

  clear() {
    this.state = {
      markdown: null,
      plan: null,
      status: 'draft',
      warnings: [],
    };
  }
}

export const planState = new PlanStateStore();
