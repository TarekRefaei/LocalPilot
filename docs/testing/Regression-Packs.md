# Regression Packs

This document lists stable regression scenarios and how to run/extend them.

## Backend packs

- Health endpoints
  - Files: `backend/app/api/health.py`, tests under `tests/`
  - Commands:
    ```bash
    pytest -q tests/test_health_endpoints.py
    ```
- WebSocket core
  - Files: `backend/app/api/websocket.py`, `app/services/ws_manager.py`
  - Commands:
    ```bash
    pytest -q tests/test_ws_manager_unit.py tests/test_websocket.py tests/test_act_websocket.py
    ```
- Retrieval + RAG metrics
  - Files: `backend/app/services/rag/*`
  - Commands:
    ```bash
    pytest -q tests/test_retrieval_integration.py tests/test_fusion.py tests/test_rag_metrics_edges.py
    ```
- VectorStore (Windows-safe)
  - Files: `backend/app/services/rag/vector_store.py`
  - Commands:
    ```bash
    pytest -q tests/test_vector_store.py tests/test_vector_store_fake_chroma.py
    ```

## Extension packs

- WebSocket client
  - Files: `extension/src/services/ws-client.ts`
  - Commands:
    ```bash
    npm run test -- __tests__/ws-client.test.ts
    ```
- Realtime service
  - Files: `extension/src/services/realtime.ts`
  - Commands:
    ```bash
    npm run test -- __tests__/realtime.test.ts __tests__/realtime.behavior.test.ts __tests__/realtime.errors.test.ts
    ```
- Commands + Views
  - Files: `extension/src/commands.ts`, `extension/src/views/*`
  - Commands:
    ```bash
    npm run test -- __tests__/commands.test.ts __tests__/views.test.ts __tests__/extension.test.ts
    ```

## Adding new scenarios

- Prefer deterministic tests (no real network, controlled timers, mocked clients)
- For backend tests that hit Chroma, favor monkeypatching to fake the client (cross-platform)
- Keep performance tests under `tests/performance` and mark with `@pytest.mark.performance`

## Notes

- CI runs these packs by default as part of the full suite across OSes.
- The nightly perf job runs smoke tests with timings and uploads artifacts.
