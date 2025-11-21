import * as vscode from 'vscode';
import { COMMAND_IDS, VIEW_CONTAINER_ID } from './ids';
import { LocalPilotState } from './services/state';

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
      (payload?: { id?: string; title?: string }) => {
        const id = payload?.id ?? String(Date.now());
        const title = payload?.title ?? 'Draft plan from Chat';
        const next = [...(state?.getPlans() ?? []), { id, title }];
        state?.setPlans(next);
        void vscode.window.showInformationMessage('Transfer to Plan');
      }
    )
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.planCreate, () => {
      void vscode.window.showInformationMessage('Create Plan');
    })
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.planUpdate, () => {
      void vscode.window.showInformationMessage('Update Plan');
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.planDelete, () => {
      void vscode.window.showInformationMessage('Delete Plan');
    })
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.actDryRun, () => {
      void vscode.window.showInformationMessage('Act: Dry Run');
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.actApprove, () => {
      void vscode.window.showInformationMessage('Act: Approve');
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.actApply, () => {
      void vscode.window.showInformationMessage('Act: Apply');
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.actRollback, () => {
      void vscode.window.showInformationMessage('Act: Rollback');
    })
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.indexStart, async () => {
      await vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', true);
      state?.setIndexingRunning(true);
      void vscode.window.showInformationMessage('Indexing: Start');
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
