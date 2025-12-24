import { queryRAG } from "./rag-client";
import { PromptBuilder } from "./prompt-builder";
import { getProjectSummary } from "../../infrastructure/http/api-client";
import { ChatSessionStore } from "./chat-session.store";

export class ChatService {
  async sendMessage(
    userMessage: string,
    onEvent: (event: any) => void,
    projectId: string
  ): Promise<void> {

    ChatSessionStore.addMessage({ role: 'user', content: userMessage });
    const chunks = await queryRAG(projectId, userMessage);
    const summary = await getProjectSummary(projectId);
    const messages = new PromptBuilder().build(userMessage, chunks, summary);

    const WS = require("ws");
    const ws = new WS("ws://localhost:8000/ws/chat");

    let assistantBuffer = "";

    ws.on("open", () => {
      ws.send(JSON.stringify({
        model: "qwen2.5-coder:7b-instruct-q4_K_M",
        messages
      }));
    });

    ws.on("message", (raw: any) => {
      const msg = JSON.parse(raw.toString());
      if (msg.type === "token" && typeof msg.value === "string") {
        assistantBuffer += msg.value;
      }
      onEvent(msg);
      if (msg.type === "done") {
        if (assistantBuffer) {
          ChatSessionStore.addMessage({ role: 'assistant', content: assistantBuffer });
          assistantBuffer = "";
        }
      }
    });

    ws.on("error", (err: any) => {
      onEvent({ type: "error", message: String(err) });
    });
  }
}
