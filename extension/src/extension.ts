import * as vscode from 'vscode';
import { registerLocalPilotViews } from './views/register';
import { registerLocalPilotCommands } from './commands';
import { COMMAND_IDS } from './ids';
import { InMemoryState, MementoState } from './services/state';
import { registerLocalPilotChat } from './chat';

export function activate(context: vscode.ExtensionContext) {
  const state = context.globalState ? new MementoState(context.globalState) : new InMemoryState();

  const cmd = vscode.commands.registerCommand(COMMAND_IDS.helloWorld, () => {
    void vscode.window.showInformationMessage('LocalPilot ready');
  });
  context.subscriptions.push(cmd);

  registerLocalPilotCommands(context, state);
  registerLocalPilotViews(context, state);
  registerLocalPilotChat(context, state);

  return { state };
}
