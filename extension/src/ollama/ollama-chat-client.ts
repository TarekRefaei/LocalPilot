export type ChatMessage = { role: 'system' | 'user' | 'assistant'; content: string };

export class OllamaChatClient {
  async chat(messages: ChatMessage[]): Promise<string> {
    const WS = require('ws');
    const ws = new WS('ws://localhost:8000/ws/chat');

    return new Promise<string>((resolve, reject) => {
      let buffer = '';

      ws.on('open', () => {
        try {
          ws.send(
            JSON.stringify({
              model: 'qwen2.5-coder:7b-instruct-q4_K_M',
              messages,
            })
          );
        } catch (e) {
          reject(e);
        }
      });

      ws.on('message', (raw: any) => {
        try {
          const msg = JSON.parse(raw.toString());
          if (msg.type === 'token' && typeof msg.value === 'string') {
            buffer += msg.value;
          }
          if (msg.type === 'done') {
            resolve(buffer);
            ws.close();
          }
        } catch (e) {
          // ignore malformed frames
        }
      });

      ws.on('error', (err: any) => {
        reject(err);
      });

      ws.on('close', () => {
        // if closed without done, resolve whatever we have
        resolve(buffer);
      });
    });
  }
}
