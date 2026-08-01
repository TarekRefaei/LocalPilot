/**
 * PLAN MODE — FINALIZED (P4)
 * Any changes require a new phase.
 */

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
import { validatePlanAgainstWorkspace } from '../../domain/plan.workspace-validator';
import { buildWorkspaceSnapshot } from '../../infrastructure/workspace/workspace-scanner';
import { isBlockingValidationCode } from '../../domain/plan.validation';
import { requestPlanRepair } from '../../infrastructure/http/plan-repair-client';
import { canApprove, canRepair, canValidate } from '../../domain/plan.lifecycle';
import { analyzePlanStructure } from '../../infrastructure/http/plan-structure-client';
import { requestPlanRefinement } from '../../infrastructure/http/plan-refine-client';

function genId(): string {
  const rnd = (globalThis as any).crypto?.randomUUID?.();
  return rnd || (Math.random().toString(36).slice(2) + Date.now().toString(36));
}

function isBlockingWarningCode(code: string): boolean {
  return isBlockingValidationCode(code as any);
}

function replaceJsonBlock(markdown: string, json: any): string {
  const block = `\`\`\`json\n${JSON.stringify(json, null, 2)}\n\`\`\``;

  if (!/```json[\s\S]*?```/i.test(markdown)) {
    return `${(markdown || '').trim()}\n\n${block}\n`;
  }

  return (markdown || '').replace(/```json[\s\S]*?```/i, block);
}

function withBlockingFlag(warnings: ValidationWarning[]): ValidationWarning[] {
  return (warnings || []).map(w => ({
    ...w,
    blocking: isBlockingValidationCode(w.code as any),
  }));
}

