import * as vscode from "vscode";
import { initChat } from "../webview/chat-controller";

export class MainPanel {
  static register(context: vscode.ExtensionContext) {
    context.subscriptions.push(
      vscode.window.registerWebviewViewProvider(
        "localpilot.sidebar",
        {
          resolveWebviewView(view) {
            view.webview.options = {
              enableScripts: true
            };

            view.webview.html = getHtml();
            initChat(view, "default");
          }
        }
      )
    );
  }
}

function getHtml(): string {
  return `
<!DOCTYPE html>
<html>
<head>
<style>
body { background:#1e1e1e; color:#d4d4d4; font-family:sans-serif; padding:10px; }
.hidden { display:none; }
progress { width:100%; }
#out { height:240px; overflow:auto; border:1px solid #333; padding:8px; }
#in { width:100%; margin-top:8px; }
#status { margin-bottom:8px; font-size:12px; }
.status-ok { color:#6ee7b7; }
.status-error { color:#f87171; }
</style>
</head>

<body>

<div id="onboarding">
  <h3>Welcome to LocalPilot</h3>
  <div id="status">Checking system status…</div>
  <button id="indexBtn">Index Current Workspace</button>
  <progress id="progress" max="100" value="0" class="hidden"></progress>
</div>

<div id="chat" class="hidden">
  <div id="out"></div>
  <input id="in" placeholder="Ask about your project..." />
</div>

<script>
const vscode = acquireVsCodeApi();

const onboarding = document.getElementById("onboarding");
const chat = document.getElementById("chat");
const out = document.getElementById("out");
const input = document.getElementById("in");
const progress = document.getElementById("progress");
const indexBtn = document.getElementById("indexBtn");

let state = "onboarding";

function render() {
  onboarding.classList.toggle("hidden", state !== "onboarding");
  chat.classList.toggle("hidden", state !== "chat");
}

render();

// ------------------------
// INDEXING (SSE)
// ------------------------
indexBtn.onclick = () => {
  progress.classList.remove("hidden");
  progress.value = 0;

  const es = new EventSource("http://localhost:8000/api/index/default");

  es.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);

    if (msg.type === "index:progress") {
      const pct = Math.round((msg.current / msg.total) * 100);
      progress.value = pct;
    }

    if (msg.type === "index:done") {
      progress.value = 100;
      es.close();
      state = "chat";
      render();
    }

    if (msg.type === "error") {
      es.close();
      alert(msg.message || "Indexing failed");
    }
  };

  es.onerror = () => {
    es.close();
    alert("Indexing connection failed");
  };
};

// ------------------------
// CHAT INPUT
// ------------------------
input.addEventListener("keydown", (e) => {
  if (e.key !== "Enter") return;

  const message = input.value.trim();
  if (!message) return;

  input.value = "";
  out.innerHTML += "<div><b>You:</b> " + message + "</div>";

  vscode.postMessage({
    type: "chat:send",
    payload: { message }
  });
});

// ------------------------
// EXTENSION EVENTS
// ------------------------
window.addEventListener("message", (e) => {
  const msg = e.data;

  if (msg.type === "token") {
    out.innerHTML += msg.value;
  }

  if (msg.type === "done") {
    input.disabled = false;
    input.focus();
  }

  if (msg.type === "ui:lock") {
    input.disabled = true;
  }

  if (msg.type === "error") {
    out.innerHTML += "<div class='error'>[error]</div>";
    input.disabled = false;
  }

  if (msg.type === "status:update") {
    const el = document.getElementById("status");
    if (!msg.backendOk) {
      el.textContent = "Backend not running";
      el.className = "status-error";
    } else if (!msg.ollamaOk) {
      el.textContent = "Ollama not available";
      el.className = "status-error";
    } else {
      el.textContent = "Ready";
      el.className = "status-ok";
    }
  }
});
</script>

</body>
</html>
`;
}
