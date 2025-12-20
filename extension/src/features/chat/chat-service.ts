import { queryRAG } from "./rag-client";
import { PromptBuilder } from "./prompt-builder";
import { getProjectSummary } from "../../infrastructure/http/api-client";

export class ChatService {
  async sendMessage(
    userMessage: string,
    onEvent: (event: any) => void,
    projectId: string
  ): Promise<void> {

    const chunks = await queryRAG(projectId, userMessage);
    const summary = await getProjectSummary(projectId);
    const messages = new PromptBuilder().build(userMessage, chunks, summary);

    const WS = require("ws");
    const ws = new WS("ws://localhost:8000/ws/chat");

    ws.on("open", () => {
      ws.send(JSON.stringify({
        model: "qwen2.5-coder:7b-instruct-q4_K_M",
        messages
      }));
    });

    ws.on("message", (raw: any) => {
      const msg = JSON.parse(raw.toString());
      onEvent(msg);
    });

    ws.on("error", (err: any) => {
      onEvent({ type: "error", message: String(err) });
    });
  }
}
