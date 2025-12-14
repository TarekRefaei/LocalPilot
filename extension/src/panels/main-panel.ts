import * as vscode from 'vscode';

export class MainPanel {
  static register(context: vscode.ExtensionContext) {
    context.subscriptions.push(
      vscode.window.registerWebviewViewProvider(
        'localpilot.sidebar',
        {
          resolveWebviewView(view: vscode.WebviewView) {
            view.webview.html = `<h1>LocalPilot</h1>`;
          }
        }
      )
    );
  }
}
