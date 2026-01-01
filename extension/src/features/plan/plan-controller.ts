import * as vscode from 'vscode';
import { generatePlan } from './plan-client';
import { openPlanView } from './plan-view-controller';
import { isIndexed } from '../../infrastructure/http/api-client';
import { getActiveProjectId } from '../../core/project-context';
import { parsePlanMarkdown } from './plan-parser';
import { validatePlan, type ValidationWarning } from './plan-validator';
import { normalizePlan } from './plan-normalizer';
import { buildPlanFixDiff } from './plan-diff';
import { approvePlan } from './plan-approval';
import { planRegistry } from './plan-registry';
import { autoFixPlanPreview } from '../../infrastructure/http/api-client';

function genId(): string {
  const rnd = (globalThis as any).crypto?.randomUUID?.();
  return rnd || (Math.random().toString(36).slice(2) + Date.now().toString(36));
}

export async function autoFixPreviewById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;
  if (!stored.markdown) {
    vscode.window.showWarningMessage('No plan markdown to auto-fix.');
    return;
  }

  try {
    const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspace) {
      vscode.window.showErrorMessage('No workspace folder open.');
      return;
    }
    const res = await autoFixPlanPreview(stored.markdown, workspace);
    // Preview unified diff
    const doc = await vscode.workspace.openTextDocument({ content: res.diff, language: 'diff' });
    await vscode.window.showTextDocument(doc, { preview: true });

    // Surface warnings inline in the Plan view without mutating plan/markdown
    const mapped = (res.warnings || []).map(w => ({ code: 'auto_fix', message: w }));
    planRegistry.update(planId, { warnings: mapped as any });
    await vscode.commands.executeCommand('localpilot.plan.refresh');

    if (mapped.length) {
      vscode.window.showInformationMessage(`Auto-fix preview generated with ${mapped.length} warning(s).`);
    } else {
      vscode.window.showInformationMessage('Auto-fix preview generated.');
    }
  } catch (err: any) {
    vscode.window.showErrorMessage(`Auto-fix preview failed: ${err?.message ?? err}`);
  }
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
    await openPlanView(markdown, id);
  } catch (err: any) {
    vscode.window.showErrorMessage(
      `Failed to generate plan: ${err?.message ?? err}`
    );
  }
}

export async function validateCurrentPlan() {
  const selected = planRegistry.getSelected();
  if (selected.length !== 1) {
    vscode.window.showWarningMessage('Select a single plan to validate.');
    return;
  }
  const stored = selected[0];
  if (!stored.markdown) {
    vscode.window.showWarningMessage('No plan to validate.');
    return;
  }

  const parsed = parsePlanMarkdown(stored.markdown);
  if (!parsed.plan) {
    vscode.window.showErrorMessage('Plan JSON is invalid or missing.');
    return;
  }

  const norm = normalizePlan(parsed.plan as any);
  const structural = validatePlan(norm.plan);
  const normAsValidation: ValidationWarning[] = (norm.warnings || []).map(w => ({
    code: 'normalized_path',
    message: w.message,
    taskId: w.taskId,
    path: w.field ? `tasks[].${w.field}` : undefined,
  }));
  const warnings: ValidationWarning[] = [...normAsValidation, ...structural];

  planRegistry.update(stored.id, {
    plan: { ...norm.plan, id: stored.id },
    warnings,
    status: 'draft',
  });

  if (norm.changed) {
    vscode.window.showInformationMessage('Plan paths were normalized to workspace-relative paths.');
    try {
      const diff = buildPlanFixDiff(stored.markdown, JSON.stringify(norm.plan, null, 2));
      const doc = await vscode.workspace.openTextDocument({ content: diff, language: 'diff' });
      await vscode.window.showTextDocument(doc, { preview: true });
    } catch {}
  }

  vscode.window.showInformationMessage(
    warnings.length
      ? `Plan validated with ${warnings.length} warning(s).`
      : 'Plan validated successfully.'
  );
  await vscode.commands.executeCommand('localpilot.plan.refresh');
}

export async function approveCurrentPlan() {
  const selected = planRegistry.getSelected();
  if (selected.length !== 1) {
    vscode.window.showWarningMessage('Select a single plan to approve.');
    return;
  }
  const stored = selected[0];

  if (!stored.plan || (stored.warnings || []).some(w => (w.code || '').startsWith('auto_fix'))) {
    vscode.window.showWarningMessage('Plan must be auto-fixed before approval.');
    return;
  }

  const parsed = parsePlanMarkdown(stored.markdown);
  if (!parsed.plan) {
    vscode.window.showErrorMessage('Cannot approve: plan JSON is invalid.');
    return;
  }

  const norm = normalizePlan(parsed.plan as any);
  if (norm.changed) {
    vscode.window.showInformationMessage('Plan paths were normalized to workspace-relative paths.');
    try {
      const diff = buildPlanFixDiff(stored.markdown, JSON.stringify(norm.plan, null, 2));
      const doc = await vscode.workspace.openTextDocument({ content: diff, language: 'diff' });
      await vscode.window.showTextDocument(doc, { preview: true });
    } catch {}
  }

  const structural = validatePlan(norm.plan);
  if (structural.length) {
    vscode.window.showWarningMessage('Cannot approve: plan has validation warnings.');
    return;
  }

  const approved = approvePlan({ ...norm.plan, id: stored.id });
  planRegistry.update(stored.id, {
    markdown: stored.markdown,
    plan: approved,
    status: 'approved',
    warnings: (norm.warnings || []).map(w => ({ code: 'normalized_path', message: w.message, taskId: w.taskId, path: w.field ? `tasks[].${w.field}` : undefined })) as any,
  });

  await vscode.commands.executeCommand('localpilot.plan.refresh');
  vscode.window.showInformationMessage('Plan validated and approved.');
  vscode.window.showInformationMessage('Note: If target files change, execution will require regeneration.');
}

