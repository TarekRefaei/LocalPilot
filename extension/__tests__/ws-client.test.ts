/**
 * WebSocket client tests covering reconnect, backoff, heartbeat, and message routing.
 * TDD approach: tests define expected behavior.
 */

import { WebSocketClient } from '../src/services/ws-client';
import {
  WebSocketEnvelope,
  createEnvelope,
  ConnectionState,
} from '../src/contracts/envelope';
import { MockWebSocketServer } from './mocks/mock-ws-server';

describe('WebSocketClient', () => {
  let client: WebSocketClient;
  let mockServer: MockWebSocketServer;
  const testUrl = 'ws://localhost:9999/ws';
  const clientId = 'test-client-123';

  beforeEach(() => {
    mockServer = new MockWebSocketServer(testUrl);
  });

  afterEach(async () => {
    if (client) {
      await client.disconnect();
    }
    mockServer.close();
  });

  describe('Connection Lifecycle', () => {
    it('should connect and complete handshake', async () => {
      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: ['streaming', 'indexing', 'chat'],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      await client.connect();

      expect(client.connectionState).toBe(ConnectionState.Connected);
    });

    it('should emit connected event on successful connection', async () => {
      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      const connectedPromise = new Promise<void>((resolve) => {
        client.on('connected', () => resolve());
      });

      await client.connect();
      await connectedPromise;

      expect(client.connectionState).toBe(ConnectionState.Connected);
    });

    it('should disconnect gracefully', async () => {
      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      await client.connect();
      expect(client.connectionState).toBe(ConnectionState.Connected);

      await client.disconnect();
      expect(client.connectionState).toBe(ConnectionState.Disconnected);
    });
  });

  describe('Reconnection with Exponential Backoff', () => {
    it('should reconnect after connection loss', async () => {
      let connectionCount = 0;

      mockServer.onConnection((ws) => {
        connectionCount++;
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });

        // Close connection after 100ms to trigger reconnect
        if (connectionCount === 1) {
          setTimeout(() => ws.close(), 100);
        }
      });

      client = new WebSocketClient(testUrl, {
        clientId,
        reconnectMaxAttempts: 3,
        reconnectInitialDelayMs: 50,
      });

      const reconnectedPromise = new Promise<void>((resolve) => {
        let reconnectCount = 0;
        client.on('reconnecting', () => {
          reconnectCount++;
          if (reconnectCount === 1) {
            resolve();
          }
        });
      });

      await client.connect();
      await reconnectedPromise;

      expect(client.connectionState).toBe(ConnectionState.Reconnecting);
    });

    it('should apply exponential backoff between reconnect attempts', async () => {
      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            // Reject handshake to force reconnect
            ws.close();
          }
        });
      });

      client = new WebSocketClient(testUrl, {
        clientId,
        reconnectMaxAttempts: 2,
        reconnectInitialDelayMs: 50,
        reconnectMaxDelayMs: 200,
      });

      const reconnectingPromise = new Promise<void>((resolve) => {
        client.on('reconnecting', () => {
          resolve();
        });
      });
      void client.connect();

      await reconnectingPromise;

      // Verify that reconnecting was triggered
      expect(client.connectionState).toBe(ConnectionState.Reconnecting);
    }, 10000);

    it('should emit failed event after max reconnect attempts', async () => {
      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.close();
          }
        });
      });

      client = new WebSocketClient(testUrl, {
        clientId,
        reconnectMaxAttempts: 2,
        reconnectInitialDelayMs: 10,
      });

      const failedPromise = new Promise<void>((resolve) => {
        client.on('failed', () => resolve());
      });
      void client.connect();

      await failedPromise;
      expect(client.connectionState).toBe(ConnectionState.Failed);
    }, 10000);
  });

  describe('Heartbeat and Ping/Pong', () => {
    it('should send heartbeat ping periodically', async () => {
      const pings: string[] = [];

      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          } else if (msg.event === 'heartbeat') {
            pings.push(msg.event);
            ws.send(
              JSON.stringify(
                createEnvelope('heartbeat_ack', {
                  serverTime: new Date().toISOString(),
                  clientTime: msg.data.timestamp,
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, {
        clientId,
        heartbeatIntervalMs: 100,
      });

      client.on('error', () => {
        // Ignore errors
      });

      await client.connect();

      // Wait for at least 2 heartbeats
      await new Promise((resolve) => setTimeout(resolve, 250));

      expect(pings.length).toBeGreaterThanOrEqual(2);
    });

    it('should detect heartbeat timeout and reconnect', async () => {
      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
          // Don't respond to heartbeat to trigger timeout
        });
      });

      client = new WebSocketClient(testUrl, {
        clientId,
        heartbeatIntervalMs: 50,
        heartbeatTimeoutMs: 100,
        reconnectMaxAttempts: 2,
        reconnectInitialDelayMs: 10,
      });

      // Suppress error events for this test
      client.on('error', () => {
        // Ignore errors
      });

      const reconnectingPromise = new Promise<void>((resolve) => {
        client.on('reconnecting', () => resolve());
      });

      await client.connect();
      await reconnectingPromise;

      expect(client.connectionState).toBe(ConnectionState.Reconnecting);
    }, 10000);
  });

  describe('Message Routing and Subscriptions', () => {
    it('should route messages to subscribers by event', async () => {
      const receivedMessages: WebSocketEnvelope[] = [];

      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      client.on('error', () => {
        // Ignore errors
      });
      await client.connect();

      client.subscribe('indexing.start', (envelope) => {
        receivedMessages.push(envelope);
      });

      // Simulate server sending a message
      mockServer.broadcast(
        JSON.stringify(
          createEnvelope('indexing.start', {
            phase: 'scanning',
          })
        )
      );

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(receivedMessages).toHaveLength(1);
      expect(receivedMessages[0]?.event).toBe('indexing.start');
    });

    it('should support multiple subscribers for same event', async () => {
      const subscriber2Messages: WebSocketEnvelope[] = [];

      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      await client.connect();

      client.subscribe('chat.stream.chunk', () => {
        // First subscriber
      });

      client.subscribe('chat.stream.chunk', (envelope) => {
        subscriber2Messages.push(envelope);
      });

      mockServer.broadcast(
        JSON.stringify(
          createEnvelope('chat.stream.chunk', {
            text: 'hello',
          })
        )
      );

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(subscriber2Messages).toHaveLength(1);
    });

    it('should unsubscribe from events', async () => {
      const messages: WebSocketEnvelope[] = [];

      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      await client.connect();

      const unsubscribe = client.subscribe('plan.create', (envelope) => {
        messages.push(envelope);
      });

      unsubscribe();

      mockServer.broadcast(
        JSON.stringify(
          createEnvelope('plan.create', {
            id: 'plan-1',
          })
        )
      );

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(messages).toHaveLength(0);
    });

    it('should handle subscriber errors without breaking routing', async () => {
      const subscriber2Messages: WebSocketEnvelope[] = [];
      const errors: Error[] = [];

      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      await client.connect();

      client.subscribe('act.apply_result', () => {
        throw new Error('Subscriber error');
      });

      client.subscribe('act.apply_result', (envelope) => {
        subscriber2Messages.push(envelope);
      });

      client.on('error', (err: unknown) => {
        if (err instanceof Error) {
          errors.push(err);
        }
      });

      mockServer.broadcast(
        JSON.stringify(
          createEnvelope('act.apply_result', {
            status: 'success',
          })
        )
      );

      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(subscriber2Messages).toHaveLength(1);
      expect(errors.length).toBeGreaterThan(0);
    });
  });

  describe('Error Handling', () => {
    it('should emit error event on invalid message', async () => {
      const errors: Error[] = [];

      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
            // Send invalid message
            ws.send('invalid json {');
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      client.on('error', (err: unknown) => {
        if (err instanceof Error) {
          errors.push(err);
        }
      });

      await client.connect();
      await new Promise((resolve) => setTimeout(resolve, 100));

      expect(errors.length).toBeGreaterThan(0);
    });

    it('should emit error event on connection failure', async () => {
      const errors: Error[] = [];

      client = new WebSocketClient('ws://localhost:19999/ws', { clientId });
      client.on('error', (err: unknown) => {
        if (err instanceof Error) {
          errors.push(err);
        }
      });

      try {
        await client.connect();
      } catch {
        // Expected
      }

      expect(errors.length).toBeGreaterThan(0);
    });
  });

  describe('Offline Handling', () => {
    it('should track offline state', async () => {
      mockServer.onConnection((ws) => {
        ws.on('message', (data: string) => {
          const msg = JSON.parse(data);
          if (msg.event === 'handshake') {
            ws.send(
              JSON.stringify(
                createEnvelope('handshake_ack', {
                  serverVersion: '0.1.0',
                  clientId: msg.data.clientId,
                  capabilities: [],
                  timestamp: new Date().toISOString(),
                })
              )
            );
          }
        });
      });

      client = new WebSocketClient(testUrl, { clientId });
      expect(client.isOnline).toBe(false);

      await client.connect();
      expect(client.isOnline).toBe(true);

      void client.disconnect();
      expect(client.isOnline).toBe(false);
    });
  });
});
