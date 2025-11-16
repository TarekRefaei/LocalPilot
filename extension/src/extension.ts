import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const cmd = vscode.commands.registerCommand('localpilot.helloWorld', () => {
    vscode.window.showInformationMessage('LocalPilot ready');
  });
  context.subscriptions.push(cmd);
}

export function deactivate() {}
