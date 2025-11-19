import * as vscode from 'vscode';
import { registerLocalPilotViews } from './views/register';
import { registerLocalPilotCommands } from './commands';
import { COMMAND_IDS } from './ids';

export function activate(context: vscode.ExtensionContext) {
  const cmd = vscode.commands.registerCommand(COMMAND_IDS.helloWorld, () => {
    void vscode.window.showInformationMessage('LocalPilot ready');
  });
  context.subscriptions.push(cmd);

  registerLocalPilotCommands(context);
  registerLocalPilotViews(context);
}
