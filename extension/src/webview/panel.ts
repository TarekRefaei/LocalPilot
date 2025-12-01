import * as vscode from 'vscode';

export class LocalPilotPanel {
  public static currentPanel: LocalPilotPanel | undefined;
  private readonly _panel: vscode.WebviewPanel;
  private readonly _state: any;
  private _abort: AbortController | null = null;
  private _sessionId: string;

  public static createOrShow(state: any) {
    const column = vscode.window.activeTextEditor ? vscode.window.activeTextEditor.viewColumn : undefined;
    if (LocalPilotPanel.currentPanel) {
      LocalPilotPanel.currentPanel._panel.reveal(column);
      return;
    }
    const panel = vscode.window.createWebviewPanel(
      'localpilotWebview',
      'LocalPilot',
      column || vscode.ViewColumn.One,
      { enableScripts: true }
    );
    LocalPilotPanel.currentPanel = new LocalPilotPanel(panel, state);
  }

  private constructor(panel: vscode.WebviewPanel, state: any) {
    this._panel = panel;
    this._state = state;
    this._sessionId = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? 'default';
    this._update();

    this._panel.webview.onDidReceiveMessage(
      (message) => {
        switch (message.command) {
          case 'log':
            console.log('Webview:', message.text);
            break;
          case 'persistModel':
            try {
              this._state.setDefaultModel(message.model);
            } catch (e) {
              console.warn('Failed to persist model to memento state', e);
            }
            break;
          case 'chat':
            import('../services/backend').then(async (backendSvc) => {
              const panelWeb = this._panel.webview;
              try {
                if (this._abort) this._abort.abort();
                this._abort = new AbortController();
                await backendSvc.streamChatFromBackend(message.text, this._abort.signal, {
                  onChunk: (chunk: string) => panelWeb.postMessage({ command: 'append', text: chunk }),
                  onEnd: () => { this._abort = null; },
                  onError: () => { panelWeb.postMessage({ command: 'append', text: '[Error contacting backend]' }); this._abort = null; },
                }, this._sessionId);
              } catch (err) {
                panelWeb.postMessage({ command: 'append', text: '[Backend error]' });
              }
            });
            break;
          case 'stop':
            try { if (this._abort) this._abort.abort(); } catch {}
            try { import('../services/backend').then((svc) => { void svc.abortLastRequest(); }); } catch {}
            break;
          case 'webviewReady':
            (async () => {
              const model = this._state.getDefaultModel?.();
              const plansRaw = this._state.getPlans?.() ?? [];
              const plans = Array.isArray(plansRaw) ? plansRaw.map((p: any) => (p && typeof p === 'object' && 'title' in p ? String(p.title) : (typeof p === 'string' ? p : String(p)))) : [];
              this._panel.webview.postMessage({ command: 'replaceMessages', messages: [] });
              this._panel.webview.postMessage({ command: 'setPlans', plans });
              if (model) this._panel.webview.postMessage({ command: 'model', model });
              // fetch persisted history from backend
              try {
                const svc = await import('../services/backend');
                const hist = await svc.fetchHistory(this._sessionId, 200);
                for (const m of hist) {
                  const prefix = m.role === 'user' ? 'You: ' : '';
                  this._panel.webview.postMessage({ command: 'append', text: prefix + m.text });
                }
              } catch {}
            })();
            break;
        }
      },
      undefined
    );
  }

  private _update() {
    this._panel.webview.html = this._getHtmlForWebview();
  }

