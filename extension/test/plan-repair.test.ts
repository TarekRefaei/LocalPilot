import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('vscode', () => {
  return {
    window: {
      showWarningMessage: vi.fn(),
      showInformationMessage: vi.fn(),
      showErrorMessage: vi.fn(),
      showTextDocument: vi.fn(),
    },
    workspace: {
      openTextDocument: vi.fn(async () => ({ uri: { fsPath: 'mem://diff' } })),
    },
    commands: {
      executeCommand: vi.fn(async () => undefined),
    },
  };
});

vi.mock('../src/infrastructure/http/plan-repair-client', () => {
  return {
    requestPlanRepair: vi.fn(),
  };
});

vi.mock('../src/infrastructure/workspace/workspace-scanner', () => {
  return {
    buildWorkspaceSnapshot: vi.fn(),
  };
});

import * as vscode from 'vscode';
import { planRegistry } from '../src/features/plan/plan-registry';
import { fixPlanById } from '../src/features/plan/plan-controller';
import { requestPlanRepair } from '../src/infrastructure/http/plan-repair-client';
import { buildWorkspaceSnapshot } from '../src/infrastructure/workspace/workspace-scanner';

const basePlan = {
  id: 'p1',
  title: 'Test',
  overview: 'Overview',
  status: 'draft',
  tasks: [
    {
      id: 't1',
      orderIndex: 0,
      title: 'Create',
      description: '',
      filePath: 'a.py',
      actionType: 'create',
      details: [],
      dependencies: [],
    },
  ],
} as any;

beforeEach(() => {
  planRegistry.clear();
  vi.clearAllMocks();

  (buildWorkspaceSnapshot as any).mockResolvedValue({
    rootPath: 'c:/repo',
    existingFiles: new Set(['a.py']),
    indexedFiles: new Set([]),
  });
});

describe('fixPlanById', () => {
  it('does not attempt repair without blocking warnings', async () => {
    planRegistry.addPlan({
      id: 'p1',
      title: 'Test',
      markdown: '```json\n{}\n```',
      plan: basePlan,
      status: 'draft',
      warnings: [{ code: 'file_not_indexed', message: 'advisory', blocking: false }],
      createdAt: Date.now(),
    });

    await fixPlanById('p1');

    expect(requestPlanRepair).not.toHaveBeenCalled();
    expect((vscode.window.showInformationMessage as any).mock.calls.length).toBeGreaterThanOrEqual(1);
    expect(planRegistry.getPlan('p1')?.repairAttempts).toBeUndefined();
  });

  it('blocks repair after two failures', async () => {
    planRegistry.addPlan({
      id: 'p2',
      title: 'Test',
      markdown: '```json\n{}\n```',
      plan: basePlan,
      status: 'draft',
      warnings: [{ code: 'file_already_exists', message: 'blocking', blocking: true }],
      repairAttempts: 2,
      createdAt: Date.now(),
    });

    await fixPlanById('p2');

    expect(requestPlanRepair).not.toHaveBeenCalled();
    expect((vscode.window.showErrorMessage as any).mock.calls.length).toBeGreaterThanOrEqual(1);
    expect(planRegistry.getPlan('p2')?.repairAttempts).toBe(2);
  });

  it('does not replace plan if repaired plan still has blocking issues', async () => {
    planRegistry.addPlan({
      id: 'p3',
      title: 'Test',
      markdown: '```json\n{}\n```',
      plan: basePlan,
      status: 'draft',
      warnings: [{ code: 'file_already_exists', message: 'blocking', blocking: true }],
      createdAt: Date.now(),
    });

    // Return an unchanged plan that will still be blocking against workspace (create existing file)
    (requestPlanRepair as any).mockResolvedValue({ ...basePlan });

    await fixPlanById('p3');

    // attempt counted
    expect(planRegistry.getPlan('p3')?.repairAttempts).toBe(1);

    // plan not replaced with a fixed one (still create)
    expect(planRegistry.getPlan('p3')?.plan?.tasks?.[0]?.actionType).toBe('create');

    // error shown
    expect((vscode.window.showErrorMessage as any).mock.calls.length).toBeGreaterThanOrEqual(1);
  });

  it('does not attempt repair when plan is approved', async () => {
    planRegistry.addPlan({
      id: 'p5',
      title: 'Test',
      markdown: '```json\n{}\n```',
      plan: { ...basePlan, status: 'approved' },
      status: 'approved',
      warnings: [{ code: 'file_already_exists', message: 'blocking', blocking: true }],
      createdAt: Date.now(),
    });

    await fixPlanById('p5');

    expect(requestPlanRepair).not.toHaveBeenCalled();
    expect((vscode.window.showWarningMessage as any).mock.calls.length).toBeGreaterThanOrEqual(1);
  });

  it('does not attempt repair when plan is acting', async () => {
    planRegistry.addPlan({
      id: 'p6',
      title: 'Test',
      markdown: '```json\n{}\n```',
      plan: basePlan,
      status: 'acting',
      warnings: [{ code: 'file_already_exists', message: 'blocking', blocking: true }],
      createdAt: Date.now(),
    });

    await fixPlanById('p6');

    expect(requestPlanRepair).not.toHaveBeenCalled();
    expect((vscode.window.showWarningMessage as any).mock.calls.length).toBeGreaterThanOrEqual(1);
  });

  it('replaces plan only when repaired plan is clean (no blocking warnings)', async () => {
    planRegistry.addPlan({
      id: 'p4',
      title: 'Test',
      markdown: '```json\n{}\n```',
      plan: basePlan,
      status: 'draft',
      warnings: [{ code: 'file_already_exists', message: 'blocking', blocking: true }],
      createdAt: Date.now(),
    });

    const repaired = {
      ...basePlan,
      tasks: [{ ...basePlan.tasks[0], actionType: 'modify' }],
    };

    (requestPlanRepair as any).mockResolvedValue(repaired);

    await fixPlanById('p4');

    expect(planRegistry.getPlan('p4')?.repairAttempts).toBe(1);
    expect(planRegistry.getPlan('p4')?.plan?.tasks?.[0]?.actionType).toBe('modify');
    expect(Array.isArray(planRegistry.getPlan('p4')?.repairSummary)).toBe(true);
    expect((vscode.commands.executeCommand as any).mock.calls.flat().includes('localpilot.plan.refresh')).toBe(true);
  });
});
