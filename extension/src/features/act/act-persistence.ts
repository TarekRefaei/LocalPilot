import * as vscode from 'vscode';
import type { ActSession } from './act-state';

const STORAGE_KEY = 'localpilot.act.session';

export class ActPersistence {
  constructor(private readonly context: vscode.ExtensionContext) {}

  load(): ActSession | null {
    return this.context.globalState.get<ActSession>(STORAGE_KEY) ?? null;
  }

  save(session: ActSession) {
    this.context.globalState.update(STORAGE_KEY, session);
  }

  clear() {
    this.context.globalState.update(STORAGE_KEY, undefined);
  }
}
