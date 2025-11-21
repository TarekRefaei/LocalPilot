# Agent 02 — Extension Views & Commands
[Kickoff prompt](./Agent_Prompts.md#agent-02)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Implement `localpilot.views` container with `Plans/Act/Indexing/Status` TreeViews and register commands.”

## Role in This Project
Deliver the VS Code Views container and four TreeViews with commands, icons, context, and tests.

## Detailed Plan & TODOs
- [x] Scaffold `localpilot` container; register in `package.json` and wire focus command.
- [x] Implement TreeDataProviders: `Plans`, `Act`, `Indexing`, `Status`.
- [x] Register commands, contexts, icons, keybindings; "Show LocalPilot views".
- [x] State management service interface (SOLID) independent of UI.
- [x] Unit tests for providers (Jest) and integration tests (@vscode/test-electron).
- [x] Accessibility: labels, descriptions, context help.
- [x] TDD: write failing provider tests first; implement; refactor.

## Milestones & Success Criteria
- Views render and update; commands visible and callable.
- Tests for providers and command wiring pass in CI.

Status: MET (local + CI workflows wired)

## Handoff
### To Agent 03 — Chat Participant
- Document view IDs/contexts and command IDs used by Chat actions.
- Provide sample events for `Plans` insertion.

Use templates:
- [Agent Handoff Template](./_templates/Agent_Handoff_Template.md)
- [Supervisor Summary Template](./_templates/Supervisor_Summary_Template.md)

### To Agent 10 — Plan Mode
- Wire TreeDataProviders (Plans/Act/Indexing/Status) to `LocalPilotState` via DI; refresh on state changes.
- Update commands to mutate `LocalPilotState` (`plan.{create,update,delete}`, `index.{start,stop}`) in addition to `setContext`.
- Add unit tests for provider-state refresh and state/context synchronization.

### To Supervisor
- Demo steps to verify views and commands.
- Test report with coverage for UI providers.

Use templates:
- [Agent Handoff Template](./_templates/Agent_Handoff_Template.md)
- [Supervisor Summary Template](./_templates/Supervisor_Summary_Template.md)
- CI: `.github/workflows/ci-extension.yml` and `.github/workflows/ci-backend.yml` run on Windows/Ubuntu.

## Orchestration Enhancements
- **Week alignment**: Week 1 — Foundations & Bootstrap
- **Dependencies**
  - Prev: Agent 01 (tooling, monorepo, CI)
  - Next: Agent 03 (Chat participant actions), Agent 10 (Plan Mode)
- **Interfaces/Artifacts**
  - View IDs: `localpilot.views.{plans,act,indexing,status}`
  - Command IDs: `localpilot.showViews`, `localpilot.focusChatInput`, `localpilot.chat.transferToPlan`, `localpilot.plan.{create,update,delete}`, `localpilot.act.{dryRun,approve,apply,rollback}`, `localpilot.index.{start,stop}`, `localpilot.model.swap`
  - Provider contracts and states independent of UI (SOLID)
- **Acceptance Gates & Checkpoints**
  - Views render and update; commands visible
  - Jest + @vscode/test-electron suites green in CI
- **Risks & Comms**
  - Align command IDs with Agent 03; avoid churn
  - Share mock providers/states with downstream agents

## Git Workflow
- **Branch**: `feat/02-views-commands`
- **Scopes**: `feat(ui)`, `test(ui)`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/02-views-commands origin/main
  git add -A
  git commit -m "feat(ui): scaffold LocalPilot views and commands"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure UI tests pass; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (see above for this agent)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
