# Agent 12 — Integration & E2E Plan

Version: 1.0  
Status: Active  
Owner: Agent 12

---

## Objective
Create a stable, deterministic, Windows-friendly E2E scenario to validate Chat → Plan → Act across extension and backend. Provide nightly CI, fixtures, and diagnostics.

## Scope
- Cross-component validation via backend APIs (REST + WebSocket)
- Deterministic seeds, temp Git workspace, safe Act operations under `docs/**`
- Nightly CI (Windows) and artifacts for failure triage

## Scenario Summary
- Scenario ID: `chat-plan-act`
- Steps:
  1. Start backend on `127.0.0.1:8765` (matches extension WS defaults)
  2. Health 200 (`GET /health`)
  3. WS `handshake` + `heartbeat`
  4. `indexing.start` broadcast echo
  5. REST `POST /chat/echo` stream smoke
  6. `act.request_approval` for create `docs/E2E_README.md`
  7. `act.apply` with `approved=true`, assert file written
- Deterministic IDs: `plan-e2e-0001`, `todo-e2e-0001`, `exec-e2e-0001`

## Fixtures
- Generated at runtime in a temp folder (no spaces), initialized as a Git repo (required by Act strict safety)
- Only safe creates under `docs/**` (auto-approvable)

## Harness
- Script: `scripts/e2e/nightly_chat_plan_act.py`
- Dependencies: backend `requirements*.txt` already include `uvicorn`, `httpx`, `websockets`
- Artifacts:
  - `artifacts/e2e/backend.log` — full backend logs
  - `artifacts/e2e/e2e-result.json` — `{ ok, scenario, retry, flaky, skipped, written[] }`
  - `artifacts/e2e/ws-trace.jsonl` — raw WS envelopes (one per line)
  - `artifacts/e2e/tree.txt` — repo snapshot for diagnostics
- Flake control:
  - Config: `scripts/e2e/.flaky.json` with `{ "skip": ["chat-plan-act"] }`
  - One retry on transient errors (connection/timeout markers)

## Nightly CI
- Workflow: `.github/workflows/nightly-e2e.yml`
- Trigger: nightly 01:00 UTC + manual dispatch
- Runner: `windows-latest`
- Steps: checkout → setup Python 3.11 → install backend deps → run harness → upload artifacts

## Local Runbook
- Setup:
  - `python -m pip install -r backend/requirements.txt`
  - `python -m pip install -r backend/requirements-dev.txt`
- Run:
  - `python scripts/e2e/nightly_chat_plan_act.py`
- Inspect:
  - Open `artifacts/e2e/e2e-result.json` and `artifacts/e2e/backend.log`

## Failure Triage
- Connection refused/timeout → harness retries once; if persists, check port conflicts or backend startup errors in `backend.log`
- Act safety blocked → ensure workspace is a Git repo and operation path is under `docs/**`
- Parsing errors → see `ws-trace.jsonl` for raw envelopes

## Acceptance
- Nightly E2E green on Windows; artifacts uploaded when failing
- Deterministic fixtures; no flakiness except transient connectivity covered by single retry

## Handoff Notes
- To Agent 13 — Testing & Coverage:
  - Scenario ID `chat-plan-act` and harness ready; artifacts include WS and server logs
  - Gaps: add coverage accounting across extension + backend, and flake dashboards
- To Supervisor:
  - Use nightly workflow run results for dashboard; inspect artifacts for diagnostics
