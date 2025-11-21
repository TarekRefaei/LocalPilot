# Agent 03 — Chat Participant
[Kickoff prompt](./Agent_Prompts.md#agent-03)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Create `localpilot` Chat participant with streaming, markdown, and ‘Transfer to Plan’ action.”

## Role in This Project
Implement the Chat participant that streams responses, formats markdown, and pushes plan drafts to the Plans view.

## Detailed Plan & TODOs
- [ ] Register Chat participant `localpilot`; stream tokens with cancellation.
- [ ] Markdown formatting; code fences; references.
- [ ] Implement “Transfer to Plan” to create a plan draft item.
- [ ] Interface with retrieval service (contract only for now).
- [ ] Integration tests for Chat + Plans insertion.
- [ ] Error handling and telemetry-free logging.
- [ ] TDD: failing integration test for streaming + transfer, then implement.

## Milestones & Success Criteria
- Chat streams responses; “Transfer to Plan” inserts draft successfully.
- Integration tests pass on CI.

## Handoff Documents
### To Agent 04 — WebSocket Client & Contract Document 
- Document message schemas used by Chat, placeholders for retrieval requests.
- Provide mock adapters used in tests.

### To Supervisor Document
- Demo script and test results for Chat participant behavior.
- Known limitations list until retrieval is integrated.

## Orchestration Enhancements
- **Week alignment**: Week 6 — Retrieval Pipeline & Chat Integration
- **Dependencies**
  - Prev: Agent 02 (views), Agent 04 (WS client)
  - Next: Agent 10 (Plan Mode), Agent 09 (Retrieval)
- **Interfaces/Artifacts**
  - Chat participant id: `localpilot`; action: "Transfer to Plan"
  - Message schemas for request/stream/transfer; mock adapters
- **Acceptance Gates & Checkpoints**
  - Streaming behavior covered by @vscode/test-electron integration tests
  - Plan draft insertion verified in Plans view
- **Risks & Comms**
  - Align schema topics with Agent 04/05; deprecate carefully

## Git Workflow
- **Branch**: `feat/03-chat-participant`
- **Scopes**: `feat(chat)`, `test(int)`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/03-chat-participant origin/main
  git add -A
  git commit -m "feat(chat): add streaming Chat participant and Transfer to Plan"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure integration tests pass; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (streaming + transfer integration tests)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
