import * as vscode from 'vscode';
import * as api from './execute-client';
import { executionState, type ExecutionUIState } from './execute-state';
import { planRegistry } from '../plan/plan-registry';
import { validatePlan, isPlanActReady } from '../plan/plan-validator';
import { canAct } from '../../domain/plan.lifecycle';

let pollTimer: NodeJS.Timeout | undefined;
let pollStartedAt = 0;
const POLL_CAP_MS = 10 * 60 * 1000; // 10 minutes
let isMutating = false;

export function startExecutionPolling(executionId: string) {
  stopExecutionPolling();

  pollStartedAt = Date.now();
  pollTimer = setInterval(async () => {
    try {
      const s = executionState.get();
      if (!s) return;

      // Stop polling on terminal states
      if ((['completed', 'failed'] as any).includes(s.status as any)) {
        stopExecutionPolling();
        return;
      }

      // UI no longer uses invented states; polling strategy remains time-capped and mutation-guarded.

      // Cap polling duration in case of a stall
      if (Date.now() - pollStartedAt > POLL_CAP_MS) {
        stopExecutionPolling();
        return;
      }

      // Avoid racing with user-triggered mutations
      if (isMutating) return;

      await refreshExecution(executionId);
    } catch {
      // silent: avoid UI spam
    }
  }, 1500);
}

export function stopExecutionPolling() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = undefined;
  }
}

export async function startPlanExecution(planId?: string) {
  try {
    let targetId = planId;

    // 1) If no planId passed, resolve from selection
    if (!targetId) {
      const selected = planRegistry.getSelected();
      if (selected.length === 1) {
        targetId = selected[0].id;
      }
    }

    // 2) Fallback: first approved plan
    if (!targetId) {
      const approved = planRegistry
        .getPlans()
        .find((p) => p.status === 'approved' && p.plan);
      if (approved) {
        targetId = approved.id;
      }
    }

    // 3) Final guard
    if (!targetId) {
      vscode.window.showErrorMessage('No approved plan selected. Please select a plan first.');
      return;
    }

    const stored = planRegistry.getPlan(targetId);

    if (!stored || !stored.plan) {
      vscode.window.showErrorMessage(`Plan ${targetId} not found or not approved.`);
      return;
    }

    if (stored.status !== 'approved') {
      vscode.window.showErrorMessage(`Plan ${targetId} must be approved before execution.`);
      return;
    }

    if (!canAct(stored.status as any, !!(stored.warnings && stored.warnings.length))) {
      vscode.window.showErrorMessage('Plan is not ready for execution. Resolve plan issues first.');
      return;
    }

    // Optional hard assertion to catch regressions early
    if (!stored.plan || stored.status !== 'approved') {
      throw new Error('Invariant violation: unapproved plan reached execution.');
    }

    // Gate: plan must be act-ready (validated, no auto-fix warnings)
    const warnings = validatePlan(stored.plan);
    if (!isPlanActReady(stored.plan, warnings)) {
      vscode.window.showErrorMessage(
        'Plan is not ready for execution. Resolve validation or auto-fix issues first.'
      );
      return;
    }

    // Start execution
    const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspace) {
      vscode.window.showErrorMessage('No workspace folder open.');
      return;
    }
    const exec = await api.startExecution({
      planId: stored.id,
      markdown: stored.markdown,
      workspaceRoot: workspace,
    });

    executionState.set({
      executionId: exec.execution_id,
      planTitle: stored.title || 'Plan',
      status: 'running',
    });
    vscode.commands.executeCommand('localpilot.execute.refresh');

    await runNext(exec.execution_id);
    startExecutionPolling(exec.execution_id);
    await refreshExecution(exec.execution_id);
  } catch (err: any) {
    vscode.window.showErrorMessage(`Failed to start execution: ${err?.message ?? err}`);
  }
}

export async function approveAndApply() {
  if (isMutating) return;
  isMutating = true;
  try {
    const prev0 = executionState.get();
    if (prev0) executionState.set({ ...prev0, isMutating: true });
    const s = executionState.get();
    if (!s) return;

    await api.applyDiff(s.executionId);
    await api.reindex(s.executionId);

    vscode.window.showInformationMessage('Changes applied');
    await runNext(s.executionId);
    await refreshExecution(s.executionId);
  } catch (err: any) {
    vscode.window.showErrorMessage(`Apply failed: ${err?.message ?? err}`);
  } finally {
    isMutating = false;
    const prev1 = executionState.get();
    if (prev1) executionState.set({ ...prev1, isMutating: false });
  }
}

