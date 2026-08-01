import * as vscode from 'vscode';
import { planRegistry } from './plan-registry';
import { updatePlanMarkdownById } from './plan-controller';

let panel: vscode.WebviewPanel | undefined;
let currentPlanId: string | undefined;

export async function openPlanView(markdown: string, planId?: string) {
  currentPlanId = planId;
  if (panel) {
    panel.reveal();
    panel.webview.postMessage({ type: 'plan:update', markdown, planId });
    return;
  }

  panel = vscode.window.createWebviewPanel(
    'localpilot.planView',
    'LocalPilot — Plan Mode',
    vscode.ViewColumn.One,
    { enableScripts: true }
  );

  panel.webview.html = render(markdown, planId);

  panel.webview.onDidReceiveMessage(async (msg) => {
    if (!msg || !msg.type) return;
    if (msg.type === 'plan:content') {
      const markdown: string = msg.markdown || '';
      const targetId: string | undefined = msg.planId || currentPlanId;
      if (targetId) {
        await updatePlanMarkdownById(targetId, markdown);
      } else {
        const selected = planRegistry.getSelected();
        if (selected.length === 1) {
          await updatePlanMarkdownById(selected[0].id, markdown);
        }
      }
    }
  });

  panel.onDidDispose(() => {
    panel = undefined;
    currentPlanId = undefined;
  });
}

function render(markdown: string, planId?: string): string {
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
            vscode.postMessage({ type: 'plan:content', markdown, planId: ${JSON.stringify(planId || '')} });
          }
          document.getElementById('md').addEventListener('input', sendPlanContent);
          window.addEventListener('beforeunload', sendPlanContent);
        </script>
      </body>
    </html>
  `;
}
