import * as vscode from 'vscode';
import { executionState } from '../../features/execute_v2/execute-state';

export class ExecuteViewProvider implements vscode.WebviewViewProvider {
  static viewId = 'localpilot.execute';
  private view?: vscode.WebviewView;

  resolveWebviewView(view: vscode.WebviewView) {
    this.view = view;
    view.webview.options = { enableScripts: true };
    this.render();
  }

  render() {
    if (!this.view) return;

    const s = executionState.get();

    if (!s) {
      this.view.webview.html = '<em>No active execution</em>';
      return;
    }

    this.view.webview.html = `
      <h3>Execution: ${escapeHtml(s.planTitle)}</h3>

      <p>Status: <b>${s.status}</b></p>

      ${s.diff ? `
        <h4>Proposed Changes</h4>
        <pre>${escapeHtml(s.diff)}</pre>
        <button onclick="approve()">Apply</button>
      ` : ` 
        <em>Waiting for task output…</em>
      `}

      <script>
        const vscode = acquireVsCodeApi();
        function approve() {
          vscode.postMessage({ command: 'apply' });
        }
      </script>
    `;

    this.view.webview.onDidReceiveMessage(msg => {
      if (msg.command === 'apply') {
        vscode.commands.executeCommand('localpilot.execute.apply');
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
