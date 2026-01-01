import * as vscode from 'vscode';
import * as api from './execute-client';
import { executionState, type ExecutionUIState } from './execute-state';
import { planRegistry } from '../plan/plan-registry';
import { validatePlan, isPlanActReady } from '../plan/plan-validator';

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
      plan: stored.plan,
      workspaceRoot: workspace,
    });


    const allowed: ExecutionUIState['status'][] = ['idle','ready','awaiting_human','applied','error'];
    const status = (allowed as readonly string[]).includes(exec.status as any)
      ? (exec.status as ExecutionUIState['status'])
      : 'ready';
    executionState.set({
      executionId: exec.execution_id,
      planTitle: stored.title || 'Plan',
      status,
    });
    vscode.commands.executeCommand('localpilot.execute.refresh');

    // Auto-advance: prepare and invoke the first task so we have a diff for approval
    try {
      const full = await api.getExecution(exec.execution_id);
      const tasks: any[] = Array.isArray(full?.tasks) ? full.tasks : [];
      const first = tasks[0];
      const firstId: string | undefined = first?.task_id || first?.id;
      if (firstId) {
        await api.prepareTask(exec.execution_id, firstId);
        const res = await api.invokeTask(exec.execution_id, firstId);
        const current = executionState.get();
        if (current) {
          executionState.set({
            ...current,
            status: 'awaiting_human',
            currentTask: firstId,
            diff: typeof res?.diff === 'string' ? res.diff : JSON.stringify(res?.diff ?? '', null, 2),
          });
        }
        vscode.commands.executeCommand('localpilot.execute.refresh');
      }
    } catch (e: any) {
      vscode.window.showErrorMessage(`Failed to prepare/invoke first task: ${e?.message ?? e}`);
    }
  } catch (err: any) {
    vscode.window.showErrorMessage(`Failed to start execution: ${err?.message ?? err}`);
  }
}

export async function approveAndApply() {
  try {
    const s = executionState.get();
    if (!s) return;

    await api.applyDiff(s.executionId);
    await api.reindex(s.executionId);

    vscode.window.showInformationMessage('Changes applied & indexed');
    executionState.clear();
    vscode.commands.executeCommand('localpilot.execute.refresh');
  } catch (err: any) {
    vscode.window.showErrorMessage(`Apply failed: ${err?.message ?? err}`);
  }
}
