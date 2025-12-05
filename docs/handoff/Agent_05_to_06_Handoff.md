# Agent 05 → Agent 06 Handoff: Backend API Gateway → Indexing Service

**Date:** 2025-01-15
**Status:** ✅ COMPLETED
**PR:** #5 (feat(api): expose REST health/config and WS topics)

---

## Summary

Agent 05 delivered a production-ready FastAPI gateway with:
- ✅ REST endpoints: `/health`, `/health/ollama`, `/config`
- ✅ WebSocket endpoint: `ws://localhost:8765/ws?client_id={uuid}`
- ✅ Pydantic models aligned with TypeScript contracts
- ✅ Structured JSON logging
- ✅ 28 passing tests (health, WebSocket, legacy)
- ✅ Configuration via environment variables and .env

---

## What Agent 06 Needs to Know

### 1. WebSocket Event Topics for Indexing

Agent 06 will implement the **Indexing Service** and emit events via WebSocket. The topics are pre-defined in the contract:

**Client → Server:**
```
event: "indexing.start"
payload: IndexingStartPayload {
  workspace_path: str
  options: {
    exclude_patterns: list[str]
    max_file_size_mb: int
    languages: list[str]
    force_reindex: bool
  }
}
```

**Server → Client (streaming):**
```
event: "indexing.progress"
payload: IndexingProgressPayload {
  indexing_id: str
  phase: str  # "discovery" | "documentation" | "structure" | "chunking" | "summarization"
  phase_number: int
  total_phases: int
  current_file: int
  total_files: int
  current_file_path: str
  percentage: float
  estimated_time_remaining_seconds: int
  message: str
}
```

**Server → Client (completion):**
```
event: "indexing.complete"
payload: IndexingCompletePayload {
  indexing_id: str
  duration_seconds: int
  statistics: {
    total_files: int
    indexed_files: int
    failed_files: int
    total_chunks: int
    total_embeddings: int
    total_symbols: int
    index_size_mb: float
  }
  project_summary: str
  failed_files: list[{path: str, error: str}]
}
```

**Server → Client (error):**
```
event: "indexing.error"
payload: ErrorData {
  message: str
  code: str  # e.g., "PARSING_FAILED"
  details: {
    failed_count: int
    total_files: int
    can_continue: bool
  }
}
```

### 2. Envelope Contract

All WebSocket messages use `WebSocketEnvelope`:

```python
class WebSocketEnvelope(BaseModel):
    event: str                    # "indexing.start", "indexing.progress", etc.
    data: Any                     # Payload (IndexingStartPayload, etc.)
    timestamp: str                # ISO 8601, auto-generated
    correlationId: str            # UUID, auto-generated
    contractVersion: str          # "0.1.0"
```

**Important:** Always include `correlationId` in responses to match client requests.

### 3. How to Send Events

Use the global `ConnectionManager` in `app.api.websocket`:

```python
from app.api.websocket import get_manager
from app.models.envelope import WebSocketEnvelope

manager = get_manager()

# Broadcast to all clients
envelope = WebSocketEnvelope(
    event="indexing.progress",
    data=IndexingProgressPayload(...).model_dump(),
    correlationId=request_correlation_id,
)
await manager.broadcast(envelope.model_dump())

# Send to specific client
await manager.send_personal(client_id, envelope.model_dump())
```

### 4. Service Integration Pattern

**Recommended structure for Indexing Service:**

```python
# app/services/indexing/indexing_service.py
from app.api.websocket import get_manager
from app.models.envelope import WebSocketEnvelope, IndexingProgressPayload

class IndexingService:
    async def index_workspace(self, workspace_path: str, client_id: str):
        manager = get_manager()
        indexing_id = f"idx-{datetime.now().isoformat()}"

        # Phase 1: Discovery
        await manager.send_personal(client_id, WebSocketEnvelope(
            event="indexing.progress",
            data=IndexingProgressPayload(
                indexing_id=indexing_id,
                phase="discovery",
                phase_number=1,
                total_phases=5,
                current_file=0,
                total_files=0,
                percentage=0.0,
                estimated_time_remaining_seconds=0,
                message="Scanning workspace..."
            ).model_dump()
        ).model_dump())

        # ... implementation ...

        # Completion
        await manager.send_personal(client_id, WebSocketEnvelope(
            event="indexing.complete",
            data=IndexingCompletePayload(...).model_dump()
        ).model_dump())
```

### 5. REST Endpoints (Future)

Agent 06 should add these REST endpoints:

```
GET /api/indexing/status?workspace_id={id}
  → IndexingStatusResponse

POST /api/indexing/cancel
  → {success: bool, indexing_id: str, status: str}
```

Models are pre-defined in `app/models/envelope.py`.

### 6. Testing Expectations

Agent 06 should:
- ✅ Write pytest tests for indexing service
- ✅ Mock WebSocket manager for unit tests
- ✅ Test all 5 phases with progress events
- ✅ Test error handling and recovery
- ✅ Test statistics calculation
- ✅ Verify envelope contract compliance

Example test:

