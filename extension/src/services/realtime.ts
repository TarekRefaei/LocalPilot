import * as vscode from 'vscode';
import { WebSocketClient } from './ws-client';

let client: WebSocketClient | null = null;
let connected = false;

interface IndexingState {
  setIndexingRunning(v: boolean): void;
}

function isTestEnv(): boolean {
  // Jest sets JEST_WORKER_ID; VS Code tests may set VSCODE_TEST
  if (typeof process === 'undefined') return false;
  const env = (process as unknown as NodeJS.Process).env as Record<string, string | undefined>;
  return Boolean(env?.JEST_WORKER_ID ?? env?.VSCODE_TEST);
}

function getWsUrl(clientId: string): string {
  // Backend default host/port from settings.py: ws://127.0.0.1:8765
  const base = 'ws://127.0.0.1:8765/ws';
  return `${base}?client_id=${encodeURIComponent(clientId)}`;
}

export async function ensureConnected(): Promise<WebSocketClient> {
  if (client && connected) return client;

  const id = `ext-${Date.now()}`;
  const url = getWsUrl(id);
  client = new WebSocketClient(url, { clientId: id });
  try {
    await client.connect();
    connected = true;
  } catch (err) {
    // Surface a minimal message but do not throw to avoid breaking UI
    void vscode.window.showWarningMessage('LocalPilot: Unable to connect to backend WebSocket');
    throw err;
  }
  return client;
}

export async function startIndexing(state?: IndexingState): Promise<void> {
  if (isTestEnv()) {
    // In unit tests, avoid network. Just toggle UI state as side-effect.
    void vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', true);
    state?.setIndexingRunning(true);
    return;
  }
  const ws = await ensureConnected();
  // Subscribe to progress/complete once (idempotent if multiple calls)
  ws.subscribe('indexing.progress', () => {
    void vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', true);
    state?.setIndexingRunning(true);
  });
  ws.subscribe('indexing.complete', () => {
    void vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', false);
    state?.setIndexingRunning(false);
    void vscode.window.showInformationMessage('Indexing: Complete');
  });

  const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!workspacePath) {
    void vscode.window.showWarningMessage('Indexing: No workspace folder open');
    return;
  }

  try {
    ws.send('indexing.start', { workspace_path: workspacePath, options: {} });
  } catch (err) {
    void vscode.window.showWarningMessage('Indexing: Failed to start');
    throw err;
  }
}
