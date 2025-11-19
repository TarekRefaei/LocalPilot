import * as vscode from 'vscode';

export interface LocalPilotState {
  readonly onDidChange: vscode.Event<void>;
  getPlans(): readonly { id: string; title: string }[];
  getIndexingRunning(): boolean;
}

export class InMemoryState implements LocalPilotState {
  private _onDidChange = new vscode.EventEmitter<void>();
  readonly onDidChange = this._onDidChange.event;

  private plans: { id: string; title: string }[] = [];
  private indexingRunning = false;

  getPlans(): readonly { id: string; title: string }[] {
    return this.plans;
  }

  getIndexingRunning(): boolean {
    return this.indexingRunning;
  }

  setPlans(plans: { id: string; title: string }[]): void {
    this.plans = [...plans];
    this._onDidChange.fire();
  }

  setIndexingRunning(value: boolean): void {
    this.indexingRunning = value;
    this._onDidChange.fire();
  }
}
