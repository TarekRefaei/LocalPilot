import type { Plan } from '../../core/entities/plan.entity';
import type { ValidationWarning } from './plan-validator';

export interface StoredPlan {
  id: string;
  title: string;
  markdown: string;
  plan: Plan | null;
  status: 'draft' | 'approved' | 'acting';
  warnings: ValidationWarning[];
  createdAt: number;
}

interface PlanRegistryState {
  plans: StoredPlan[];
  selectedPlanIds: Set<string>;
}

class PlanRegistry {
  private state: PlanRegistryState = {
    plans: [],
    selectedPlanIds: new Set(),
  };

  getPlans(): StoredPlan[] {
    return [...this.state.plans];
  }

  getPlan(id: string): StoredPlan | undefined {
    return this.state.plans.find((p) => p.id === id);
  }

  addPlan(plan: StoredPlan) {
    this.state.plans.unshift(plan);
    this.state.selectedPlanIds.clear();
    this.state.selectedPlanIds.add(plan.id);
  }

  removePlan(id: string) {
    this.state.plans = this.state.plans.filter((p) => p.id !== id);
    this.state.selectedPlanIds.delete(id);
  }

  select(id: string, multi = false) {
    if (!multi) this.state.selectedPlanIds.clear();
    this.state.selectedPlanIds.add(id);
  }

  deselect(id: string) {
    this.state.selectedPlanIds.delete(id);
  }

  getSelected(): StoredPlan[] {
    return this.state.plans.filter((p) => this.state.selectedPlanIds.has(p.id));
  }

  update(id: string, patch: Partial<StoredPlan>) {
    const p = this.getPlan(id);
    if (!p) return;
    Object.assign(p, patch);
  }

  clear() {
    this.state.plans = [];
    this.state.selectedPlanIds.clear();
  }
}

export const planRegistry = new PlanRegistry();
