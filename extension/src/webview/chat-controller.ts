import * as vscode from "vscode";
import { ChatService } from "../features/chat/chat-service";
import { ChatSessionStore } from "../features/chat/chat-session.store";
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
    // CHAT → PLAN: open Plan tab
    // ------------------------
    if (msg.type === "open:planTab") {
      await vscode.commands.executeCommand("workbench.view.extension.localpilot");
      return;
    }

    if (msg.type === "index:done") {
      ChatSessionStore.clear();
      return;
    }

    // ------------------------
    // CHAT ONLY
    // ------------------------
    if (msg.type === "chat:send") {
      // Planning intent hint (non-blocking)
      const text: string = msg.payload?.message || "";
      const planningIntent = /(\bplan\b|planning|implementation plan|create plan|propose plan|migration plan|write a plan)/i;
      if (planningIntent.test(text)) {
        panel.webview.postMessage({
          type: "hint",
          message: "Planning is available in the Plan tab.",
          action: { label: "Open Plan Tab" }
        });
        vscode.window
          .showInformationMessage(
            "Planning is available in the Plan tab.",
            "Open Plan Tab"
          )
          .then(async (choice) => {
            if (choice === "Open Plan Tab") {
              await vscode.commands.executeCommand(
                "workbench.view.extension.localpilot"
              );
            }
          });
      }

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
