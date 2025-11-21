/**
 * Shared WebSocket envelope and message contracts.
 * Single source of truth for extension-backend communication.
 * Contract version: 0.1.0
 */

/**
 * Unique identifier for correlation and tracing.
 */
export type CorrelationId = string & { readonly __brand: 'CorrelationId' };

export function createCorrelationId(): CorrelationId {
  return generateUUID() as CorrelationId;
}

/**
 * WebSocket message envelope wrapping all messages.
 * Provides routing, correlation, and versioning.
 */
export interface WebSocketEnvelope<T = unknown> {
  /** Event topic in dot-separated format (e.g., "indexing.start") */
  event: string;

  /** Payload data specific to the event type */
  data: T;

  /** ISO 8601 timestamp when message was created */
  timestamp: string;

  /** Unique identifier for request/response correlation */
  correlationId: CorrelationId;

  /** Contract version for forward compatibility */
  contractVersion: string;
}

/**
 * Error envelope for error events.
 */
export interface ErrorData {
  message: string;
  code: string;
  details?: Record<string, unknown>;
}

/**
 * Handshake payload sent by client on connection.
 */
export interface HandshakePayload {
  version: string;
  workspace?: string;
  clientId: string;
}

/**
 * Handshake acknowledgement from server.
 */
export interface HandshakeAckPayload {
  serverVersion: string;
  clientId: string;
  capabilities: string[];
  timestamp: string;
}

/**
 * Heartbeat/ping payload.
 */
export interface HeartbeatPayload {
  clientId: string;
  timestamp: string;
}

/**
 * Heartbeat acknowledgement/pong payload.
 */
export interface HeartbeatAckPayload {
  serverTime: string;
  clientTime: string;
}

/**
 * Connection state for the WebSocket client.
 */
export enum ConnectionState {
  Disconnected = 'disconnected',
  Connecting = 'connecting',
  Connected = 'connected',
  Reconnecting = 'reconnecting',
  Failed = 'failed',
}

/**
 * Error codes for WebSocket operations.
 */
export enum WsErrorCode {
  ConnectionFailed = 'CONNECTION_FAILED',
  ConnectionTimeout = 'CONNECTION_TIMEOUT',
  HandshakeFailed = 'HANDSHAKE_FAILED',
  MessageRoutingFailed = 'MESSAGE_ROUTING_FAILED',
  SubscriberError = 'SUBSCRIBER_ERROR',
  HeartbeatTimeout = 'HEARTBEAT_TIMEOUT',
  InvalidMessage = 'INVALID_MESSAGE',
  UnknownError = 'UNKNOWN_ERROR',
}

/**
 * WebSocket client error with context.
 */
export class WsError extends Error {
  constructor(
    public code: WsErrorCode,
    message: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'WsError';
  }
}

/**
 * Generate a UUID v4.
 */
export function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

/**
 * Create a WebSocket envelope with defaults.
 */
export function createEnvelope<T>(
  event: string,
  data: T,
  correlationId?: CorrelationId
): WebSocketEnvelope<T> {
  return {
    event,
    data,
    timestamp: new Date().toISOString(),
    correlationId: correlationId ?? createCorrelationId(),
    contractVersion: '0.1.0',
  };
}

/**
 * Create an error envelope.
 */
export function createErrorEnvelope(
  event: string,
  code: string,
  message: string,
  details?: Record<string, unknown>,
  correlationId?: CorrelationId
): WebSocketEnvelope<ErrorData> {
  return createEnvelope(
    event,
    {
      message,
      code,
      details: details ?? {},
    },
    correlationId
  );
}
