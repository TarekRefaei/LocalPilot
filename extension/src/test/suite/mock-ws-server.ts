/**
 * Mock WebSocket server for integration tests.
 * Provides a minimal WebSocket server that simulates the backend for testing.
 */

import { WebSocketServer, WebSocket as WSWebSocket } from 'ws';
import { WebSocketEnvelope, createEnvelope } from '@/contracts/envelope';

interface MockServerConfig {
  port?: number;
  host?: string;
}

/**
 * Simple mock WebSocket server that handles handshake and heartbeat.
 * Useful for testing without needing the full backend running.
 */
export class MockWebSocketServer {
  private wss: WebSocketServer | null = null;
  private port: number;
  private host: string;

  constructor(config: MockServerConfig = {}) {
    this.port = config.port ?? 8765;
    this.host = config.host ?? '127.0.0.1';
  }

  /**
   * Start the mock WebSocket server.
   */
  async start(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.wss = new WebSocketServer({ port: this.port, host: this.host });

        this.wss.on('connection', (ws: WSWebSocket) => {
          // eslint-disable-next-line no-console
          console.log('[mock-ws] Client connected');

          ws.on('message', (data: Buffer) => {
            try {
              const envelope = JSON.parse(data.toString()) as WebSocketEnvelope;
              // eslint-disable-next-line no-console
              console.log(`[mock-ws] Received: ${envelope.event}`);

              // Handle handshake
              if (envelope.event === 'handshake') {
                const ackEnvelope = createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: (envelope.data as Record<string, unknown>)?.clientId ?? 'mock-client',
                  capabilities: ['streaming', 'indexing', 'chat', 'plan', 'act', 'vram'],
                  timestamp: new Date().toISOString(),
                });
                ws.send(JSON.stringify(ackEnvelope));
              }

              // Handle heartbeat
              if (envelope.event === 'heartbeat') {
                const ackEnvelope = createEnvelope('heartbeat_ack', {
                  clientId: (envelope.data as Record<string, unknown>)?.clientId ?? 'mock-client',
                  timestamp: new Date().toISOString(),
                });
                ws.send(JSON.stringify(ackEnvelope));
              }

              // Handle indexing.start - broadcast it back
              if (envelope.event === 'indexing.start') {
                // Just echo it back to acknowledge
                ws.send(JSON.stringify(envelope));
              }
            } catch (err) {
              // eslint-disable-next-line no-console
              console.error('[mock-ws] Message parse error:', err);
            }
          });

          ws.on('error', (err) => {
            // eslint-disable-next-line no-console
            console.error('[mock-ws] WebSocket error:', err);
          });

          ws.on('close', () => {
            // eslint-disable-next-line no-console
            console.log('[mock-ws] Client disconnected');
          });
        });

        this.wss.on('error', (err) => {
          // eslint-disable-next-line no-console
          console.error('[mock-ws] Server error:', err);
          reject(err);
        });

        // Server is ready when listening
        this.wss.on('listening', () => {
          // eslint-disable-next-line no-console
          console.log(`[mock-ws] Server listening on ws://${this.host}:${this.port}`);
          resolve();
        });
      } catch (err) {
        reject(err);
      }
    });
  }

  /**
   * Stop the mock WebSocket server.
   */
  async stop(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.wss) {
        resolve();
        return;
      }

      this.wss.close((err) => {
        if (err) {
          reject(err);
        } else {
          // eslint-disable-next-line no-console
          console.log('[mock-ws] Server stopped');
          resolve();
        }
      });
    });
  }
}
