import type { ExecutionStatus } from './execution.status';

/**
 * Derives UI-visible status from backend status and flags without inventing new states.
 * - backend running + awaiting approval → 'running'
 * - backend failed → 'failed'
 * - backend completed → 'completed'
 * - paused passes through
 */
export function deriveUIStatus(
  backendStatus: ExecutionStatus,
  hasError: boolean,
  awaitingApproval: boolean
): ExecutionStatus {
  if (backendStatus === 'failed') return 'failed';
  if (backendStatus === 'completed') return 'completed';
  if (backendStatus === 'paused') return 'paused';
  // running: regardless of awaitingApproval or hasError, UI shows 'running';
  // actual gating is handled by UI controls using the flags, not the label.
  return 'running';
}
