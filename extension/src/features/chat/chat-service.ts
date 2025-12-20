import { queryRAG } from "./rag-client";
import { PromptBuilder } from "./prompt-builder";

export class ChatService {
  async sendMessage(
    userMessage: string,
    onEvent: (event: any) => void,
    projectId: string
  ): Promise<void> {

    const chunks = await queryRAG(projectId, userMessage);
    const messages = new PromptBuilder().build(userMessage, chunks);

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
