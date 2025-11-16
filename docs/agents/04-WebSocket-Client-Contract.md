# Agent 04 — WebSocket Client & Contract

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Implement robust WS client with reconnect, backoff, heartbeat; shared message types.”

## Role in This Project
Provide a resilient WS client and stable shared message contracts for extension-backend communication.

## Detailed Plan & TODOs
- [ ] Define shared TypeScript types and envelope with topic/routing/ids.
- [ ] WS client with reconnect, exponential backoff, heartbeat/ping.
- [ ] Subscription router, observers, and error state propagation.
- [ ] Unit tests for reconnect, backoff, and message routing.
- [ ] Mock server for tests; ensure deterministic timing.
- [ ] TDD: failing tests for reconnect/heartbeat; implement.

## Milestones & Success Criteria
- Reconnect works; messages routed to subscribers.
- Unit tests pass; contract types compile strictly.

## Handoff
### To Agent 05 — Backend API Gateway
- Share the envelope spec and topics; provide client test harness.

### To Supervisor
- Contracts documented; stability/latency observations recorded.
- Risk notes for cross-version compatibility.

## Orchestration Enhancements
- **Week alignment**: Week 2 — Contracts & Messaging
- **Dependencies**
  - Prev: Agent 01 (tooling)
  - Next: Agent 05 (backend gateway), Agent 03 (chat streaming)
- **Interfaces/Artifacts**
  - Envelope spec, topics, routing, and error codes
  - Client test harness and mock server
- **Acceptance Gates & Checkpoints**
  - Reconnect/backoff/heartbeat unit tests green in CI
  - Contract types compiled in strict TS mode
- **Risks & Comms**
  - Version contracts; add deprecation policy for topics

## Git Workflow
- **Branch**: `feat/04-ws-client-contract`
- **Scopes**: `feat(core)`, `test`, `refactor`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/04-ws-client-contract origin/main
  git add -A
  git commit -m "feat(core): resilient WS client and envelope contract"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure unit tests pass; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (reconnect/backoff/heartbeat unit tests)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
