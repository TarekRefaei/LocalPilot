import * as vscode from 'vscode';
import { actState } from '../../features/act/act-state';

export class ActViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.act';
  private view?: vscode.WebviewView;

  resolveWebviewView(view: vscode.WebviewView) {
    this.view = view;
    view.webview.options = { enableScripts: true };

    view.webview.onDidReceiveMessage(async (msg) => {
      if (!msg?.command) return;

      await vscode.commands.executeCommand(msg.command, msg.taskId);
      await vscode.commands.executeCommand('localpilot.act.refresh');
    });

    this.render();
  }

  render() {
    if (!this.view) return;

    const session = actState.get();

    if (!session) {
      this.view.webview.html = `
        <style>
          body { color: #888; font-family: sans-serif; padding: 8px; }
        </style>
        <em>No active Act session.</em>
      `;
      return;
    }

    this.view.webview.html = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body {
            background: #1e1e1e;
            color: #d4d4d4;
            font-family: sans-serif;
            padding: 8px;
          }
          h3 { margin-bottom: 4px; }
          .plan {
            font-size: 12px;
            color: #9cdcfe;
            margin-bottom: 8px;
          }
          ul {
            list-style: none;
            padding-left: 0;
          }
          li {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 0;
          }
          button {
            background: none;
            border: none;
            cursor: pointer;
            color: #d4d4d4;
          }
          button:hover { color: white; }
          .status {
            width: 18px;
            text-align: center;
          }
        </style>
      </head>
      <body>
        <h3>Act Mode</h3>
        <div class="plan"><b>Plan:</b> ${escapeHtml(session.planTitle)}</div>

        <button onclick="runAll()">▶ Run All</button>

        <ul>
          ${session.tasks.map(t => `
            <li>
              <span class="status">${icon(t.status)}</span>
              <span>${escapeHtml(t.title)}</span>
              <button onclick="run('${t.id}')" title="Run">▶</button>
              <button onclick="skip('${t.id}')" title="Skip">⏭</button>
            </li>
          `).join('')}
        </ul>

        <script>
          const vscode = acquireVsCodeApi();
          function run(id) {
            vscode.postMessage({ command: 'localpilot.act.runTask', taskId: id });
          }
          function skip(id) {
            vscode.postMessage({ command: 'localpilot.act.skipTask', taskId: id });
          }
          function runAll() {
            vscode.postMessage({ command: 'localpilot.act.runAll' });
          }
        </script>
      </body>
      </html>
    `;
  }
}

function icon(status: string): string {
  switch (status) {
    case 'pending': return '⬜';
    case 'running': return '⏳';
    case 'done': return '✅';
    case 'failed': return '❌';
    case 'skipped': return '⏭';
    default: return '⬜';
  }
}

function escapeHtml(str: string): string {
  return str.replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[m]!));
}
