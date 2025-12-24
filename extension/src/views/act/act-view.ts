import * as vscode from 'vscode';

export class ActViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.act';

  resolveWebviewView(view: vscode.WebviewView) {
    view.webview.html = `
      <html>
        <body>
          <h3>Act Mode</h3>
          <p>Act Mode will be available once a plan is approved.</p>
        </body>
      </html>
    `;
  }
}
