# LocalPilot Testing Guide

## Backend

- Run tests:
  - `pytest -q --maxfail=1 --cov=app --cov-report=term-missing -rs`
- Windows-safe ChromaDB:
  - Tests use an in-memory fake Chroma client via env/fixtures to avoid file locks.
- Coverage targets:
  - Backend: ≥85% (currently ~89%)
- Key areas covered:
  - WebSocket: handshake, heartbeat, routing
  - Retrieval: endpoint, metrics, evaluation harness
  - Indexing: symbol map, chunking (lexical) helpers and patterns

## Extension (VS Code)

- Run tests:
  - `npm test -- --coverage` (or `pnpm test -- --coverage`)
- Coverage thresholds:
  - Lines ≥85%, Branches ≥75%
- Areas covered:
  - WebSocket client reconnection, heartbeat, message routing

## Notes

- No skipped tests. All suites are Windows-compatible.
- FastAPI lifespan handlers are used (no startup/shutdown deprecation warnings).
- If any test hangs:
  - Check WebSocket tests for blocking receives after disconnects.