```python
def test_indexing_emits_progress_events(mock_manager):
    service = IndexingService()

    # Mock manager.send_personal
    mock_manager.send_personal = AsyncMock()

    # Run indexing
    await service.index_workspace("/path", "client-123")

    # Verify progress events sent
    calls = mock_manager.send_personal.call_args_list
    assert len(calls) >= 5  # At least one per phase

    # Verify first event is discovery
    first_call = calls[0]
    assert first_call[0][0] == "client-123"
    assert first_call[0][1]["event"] == "indexing.progress"
    assert first_call[0][1]["data"]["phase"] == "discovery"
```

### 7. Configuration Available

Agent 06 can use these settings from `app.core.config`:

```python
from app.core.config import settings

settings.vector_db_path      # "./data/chroma"
settings.ollama_host         # "http://localhost:11434"
settings.ollama_timeout_seconds  # 120
```

Add new settings as needed (e.g., `INDEXING_BATCH_SIZE`, `CHUNK_SIZE`).

### 8. Logging

Use the logger from `app.core.logging`:

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

logger.info("Starting indexing", extra={"indexing_id": indexing_id})
logger.error("Indexing failed", extra={"error": str(e)})
```

Logs are JSON-formatted with timestamp, level, logger, message.

### 9. Error Handling

Always send error envelopes on failure:

```python
from app.models.envelope import ErrorData, WebSocketEnvelope

error_envelope = WebSocketEnvelope(
    event="indexing.error",
    data=ErrorData(
        message="Failed to parse file",
        code="PARSING_FAILED",
        details={"file": path, "error": str(e)}
    ).model_dump(),
    correlationId=request_correlation_id
)
await manager.send_personal(client_id, error_envelope.model_dump())
```

### 10. Files to Reference

- **Models:** `app/models/envelope.py` (IndexingStartPayload, IndexingProgressPayload, etc.)
- **Manager:** `app/api/websocket.py` (ConnectionManager, get_manager())
- **Logging:** `app/core/logging.py` (get_logger)
- **Config:** `app/core/config.py` (settings)
- **Tests:** `tests/test_websocket.py` (WebSocket test patterns)

---

## What's Ready for Agent 06

### ✅ Infrastructure
- FastAPI app running on 127.0.0.1:8765
- WebSocket endpoint accepting connections
- Connection manager for message routing
- Structured logging (JSON format)
- Configuration system (env vars + .env)

### ✅ Contracts
- All Pydantic models for indexing events
- Envelope format with correlation IDs
- Error handling patterns
- Timestamp and versioning

### ✅ Testing
- Test client setup (TestClient)
- WebSocket connection patterns
- Message assertion patterns
- Mock patterns for async code

### ⚠️ Not Yet Implemented
- Indexing service logic (Agent 06 responsibility)
- Vector database integration (Agent 06 responsibility)
- Embedding service (Agent 06 responsibility)
- Tree-sitter parser (Agent 06 responsibility)
- File discovery and chunking (Agent 06 responsibility)

---

## Acceptance Criteria for Agent 06

Agent 06 is complete when:

- ✅ Indexing service implements 5-phase pipeline
- ✅ All phases emit progress events with correct structure
- ✅ Completion event includes statistics
- ✅ Error events sent on failures
- ✅ Correlation IDs preserved in responses
- ✅ All pytest tests pass
- ✅ WebSocket integration smoke test passes
- ✅ Handoff document created for Agent 07 (Chat)

---

## Quick Start for Agent 06

1. **Create indexing service:**
   ```bash
   touch app/services/indexing/__init__.py
   touch app/services/indexing/indexing_service.py
   ```

2. **Add to main.py router:**
   ```python
   from app.services.indexing import indexing_service
   # Wire up WebSocket handler for "indexing.start" events
   ```

3. **Write tests:**
   ```bash
   touch tests/test_indexing_service.py
   ```

4. **Run tests:**
   ```bash
   pytest tests/test_indexing_service.py -v
   ```

5. **Verify WebSocket integration:**
   ```bash
   pytest tests/test_websocket.py::TestWebSocketMessageRouting -v
   ```

---

## Known Issues & Limitations

1. **Ollama Integration** — Currently mocked in health endpoint
   - Agent 06 should implement real Ollama client
   - Test with actual Ollama running on localhost:11434

2. **Vector Database** — Not yet initialized
   - Agent 06 should set up ChromaDB at `./data/chroma`
   - Create collection for embeddings

3. **File System Access** — Not yet implemented
   - Agent 06 should use `pathlib` for cross-platform paths
   - Handle Windows path separators correctly

4. **Async Patterns** — All services should be async
   - Use `async def` and `await`
   - Avoid blocking I/O in handlers

---

## Questions for Agent 06?

Refer to:
- **API Spec:** `docs/projectdocuments/API_Specifications.md`
- **Tech Architecture:** `docs/projectdocuments/Technical_Architecture.md`
- **WebSocket Contract:** `docs/agents/04-WebSocket-Client-Contract.md`
- **API Gateway Summary:** `backend/docs/API_GATEWAY_SUMMARY.md`

Good luck! 🚀
