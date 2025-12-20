// ------------------------------------------------------------
// VS Code Webview API declaration (TypeScript-only)
// ------------------------------------------------------------
declare function acquireVsCodeApi(): {
  postMessage(message: any): void;
};

// Acquire VS Code API
const vscode = acquireVsCodeApi();

export function renderChat(container: HTMLElement) {
  // ============================
  // Index button
  // ============================
  const indexBtn = document.createElement("button");
  indexBtn.textContent = "Index Current Workspace";
  indexBtn.style.width = "100%";
  indexBtn.style.marginBottom = "6px";

  container.appendChild(indexBtn);

  indexBtn.onclick = () => {
    vscode.postMessage({ type: "index:start" });
  };

  // ============================
  // Progress bar
  // ============================
  const progress = document.createElement("progress");
  progress.max = 100;
  progress.value = 0;
  progress.style.width = "100%";
  progress.style.display = "none";

  container.appendChild(progress);

  // ============================
  // Output
  // ============================
  const output = document.createElement("div");
  output.style.marginTop = "8px";
  output.style.fontFamily = "monospace";
  container.appendChild(output);

  // ============================
  // Input
  // ============================
  const input = document.createElement("input");
  input.placeholder = "Ask about your project...";
  input.style.width = "100%";
  input.style.marginTop = "8px";
  container.appendChild(input);

  input.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;

    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    output.innerHTML += `<div><b>You:</b> ${message}</div>`;

    vscode.postMessage({
      type: "chat:send",
      payload: { message },
    });
  });

  // ============================
  // Incoming messages
  // ============================
  window.addEventListener("message", (event) => {
    const msg = event.data;
    if (!msg || !msg.type) return;

    // ----------------------------
    // Indexing begins
    // ----------------------------
    if (msg.type === "index:begin") {
      progress.value = 0;
      progress.style.display = "block";

      const es = new EventSource(
        `http://localhost:8000/api/index/${encodeURIComponent(
          msg.projectId
        )}`
      );

      es.onmessage = (ev) => {
        const data = JSON.parse(ev.data);

        if (data.type === "index:progress") {
          progress.value =
            data.total > 0
              ? Math.round((data.current / data.total) * 100)
              : 0;
        }

        if (data.type === "index:done") {
          progress.value = 100;
          es.close();
        }

        if (data.type === "error") {
          output.innerHTML += `<div style="color:red">${data.message}</div>`;
          es.close();
        }
      };

      es.onerror = () => {
        output.innerHTML += `<div style="color:red">Indexing failed</div>`;
        es.close();
      };
    }

    // ----------------------------
    // Chat stream
    // ----------------------------
    if (msg.type === "chat:chunk") {
      output.innerHTML += `<div>${msg.content}</div>`;
    }

    if (msg.type === "chat:done") {
      output.innerHTML += `<div><i>Done.</i></div>`;
    }

    if (msg.type === "error") {
      output.innerHTML += `<div style="color:red">${msg.message}</div>`;
    }
  });
}
