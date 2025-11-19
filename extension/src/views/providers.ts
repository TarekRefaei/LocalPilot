import * as vscode from 'vscode';

export class PlansTreeDataProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem | Thenable<vscode.TreeItem> {
    return element;
  }

  getChildren(): vscode.ProviderResult<vscode.TreeItem[]> {
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

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem | Thenable<vscode.TreeItem> {
    return element;
  }

  getChildren(): vscode.ProviderResult<vscode.TreeItem[]> {
    const item = new vscode.TreeItem('Idle', vscode.TreeItemCollapsibleState.None);
    item.tooltip = 'Indexing is idle';
    item.description = 'Start indexing to scan the workspace';
    item.contextValue = 'indexing.idle';
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
