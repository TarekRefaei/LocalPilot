import * as vscode from 'vscode';
import { generatePlan } from './plan-client';
import { openPlanView } from './plan-view-controller';
import { isIndexed } from '../../infrastructure/http/api-client';
import { getActiveProjectId } from '../../core/project-context';
import { parsePlanMarkdown } from './plan-parser';
import { validatePlan } from './plan-validator';
import { approvePlan } from './plan-approval';
import { planState } from './plan-state';
import { planRegistry } from './plan-registry';

function genId(): string {
  const rnd = (globalThis as any).crypto?.randomUUID?.();
  return rnd || (Math.random().toString(36).slice(2) + Date.now().toString(36));
}

export async function createPlanFromChat(messages: any[]) {
  try {
    const projectId = getActiveProjectId();

    const indexed = await isIndexed(projectId);
    if (!indexed) {
      vscode.window.showWarningMessage(
        'Project must be indexed before creating a plan.'
      );
      return;
    }

    const markdown = await generatePlan({ projectId, messages });
    const id = genId();
    planRegistry.addPlan({
      id,
      title: 'New Plan',
      markdown,
      plan: null,
      status: 'draft',
      warnings: [],
      createdAt: Date.now(),
    });
    // await openPlanView(markdown);
    await vscode.commands.executeCommand('localpilot.plan.refresh');
    await openPlanView(markdown);
  } catch (err: any) {
    vscode.window.showErrorMessage(
      `Failed to generate plan: ${err?.message ?? err}`
    );
  }
}

export async function validateCurrentPlan() {
  const state = planState.get();
  if (!state.markdown) {
    vscode.window.showWarningMessage('No plan to validate.');
    return;
  }

  const result = parsePlanMarkdown(state.markdown);
  if (!result.plan) {
    vscode.window.showErrorMessage('Plan JSON is invalid or missing.');
    return;
  }

  const warnings = validatePlan(result.plan);
  planState.set({ plan: result.plan, warnings, status: 'draft' });

  vscode.window.showInformationMessage(
    warnings.length
      ? `Plan validated with ${warnings.length} warning(s).`
      : 'Plan validated successfully.'
  );
}

export async function approveCurrentPlan() {
  const state = planState.get();
  if (!state.plan) {
    vscode.window.showWarningMessage('Validate the plan before approval.');
    return;
  }

  const approved = approvePlan(state.plan);
  planState.set({ plan: approved, status: 'approved' });
  vscode.window.showInformationMessage('Plan approved.');
}

export async function discardCurrentPlan() {
  planState.clear();
  vscode.window.showInformationMessage('Plan discarded.');
  await openPlanView('');
}

export async function regeneratePlan(messages: any[]) {
  const state = planState.get();
  if (state.markdown) {
    const choice = await vscode.window.showWarningMessage(
      'Regenerating will replace the current plan.',
      { modal: true },
      'Regenerate'
    );
    if (choice !== 'Regenerate') return;
  }
  await createPlanFromChat(messages);
}


// ------------------------------
// Plan List helpers (read-only)
// ------------------------------
export function getAllPlans() {
  return planRegistry.getPlans();
}

export function selectPlan(planId: string, multi: boolean) {
  planRegistry.select(planId, multi);
}

export async function openPlan(planId: string) {
  const plan = planRegistry.getPlan(planId);
  if (!plan) return;
  await openPlanView(plan.markdown);
}

/* ---------------------------
   Per-plan actions (3.C-3)
---------------------------- */
export async function validatePlanById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;

  const parsed = parsePlanMarkdown(stored.markdown);
  if (!parsed.plan) {
    vscode.window.showErrorMessage('Invalid or missing plan JSON.');
    return;
  }

  const warnings = validatePlan(parsed.plan);
  planRegistry.update(planId, {
    plan: parsed.plan,
    warnings,
    status: 'draft',
  });

  vscode.window.showInformationMessage(
    warnings.length
      ? `Plan validated with ${warnings.length} warning(s).`
      : 'Plan validated successfully.'
  );
  await vscode.commands.executeCommand('localpilot.plan.refresh');
}

export async function approvePlanById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored || !stored.plan) {
    vscode.window.showWarningMessage('Validate plan before approval.');
    return;
  }

  const approved = approvePlan(stored.plan);
  planRegistry.update(planId, {
    plan: approved,
    status: 'approved',
  });

  await vscode.commands.executeCommand('localpilot.plan.refresh');

  vscode.window.showInformationMessage('Plan approved.');
}

export async function discardPlanById(planId: string) {
  planRegistry.removePlan(planId);
  await vscode.commands.executeCommand('localpilot.plan.refresh');
  vscode.window.showInformationMessage('Plan discarded.');
}

export async function regeneratePlanById(planId: string, messages: any[]) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;

  const choice = await vscode.window.showWarningMessage(
    'Regenerating will create a new plan.',
    { modal: true },
    'Regenerate'
  );
  if (choice !== 'Regenerate') return;

  const projectId = getActiveProjectId();
  const markdown = await generatePlan({ projectId, messages });

  planRegistry.addPlan({
    id: genId(),
    title: stored.title + ' (regenerated)',
    markdown,
    plan: null,
    status: 'draft',
    warnings: [],
    createdAt: Date.now(),
  });

  await vscode.commands.executeCommand('localpilot.plan.refresh');
}
