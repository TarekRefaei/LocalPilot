import * as vscode from 'vscode';
import type { LocalPilotState } from '../services/state';
import { COMMAND_IDS } from '../ids';
import { streamChatFromBackend } from '../services/backend';

export class ChatViewProvider implements vscode.WebviewViewProvider {
  private view: vscode.WebviewView | undefined;
  private state: LocalPilotState | undefined;
  private readonly extensionUri: vscode.Uri;
  private currentAbort: AbortController | undefined;
  private lastPrompt: string | undefined;
  private lastStatePayload: { plans: number; recent: string[]; model: string } | undefined;

  constructor(extensionUri: vscode.Uri, state?: LocalPilotState) {
    this.extensionUri = extensionUri;
    this.state = state;
  }

  private async streamFromBackendOrFallback(prompt: string): Promise<void> {
    const webview = this.view?.webview;
    if (!webview) return;
    // try backend first
    try {
      this.currentAbort?.abort();
      this.currentAbort = new AbortController();
      void webview.postMessage({ type: 'beginAssistant' });
      await streamChatFromBackend(prompt, this.currentAbort.signal, {
        onChunk: (text) => void webview.postMessage({ type: 'stream', markdown: text }),
        onEnd: () => void webview.postMessage({ type: 'endAssistant' }),
        onError: () => {
          // Fallback to demo content if backend fails
          void this.streamInlineResponse(prompt);
        },
      });
      return;
    } catch {
      // ignore and fallback
    }
    await this.streamInlineResponse(prompt);
  }

  resolveWebviewView(webviewView: vscode.WebviewView): void {
    this.view = webviewView;
    const webview = webviewView.webview;
    webview.options = { enableScripts: true };
    webview.onDidReceiveMessage((msg: { type?: string; text?: unknown; title?: unknown }) => {
      void this.handleMessage(msg);
    });
    webview.html = this.getHtml(webview);
    void this.sendState();
  }

  private async handleMessage(msg: {
    type?: string;
    text?: unknown;
    title?: unknown;
  }): Promise<void> {
    if (msg?.type === 'inlineChat') {
      const prompt: string = typeof msg.text === 'string' ? msg.text : '';
      this.lastPrompt = prompt;
      const prev = [...(this.state?.getRecentPrompts?.() ?? [])];
      const trimmed = prompt.trim();
      if (trimmed) {
        const next = [trimmed, ...prev.filter((p) => p !== trimmed)].slice(0, 10);
        this.state?.setRecentPrompts?.(next);
        this.sendState();
      }
      await this.streamFromBackendOrFallback(prompt);
      return;
    }
    if (msg?.type === 'transfer') {
      const title: string = typeof msg.title === 'string' ? msg.title : 'Draft plan from Chat';
      await vscode.commands.executeCommand(COMMAND_IDS.chatTransferToPlan, { title });
      try {
        await vscode.commands.executeCommand('setContext', 'localpilot.views.visible', true);
        await vscode.commands.executeCommand('workbench.view.extension.localpilot');
      } catch {
        void 0;
      }
      return;
    }
    if (msg?.type === 'pickModel') {
      const cfg = vscode.workspace.getConfiguration('localpilot');
      const current = String(cfg.get('model') ?? 'local');
      const choice = await vscode.window.showQuickPick(
        ['local', 'ollama:llama3', 'openai:gpt-4o-mini'],
        { placeHolder: `Current: ${current}` }
      );
      if (choice) {
        await cfg.update('model', choice, vscode.ConfigurationTarget.Global);
        this.sendState();
      }
      return;
    }
    if (msg?.type === 'stop') {
      this.currentAbort?.abort();
      this.currentAbort = undefined;
      void this.view?.webview.postMessage({ type: 'endAssistant' });
      return;
    }
    if (msg?.type === 'regen') {
      const p = this.lastPrompt ?? '';
      if (p) {
        await this.streamFromBackendOrFallback(p);
      }
      return;
    }
    if (msg?.type === 'copy' && typeof msg.text === 'string') {
      await vscode.env.clipboard.writeText(msg.text);
      return;
    }
    if (msg?.type === 'refresh') {
      this.sendState();
      return;
    }
  }

  private async streamInlineResponse(prompt: string): Promise<void> {
    const planCount = this.state?.getPlans().length ?? 0;
    const webview = this.view?.webview;
    if (!webview) return;
    void webview.postMessage({ type: 'beginAssistant' });
    const parts: string[] = [
      '### LocalPilot\n\n',
      'I can draft a plan from your request.\n\n',
      `You currently have ${planCount} plan(s).\n`,
      'Preview:\n',
      `- Draft plan: ${prompt.trim() ? prompt.slice(0, 40) : 'Untitled'}\n`,
      '\n',
    ];
    for (const p of parts) {
      void webview.postMessage({ type: 'stream', markdown: p });
      await new Promise((r) => setTimeout(r, 60));
    }
    void webview.postMessage({
      type: 'action',
      command: COMMAND_IDS.chatTransferToPlan,
      title: 'Transfer to Plan',
    });
    void webview.postMessage({ type: 'endAssistant' });
  }

