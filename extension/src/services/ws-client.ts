/**
 * Robust WebSocket client with reconnect, exponential backoff, and heartbeat.
 * Provides message routing and subscription management.
 */

import { EventEmitter } from 'events';
import {
  WebSocketEnvelope,
  ConnectionState,
  WsError,
  WsErrorCode,
  createEnvelope,
  HandshakePayload,
  HeartbeatPayload,
  generateUUID,
} from '../contracts/envelope';

// Use native WebSocket in browser, ws package in Node.js (tests)
// eslint-disable-next-line @typescript-eslint/no-var-requires, @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unnecessary-type-assertion
const WS = typeof WebSocket !== 'undefined' ? WebSocket : require('ws');

/**
 * Configuration for WebSocket client.
 */
export interface WebSocketClientConfig {
  clientId?: string;
  reconnectMaxAttempts?: number;
  reconnectInitialDelayMs?: number;
  reconnectMaxDelayMs?: number;
  heartbeatIntervalMs?: number;
  heartbeatTimeoutMs?: number;
  handshakeTimeoutMs?: number;
}

/**
 * Message subscriber callback.
 */
type MessageSubscriber = (envelope: WebSocketEnvelope) => void;

/**
 * Unsubscribe function.
 */
type Unsubscribe = () => void;

/**
 * Robust WebSocket client with automatic reconnection and heartbeat.
 */
export class WebSocketClient {
  private emitter: EventEmitter;
  private ws: WebSocket | null = null;
  private state: ConnectionState = ConnectionState.Disconnected;
  private clientId: string;
  private url: string;
  private config: Required<WebSocketClientConfig>;
  private subscribers = new Map<string, Set<MessageSubscriber>>();
  private reconnectAttempts = 0;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private heartbeatTimeoutTimer: NodeJS.Timeout | null = null;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private isManualDisconnect = false;

  constructor(url: string, config: WebSocketClientConfig = {}) {
    this.emitter = new EventEmitter();
    this.url = url;
    this.clientId = config.clientId ?? generateUUID();
    this.config = {
      clientId: this.clientId,
      reconnectMaxAttempts: config.reconnectMaxAttempts ?? 5,
      reconnectInitialDelayMs: config.reconnectInitialDelayMs ?? 1000,
      reconnectMaxDelayMs: config.reconnectMaxDelayMs ?? 30000,
      heartbeatIntervalMs: config.heartbeatIntervalMs ?? 30000,
      heartbeatTimeoutMs: config.heartbeatTimeoutMs ?? 10000,
      handshakeTimeoutMs: config.handshakeTimeoutMs ?? 5000,
    } as Required<WebSocketClientConfig>;
  }

  /**
   * Register event listener.
   */
  on(event: string, listener: (...args: unknown[]) => void): void {
    this.emitter.on(event, listener);
  }

  /**
   * Emit event.
   */
  private emit(event: string, ...args: unknown[]): void {
    this.emitter.emit(event, ...args);
  }

  /**
   * Get current connection state.
   */
  get connectionState(): ConnectionState {
    return this.state;
  }

  /**
   * Check if client is online.
   */
  get isOnline(): boolean {
    return this.state === ConnectionState.Connected;
  }

  /**
   * Connect to the WebSocket server.
   */
  async connect(): Promise<void> {
    if (this.state === ConnectionState.Connected || this.state === ConnectionState.Connecting) {
      return;
    }

    this.isManualDisconnect = false;
    this.setState(ConnectionState.Connecting);

    return new Promise((resolve, reject) => {
      try {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call
        this.ws = new WS(this.url);

        const handshakeTimeout = setTimeout(() => {
          const error = new WsError(WsErrorCode.HandshakeFailed, 'Handshake timeout');
          this.handleError(error);
          reject(error);
        }, this.config.handshakeTimeoutMs);

        this.ws!.onopen = () => {
          this.sendHandshake();
        };

        this.ws!.onmessage = (event: Event) => {
          const message = this.parseMessage((event as MessageEvent).data as string);
          if (!message) return;

          if (message.event === 'handshake_ack') {
            clearTimeout(handshakeTimeout);
            this.setState(ConnectionState.Connected);
            this.reconnectAttempts = 0;
            this.startHeartbeat();
            this.emit('connected');
            resolve();
          } else {
            this.routeMessage(message);
          }
        };

        this.ws!.onerror = (event: Event | string) => {
          clearTimeout(handshakeTimeout);
          const eventStr = typeof event === 'string' ? event : String(event);
          const error = new WsError(WsErrorCode.ConnectionFailed, `WebSocket error: ${eventStr}`);
          this.handleError(error);
          reject(error);
        };

        this.ws!.onclose = () => {
          clearTimeout(handshakeTimeout);
          if (!this.isManualDisconnect) {
            this.attemptReconnect();
          } else {
            this.setState(ConnectionState.Disconnected);
          }
        };
      } catch (err) {
        const error = new WsError(
          WsErrorCode.ConnectionFailed,
          err instanceof Error ? err.message : String(err)
        );
        this.handleError(error);
        reject(error);
      }
    });
  }

  /**
   * Disconnect from the WebSocket server.
   */
  disconnect(): Promise<void> {
    this.isManualDisconnect = true;
    this.stopHeartbeat();
    this.clearReconnectTimer();

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.setState(ConnectionState.Disconnected);
    return Promise.resolve();
  }

