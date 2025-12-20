import * as vscode from "vscode";
import { ChatService } from "../features/chat/chat-service";
import {
  checkServerHealth,
  checkOllamaHealth,
  isIndexed,
  getProjectSummary
} from "../infrastructure/http/api-client";

export function initChat(panel: vscode.WebviewView, projectId: string) {
  const chat = new ChatService();

  // Initial status check
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

    // ------------------------
    // CHAT ONLY
    // ------------------------
    if (msg.type === "chat:send") {
      const indexed = await isIndexed(projectId);
      if (!indexed) {
        panel.webview.postMessage({
          type: "error",
          message: "Project not indexed. Please index the workspace first."
        });
        return;
      }

      try {
        await getProjectSummary(projectId);
      } catch {
        panel.webview.postMessage({
          type: "error",
          message: "Project summary missing. Please re-index."
        });
        return;
      }

      panel.webview.postMessage({ type: "ui:lock" });

      await chat.sendMessage(
        msg.payload.message,
        (event) => panel.webview.postMessage(event),
        projectId
      );
    }
  });
}
