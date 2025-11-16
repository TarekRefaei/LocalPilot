# Orchestration Guidelines

All agents follow TDD, SOLID, and Clean Architecture. Default flow: Red → Green → Refactor. Keep PRs small and test-driven.

## Cross-Cutting Rules
- Declare Inputs/Outputs, Prev/Next dependencies, and Week alignment in each task.
- Use acceptance gates from the Master Implementation Plan; do not merge until your gate is met.
- Keep contracts stable; prefer adapters to isolate infra details.
- Daily: post standup notes (blockers, risks, today’s failing tests first).
- Handoffs: include overview, artifacts, open risks, and explicit next steps.

## Git Workflow (Conventional Commits)
- Branch naming: <type>/<agent>-<short-topic> (e.g., `feat/10-plan-mode-crud`). Types: feat, fix, docs, test, refactor, chore, ci, build, perf.
- Create branch: `git fetch origin && git checkout -b <branch> origin/main`
- Commit: `git add -A && git commit -m "<type>(<scope>): <message>"`
- Push: `git push -u origin HEAD`
- Update from main: `git fetch origin && git rebase origin/main` (preferred) or merge if policy requires.
- Open PR: GitHub UI or `gh pr create -f -B main -t "<title>" -b "<body>"`
- Required checks: lint, type, tests, coverage gates, integration/E2E when applicable.
- Merge: Squash merge to keep linear history; delete branch. Post-merge sync: `git checkout main && git pull`.
- Tag (when releasing): `git tag -a v0.1.0 -m "MVP v0.1" && git push origin v0.1.0`

## PR Template (use/adapt)
- Summary
- Problem / Context
- Approach
- Tests (failing first → passing)
- Screenshots / Demos
- Acceptance Gates satisfied
- Risks & Rollback
- Checklist: lint, type, tests, coverage, docs

## Handoff Template
- Overview
- Inputs consumed
- Outputs produced (paths, contracts)
- Acceptance gates status
- Open risks / decisions
- Next agent and explicit TODOs

## Coordination Signals
- View/Command/Topic IDs are single source of truth; document any change. See:
  - ../projectdocuments/contracts/IDs_and_Constants.md
  - ../projectdocuments/contracts/Contracts_Index.md
- Nightly E2E is the ground truth for integration health; fix regressions before new scope.

## Branch Protection Policy (Main)
- Require status checks to pass: lint, type, unit, integration (when applicable), coverage gates
- Require branches to be up to date before merging (rebase preferred)
- Require at least 1 approving review; dismiss stale approvals on new commits
- Restrict who can push to `main` (maintainers only)
- Enforce linear history with squash merges

## Merge Strategy & Approvals
- Default: Squash merge with Conventional Commit title
- Approvals: ≥1 reviewer (CODEOWNERS where defined); Supervisor for risky changes
- PR Size: Aim < 400 lines diff; split otherwise
- Link issues in title/body: e.g., `Closes #123`, `Relates-to #456`

## Hotfix Flow
- Branch from latest tag or `main`: `git checkout -b hotfix/<topic> <ref>`
- Keep scope minimal; add tests proving the regression
- Open PR to `main`, obtain expedited review, squash merge
- Tag patch release: `git tag -a v0.1.x -m "Hotfix: <topic>" && git push origin v0.1.x`

## GitHub CLI Examples
- Create PR (draft):
  ```sh
  gh pr create -f -B main -t "feat(agent-02): views and commands" -b "See checklist" --draft
  ```
- Request reviewers and labels:
  ```sh
  gh pr edit --add-reviewer user1 --add-reviewer user2 --add-label ui --add-label agent-02
  ```
- Watch checks and approve:
  ```sh
  gh pr checks --watch
  gh pr review --approve -b "Meets acceptance gates"
  ```
- Merge with squash and delete branch:
  ```sh
  gh pr merge --squash --delete-branch
  ```
