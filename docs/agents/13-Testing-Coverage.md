# Agent 13 — Testing & Coverage
[Kickoff prompt](./Agent_Prompts.md#agent-13)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Fill coverage gaps, edge cases, performance and regression; enforce gates.”

## Role in This Project
Raise test coverage, add edge cases, performance/load tests where feasible, and ensure all quality gates pass.

## Detailed Plan & TODOs
- [ ] Coverage gap analysis per folder; add tests where missing.
- [ ] Edge-case and error-path tests across components.
- [ ] Performance/load tests and smoke perf checks.
- [ ] Regression test packs; mutation tests (optional).
- [ ] Enforce coverage/type/lint gates in CI.
- [ ] TDD: write failing tests for gaps first; implement fixes or tests.

## Milestones & Success Criteria
- Coverage > 90% where feasible; type coverage 100%.
- CI stable; no cyclic deps; perf smoke passes.

## Handoff
### To Agent 14 — Docs & DX
- Provide test coverage reports, perf results, and regression packs.

### To Supervisor
- Final quality report with gates status and risk register updates.
- Backlog of remaining gaps (if any).

## Orchestration Enhancements
- **Week alignment**: Week 9 — Hardening & Coverage
- **Dependencies**
  - Prev: Agent 12 (E2E readiness)
  - Next: Agent 14 (Docs & DX)
- **Interfaces/Artifacts**
  - Coverage reports, regression packs, perf/load harness
- **Acceptance Gates & Checkpoints**
  - Coverage > 90% feasible areas; type coverage 100%; CI stable
- **Risks & Comms**
  - Avoid superficial tests; target meaningful behavior and error paths

## Git Workflow
- **Branch**: `test/13-coverage-hardening`
- **Scopes**: `test`, `perf`, `ci`, `refactor`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b test/13-coverage-hardening origin/main
  git add -A
  git commit -m "test: raise coverage; add perf/load and regression packs"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; enforce gates; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (coverage > 90% feasible; type 100%; CI stable)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