function summarizeRepair(before: any, after: any) {
  const changes: string[] = [];
  try {
    const beforeTasks = (before?.tasks || []) as any[];
    const afterTasks = (after?.tasks || []) as any[];
    beforeTasks.forEach((t: any, i: number) => {
      const r = afterTasks[i];
      if (!t || !r) return;
      if (t.actionType !== r.actionType) {
        changes.push(`Task ${t.id}: actionType ${t.actionType} → ${r.actionType}`);
      }
      if (t.filePath !== r.filePath) {
        changes.push(`Task ${t.id}: filePath ${t.filePath} → ${r.filePath}`);
      }
    });
  } catch {
    // ignore
  }
  return changes;
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
    const mapped = (res.warnings || []).map(w => ({ code: 'auto_fix', message: w, blocking: false }));
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
  if (!canValidate(stored.status as any)) {
    vscode.window.showWarningMessage('Only draft plans can be validated.');
    return;
  }
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
  let structuralIssues: any[] = [];
  try {
    structuralIssues = await analyzePlanStructure(norm.plan);
  } catch {
    structuralIssues = [];
  }
  const normAsValidation: ValidationWarning[] = (norm.warnings || []).map(w => ({
    code: 'normalized_path',
    message: w.message,
    taskId: w.taskId,
    path: w.field ? `tasks[].${w.field}` : undefined,
  }));

  let workspaceWarnings: ValidationWarning[] = [];
  if (!structural.length) {
    try {
      const snapshot = await buildWorkspaceSnapshot([]);
      workspaceWarnings = validatePlanAgainstWorkspace(norm.plan, snapshot);
    } catch {
      // If no workspace folder is open, workspace-aware validation can't run.
      // Keep structural warnings only.
    }
  }

  const warnings: ValidationWarning[] = withBlockingFlag([...normAsValidation, ...workspaceWarnings]);

  planRegistry.update(stored.id, {
    plan: { ...norm.plan, id: stored.id },
    warnings,
    structuralIssues,
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

  if (!canApprove(stored.status as any)) {
    vscode.window.showWarningMessage('Only draft plans can be approved.');
    return;
  }

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

  let workspaceWarnings: ValidationWarning[] = [];
  try {
    const snapshot = await buildWorkspaceSnapshot([]);
    workspaceWarnings = validatePlanAgainstWorkspace(norm.plan, snapshot);
  } catch {
    workspaceWarnings = [];
  }

  if (workspaceWarnings.some(w => isBlockingWarningCode(w.code))) {
    vscode.window.showWarningMessage('Plan cannot be approved due to workspace validation errors.');
    planRegistry.update(stored.id, {
      plan: { ...norm.plan, id: stored.id },
      warnings: withBlockingFlag([...(norm.warnings || []).map(w => ({ code: 'normalized_path', message: w.message, taskId: w.taskId, path: w.field ? `tasks[].${w.field}` : undefined })) as any, ...workspaceWarnings]),
      status: 'draft',
    });
    await vscode.commands.executeCommand('localpilot.plan.refresh');
    return;
  }

  const approved = approvePlan({ ...norm.plan, id: stored.id });
  planRegistry.update(stored.id, {
    markdown: stored.markdown,
    plan: approved,
    status: 'approved',
    warnings: withBlockingFlag([...(norm.warnings || []).map(w => ({ code: 'normalized_path', message: w.message, taskId: w.taskId, path: w.field ? `tasks[].${w.field}` : undefined })) as any, ...workspaceWarnings]),
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

export async function updatePlanMarkdownById(planId: string, markdown: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;
  planRegistry.update(planId, {
    markdown: markdown || '',
    plan: null,
    status: 'draft',
    warnings: [],
  });
  await vscode.commands.executeCommand('localpilot.plan.refresh');
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

export async function fixPlanById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored || !stored.markdown || !stored.plan) {
    vscode.window.showWarningMessage('No valid plan available to fix.');
    return;
  }

  if (!canRepair(stored.status as any)) {
    vscode.window.showWarningMessage('Only draft plans can be repaired.');
    return;
  }

  if (!stored.structuralIssues || !stored.structuralIssues.length) {
    vscode.window.showWarningMessage('No structural issues to fix.');
    return;
  }

  try {
    const result = await requestPlanRefinement(stored.plan, stored.structuralIssues);

    const repairedPlan = result?.repairedPlan;
    if (!repairedPlan) {
      vscode.window.showErrorMessage('Plan refinement failed: missing repaired plan.');
      return;
    }

    const repairedMarkdown = replaceJsonBlock(stored.markdown, repairedPlan);
    const diff = buildPlanFixDiff(stored.markdown, repairedMarkdown);

    const doc = await vscode.workspace.openTextDocument({
      content: diff,
      language: 'diff',
    });
    await vscode.window.showTextDocument(doc, { preview: true });

    const choice = await vscode.window.showInformationMessage(
      'Apply AI repair as a new draft plan?',
      'Apply',
      'Cancel'
    );
    if (choice !== 'Apply') return;

    planRegistry.addPlan({
      id: genId(),
      title: stored.title + ' (repaired)',
      markdown: repairedMarkdown,
      plan: repairedPlan,
      status: 'draft',
      warnings: [],
      createdAt: Date.now(),
    });

    vscode.window.showInformationMessage('New repaired draft plan created.');
    await vscode.commands.executeCommand('localpilot.plan.refresh');
  } catch (err: any) {
    vscode.window.showErrorMessage(`Plan refinement failed: ${err?.message ?? err}`);
  }
}

/* ---------------------------
   Per-plan actions (3.C-3)
---------------------------- */
export async function validatePlanById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;

  if (!canValidate(stored.status as any)) {
    vscode.window.showWarningMessage('Only draft plans can be validated.');
    return;
  }

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

  let workspaceWarnings: ValidationWarning[] = [];
  if (!structural.length) {
    try {
      const snapshot = await buildWorkspaceSnapshot([]);
      workspaceWarnings = validatePlanAgainstWorkspace(norm.plan, snapshot);
    } catch {
      workspaceWarnings = [];
    }
  }

  const warnings: ValidationWarning[] = withBlockingFlag([...normAsValidation, ...structural, ...workspaceWarnings]);

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

  if (!canApprove(stored.status as any)) {
    vscode.window.showWarningMessage('Only draft plans can be approved.');
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

  let workspaceWarnings: ValidationWarning[] = [];
  try {
    const snapshot = await buildWorkspaceSnapshot([]);
    workspaceWarnings = validatePlanAgainstWorkspace(norm.plan, snapshot);
  } catch {
    workspaceWarnings = [];
  }

  if (workspaceWarnings.some(w => isBlockingWarningCode(w.code))) {
    vscode.window.showWarningMessage('Plan cannot be approved due to workspace validation errors.');
    planRegistry.update(planId, {
      plan: {
        ...norm.plan,
        id: planId,
      },
      warnings: withBlockingFlag([...normAsValidation, ...workspaceWarnings]),
      status: 'draft',
    });
    await vscode.commands.executeCommand('localpilot.plan.refresh');
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
    warnings: withBlockingFlag([...normAsValidation, ...workspaceWarnings]),
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