  private _getHtmlForWebview() {
    const css = `
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #ddd; background:#0f1720; margin:0; padding:0; }
      .header { padding: 12px 16px; border-bottom: 1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items:center;}
      .title { font-size: 16px; font-weight:700; color:#fff; }
      .model-badge { background:#111827; padding:6px 10px; border-radius:8px; font-size:12px; color:#9ca3af; }
      .container { display:flex; height: calc(100vh - 70px); }
      .sidebar { width:240px; border-right:1px solid rgba(255,255,255,0.03); padding:12px; box-sizing:border-box; }
      .plans { margin-top:8px; }
      .plan-item { padding:8px; border-radius:6px; margin-bottom:6px; background:#071026; cursor:pointer; }
      .messages { padding: 12px; flex:1; overflow:auto; }
      .message { padding:8px 12px; border-radius:8px; margin-bottom:8px; background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); }
      .msg-row { display:flex; align-items:center; gap:8px; }
      .msg-text { flex:1; white-space:pre-wrap; }
      .msg-time { color:#9ca3af; font-size:11px; }
      .btn.small { padding:4px 8px; font-size:12px; }
      .progress { height:6px; background:#06202a; border-radius:6px; width:100%; margin-bottom:8px; overflow:hidden; }
      .progress > div { height:100%; width:0%; background: linear-gradient(90deg, #06b6d4, #0ea5a3); transition: width 200ms linear; }
      .input-bar { padding:12px; border-top:1px solid rgba(255,255,255,0.03); display:flex; gap:8px; background: linear-gradient(180deg, rgba(15,23,37,0.9), rgba(2,6,23,0.9)); box-sizing:border-box; }
      .input { flex:1; padding:10px 12px; border-radius:8px; background:#0b1220; color:#fff; border:1px solid rgba(255,255,255,0.03); min-height:36px; }
      .btn { padding:8px 12px; border-radius:8px; background:#0369a1; color:#fff; border:none; cursor:pointer; }
      .muted { color:#9ca3af; font-size:12px; }
    `;

    const nonce = Date.now().toString(36);
    return `<!doctype html>
    <html>
    <head>
      <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'nonce-${nonce}';">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>${css}</style>
    </head>
    <body>
      <div class="header">
        <div class="title">LocalPilot</div>
        <div class="model-badge" id="modelBadge">model: —</div>
      </div>
      <div class="container">
        <div class="sidebar">
          <div class="muted">Plans</div>
          <div id="plans" class="plans"></div>
        </div>
        <div style="flex:1; display:flex; flex-direction:column;">
          <div class="progress"><div></div></div>
          <div class="messages" id="msgs"></div>
          <div class="input-bar">
            <div contenteditable="true" class="input" id="input" placeholder="Type a message..."></div>
            <button class="btn" id="send">Send</button>
            <button class="btn" id="stop">Stop</button>
            <button class="btn" id="regenerate">Regenerate</button>
            <button class="btn" id="copy">Copy</button>
          </div>
        </div>
      </div>
      <script nonce="${nonce}">
        const vscode = acquireVsCodeApi();
        const state = vscode.getState() || { messages: [], plans: [], model: null };

        function renderState() {
          const msgs = document.getElementById('msgs');
          msgs.innerHTML = '';
          for (const m of state.messages) {
            const el = document.createElement('div'); el.className='message';
            const row = document.createElement('div'); row.className='msg-row';
            const txt = document.createElement('span'); txt.className='msg-text'; txt.textContent=String(m);
            const time = document.createElement('span'); time.className='msg-time'; time.textContent=new Date().toLocaleTimeString();
            const btn = document.createElement('button'); btn.className='btn small'; btn.textContent='Copy'; btn.addEventListener('click', () => { navigator.clipboard.writeText(txt.textContent || ''); });
            row.appendChild(txt); row.appendChild(time); row.appendChild(btn); el.appendChild(row); msgs.appendChild(el);
          }
          const plansEl = document.getElementById('plans');
          plansEl.innerHTML = '';
          for (let i=0;i<state.plans.length;i++) {
            const p = state.plans[i];
            const el = document.createElement('div'); el.className='plan-item'; el.textContent = p;
            el.onclick = () => { document.getElementById('input').innerText = p; };
            plansEl.appendChild(el);
          }
          document.getElementById('modelBadge').textContent = 'model: ' + (state.model || '—');
        }

        renderState();

        window.addEventListener('message', (ev) => {
          const msg = ev.data;
          if (msg.command === 'append') {
            state.messages.push(msg.text);
            if (state.messages.length > 200) state.messages.shift();
            vscode.setState(state);
            // fast append without full render
            const msgs = document.getElementById('msgs');
            const el = document.createElement('div'); el.className='message';
            const row = document.createElement('div'); row.className='msg-row';
            const txt = document.createElement('span'); txt.className='msg-text'; txt.textContent=String(msg.text);
            const time = document.createElement('span'); time.className='msg-time'; time.textContent=new Date().toLocaleTimeString();
            const btn = document.createElement('button'); btn.className='btn small'; btn.textContent='Copy'; btn.addEventListener('click', () => { navigator.clipboard.writeText(txt.textContent || ''); });
            row.appendChild(txt); row.appendChild(time); row.appendChild(btn); el.appendChild(row);
            msgs.appendChild(el);
            msgs.scrollTop = msgs.scrollHeight;
          } else if (msg.command === 'model') {
            state.model = msg.model;
            vscode.setState(state);
            vscode.postMessage({ command: 'persistModel', model: msg.model });
            renderState();
          } else if (msg.command === 'setPlans') {
            state.plans = msg.plans || [];
            vscode.setState(state);
            renderState();
          } else if (msg.command === 'replaceMessages') {
            state.messages = msg.messages || [];
            vscode.setState(state);
            renderState();
          }
        });

        document.getElementById('send').addEventListener('click', () => {
          const txt = document.getElementById('input').innerText.trim();
          if (!txt) return;
          state.messages.push('You: ' + txt);
          vscode.setState(state);
          renderState();
          vscode.postMessage({ command: 'chat', text: txt });
          document.getElementById('input').innerText = '';
        });
        document.getElementById('stop').addEventListener('click', () => {
          vscode.postMessage({ command: 'stop' });
        });
        document.getElementById('regenerate').addEventListener('click', () => {
          const lastUser = [...state.messages].reverse().find(m => m.startsWith('You:'));
          if (lastUser) {
            const text = lastUser.replace(/^You:\s*/, '');
            vscode.postMessage({ command: 'chat', text });
          }
        });
        document.getElementById('copy').addEventListener('click', () => {
          const lastAssistant = [...state.messages].reverse().find(m => !m.startsWith('You:'));
          if (lastAssistant) {
            navigator.clipboard.writeText(lastAssistant);
          }
        });

        vscode.postMessage({ command: 'webviewReady' });
      </script>
    </body>
    </html>`;
  }
}
