import * as vscode from 'vscode';
import { executionState } from '../../features/execute_v2/execute-state';
import { stopExecutionPolling } from '../../features/execute_v2/execute-controller';

export class ExecuteViewProvider implements vscode.WebviewViewProvider {
  static viewId = 'localpilot.execute';
  private view?: vscode.WebviewView;

  resolveWebviewView(view: vscode.WebviewView) {
    this.view = view;
    view.webview.options = { enableScripts: true };
    view.onDidDispose(() => {
      stopExecutionPolling();
    });
    this.render();
  }

  render() {
    if (!this.view) return;

    const s = executionState.get();

    if (!s) {
      this.view.webview.html = '<em>No active execution</em>';
      return;
    }

    const tasks = s.tasks ?? [];
    const disabledGlobal = s.isMutating === true;
    const runningIndex = tasks.findIndex((x: any) => x.status === 'running');
    const showSpinner = s.isMutating === true;

    this.view.webview.html = `
      <style>
        .lp-spinner { display:inline-block; width:12px; height:12px; border:2px solid #ccc; border-top-color:#3f51b5; border-radius:50%; animation: lp-spin 0.8s linear infinite; margin-left:6px; vertical-align:middle; }
        @keyframes lp-spin { to { transform: rotate(360deg); } }
      </style>
      <h3>Execution: ${escapeHtml(s.planTitle)} ${showSpinner ? '<span class="lp-spinner" title="Working..."></span>' : ''}</h3>
      <div style="font-size: 11px; color: #888; margin-bottom: 8px;">ID: ${escapeHtml(s.executionId)}</div>

      <p>Status: <b>${s.status}</b></p>

      <ul>
        ${tasks.map((t: any, i: number) => `
          <li style="margin-bottom: 10px; ${i === (s.currentTaskIndex ?? -1) ? 'font-weight:bold;' : ''}">
            ${statusIcon(t.status)}
            ${escapeHtml(t.title)}
            <code>(${escapeHtml(t.actionType)} ${escapeHtml(t.filePath)})</code>

            <div style="margin-top:4px;">
              ${t.status === 'failed' ? `
                <button onclick="retry()" ${disabledGlobal || (runningIndex !== -1 && runningIndex !== i) ? 'disabled' : ''}>Retry</button>
              ` : ''}

              ${t.status === 'pending' || t.status === 'running' ? `
                <button onclick="skip()" ${disabledGlobal || t.status === 'running' ? 'disabled' : ''}>Skip</button>
              ` : ''}
            </div>

            ${t.lastDiff ? `
              <details>
                <summary>Diff</summary>
                <pre>${escapeHtml(t.lastDiff)}</pre>
              </details>
            ` : ''}

            ${t.error ? `<div style=\"color:red;\">${escapeHtml(t.error)}</div>` : ''}
          </li>
        `).join('')}
      </ul>

      ${s.canApply ? `
        <button onclick="approve()" ${disabledGlobal ? 'disabled' : ''}>Apply & Continue</button>
      ` : ''}

      <script>
        const vscode = acquireVsCodeApi();
        function approve() {
          vscode.postMessage({ command: 'apply' });
        }
        function retry() {
          vscode.postMessage({ command: 'retry' });
        }
        function skip() {
          vscode.postMessage({ command: 'skip' });
        }
        function resume() {
          vscode.postMessage({ command: 'resume' });
        }
      </script>
    `;

    this.view.webview.onDidReceiveMessage(msg => {
      if (msg.command === 'apply') {
        vscode.commands.executeCommand('localpilot.execute.apply');
      }
      if (msg.command === 'retry') {
        vscode.commands.executeCommand('localpilot.execute.retry');
      }
      if (msg.command === 'skip') {
        vscode.commands.executeCommand('localpilot.execute.skip');
      }
      if (msg.command === 'resume') {
        vscode.commands.executeCommand('localpilot.execute.resume');
      }
    });
  }
}

function escapeHtml(str: string): string {
  return str.replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  } as any)[m]);
}

function statusIcon(status: string): string {
  switch (status) {
    case 'done': return '✅';
    case 'running': return '▶️';
    case 'failed': return '❌';
    case 'skipped': return '⏭';
    default: return '⬜';
  }
}
