import * as vscode from 'vscode';
import { VIEW_IDS } from '../ids';
import {
  PlansTreeDataProvider,
  ActTreeDataProvider,
  IndexingTreeDataProvider,
  StatusTreeDataProvider,
} from './providers';

export function registerLocalPilotViews(context: vscode.ExtensionContext): void {
  const plans = new PlansTreeDataProvider();
  const act = new ActTreeDataProvider();
  const indexing = new IndexingTreeDataProvider();
  const status = new StatusTreeDataProvider();

  context.subscriptions.push(
    vscode.window.registerTreeDataProvider(VIEW_IDS.plans, plans),
    vscode.window.registerTreeDataProvider(VIEW_IDS.act, act),
    vscode.window.registerTreeDataProvider(VIEW_IDS.indexing, indexing),
    vscode.window.registerTreeDataProvider(VIEW_IDS.status, status)
  );
}
