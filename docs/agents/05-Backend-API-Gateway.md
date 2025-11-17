# Agent 05 — Backend API Gateway (Python)

[Kickoff prompt](./Agent_Prompts.md#agent-05)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Expose WS + REST; schema-validated endpoints; logging; config.”

## Role in This Project
Deliver FastAPI-based REST and WS endpoints with Pydantic schemas, logging, config, and tests.

## Detailed Plan & TODOs
- [ ] FastAPI app with health and config REST endpoints.
- [ ] WebSocket server with topics for indexing/chat/plan/act/vram.
- [ ] Pydantic models aligning to shared contracts.
- [ ] Structured logging and configuration (env, .env).
- [ ] Pytest: unit tests for routers and WS topics.
- [ ] TDD: failing tests for health and WS round-trip; implement.

## Milestones & Success Criteria
- Health and config endpoints pass tests.
- WS topics accept/emit messages with schema validation.

## Handoff
### To Agent 06 — Indexing: Discovery & Docs
- Document endpoints and topics used for indexing events.

### To Supervisor
- API docs (OpenAPI) generated; test report and coverage.
- Deployment notes for local dev on Windows.

## Orchestration Enhancements
- **Week alignment**: Week 2 — Contracts & Messaging
- **Dependencies**
  - Prev: Agent 04 (WS envelope)
  - Next: Agent 06 (indexing), Agent 03 (chat), Agent 09 (retrieval)
- **Interfaces/Artifacts**
  - REST health/config, WS topics for indexing/chat/plan/act/vram
  - Pydantic models aligned with TS contracts
- **Acceptance Gates & Checkpoints**
  - REST + WS round-trip tests pass in CI
  - Structured logging and config validated
- **Risks & Comms**
  - Windows path/env handling; document .env usage

## Git Workflow
- **Branch**: `feat/05-backend-gateway`
- **Scopes**: `feat(api)`, `test(py)`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/05-backend-gateway origin/main
  git add -A
  git commit -m "feat(api): expose REST health/config and WS topics"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure API tests pass; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (REST + WS round-trip tests)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
