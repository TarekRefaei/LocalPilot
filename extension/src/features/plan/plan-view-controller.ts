import * as vscode from 'vscode';

let panel: vscode.WebviewPanel | undefined;

export async function openPlanView(markdown: string) {
  if (panel) {
    panel.reveal();
    panel.webview.postMessage({ type: 'plan:update', markdown });
    return;
  }

  panel = vscode.window.createWebviewPanel(
    'localpilot.planView',
    'LocalPilot — Plan Mode',
    vscode.ViewColumn.One,
    { enableScripts: true }
  );

  panel.webview.html = render(markdown);

  panel.onDidDispose(() => {
    panel = undefined;
  });
}

function render(markdown: string): string {
  const escaped = markdown.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <style>
          html, body, textarea { height: 100%; }
          body { margin: 0; padding: 0; }
          textarea { width: 100%; box-sizing: border-box; font-family: monospace; }
        </style>
      </head>
      <body>
        <textarea id="md">${escaped}</textarea>
        <script>
          const vscode = acquireVsCodeApi();
          window.addEventListener('message', (e) => {
            const msg = e.data;
            if (msg && msg.type === 'plan:update') {
              const el = document.getElementById('md');
              if (el) el.value = msg.markdown || '';
            }
          });
          function sendPlanContent() {
            const el = document.getElementById('md');
            const markdown = el && el.value ? el.value : '';
            vscode.postMessage({ type: 'plan:content', markdown });
          }
          window.addEventListener('beforeunload', sendPlanContent);
        </script>
      </body>
    </html>
  `;
}
