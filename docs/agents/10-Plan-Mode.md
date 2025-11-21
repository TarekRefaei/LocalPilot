# Agent 10 — Plan Mode
[Kickoff prompt](./Agent_Prompts.md#agent-10)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Plan CRUD in TreeView; persistent storage; from‑Chat conversion; acceptance criteria model.”

## Role in This Project
Implement planning models, CRUD UI, persistence, and conversion from Chat into Plans with acceptance criteria.

## Detailed Plan & TODOs
- [ ] Plan data model and persistence (storage service).
- [ ] TreeView CRUD: create/edit/reorder/complete steps.
- [ ] From-Chat conversion: parse and insert plan drafts.
- [ ] Acceptance criteria model with file refs.
- [ ] Unit and integration tests for Plan components.
- [ ] TDD: failing CRUD tests first; implement.
- [ ] Wire TreeDataProviders (Plans/Act/Indexing/Status) to `LocalPilotState` via DI; subscribe to `onDidChange` and refresh.
- [ ] Update commands to mutate `LocalPilotState`: `plan.{create,update,delete}` and `index.{start,stop}` (preserve `setContext` toggles).
- [ ] Add unit tests for provider-state refresh and state/context synchronization.

## Milestones & Success Criteria
- Full CRUD works; keyboard navigation and persistence validated.
- Tests ≥ 80% for Plan components.
- Providers refresh on `LocalPilotState` changes; Plans view reflects create/update/delete.
- Indexing menu + view reflect `getIndexingRunning()` and context toggles.

## Handoff
### To Agent 11 — Act Mode
- Provide plan schema, step states, and acceptance criteria format.

### To Supervisor
- Demo scenario from Chat → Plan with persisted data.
- Test coverage report and known gaps.

## Orchestration Enhancements
- **Week alignment**: Week 7 — Plans View
- **Dependencies**
  - Prev: Agent 02 (views/commands), Agent 03 (from-Chat transfer), Agent 09 (retrieval API)
  - Next: Agent 11 (Act Mode)
- **Interfaces/Artifacts**
  - View IDs: `localpilot.views.{plans,act,indexing,status}`
  - Command IDs: `localpilot.showViews`, `localpilot.focusChatInput`, `localpilot.chat.transferToPlan`, `localpilot.plan.{create,update,delete}`, `localpilot.act.{dryRun,approve,apply,rollback}`, `localpilot.index.{start,stop}`, `localpilot.model.swap`
  - Plan schema, acceptance criteria with file refs, persistence API
- **Acceptance Gates & Checkpoints**
  - CRUD + keyboard navigation + persistence tested (≥ 80%)
  - Provider-state refresh verified by tests; Indexing context→state sync works
- **Risks & Comms**
  - Ensure model changes are backward compatible with stored plans

## Git Workflow
- **Branch**: `feat/10-plan-mode`
- **Scopes**: `feat(ui-plan)`, `test(ui)`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/10-plan-mode origin/main
  git add -A
  git commit -m "feat(plan): CRUD, persistence, and from-Chat conversion"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure UI tests ≥ 80%; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (CRUD + persistence + keyboard; ≥80% tests)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