  /**
   * Subscribe to messages for a specific event.
   */
  subscribe(event: string, subscriber: MessageSubscriber): Unsubscribe {
    if (!this.subscribers.has(event)) {
      this.subscribers.set(event, new Set());
    }

    this.subscribers.get(event)!.add(subscriber);

    return () => {
      const set = this.subscribers.get(event);
      if (set) {
        set.delete(subscriber);
        if (set.size === 0) {
          this.subscribers.delete(event);
        }
      }
    };
  }

  /**
   * Send a message to the server.
   */
  send<T>(event: string, data: T): void {
    if (!this.isOnline) {
      throw new WsError(WsErrorCode.ConnectionFailed, 'Cannot send message: not connected');
    }

    const envelope = createEnvelope(event, data);
    this.ws!.send(JSON.stringify(envelope));
  }

  /**
   * Private: Send handshake to server.
   */
  private sendHandshake(): void {
    const payload: HandshakePayload = {
      version: '0.1.0',
      clientId: this.clientId,
    };

    const envelope = createEnvelope('handshake', payload);
    this.ws!.send(JSON.stringify(envelope));
  }

  /**
   * Private: Start heartbeat timer.
   */
  private startHeartbeat(): void {
    this.stopHeartbeat();

    this.heartbeatTimer = setInterval(() => {
      if (this.isOnline) {
        this.sendHeartbeat();
      }
    }, this.config.heartbeatIntervalMs);
  }

  /**
   * Private: Stop heartbeat timer.
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }

    if (this.heartbeatTimeoutTimer) {
      clearTimeout(this.heartbeatTimeoutTimer);
      this.heartbeatTimeoutTimer = null;
    }
  }

  /**
   * Private: Send heartbeat ping.
   */
  private sendHeartbeat(): void {
    try {
      const payload: HeartbeatPayload = {
        clientId: this.clientId,
        timestamp: new Date().toISOString(),
      };

      const envelope = createEnvelope('heartbeat', payload);
      this.ws!.send(JSON.stringify(envelope));

      // Set timeout for heartbeat response
      this.heartbeatTimeoutTimer = setTimeout(() => {
        const error = new WsError(
          WsErrorCode.HeartbeatTimeout,
          'Heartbeat timeout: no response from server'
        );
        this.handleError(error);
        this.attemptReconnect();
      }, this.config.heartbeatTimeoutMs);
    } catch (err: unknown) {
      const error = new WsError(
        WsErrorCode.ConnectionFailed,
        err instanceof Error ? err.message : String(err)
      );
      this.handleError(error);
    }
  }

  /**
   * Private: Handle heartbeat acknowledgement.
   */
  private handleHeartbeatAck(): void {
    if (this.heartbeatTimeoutTimer) {
      clearTimeout(this.heartbeatTimeoutTimer);
      this.heartbeatTimeoutTimer = null;
    }
  }

  /**
   * Private: Attempt to reconnect with exponential backoff.
   */
  private attemptReconnect(): void {
    if (this.isManualDisconnect) {
      return;
    }

    if (this.reconnectAttempts >= this.config.reconnectMaxAttempts) {
      this.setState(ConnectionState.Failed);
      this.emit('failed');
      return;
    }

    this.reconnectAttempts++;
    this.setState(ConnectionState.Reconnecting);
    this.emit('reconnecting');

    const delay = this.calculateBackoffDelay(this.reconnectAttempts);
    this.reconnectTimer = setTimeout(() => {
      this.connect().catch((err: unknown) => {
        if (err instanceof Error) {
          this.handleError(err);
        }
      });
    }, delay);
  }

  /**
   * Private: Calculate exponential backoff delay.
   */
  private calculateBackoffDelay(attempt: number): number {
    const exponentialDelay = this.config.reconnectInitialDelayMs * Math.pow(2, attempt - 1);
    const jitter = Math.random() * 1000;
    const delay = Math.min(exponentialDelay + jitter, this.config.reconnectMaxDelayMs);
    return Math.floor(delay);
  }

  /**
   * Private: Route incoming message to subscribers.
   */
  private routeMessage(envelope: WebSocketEnvelope): void {
    // Handle heartbeat ack
    if (envelope.event === 'heartbeat_ack') {
      this.handleHeartbeatAck();
      return;
    }

    // Route to subscribers
    const subscribers = this.subscribers.get(envelope.event);
    if (subscribers) {
      subscribers.forEach((subscriber) => {
        try {
          subscriber(envelope);
        } catch (err: unknown) {
          const errMsg = err instanceof Error ? err.message : String(err);
          const error = new WsError(WsErrorCode.SubscriberError, errMsg, { event: envelope.event });
          this.handleError(error);
        }
      });
    }
  }

  /**
   * Private: Parse incoming message.
   */
  private parseMessage(data: string): WebSocketEnvelope | null {
    try {
      return JSON.parse(data) as WebSocketEnvelope;
    } catch (err: unknown) {
      const error = new WsError(
        WsErrorCode.InvalidMessage,
        err instanceof Error ? err.message : String(err)
      );
      this.handleError(error);
      return null;
    }
  }

  /**
   * Private: Update connection state.
   */
  private setState(newState: ConnectionState): void {
    if (this.state !== newState) {
      this.state = newState;
    }
  }

  /**
   * Private: Handle errors.
   */
  private handleError(error: Error): void {
    this.emit('error', error);
  }

  /**
   * Private: Clear reconnect timer.
   */
  private clearReconnectTimer(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }
}
