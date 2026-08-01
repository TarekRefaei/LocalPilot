export type PlanStatus = 'draft' | 'approved' | 'acting';

export function canValidate(status: PlanStatus) {
  return status === 'draft';
}

export function canApprove(status: PlanStatus) {
  return status === 'draft';
}

export function canRepair(status: PlanStatus) {
  return status === 'draft';
}

export function canAct(status: PlanStatus, hasWarnings: boolean) {
  return status === 'approved' && !hasWarnings;
}
