import * as vscode from 'vscode';
import type { LocalPilotState } from '../services/state';
import type { Plan } from '../models/plan';
import { COMMAND_IDS } from '../ids';

type PlansElement = vscode.TreeItem & { planId?: string; stepId?: string };

export class PlansTreeDataProvider implements vscode.TreeDataProvider<PlansElement> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
  private state: LocalPilotState | undefined;

  constructor(state?: LocalPilotState) {
    this.state = state;
    this.state?.onDidChange(() => this._onDidChangeTreeData.fire());
  }

  getTreeItem(element: PlansElement): vscode.TreeItem | Thenable<vscode.TreeItem> {
    return element;
  }

  getChildren(element?: PlansElement): vscode.ProviderResult<PlansElement[]> {
    const plans = (this.state?.getPlans() ?? []) as Plan[];
    if (!element) {
      if (plans.length > 0) {
        return plans.map((p) => {
          const it = new vscode.TreeItem(
            p.title,
            vscode.TreeItemCollapsibleState.Collapsed
          ) as PlansElement;
          it.id = p.id;
          it.planId = p.id;
          it.contextValue = 'plans.plan';
          return it;
        });
      }
      const item = new vscode.TreeItem(
        'No plans yet',
        vscode.TreeItemCollapsibleState.None
      ) as PlansElement;
      item.tooltip = 'No plans yet';
      item.description = 'Create a plan from chat or the command palette';
      item.contextValue = 'plans.empty';
      return [item];
    }

    if (element.contextValue === 'plans.plan' && element.planId) {
      const plan = plans.find((p) => p.id === element.planId);
      const steps = plan?.steps ?? [];
      return steps.map((s) => {
        const prefix = s.done ? '$(check) ' : '';
        const it = new vscode.TreeItem(
          prefix + s.title,
          vscode.TreeItemCollapsibleState.None
        ) as PlansElement;
        it.planId = element.planId!;
        it.stepId = s.id;
        it.contextValue = 'plans.step';
        it.tooltip = s.done ? 'Completed' : 'Pending';
        it.command = {
          command: COMMAND_IDS.planStepToggle,
          title: 'Toggle Step',
          arguments: [{ planId: element.planId!, stepId: s.id }],
        } satisfies vscode.Command;
        return it;
      });
    }

    return [];
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
