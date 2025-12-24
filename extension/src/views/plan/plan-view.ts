import * as vscode from 'vscode';

export class PlanViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.plan';
  private view?: vscode.WebviewView;

  resolveWebviewView(view: vscode.WebviewView) {
    this.view = view;
    view.webview.options = { enableScripts: true };
    view.webview.html = render([]);

    view.webview.onDidReceiveMessage((msg) => {
      if (!msg || !msg.type) return;

      switch (msg.type) {
        case 'plan:select':
          vscode.commands.executeCommand(
            'localpilot.plan.select',
            msg.planId,
            msg.multi
          );
          break;
        case 'plan:open':
          vscode.commands.executeCommand(
            'localpilot.plan.open',
            msg.planId
          );
          break;
        case 'plan:validateById':
          vscode.commands.executeCommand(
            'localpilot.plan.validateById',
            msg.planId
          );
          break;
        case 'plan:approveById':
          vscode.commands.executeCommand(
            'localpilot.plan.approveById',
            msg.planId
          );
          break;
        case 'plan:regenerateById':
          vscode.commands.executeCommand(
            'localpilot.plan.regenerateById',
            msg.planId
          );
          break;
        case 'plan:discardById':
          vscode.commands.executeCommand(
            'localpilot.plan.discardById',
            msg.planId
          );
          break;
      }
    });

    // Initial render
    vscode.commands.executeCommand('localpilot.plan.refresh');
  }

  /** called by controller via command to update list */
  update(plans: any[]) {
    if (!this.view) return;
    this.view.webview.html = render(plans);
  }
}

function render(plans: any[]): string {
  const rows = plans
    .map(
      (p) => `
    <div class="plan-row">
      <input type="checkbox" data-id="${p.id}" />
      <span class="title">${p.title}</span>
      <span class="status ${p.status}">${p.status.toUpperCase()} </span>
      <div class="actions">
        <button data-open="${p.id}" title="Open">🔍</button>
        <button data-validate="${p.id}" title="Validate">✔</button>
        <button data-approve="${p.id}" title="Approve">🔐</button>
        <button data-regenerate="${p.id}" title="Regenerate">🔄</button>
        <button data-discard="${p.id}" title="Discard">🗑</button>
        <button disabled title="Act (coming soon)">⚙</button>
      </div>
    </div>
  `
    )
    .join('');

  return `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { background: #1e1e1e; color: #d4d4d4; font-family: sans-serif; padding: 8px; }
    .plan-row { display: grid; grid-template-columns: auto 1fr auto auto; gap: 6px; align-items: center; padding: 4px; border-bottom: 1px solid #333; }
    .plan-row:hover { background: #252525; }
    .title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .status { font-size: 11px; }
    .status.draft { color: #facc15; }
    .status.approved { color: #4ade80; }
    .actions { display: flex; gap: 6px; }
    button { background: none; border: none; cursor: pointer; color: #d4d4d4; }
    button:hover { color: white; }
  </style>
</head>
<body>
<h3>Plans</h3>
<div id="list">
  ${rows || '<em>No plans yet</em>'}
</div>
<script>
  const vscode = acquireVsCodeApi();
  document.querySelectorAll('input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', (e) => {
      vscode.postMessage({
        type: 'plan:select',
        planId: e.target.dataset.id,
        multi: e.ctrlKey || e.metaKey
      });
    });
  });
  document.querySelectorAll('button[data-open]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:open', planId: btn.dataset.open });
    });
  });

  document.querySelectorAll('[data-validate]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:validateById', planId: btn.dataset.validate });
    });
  });

  document.querySelectorAll('[data-approve]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:approveById', planId: btn.dataset.approve });
    });
  });

  document.querySelectorAll('[data-regenerate]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:regenerateById', planId: btn.dataset.regenerate });
    });
  });

  document.querySelectorAll('[data-discard]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:discardById', planId: btn.dataset.discard });
    });
  });
</script>
</body>
</html>
`;
}