  private getHtml(webview: vscode.Webview): string {
    const nonce = this.getNonce();
    const scriptUri = webview
      .asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'media', 'localpilot-chat.js'))
      .toString();
    const style = `
      <style>
        html, body { height: 100%; }
        body { color: var(--vscode-foreground); font-family: var(--vscode-font-family); margin: 0; }
        .container { height: 100%; padding: 8px; display: flex; flex-direction: column; gap: 8px; }
        .messages { flex: 1; overflow: auto; border: 1px solid var(--vscode-input-border); border-radius: 6px; padding: 8px; min-height: 0; background: var(--vscode-editor-background); }
        .msg { margin: 6px 0; }
        .assistant { border-left: 3px solid var(--vscode-charts-blue); padding-left: 6px; }
        .user { opacity: 0.9; }
        .row { display: flex; gap: 6px; }
        textarea { width: 100%; height: 60px; resize: vertical; background: var(--vscode-input-background); color: var(--vscode-input-foreground); border: 1px solid var(--vscode-input-border); border-radius: 4px; padding: 6px; }
        button { background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: 0; border-radius: 4px; padding: 6px 10px; cursor: pointer; }
        button:hover { background: var(--vscode-button-hoverBackground); }
        .hint { opacity: 0.8; font-size: 12px; }
        .toolbar { display: flex; gap: 6px; }
        .composer { display: flex; flex-direction: column; gap: 6px; border-top: 1px solid var(--vscode-input-border); padding-top: 6px; }
        .statusbar { display: flex; justify-content: space-between; align-items: center; font-size: 12px; opacity: 0.9; }
        .badge { padding: 2px 6px; border: 1px solid var(--vscode-input-border); border-radius: 999px; }
        .recent { font-size: 12px; opacity: 0.9; }
        .recent .item { display: inline-block; margin: 2px 6px 2px 0; padding: 2px 6px; border: 1px solid var(--vscode-input-border); border-radius: 999px; cursor: pointer; }
      </style>
    `;
    const script = `
      <script nonce="${nonce}" src="${scriptUri}"></script>
    `;
    const html = `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8" />
          <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src ${webview.cspSource} https: data:; style-src 'unsafe-inline' ${webview.cspSource}; script-src ${webview.cspSource} 'nonce-${nonce}';" />
          ${style}
        </head>
        <body>
          <div class="container">
            <div id="hint" class="hint">LocalPilot Chat (inline). Type a prompt, send, and optionally transfer to Plans.</div>
            <div id="recent" class="recent"></div>
            <div id="messages" class="messages"></div>
            <div class="composer">
              <div class="statusbar">
                <span>Type @ for context, / for commands</span>
                <span class="badge" id="model-badge">model: local</span>
              </div>
              <textarea id="prompt" placeholder="Type your task here..."></textarea>
              <div class="toolbar">
                <button id="btn-send">Send</button>
                <button id="btn-stop">Stop</button>
                <button id="btn-regen">Regenerate</button>
                <button id="btn-copy">Copy</button>
                <button id="btn-transfer">Transfer to Plan</button>
                <button id="btn-clear">Clear</button>
              </div>
            </div>
          </div>
          ${script}
        </body>
      </html>
    `;
    return html;
  }

  private sendState(): void {
    const webview = this.view?.webview;
    if (!webview) return;
    const count = this.state?.getPlans().length ?? 0;
    const recent = this.state?.getRecentPrompts?.() ?? [];
    const cfg = vscode.workspace.getConfiguration('localpilot');
    const model = String(cfg.get('model') ?? 'local');
    const payload = { type: 'state', plans: count, recent, model } as const;
    this.lastStatePayload = { plans: count, recent: [...recent], model };
    void webview.postMessage(payload);
  }

  public __testGetLastState(): { plans: number; recent: string[]; model: string } | undefined {
    return this.lastStatePayload;
  }

  public __testComputeState(): { plans: number; recent: string[]; model: string } {
    const count = this.state?.getPlans().length ?? 0;
    const recentRo = this.state?.getRecentPrompts?.() ?? [];
    const recent = [...recentRo];
    const cfg = vscode.workspace.getConfiguration('localpilot');
    const model = String(cfg.get('model') ?? 'local');
    return { plans: count, recent, model };
  }

  public __testSendState(): void {
    this.sendState();
  }

  private getNonce(): string {
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let text = '';
    for (let i = 0; i < 32; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
  }
}
