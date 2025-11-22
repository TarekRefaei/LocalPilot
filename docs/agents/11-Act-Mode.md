# Agent 11 — Act Mode (Safe Execution)
[Kickoff prompt](./Agent_Prompts.md#agent-11)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Dry‑run diffs; approval workflow; Git safety; apply/rollback.”

## Role in This Project
Implement safe execution with dry-run diffs, approvals, Git safety checks, apply and rollback mechanisms.

## Detailed Plan & TODOs
- [x] Diff engine producing patch previews.
- [x] Approval workflow UI and state.
- [x] Git safety checks; block outside Git unless override.
- [x] Apply and rollback commands with logging.
- [x] Integration tests for blocked/approved flows.
- [x] TDD: failing tests for safety gates; implement.

## Milestones & Success Criteria
- Cannot apply without approval; safety gates enforced.
- Integration tests pass; logs capture approvals.

## Finalized Settings & Policies
- Apply safety mode: `localpilot.act.applySafety` = `strict` (default) | `git-optional` | `unsafe` (env: `ACT_APPLY_SAFETY`).
- Auto-approve safe creates: `localpilot.act.autoApprove.safeCreates` = true for `docs/**` (.md/.mdx/.txt/.rst), `tests/**` or `__tests__/**` (*.test.*, *.spec.*), `.localpilot/**`; config auto-approve disabled by default (`localpilot.act.autoApprove.configFiles` = false).
- Diff format: Unified diff; UI preview truncated to 300 lines/file and 2000 total; full diffs persisted to `.localpilot/audit`.
- Approval timeout: `localpilot.act.approvalTimeoutSeconds` = 300 (5 min; 0 disables). On timeout, re-diff required.

## Handoff
### To Agent 12 — Integration & E2E
- Provide act command APIs and test fixtures for E2E scenario.

### To Supervisor
- Safety report (blocked cases, overrides) and audit trail notes.
- Rollback verification steps.

## Orchestration Enhancements
- **Week alignment**: Week 8 — Act Mode (Safe Execution)
- **Dependencies**
  - Prev: Agent 10 (plan schema and steps)
  - Next: Agent 12 (integration & E2E)
- **Interfaces/Artifacts**
  - Diff preview format, approval workflow states, Git safety checks
- **Acceptance Gates & Checkpoints**
  - Cannot apply without explicit approval; integration tests enforce gates
- **Risks & Comms**
  - Ensure idempotent apply/rollback; log audit trail

## Git Workflow
- **Branch**: `feat/11-act-mode`
- **Scopes**: `feat(act)`, `test(int)`, `refactor`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/11-act-mode origin/main
  git add -A
  git commit -m "feat(act): dry-run diffs, approvals, and git safety"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure safety gates enforced by tests; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (approvals required; safety gates enforced)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
