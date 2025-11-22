import * as vscode from 'vscode';
import type { Plan } from '../models/plan';
import { createPlan } from '../models/plan';

function isPlanV2(x: unknown): x is Plan {
  return (
    typeof x === 'object' &&
    x !== null &&
    'steps' in (x as Record<string, unknown>) &&
    'acceptance' in (x as Record<string, unknown>) &&
    'version' in (x as Record<string, unknown>)
  );
}

interface LegacyPlan {
  id: string | number;
  title: string;
}
function isLegacyPlan(x: unknown): x is LegacyPlan {
  if (typeof x !== 'object' || x === null) return false;
  const r = x as Record<string, unknown>;
  const hasId = 'id' in r && (typeof r.id === 'string' || typeof r.id === 'number');
  const hasTitle = 'title' in r && typeof r.title === 'string';
  return hasId && hasTitle;
}

export interface LocalPilotState {
  readonly onDidChange: vscode.Event<void>;
  getPlans(): readonly Plan[];
  getIndexingRunning(): boolean;
  getRecentPrompts(): readonly string[];
  setPlans(plans: Plan[]): void;
  setIndexingRunning(value: boolean): void;
  setRecentPrompts(list: string[]): void;
}

export class InMemoryState implements LocalPilotState {
  private _onDidChange = new vscode.EventEmitter<void>();
  readonly onDidChange = this._onDidChange.event;

  private plans: Plan[] = [];
  private indexingRunning = false;
  private recentPrompts: string[] = [];

  getPlans(): readonly Plan[] {
    return this.plans;
  }

  getIndexingRunning(): boolean {
    return this.indexingRunning;
  }

  setPlans(plans: Plan[]): void {
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
    const rawPlans = (this.m.get<unknown>(this.K_PLANS) ?? []) as unknown[];
    const plans: Plan[] = Array.isArray(rawPlans)
      ? (() => {
          const out: Plan[] = [];
          for (const entry of rawPlans) {
            if (isPlanV2(entry)) {
              out.push(entry);
            } else if (isLegacyPlan(entry)) {
              out.push(createPlan({ id: String(entry.id), title: entry.title }));
            }
          }
          return out;
        })()
      : [];
    const indexing = !!this.m.get<boolean>(this.K_INDEXING);
    const recent = (this.m.get<string[]>(this.K_RECENT) ?? []).filter(Boolean);
    super.setPlans(plans);
    super.setIndexingRunning(indexing);
    super.setRecentPrompts(recent);
  }

  override setPlans(plans: Plan[]): void {
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
