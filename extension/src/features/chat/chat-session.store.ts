export type ChatMessage = { role: 'system' | 'user' | 'assistant'; content: string };

export class ChatSessionStore {
  private static messages: ChatMessage[] = [];

  static addMessage(msg: ChatMessage) {
    if (!msg || !msg.role || typeof msg.content !== 'string') return;
    this.messages.push({ role: msg.role, content: msg.content });
  }

  static getMessages(): ChatMessage[] {
    return [...this.messages];
  }

  static clear() {
    this.messages = [];
  }
}
