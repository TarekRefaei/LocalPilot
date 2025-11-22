import * as vscode from 'vscode';
import { COMMAND_IDS, VIEW_CONTAINER_ID } from './ids';
import { LocalPilotState } from './services/state';
import { startIndexing, actDryRun, actApprove, actApply, actRollback } from './services/realtime';
import { createPlan, createStep, Plan } from './models/plan';
import { parsePlanDraft } from './services/planParser';

export function registerLocalPilotCommands(
  context: vscode.ExtensionContext,
  state?: LocalPilotState
): void {
  const d: vscode.Disposable[] = [];

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.showViews, async () => {
      await vscode.commands.executeCommand('setContext', 'localpilot.views.visible', true);
      await vscode.commands.executeCommand(`workbench.view.extension.${VIEW_CONTAINER_ID}`);
      void vscode.window.showInformationMessage('LocalPilot views opened');
    })
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.focusChatInput, async () => {
      // Try to focus the Secondary Side Bar, where Chat usually lives
      try {
        await vscode.commands.executeCommand('workbench.action.focusAuxiliaryBar');
      } catch {
        try {
          await vscode.commands.executeCommand('workbench.action.toggleAuxiliaryBar');
        } catch {
          void 0;
        }
      }

      const candidates: { id: string; args?: unknown[] }[] = [
        { id: 'workbench.action.chat.open', args: ['@localpilot '] },
        { id: 'workbench.action.openChat', args: ['@localpilot '] },
        { id: 'workbench.action.chat.focus' },
        { id: 'workbench.view.chat' },
        { id: 'workbench.panel.chat.view.focus' },
        { id: 'workbench.action.openQuickChat', args: ['@localpilot '] },
        { id: 'workbench.action.chat.start', args: ['@localpilot '] },
      ];

      let opened = false;
      for (const c of candidates) {
        const args = c.args ?? [];
        // execute and coerce to boolean success
        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
        const ok = await vscode.commands.executeCommand(c.id, ...args).then(
          () => true,
          () => false
        );
        if (ok) {
          opened = true;
          break;
        }
      }

      if (!opened) {
        void vscode.window.showWarningMessage(
          'Could not automatically open the Chat view. Open View → Chat, then mention @localpilot.'
        );
      } else {
        void vscode.window.showInformationMessage('Focus Chat input (LocalPilot)');
      }
    })
  );

  d.push(
    vscode.commands.registerCommand(
      COMMAND_IDS.chatTransferToPlan,
      (payload?: { id?: string; title?: string; prompt?: string }) => {
        const id = payload?.id ?? String(Date.now());
        const title = payload?.title ?? 'Draft plan from Chat';
        const parsed = parsePlanDraft(payload?.prompt);
        const draft = createPlan({ id, title, steps: parsed.steps, acceptance: parsed.acceptance });
        const next = [...(state?.getPlans() ?? []), draft];
        state?.setPlans(next);
        void vscode.window.showInformationMessage('Transfer to Plan');
      }
    )
  );

  d.push(
    vscode.commands.registerCommand(
      COMMAND_IDS.planCreate,
      (payload?: { id?: string; title?: string; steps?: number }) => {
        const id = payload?.id ?? String(Date.now());
        const title = payload?.title ?? 'Untitled Plan';
        const base = createPlan({ id, title });
        const stepsCount = Math.max(0, Math.min(10, payload?.steps ?? 0));
        const steps = Array.from({ length: stepsCount }, (_, i) => createStep(`Step ${i + 1}`, i));
        const plan: Plan = { ...base, steps };
        const next = [...(state?.getPlans() ?? []), plan];
        state?.setPlans(next);
        void vscode.window.showInformationMessage('Create Plan');
      }
    )
  );

  d.push(
    vscode.commands.registerCommand(
      COMMAND_IDS.planUpdate,
      (payload?: { id: string; title?: string; status?: Plan['status'] }) => {
        if (!payload?.id) {
          void vscode.window.showInformationMessage('Update Plan');
          return;
        }
        const plans = [...(state?.getPlans() ?? [])];
        const idx = plans.findIndex((p) => p.id === payload.id);
        if (idx >= 0 && idx < plans.length) {
          const prev = plans[idx]!;
          const updated: Plan = {
            ...prev,
            title: payload.title ?? prev.title,
            status: payload.status ?? prev.status,
            updatedAt: new Date().toISOString(),
          };
          plans[idx] = updated;
          state?.setPlans(plans);
        }
        void vscode.window.showInformationMessage('Update Plan');
      }
    )
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.planDelete, (payload?: { id: string }) => {
      if (!payload?.id) {
        void vscode.window.showInformationMessage('Delete Plan');
        return;
      }
      const next = (state?.getPlans() ?? []).filter((p) => p.id !== payload.id);
      state?.setPlans(next);
      void vscode.window.showInformationMessage('Delete Plan');
    })
  );

  // Step operations
  d.push(
    vscode.commands.registerCommand(
      COMMAND_IDS.planStepAdd,
      (payload?: { planId: string; title?: string; index?: number }) => {
        if (!payload?.planId) return;
        const plans = [...(state?.getPlans() ?? [])];
        const idx = plans.findIndex((p) => p.id === payload.planId);
        if (idx < 0) return;
        const plan = plans[idx]!;
        const order = payload.index ?? plan.steps.length;
        const step = createStep(payload.title ?? 'New Step', order);
        const steps = [...plan.steps];
        steps.splice(order, 0, { ...step, order });
        // reassign order
        steps.forEach((s, i) => (s.order = i));
        const updated: Plan = { ...plan, steps, updatedAt: new Date().toISOString() };
        plans[idx] = updated;
        state?.setPlans(plans);
      }
    )
  );

  d.push(
    vscode.commands.registerCommand(
      COMMAND_IDS.planStepToggle,
      (payload?: { planId: string; stepId: string }) => {
        if (!payload?.planId || !payload?.stepId) return;
        const plans = [...(state?.getPlans() ?? [])];
        const idx = plans.findIndex((p) => p.id === payload.planId);
        if (idx < 0) return;
        const plan = plans[idx]!;
        const steps = plan.steps.map((s) =>
          s.id === payload.stepId ? { ...s, done: !s.done } : s
        );
        const updated: Plan = { ...plan, steps, updatedAt: new Date().toISOString() };
        plans[idx] = updated;
        state?.setPlans(plans);
      }
    )
  );

  d.push(
    vscode.commands.registerCommand(
      COMMAND_IDS.planStepMoveUp,
      (payload?: { planId: string; stepId: string }) => {
        if (!payload?.planId || !payload?.stepId) return;
        const plans = [...(state?.getPlans() ?? [])];
        const idx = plans.findIndex((p) => p.id === payload.planId);
        if (idx < 0) return;
        const plan = plans[idx]!;
        const steps = [...plan.steps];
        const i = steps.findIndex((s) => s.id === payload.stepId);
        if (i > 0) {
          const tmp = steps[i - 1]!;
          steps[i - 1] = steps[i]!;
          steps[i] = tmp;
          steps.forEach((s, k) => (s.order = k));
          const updated: Plan = { ...plan, steps, updatedAt: new Date().toISOString() };
          plans[idx] = updated;
          state?.setPlans(plans);
        }
      }
    )
  );

  d.push(
    vscode.commands.registerCommand(
      COMMAND_IDS.planStepMoveDown,
      (payload?: { planId: string; stepId: string }) => {
        if (!payload?.planId || !payload?.stepId) return;
        const plans = [...(state?.getPlans() ?? [])];
        const idx = plans.findIndex((p) => p.id === payload.planId);
        if (idx < 0) return;
        const plan = plans[idx]!;
        const steps = [...plan.steps];
        const i = steps.findIndex((s) => s.id === payload.stepId);
        if (i >= 0 && i < steps.length - 1) {
          const tmp = steps[i + 1]!;
          steps[i + 1] = steps[i]!;
          steps[i] = tmp;
          steps.forEach((s, k) => (s.order = k));
          const updated: Plan = { ...plan, steps, updatedAt: new Date().toISOString() };
          plans[idx] = updated;
          state?.setPlans(plans);
        }
      }
    )
  );

  d.push(
    vscode.commands.registerCommand(
      COMMAND_IDS.planStepDelete,
      (payload?: { planId: string; stepId: string }) => {
        if (!payload?.planId || !payload?.stepId) return;
        const plans = [...(state?.getPlans() ?? [])];
        const idx = plans.findIndex((p) => p.id === payload.planId);
        if (idx < 0) return;
        const plan = plans[idx]!;
        const steps = plan.steps
          .filter((s) => s.id !== payload.stepId)
          .map((s, i) => ({ ...s, order: i }));
        const updated: Plan = { ...plan, steps, updatedAt: new Date().toISOString() };
        plans[idx] = updated;
        state?.setPlans(plans);
      }
    )
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.actDryRun, () => {
      void vscode.window.showInformationMessage('Act: Dry Run');
      void actDryRun({ executionId: String(Date.now()) }).catch(() => void 0);
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.actApprove, () => {
      void vscode.window.showInformationMessage('Act: Approve');
      void actApprove({ executionId: String(Date.now()) }).catch(() => void 0);
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.actApply, () => {
      void vscode.window.showInformationMessage('Act: Apply');
      void actApply({ executionId: String(Date.now()) }).catch(() => void 0);
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.actRollback, () => {
      void vscode.window.showInformationMessage('Act: Rollback');
      void actRollback({ executionId: String(Date.now()) }).catch(() => void 0);
    })
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.indexStart, async () => {
      await vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', true);
      state?.setIndexingRunning(true);
      void vscode.window.showInformationMessage('Indexing: Start');
      // Fire-and-forget start; ignore connection failures in tests
      void startIndexing(state).catch(() => void 0);
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.indexStop, async () => {
      await vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', false);
      state?.setIndexingRunning(false);
      void vscode.window.showInformationMessage('Indexing: Stop');
    })
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.modelSwap, () => {
      void vscode.window.showInformationMessage('Model: Swap');
    })
  );

  d.forEach((x) => context.subscriptions.push(x));
}
