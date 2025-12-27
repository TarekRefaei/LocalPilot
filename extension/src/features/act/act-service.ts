import { actState } from './act-state';
import type { Plan } from '../../core/entities/plan.entity';
import * as vscode from 'vscode';
import { planRegistry } from '../plan/plan-registry';
import { executeTask } from './act-executor.js';
import { applyDiff } from './act-apply.js';

// Phase 4.7 backbone: simplified execution state and actions

export class ActService {
  start(plan: Plan) {
    actState.set({
      planId: plan.id,
      planTitle: (plan as any).title ?? 'Plan',
      currentIndex: 0,
      tasks: [...plan.tasks]
        .sort((a, b) => a.orderIndex - b.orderIndex)
        .map(t => ({ id: t.id, title: t.title, status: 'pending' as const }))
    });
  }

  // Legacy run/pause/resume no-ops retained for compatibility
  run() {}
  pause() {}
  resume() {}

  async runTask(taskId: string) {
    const s = actState.get();
    if (!s) return;

    const plan = planRegistry.getPlan(s.planId)?.plan;
    if (!plan) throw new Error('Plan missing');
    const task = plan.tasks.find(t => t.id === taskId);
    if (!task) throw new Error('Task missing');

    actState.updateTask(taskId, 'running');
    await vscode.commands.executeCommand('localpilot.act.refresh');

    try {
      const root = vscode.workspace.workspaceFolders?.[0]?.uri;
      if (!root) throw new Error('No workspace folder is open.');

      const diff = await executeTask(task as any, root);
      const applied = await applyDiff(diff);
      if (!applied) {
        actState.updateTask(taskId, 'skipped');
        return;
      }

      actState.updateTask(taskId, 'done');
    } catch {
      actState.updateTask(taskId, 'failed');
    }

    await vscode.commands.executeCommand('localpilot.act.refresh');
  }

  async runAll() {
    const s = actState.get();
    if (!s) return;
    for (const t of s.tasks) {
      if (t.status !== 'pending') continue;
      await this.runTask(t.id);
      const updated = actState.get();
      const after = updated?.tasks.find(x => x.id === t.id);
      if (after?.status === 'failed') break;
    }
    try {
      await vscode.commands.executeCommand('localpilot.index.sync');
    } catch {}
  }

  skip(taskId: string) {
    actState.updateTask(taskId, 'skipped');
  }

  cancel() {
    actState.clear();
  }
}
