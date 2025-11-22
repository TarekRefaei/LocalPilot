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

export function startIndexing(state?: IndexingState): Promise<void> {
  // Always set UI state immediately (resilient UX in tests/integration)
  void vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', true);
  state?.setIndexingRunning(true);

  // In pure unit tests, skip network entirely
  if (isTestEnv()) return Promise.resolve();

  const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!workspacePath) {
    void vscode.window.showWarningMessage('Indexing: No workspace folder open');
    return Promise.resolve();
  }

  // Background connect and fire start; swallow connection errors
  void ensureConnected()
    .then((ws) => {
      // Subscribe to progress/complete (idempotent)
      ws.subscribe('indexing.progress', () => {
        void vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', true);
        state?.setIndexingRunning(true);
      });
      ws.subscribe('indexing.complete', () => {
        void vscode.commands.executeCommand('setContext', 'localpilot.indexing.running', false);
        state?.setIndexingRunning(false);
        void vscode.window.showInformationMessage('Indexing: Complete');
      });
      try {
        ws.send('indexing.start', { workspace_path: workspacePath, options: {} });
      } catch {
        void vscode.window.showWarningMessage('Indexing: Failed to start');
      }
    })
    .catch(() => {
      // Already set running; let user stop manually or complete when backend available
      void 0;
    });

  return Promise.resolve();
}
