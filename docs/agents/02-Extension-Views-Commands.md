# Agent 02 — Extension Views & Commands

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Implement `localpilot.views` container with `Plans/Act/Indexing/Status` TreeViews and register commands.”

## Role in This Project
Deliver the VS Code Views container and four TreeViews with commands, icons, context, and tests.

## Detailed Plan & TODOs
- [ ] Scaffold `localpilot.views` container; register in `package.json`.
- [ ] Implement TreeDataProviders: `Plans`, `Act`, `Indexing`, `Status`.
- [ ] Register commands, contexts, icons, keybindings; "Show LocalPilot views".
- [ ] State management service interface (SOLID) independent of UI.
- [ ] Unit tests for providers (Jest) and integration tests (@vscode/test-electron).
- [ ] Accessibility: labels, descriptions, context help.
- [ ] TDD: write failing provider tests first; implement; refactor.

## Milestones & Success Criteria
- Views render and update; commands visible and callable.
- Tests for providers and command wiring pass in CI.

## Handoff
### To Agent 03 — Chat Participant
- Document view IDs/contexts and command IDs used by Chat actions.
- Provide sample events for `Plans` insertion.

### To Supervisor
- Demo steps to verify views and commands.
- Test report with coverage for UI providers.

## Orchestration Enhancements
- **Week alignment**: Week 1 — Foundations & Bootstrap
- **Dependencies**
  - Prev: Agent 01 (tooling, monorepo, CI)
  - Next: Agent 03 (Chat participant actions), Agent 10 (Plan Mode)
- **Interfaces/Artifacts**
  - View IDs: `localpilot.views.{plans,act,indexing,status}`
  - Command IDs: document exact IDs used by Chat and Plans
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
