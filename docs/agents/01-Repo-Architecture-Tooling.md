# Agent 01 — Repo Architecture & Tooling
[Kickoff prompt](./Agent_Prompts.md#agent-01)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Set up monorepo structure for VS Code extension (TS) and FastAPI backend (Python). Enforce strict typing, linting, test runners, and CI.”

## Role in This Project
Establish the monorepo foundation, strict quality gates, local dev ergonomics, and CI pipelines for TypeScript (extension) and Python (backend).

## Detailed Plan & TODOs
- [x] Monorepo layout: `extension/`, `backend/`, shared `/.vscode/`, `.github/`. (Done)
- [x] TypeScript strict config with path aliases. (Files: `extension/tsconfig.json`)
- [x] Jest setup with coverage thresholds. (Files: `extension/jest.config.js`; tests added)
- [x] ESLint + Prettier with scripts. (Files: `extension/.eslintrc.json`, `package.json`, `.prettierrc.json`)
- [x] Python formatting/linting (Black/Ruff) and Pytest config. (Files: `backend/pyproject.toml`, `backend/ruff.toml`, `pytest.ini`)
- [x] VS Code tasks and launch (extension debug, backend debugpy) on Windows. (Files: `.vscode/tasks.json`, `.vscode/launch.json`)
- [x] CI on Windows+Linux with caching; run typecheck/lint/tests; upload coverage artifacts. (Files: `.github/workflows/ci-*`)
- [x] Pre-commit hooks (optional). (File: `.pre-commit-config.yaml`)
- [x] TDD smoke tests: extension activates; backend health 200. (Files: `extension/__tests__/extension.test.ts`, `backend/tests/test_health.py`)

## Milestones & Success Criteria
- [x] CI green across platforms. (Green on PR #1 for Windows & Ubuntu)
- [x] Scripts exist for lint/type/test; strict TS and Python linters enforced. (npm/pytest tasks)
- [x] Baseline tests implemented and passing locally; coverage thresholds configured in CI.

## Handoff Documents
Links:
- [Agent 01 Handoff — Extension Views & Commands](../handoff/Agent_01_Handoff.md)
- [Supervisor Summary — Agent 01](../handoff/Supervisor_Summary_Agent_01.md)

### To Agent 02 — Extension Views & Commands
- Extension project boots in debug with sample activation test passing.
- Document scripts, tasks, launch configs, folder structure.

### To Supervisor Documents
- Summary of CI status, scripts, configs, and initial coverage.
- Risks/decisions log (tooling choices) and next steps.

## Orchestration Enhancements
- **Week alignment**: Week 1 — Foundations & Bootstrap
- **Dependencies**
  - Prev: None
  - Next: Agent 02 (extension scaffolding), Agent 05 (backend scaffolding)
- **Interfaces/Artifacts**
  - [x] Monorepo layout, strict TS/Python configs, CI workflows, VS Code tasks/launch
  - [x] Baseline smoke tests (extension activates; backend health 200)
- **Acceptance Gates & Checkpoints**
  - [x] CI green on Windows/Linux; lint/type/test scripts present and enforced (PR #1 checks passed)
  - [x] Coverage baseline configured and reported (text + artifacts) in CI workflows
- **Risks & Comms**
  - [x] Pin VS Code engine version (extension `engines.vscode` ≥ 1.88); Windows onboarding validated
  - Daily: share failing tests first; list blockers on CI or tooling

## Git Workflow
- **Branch**: `feat/01-tooling-monorepo` (Executed using `chore/ci-quality-gates`)
- **Scopes**: `build`, `ci`, `chore(tooling)`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/01-tooling-monorepo origin/main
  git add -A
  git commit -m "build(tooling): scaffold monorepo and CI"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR, ensure lint/type/test green, coverage baseline present
  # squash-merge when checks pass, then:
  git checkout main && git pull
  ```
  Status: Implemented on branch `chore/ci-quality-gates`; PR #1 opened.

## PR & Merge Checklist
- [x] Branch up to date with `main` (rebase preferred)
- [x] Required checks passed (lint, type, tests, coverage) — green on PR #1
- [x] Acceptance gates satisfied (see above for this agent)
- [ ] ≥1 approval obtained; risks documented
- [ ] Squash merge with Conventional Commit title; delete branch
- [ ] Post-merge: `git checkout main && git pull`
