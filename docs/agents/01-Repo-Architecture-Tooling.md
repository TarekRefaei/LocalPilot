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
- [ ] Monorepo layout: `extension/` (TS), `backend/` (Python), shared `/.vscode/` and `.github/`.
- [ ] TypeScript strict config: `tsconfig.json` with `strict: true`, path aliases.
- [ ] Jest setup for TS units; coverage threshold baseline.
- [ ] ESLint + Prettier with scripts: `lint`, `format`, `typecheck`, `test`.
- [ ] Python `pyproject.toml` with Ruff/Flake8 + Black; Pytest config and scripts.
- [ ] VS Code: tasks and launch configs (extension debug, backend debug) on Windows.
- [ ] CI: GitHub Actions for TS and Python on Windows + Linux; cache deps; run lint/type/test.
- [ ] Pre-commit hooks (optional) for format/lint.
- [ ] TDD: add failing smoke tests (extension activates; backend health 200), implement to pass, refactor.

## Milestones & Success Criteria
- CI green across platforms.
- Scripts exist for lint/type/test; strict TS and Python linters enforced.
- Baseline tests implemented and passing locally and on CI.

## Handoff
### To Agent 02 — Extension Views & Commands
- Extension project boots in debug with sample activation test passing.
- Document scripts, tasks, launch configs, folder structure.

### To Supervisor
- Summary of CI status, scripts, configs, and initial coverage.
- Risks/decisions log (tooling choices) and next steps.

## Orchestration Enhancements
- **Week alignment**: Week 1 — Foundations & Bootstrap
- **Dependencies**
  - Prev: None
  - Next: Agent 02 (extension scaffolding), Agent 05 (backend scaffolding)
- **Interfaces/Artifacts**
  - Monorepo layout, strict TS/Python configs, CI workflows, VS Code tasks/launch
  - Baseline smoke tests (extension activates; backend health 200)
- **Acceptance Gates & Checkpoints**
  - CI green on Windows/Linux; lint/type/test scripts present and enforced
  - Coverage baseline established and reported in CI
- **Risks & Comms**
  - Pin VS Code engine version; ensure Windows developer onboarding tested
  - Daily: share failing tests first; list blockers on CI or tooling

## Git Workflow
- **Branch**: `feat/01-tooling-monorepo`
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

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (see above for this agent)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
