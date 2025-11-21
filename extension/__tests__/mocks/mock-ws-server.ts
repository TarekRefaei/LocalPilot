/**
 * Mock WebSocket server for deterministic testing.
 * Uses ws library to simulate backend behavior.
 */

import { Server, WebSocket } from 'ws';

export class MockWebSocketServer {
  private server: Server;

  constructor(url: string) {
    const port = parseInt(url.split(':')[2] || '9999', 10);
    this.server = new Server({ port });
  }

  onConnection(handler: (ws: WebSocket) => void): void {
    this.server.on('connection', (ws) => {
      handler(ws);
    });
  }

  broadcast(data: string): void {
    this.server.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(data);
      }
    });
  }

  close(): void {
    this.server.clients.forEach((client) => {
      client.close();
    });
    this.server.close();
  }
}
