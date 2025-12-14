import * as vscode from 'vscode';
import { MainPanel } from './panels/main-panel';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  MainPanel.register(context);
}

export function deactivate() {}
