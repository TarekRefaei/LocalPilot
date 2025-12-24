import type { Plan } from '../../core/entities/plan.entity';

export function approvePlan(plan: Plan): Plan {
  return { ...plan, status: 'approved' };
}
