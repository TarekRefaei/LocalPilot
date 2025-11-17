# Agent 12 — Integration & E2E
[Kickoff prompt](./Agent_Prompts.md#agent-12)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Orchestrate cross‑component tests, fixtures, and nightly scenario.”

## Role in This Project
Create integration and E2E harness, fixtures, and CI configuration for nightly Chat→Plan→Act validation.

## Detailed Plan & TODOs
- [ ] Test harness setup for extension + backend.
- [ ] Sample repositories and data fixtures.
- [ ] Nightly E2E pipeline on Windows runner.
- [ ] Flaky-test detection and quarantine.
- [ ] TDD: write failing E2E scenario; implement fixes across components.

## Milestones & Success Criteria
- E2E green locally and on nightly CI; fixtures reproducible.

## Handoff
### To Agent 13 — Testing & Coverage
- List coverage gaps and flaky areas; hand over fixtures.

### To Supervisor
- E2E dashboard, stability metrics, and runbooks.
- Open issues linked for failing cases.

## Orchestration Enhancements
- **Week alignment**: Weeks 6–10 (setup early, stabilize by Week 9)
- **Dependencies**
  - Prev: Agent 11 (act APIs), cumulative outputs from 01–11
  - Next: Agent 13 (coverage), nightly gates for 14 (release docs)
- **Interfaces/Artifacts**
  - E2E harness, fixtures, CI workflows, dashboards
- **Acceptance Gates & Checkpoints**
  - E2E green locally and on nightly CI; flaky tests quarantined
- **Risks & Comms**
  - Flake management; Windows runner stability

## Git Workflow
- **Branch**: `test/12-integration-e2e`
- **Scopes**: `test(e2e)`, `ci`, `chore(fixtures)`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b test/12-integration-e2e origin/main
  git add -A
  git commit -m "test(e2e): Chat→Plan→Act nightly scenario and fixtures"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure nightly passes; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (nightly E2E green; flake quarantine)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