export async function discardCurrentPlan() {
  const selected = planRegistry.getSelected();
  if (!selected.length) return;
  for (const p of selected) {
    planRegistry.removePlan(p.id);
  }
  await vscode.commands.executeCommand('localpilot.plan.refresh');
  vscode.window.showInformationMessage('Plan discarded.');
}

export async function regeneratePlan(messages: any[]) {
  const choice = await vscode.window.showWarningMessage(
    'Regenerating will create a new plan based on the current chat.',
    { modal: true },
    'Regenerate'
  );
  if (choice !== 'Regenerate') return;
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
  await openPlanView(plan.markdown, plan.id);
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

  // Normalize paths to workspace-relative
  const norm = normalizePlan(parsed.plan as any);

  // Structural validation
  const structural = validatePlan(norm.plan);
  const normAsValidation: ValidationWarning[] = (norm.warnings || []).map(w => ({
    code: 'normalized_path',
    message: w.message,
    taskId: w.taskId,
    path: w.field ? `tasks[].${w.field}` : undefined,
  }));
  const warnings: ValidationWarning[] = [...normAsValidation, ...structural];

  planRegistry.update(planId, {
    plan: {
      ...norm.plan,
      id: planId,
    },
    warnings,
    status: 'draft',
  });

  if (norm.changed) {
    vscode.window.showInformationMessage(
      'Plan paths were normalized to workspace-relative paths.'
    );
    try {
      const diff = buildPlanFixDiff(
        stored.markdown,
        JSON.stringify(norm.plan, null, 2)
      );
      const doc = await vscode.workspace.openTextDocument({ content: diff, language: 'diff' });
      await vscode.window.showTextDocument(doc, { preview: true });
    } catch {}
  }

  vscode.window.showInformationMessage(
    warnings.length
      ? `Plan validated with ${warnings.length} warning(s).`
      : 'Plan validated successfully.'
  );
  await vscode.commands.executeCommand('localpilot.plan.refresh');
}

// Removed: fixPlanJsonById — frontend auto-mutation is disallowed; rely on backend auto-fix preview

export async function approvePlanById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) {
    vscode.window.showErrorMessage('Plan not found.');
    return;
  }

  // Approval must require auto-fix pass and parsed plan present
  if (!stored.plan || (stored.warnings || []).some(w => (w.code || '').startsWith('auto_fix'))) {
    vscode.window.showWarningMessage('Plan must be auto-fixed before approval.');
    return;
  }

  const parsed = parsePlanMarkdown(stored.markdown);
  if (!parsed.plan) {
    vscode.window.showErrorMessage('Cannot approve: plan JSON is invalid.');
    return;
  }

  // Normalize before approval
  const norm = normalizePlan(parsed.plan as any);
  if (norm.changed) {
    vscode.window.showInformationMessage(
      'Plan paths were normalized to workspace-relative paths.'
    );
    try {
      const diff = buildPlanFixDiff(
        stored.markdown,
        JSON.stringify(norm.plan, null, 2)
      );
      const doc = await vscode.workspace.openTextDocument({ content: diff, language: 'diff' });
      await vscode.window.showTextDocument(doc, { preview: true });
    } catch {}
  }

  const structural = validatePlan(norm.plan);
  const normAsValidation: ValidationWarning[] = (norm.warnings || []).map(w => ({
    code: 'normalized_path',
    message: w.message,
    taskId: w.taskId,
    path: w.field ? `tasks[].${w.field}` : undefined,
  }));
  if (structural.length) {
    vscode.window.showWarningMessage(
      'Cannot approve: plan has validation warnings.'
    );
    return;
  }

  const approved = approvePlan({
    ...norm.plan,
    id: planId, // enforce identity
  });

  // Sync back into registry authoritatively
  planRegistry.update(planId, {
    markdown: stored.markdown,
    plan: approved,
    status: 'approved',
    warnings: normAsValidation,
  });

  await vscode.commands.executeCommand('localpilot.plan.refresh');
  vscode.window.showInformationMessage('Plan validated and approved.');
  vscode.window.showInformationMessage(
    'Note: If target files change, execution will require regeneration.'
  );
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
