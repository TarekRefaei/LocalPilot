import * as vscode from 'vscode';

export interface LocalPilotState {
  readonly onDidChange: vscode.Event<void>;
  getPlans(): readonly { id: string; title: string }[];
  getIndexingRunning(): boolean;
  getRecentPrompts(): readonly string[];
  setPlans(plans: { id: string; title: string }[]): void;
  setIndexingRunning(value: boolean): void;
  setRecentPrompts(list: string[]): void;
}

export class InMemoryState implements LocalPilotState {
  private _onDidChange = new vscode.EventEmitter<void>();
  readonly onDidChange = this._onDidChange.event;

  private plans: { id: string; title: string }[] = [];
  private indexingRunning = false;
  private recentPrompts: string[] = [];

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

  getRecentPrompts(): readonly string[] {
    return this.recentPrompts;
  }

  setRecentPrompts(list: string[]): void {
    this.recentPrompts = [...list];
    this._onDidChange.fire();
  }
}

export class MementoState extends InMemoryState {
  private m: vscode.Memento;
  private readonly K_PLANS = 'localpilot.plans';
  private readonly K_INDEXING = 'localpilot.indexing';
  private readonly K_RECENT = 'localpilot.recentPrompts';

  constructor(memento: vscode.Memento) {
    super();
    this.m = memento;
    const plans = (this.m.get<{ id: string; title: string }[]>(this.K_PLANS) ?? []).filter(Boolean);
    const indexing = !!this.m.get<boolean>(this.K_INDEXING);
    const recent = (this.m.get<string[]>(this.K_RECENT) ?? []).filter(Boolean);
    super.setPlans(plans);
    super.setIndexingRunning(indexing);
    super.setRecentPrompts(recent);
  }

  override setPlans(plans: { id: string; title: string }[]): void {
    super.setPlans(plans);
    void this.m.update(this.K_PLANS, plans);
  }

  override setIndexingRunning(value: boolean): void {
    super.setIndexingRunning(value);
    void this.m.update(this.K_INDEXING, value);
  }

  override setRecentPrompts(list: string[]): void {
    super.setRecentPrompts(list);
    void this.m.update(this.K_RECENT, list);
  }
}
