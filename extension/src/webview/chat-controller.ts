import * as vscode from "vscode";
import { ChatService } from "../features/chat/chat-service";
import { checkServerHealth, checkOllamaHealth } from "../infrastructure/http/api-client";

export function initChat(panel: vscode.WebviewView, projectId: string) {
  const chat = new ChatService();

  (async () => {
    const backendOk = await checkServerHealth();
    const ollamaOk = await checkOllamaHealth();
    panel.webview.postMessage({
      type: "status:update",
      backendOk,
      ollamaOk
    });
  })();

  panel.webview.onDidReceiveMessage(async (msg: any) => {
    if (!msg) return;

    if (msg.type === "chat:send") {
      panel.webview.postMessage({ type: "ui:lock" });

      await chat.sendMessage(
        msg.payload.message,
        (event) => panel.webview.postMessage(event),
        projectId
      );
    }

    if (msg.type === "index:start") {
      panel.webview.postMessage({ type: "index:progress", percent: 10 });
      panel.webview.postMessage({ type: "index:progress", percent: 50 });
      panel.webview.postMessage({ type: "index:progress", percent: 100 });
      panel.webview.postMessage({ type: "index:done" });
    }
  });
}