async function runNext(executionId: string) {
  const res = await api.nextTask(executionId);

  if (res.status === 'completed') {
    executionState.set({
      executionId,
      planTitle: executionState.get()?.planTitle ?? '',
      status: 'completed' as any,
    });
    vscode.commands.executeCommand('localpilot.execute.refresh');
    return;
  }

  // Awaiting approval path: backend remains 'running'; capabilities will be set on refresh
  executionState.set({
    executionId,
    planTitle: executionState.get()?.planTitle ?? '',
    status: 'running' as any,
  });

  vscode.commands.executeCommand('localpilot.execute.refresh');
}

export async function refreshExecution(executionId: string) {
  const data = await api.getExecution(executionId);

  const normalizedTasks = Array.isArray(data.tasks)
    ? data.tasks.map((t: any) => ({
        executionTaskId: t.executionTaskId ?? t.execution_task_id,
        title: t.title,
        filePath: t.filePath ?? t.file_path,
        actionType: t.actionType ?? t.action_type,
        status: t.status,
        lastDiff: t.lastDiff ?? t.last_diff,
        error: t.error,
      }))
    : [];

  const prev = executionState.get();
  const idx = (data.currentTaskIndex ?? data.current_task_index) as number;
  const backendStatus = (data.status ?? 'running') as any;
  const currentTask = Array.isArray(normalizedTasks) ? normalizedTasks[idx] : undefined;
  const hasDiff = !!currentTask?.lastDiff;
  const isTerminalTask =
    currentTask?.status === 'done' || currentTask?.status === 'skipped' || currentTask?.status === 'failed';

  const state: ExecutionUIState = {
    executionId: data.executionId ?? data.execution_id ?? executionId,
    planTitle: data.planTitle ?? data.plan_title ?? '',
    status: backendStatus,
    currentTaskIndex: idx,
    tasks: normalizedTasks,
    isMutating: prev?.isMutating ?? false,
    canApply: backendStatus === 'running' && hasDiff && !isTerminalTask,
    canSkip: backendStatus === 'running' && !isTerminalTask,
  };

  executionState.set(state);

  vscode.commands.executeCommand('localpilot.execute.refresh');
}

export async function resumeExecutionAction() {
  if (isMutating) return;
  isMutating = true;
  try {
    const prev0 = executionState.get();
    if (prev0) executionState.set({ ...prev0, isMutating: true });
    const s = executionState.get();
    if (!s) return;
    await api.resumeExecution(s.executionId);
    await refreshExecution(s.executionId);
  } catch (err: any) {
    vscode.window.showErrorMessage(`Resume failed: ${err?.message ?? err}`);
  } finally {
    isMutating = false;
    const prev1 = executionState.get();
    if (prev1) executionState.set({ ...prev1, isMutating: false });
  }
}

export async function skipTaskAction() {
  if (isMutating) return;
  isMutating = true;
  try {
    const prev0 = executionState.get();
    if (prev0) executionState.set({ ...prev0, isMutating: true });
    const s = executionState.get();
    if (!s) return;
    await api.skipTask(s.executionId);
    await api.nextTask(s.executionId);
    await refreshExecution(s.executionId);
  } catch (err: any) {
    vscode.window.showErrorMessage(`Skip failed: ${err?.message ?? err}`);
  } finally {
    isMutating = false;
    const prev1 = executionState.get();
    if (prev1) executionState.set({ ...prev1, isMutating: false });
  }
}

export async function retryTaskAction() {
  if (isMutating) return;
  isMutating = true;
  try {
    const prev0 = executionState.get();
    if (prev0) executionState.set({ ...prev0, isMutating: true });
    const s = executionState.get();
    if (!s) return;
    await api.retryTask(s.executionId);
    await api.nextTask(s.executionId);
    await refreshExecution(s.executionId);
  } catch (err: any) {
    vscode.window.showErrorMessage(`Retry failed: ${err?.message ?? err}`);
  } finally {
    isMutating = false;
    const prev1 = executionState.get();
    if (prev1) executionState.set({ ...prev1, isMutating: false });
  }
}
