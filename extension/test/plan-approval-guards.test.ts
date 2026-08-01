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

vi.mock('../src/infrastructure/workspace/workspace-scanner', () => {
  return {
    buildWorkspaceSnapshot: vi.fn(),
  };
});

import * as vscode from 'vscode';
import { planRegistry } from '../src/features/plan/plan-registry';
import { approvePlanById } from '../src/features/plan/plan-controller';
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

function mdFromPlan(plan: any) {
  return '```json\n' + JSON.stringify(plan, null, 2) + '\n```';
}

beforeEach(() => {
  planRegistry.clear();
  vi.clearAllMocks();

  (buildWorkspaceSnapshot as any).mockResolvedValue({
    rootPath: 'c:/repo',
    existingFiles: new Set(['a.py']),
    indexedFiles: new Set([]),
  });
});

describe('approvePlanById guards', () => {
  it('cannot approve when blocking workspace warnings exist', async () => {
    planRegistry.addPlan({
      id: 'p_block',
      title: 'Test',
      markdown: mdFromPlan(basePlan),
      plan: basePlan,
      status: 'draft',
      warnings: [],
      createdAt: Date.now(),
    });

    await approvePlanById('p_block');

    const stored = planRegistry.getPlan('p_block');
    expect(stored?.status).toBe('draft');
    expect((vscode.window.showWarningMessage as any).mock.calls.length).toBeGreaterThanOrEqual(1);
  });
});
