import * as vscode from 'vscode';
import { VIEW_IDS } from '../ids';
import {
  PlansTreeDataProvider,
  ActTreeDataProvider,
  IndexingTreeDataProvider,
  StatusTreeDataProvider,
} from './providers';
import type { LocalPilotState } from '../services/state';
import { ChatViewProvider } from './chatView';

export function registerLocalPilotViews(
  context: vscode.ExtensionContext,
  state?: LocalPilotState
): void {
  // Chat (webview) in LocalPilot container
  try {
    if ('extensionUri' in context && context.extensionUri) {
      const chat = new ChatViewProvider(context.extensionUri, state);
      context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(VIEW_IDS.chat, chat, {
          webviewOptions: { retainContextWhenHidden: true },
        })
      );
      context.subscriptions.push(
        vscode.commands.registerCommand('localpilot.__test.chat.computeState', () => {
          return chat.__testComputeState();
        })
      );
    }
  } catch {
    // ignore in unit tests without full ExtensionContext
  }

  const plans = new PlansTreeDataProvider(state);
  const act = new ActTreeDataProvider();
  const indexing = new IndexingTreeDataProvider(state);
  const status = new StatusTreeDataProvider();

  context.subscriptions.push(
    vscode.window.registerTreeDataProvider(VIEW_IDS.plans, plans),
    vscode.window.registerTreeDataProvider(VIEW_IDS.act, act),
    vscode.window.registerTreeDataProvider(VIEW_IDS.indexing, indexing),
    vscode.window.registerTreeDataProvider(VIEW_IDS.status, status)
  );
}
