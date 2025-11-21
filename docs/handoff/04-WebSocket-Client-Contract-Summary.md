# Agent 04 — WebSocket Client & Contract Summary

## Overview
Implemented a robust WebSocket client with automatic reconnection, exponential backoff, heartbeat/ping-pong, and message routing. Shared contract types ensure type-safe communication between extension and backend.

## Deliverables

### 1. Shared Contract Types (`src/contracts/envelope.ts`)
- **WebSocketEnvelope**: Standard message format with event, data, timestamp, correlationId, contractVersion
- **ConnectionState**: Enum for client states (Disconnected, Connecting, Connected, Reconnecting, Failed)
- **WsErrorCode**: Standardized error codes (ConnectionFailed, HandshakeFailed, HeartbeatTimeout, etc.)
- **WsError**: Custom error class with code and details
- **Payload Types**: HandshakePayload, HandshakeAckPayload, HeartbeatPayload, HeartbeatAckPayload
- **Utilities**: createEnvelope(), createErrorEnvelope(), generateUUID(), createCorrelationId()

### 2. WebSocket Client (`src/services/ws-client.ts`)
**Features:**
- Automatic reconnection with exponential backoff (configurable delays and max attempts)
- Heartbeat/ping-pong mechanism with timeout detection
- Message routing to subscribers by event topic
- Error handling and propagation
- Offline state tracking
- Clean disconnect with resource cleanup

**Configuration:**
```typescript
interface WebSocketClientConfig {
  clientId?: string;                    // Default: generated UUID
  reconnectMaxAttempts?: number;        // Default: 5
  reconnectInitialDelayMs?: number;     // Default: 1000ms
  reconnectMaxDelayMs?: number;         // Default: 30000ms
  heartbeatIntervalMs?: number;         // Default: 30000ms
  heartbeatTimeoutMs?: number;          // Default: 10000ms
  handshakeTimeoutMs?: number;          // Default: 5000ms
}
```

**Public API:**
- `connect(): Promise<void>` — Connect to server with handshake
- `disconnect(): Promise<void>` — Graceful disconnect
- `subscribe(event: string, subscriber): Unsubscribe` — Subscribe to events
- `send<T>(event: string, data: T): void` — Send message to server
- `get connectionState(): ConnectionState` — Current connection state
- `get isOnline(): boolean` — Quick online check
- `on(event: string, handler)` — EventEmitter for: 'connected', 'reconnecting', 'failed', 'error'

### 3. Mock WebSocket Server (`__tests__/mocks/mock-ws-server.ts`)
- Deterministic testing with ws library
- Supports connection handlers and message broadcasting
- Used for all unit tests

### 4. Comprehensive Unit Tests (`__tests__/ws-client.test.ts`)
**Test Coverage:**
- Connection lifecycle (connect, handshake, disconnect)
- Reconnection with exponential backoff
- Heartbeat/ping-pong with timeout detection
- Message routing to single and multiple subscribers
- Unsubscribe functionality
- Subscriber error isolation
- Invalid message handling
- Connection failure handling
- Offline state tracking

## Contract Specification

### Message Envelope Format
```json
{
  "event": "<category.name>",
  "data": { /* payload */ },
  "timestamp": "<ISO8601>",
  "correlationId": "<uuid>",
  "contractVersion": "0.1.0"
}
```

### Handshake Flow
1. Client connects to `ws://localhost:8765/ws`
2. Client sends `handshake` event with clientId and version
3. Server responds with `handshake_ack` containing capabilities
4. Client starts heartbeat timer

### Heartbeat Flow
1. Client sends `heartbeat` event every 30s (configurable)
2. Server responds with `heartbeat_ack`
3. If no response within 10s (configurable), client reconnects

### Error Handling
- Invalid JSON messages logged and ignored (routing continues)
- Subscriber errors caught and emitted as 'error' events (other subscribers unaffected)
- Connection errors trigger reconnection with backoff
- Heartbeat timeouts trigger reconnection

### Reconnection Strategy
- Exponential backoff: `delay = min(initialDelay * 2^(attempt-1) + jitter, maxDelay)`
- Jitter: random 0-1000ms to prevent thundering herd
- Max attempts: 5 (configurable)
- After max attempts: emit 'failed' event and stop reconnecting

## Integration Points

### Extension Integration
1. Initialize client in extension activation:
```typescript
const wsClient = new WebSocketClient('ws://localhost:8765/ws', {
  clientId: generateUUID(),
  reconnectMaxAttempts: 5,
});

await wsClient.connect();

// Subscribe to events
wsClient.subscribe('indexing.progress', (envelope) => {
  // Handle indexing progress
});

// Send messages
wsClient.send('chat.request', { prompt: 'hello' });
```

2. Store client in extension state for access across commands/views

### Backend Integration
- Backend must implement WebSocket endpoint at `/ws`
- Must respond to `handshake` with `handshake_ack`
- Must respond to `heartbeat` with `heartbeat_ack`
- Should validate `contractVersion` for forward compatibility

## Testing

### Run Tests
```bash
npm test
```

### Test Structure
- **Connection Lifecycle**: 3 tests
- **Reconnection with Backoff**: 3 tests
- **Heartbeat/Ping-Pong**: 2 tests
- **Message Routing**: 5 tests
- **Error Handling**: 2 tests
- **Offline Handling**: 1 test

**Total: 16 tests** covering all critical paths

## Type Safety
- Strict TypeScript mode enabled
- All event types use branded strings for correlation IDs
- Envelope types are generic for type-safe payloads
- Error codes are enums (not strings)

## Performance Considerations
- Heartbeat interval: 30s (configurable, prevents excessive traffic)
- Heartbeat timeout: 10s (detects stale connections quickly)
- Reconnect backoff: exponential with jitter (prevents thundering herd)
- Message routing: O(1) lookup by event topic using Map

## Future Enhancements
1. **Message Queuing**: Queue messages while offline, send on reconnect
2. **Compression**: Add optional message compression for large payloads
3. **Request/Response Pattern**: Add request ID tracking for RPC-style calls
4. **Metrics**: Track connection uptime, message latency, error rates
5. **Multiplexing**: Support multiple concurrent subscriptions per event

## Files Modified/Created
- ✅ `src/contracts/envelope.ts` — Shared contract types
- ✅ `src/services/ws-client.ts` — WebSocket client implementation
- ✅ `__tests__/ws-client.test.ts` — Comprehensive unit tests
- ✅ `__tests__/mocks/mock-ws-server.ts` — Mock server for testing
- ✅ `package.json` — Added ws and @types/ws dependencies

## Acceptance Criteria Status
- ✅ Reconnect works with exponential backoff
- ✅ Messages routed to subscribers
- ✅ Heartbeat/ping-pong verified in tests
- ✅ Unit tests pass (16 tests)
- ✅ Contract types compile in strict TS mode
- ✅ Lint and format pass

## Next Steps (Agent 05)
1. Implement backend WebSocket endpoint at `/ws`
2. Implement handshake_ack and heartbeat_ack handlers
3. Implement message broadcasting for events (indexing, chat, plan, act)
4. Add integration tests with real backend
5. Document topic-specific payloads in Contracts_Index.md
