import * as vscode from 'vscode';
import { COMMAND_IDS, VIEW_CONTAINER_ID } from './ids';

export function registerLocalPilotCommands(context: vscode.ExtensionContext): void {
  const d: vscode.Disposable[] = [];

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.showViews, async () => {
      await vscode.commands.executeCommand('setContext', 'localpilot.views.visible', true);
      await vscode.commands.executeCommand(`workbench.view.extension.${VIEW_CONTAINER_ID}`);
      void vscode.window.showInformationMessage('LocalPilot views opened');
    })
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.focusChatInput, () => {
      void vscode.window.showInformationMessage('Focus Chat input (LocalPilot)');
    })
  );

  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.chatTransferToPlan, () => {
      void vscode.window.showInformationMessage('Transfer to Plan');
    })
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
      void vscode.window.showInformationMessage('Indexing: Start');
    })
  );
  d.push(
    vscode.commands.registerCommand(COMMAND_IDS.indexStop, async () => {
      await vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', false);
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
