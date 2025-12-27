import * as vscode from 'vscode';
import { planRegistry } from '../plan/plan-registry';
import { ActService } from './act-service';

const actService = new ActService();

export async function startActByPlanId(planId?: string) {
  let targetId = planId;

  if (!targetId) {
    const selected = planRegistry.getSelected();
    if (selected.length === 1) {
      targetId = selected[0].id;
    } else {
      const ready = planRegistry
        .getPlans()
        .find(p => p.status === 'approved' && p.plan && (!p.warnings || !p.warnings.length));
      if (ready) targetId = ready.id;
    }
  }

  if (!targetId) {
    vscode.window.showErrorMessage('Plan not found.');
    return;
  }

  const stored = planRegistry.getPlan(targetId);

  if (!stored) {
    vscode.window.showErrorMessage('Plan not found.');
    return;
  }

  if (stored.status !== 'approved' || !stored.plan || (stored.warnings && stored.warnings.length)) {
    vscode.window.showErrorMessage(
      'Plan is not ready for Act Mode. Fix all plan issues first.'
    );
    return;
  }

  if (stored.plan.id !== targetId) {
    vscode.window.showErrorMessage(
      'Internal error: plan identity mismatch. Please revalidate the plan.'
    );
    return;
  }

  try {
    // Lock plan
    planRegistry.update(targetId, { status: 'acting' });
    // Start Act Session BEFORE refresh to ensure view has session
    actService.start(stored.plan);

    // Then refresh and focus
    await vscode.commands.executeCommand('localpilot.plan.refresh');
    await vscode.commands.executeCommand('localpilot.act.refresh');
    await vscode.commands.executeCommand('localpilot.act.focus');
  } catch (err: any) {
    vscode.window.showErrorMessage(err?.message ?? 'Failed to start Act Mode.');
  }
}

export async function runActTask(taskId: string) {
  await actService.runTask(taskId);
}

export async function runAllActTasks() {
  await actService.runAll();
}

export function skipActTask(taskId: string) {
  actService.skip(taskId);
}
