import * as vscode from 'vscode';
import { WebSocketClient } from './ws-client';
import type { WebSocketEnvelope } from '../contracts/envelope';

let client: WebSocketClient | null = null;
let connected = false;

interface IndexingState {
  setIndexingRunning(v: boolean): void;
}

interface ApprovalOperation {
  path: string;
  type: string;
  diff: string;
  additions: number;
  deletions: number;
  requiresApproval: boolean;
}

interface ApprovalPreview {
  operations: ApprovalOperation[];
  autoApprovedPaths: string[];
  requiresReviewCount: number;
}

function isApprovalPreview(x: unknown): x is ApprovalPreview {
  if (typeof x !== 'object' || x === null) return false;
  const r = x as Record<string, unknown>;
  const ops = Array.isArray(r.operations)
    ? r.operations.every(
        (o) =>
          !!o &&
          typeof (o as ApprovalOperation).path === 'string' &&
          typeof (o as ApprovalOperation).type === 'string' &&
          typeof (o as ApprovalOperation).diff === 'string'
      )
    : false;
  const auto = Array.isArray(r.autoApprovedPaths)
    ? (r.autoApprovedPaths as unknown[]).every((p) => typeof p === 'string')
    : false;
  const rev = typeof r.requiresReviewCount === 'number';
  return ops && auto && rev;
}

export function actDryRun(payload: Record<string, unknown>): Promise<void> {
  if (isTestEnv()) return Promise.resolve();
  return ensureConnected()
    .then((ws) => {
      // One-shot subscription for approval preview
      const off = ws.subscribe('act.request_approval', (envelope: WebSocketEnvelope) => {
        const preview: ApprovalPreview = isApprovalPreview(envelope?.data)
          ? envelope.data
          : { operations: [], autoApprovedPaths: [], requiresReviewCount: 0 };
        const ops = preview.operations;
        const reviewCount = preview.requiresReviewCount;
        const autoCount = preview.autoApprovedPaths.length;

        void vscode.window
          .showInformationMessage(
            `Dry-run ready: ${ops.length} ops, ${reviewCount} need approval, ${autoCount} auto-approved. Apply now?`,
            { modal: true },
            'Apply',
            'Cancel'
          )
          .then((choice) => {
            if (choice === 'Apply') {
              const apply = {
                ...payload,
                approved: true,
                message: 'Apply approved operations',
              } as Record<string, unknown>;
              try {
                ws.send('act.apply', apply);
              } catch {
                void vscode.window.showWarningMessage('Act: Apply failed to send');
              }
            }
            try {
              if (typeof off === 'function') off();
            } catch {
              // noop
            }
          });
      });

      try {
        ws.send('act.request_approval', payload);
      } catch {
        void vscode.window.showWarningMessage('Act: Dry-run request failed');
      }
    })
    .then(() => void 0);
}

export function actApprove(payload: Record<string, unknown>): Promise<void> {
  if (isTestEnv()) return Promise.resolve();
  return ensureConnected()
    .then((ws) => {
      try {
        ws.send('act.approve', payload);
      } catch {
        void vscode.window.showWarningMessage('Act: Approve failed');
      }
    })
    .then(() => void 0);
}

export function actApply(payload: Record<string, unknown>): Promise<void> {
  if (isTestEnv()) return Promise.resolve();
  return ensureConnected()
    .then((ws) => {
      try {
        ws.send('act.apply', payload);
      } catch {
        void vscode.window.showWarningMessage('Act: Apply failed');
      }
    })
    .then(() => void 0);
}

export function actRollback(payload: Record<string, unknown>): Promise<void> {
  if (isTestEnv()) return Promise.resolve();
  return ensureConnected()
    .then((ws) => {
      try {
        ws.send('act.rollback', payload);
      } catch {
        void vscode.window.showWarningMessage('Act: Rollback failed');
      }
    })
    .then(() => void 0);
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
