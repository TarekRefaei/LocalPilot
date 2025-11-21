import * as vscode from 'vscode';
import type { LocalPilotState } from '../services/state';

export class PlansTreeDataProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
  private state: LocalPilotState | undefined;

  constructor(state?: LocalPilotState) {
    this.state = state;
    this.state?.onDidChange(() => this._onDidChangeTreeData.fire());
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem | Thenable<vscode.TreeItem> {
    return element;
  }

  getChildren(): vscode.ProviderResult<vscode.TreeItem[]> {
    const plans = this.state?.getPlans() ?? [];
    if (plans.length > 0) {
      return plans.map((p) => {
        const it = new vscode.TreeItem(p.title, vscode.TreeItemCollapsibleState.None);
        it.contextValue = 'plans.item';
        return it;
      });
    }
    const item = new vscode.TreeItem('No plans yet', vscode.TreeItemCollapsibleState.None);
    item.tooltip = 'No plans yet';
    item.description = 'Create a plan from chat or the command palette';
    item.contextValue = 'plans.empty';
    return [item];
  }
}

export class ActTreeDataProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem | Thenable<vscode.TreeItem> {
    return element;
  }

  getChildren(): vscode.ProviderResult<vscode.TreeItem[]> {
    const item = new vscode.TreeItem('Ready to act', vscode.TreeItemCollapsibleState.None);
    item.tooltip = 'Ready to act';
    item.description = 'Review and approve actions';
    item.contextValue = 'act.ready';
    return [item];
  }
}

export class IndexingTreeDataProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
  private state: LocalPilotState | undefined;

  constructor(state?: LocalPilotState) {
    this.state = state;
    this.state?.onDidChange(() => this._onDidChangeTreeData.fire());
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem | Thenable<vscode.TreeItem> {
    return element;
  }

  getChildren(): vscode.ProviderResult<vscode.TreeItem[]> {
    const running = this.state?.getIndexingRunning() ?? false;
    const label = running ? 'Running' : 'Idle';
    const item = new vscode.TreeItem(label, vscode.TreeItemCollapsibleState.None);
    item.tooltip = running ? 'Indexing in progress' : 'Indexing is idle';
    item.description = running ? 'Scanning workspace…' : 'Start indexing to scan the workspace';
    item.contextValue = running ? 'indexing.running' : 'indexing.idle';
    return [item];
  }
}

export class StatusTreeDataProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem | Thenable<vscode.TreeItem> {
    return element;
  }

  getChildren(): vscode.ProviderResult<vscode.TreeItem[]> {
    const item = new vscode.TreeItem('All systems nominal', vscode.TreeItemCollapsibleState.None);
    item.tooltip = 'All systems nominal';
    item.description = 'No issues detected';
    item.contextValue = 'status.ok';
    return [item];
  }
}
