# Agent 14 — Docs & DX

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Maintain docs, changelogs, contribution guide, onboarding; ensure Windows flow polished.”

## Role in This Project
Deliver developer and user documentation, onboarding, contribution guidelines, and ensure a polished Windows experience.

## Detailed Plan & TODOs
- [ ] Update master docs, changelog, contribution guide, READMEs.
- [ ] Onboarding guides for Windows; screenshots where helpful.
- [ ] Issue templates and PR templates.
- [ ] Verify examples and VSIX packaging docs.
- [ ] TDD-aligned documentation: show tests-first flows in examples.

## Milestones & Success Criteria
- Docs up-to-date; onboarding reproducible on Windows.
- Release readiness docs complete (Week 10 gates).

## Handoff
### To Supervisor
- Final docs index, change log, onboarding steps, and open doc gaps.
- Post-MVP backlog doc handed off.

## Orchestration Enhancements
- **Week alignment**: Week 10 — Release Readiness
- **Dependencies**
  - Prev: Agent 13 (quality gates & reports)
  - Next: Supervisor sign-off and packaging
- **Interfaces/Artifacts**
  - Master docs, onboarding guides, changelog, contribution guide
- **Acceptance Gates & Checkpoints**
  - Release docs complete; Windows onboarding reproducible; VSIX docs verified
- **Risks & Comms**
  - Keep docs synced with latest command/view/topic IDs

## Git Workflow
- **Branch**: `docs/14-docs-dx`
- **Scopes**: `docs`, `chore`, `build`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b docs/14-docs-dx origin/main
  git add -A
  git commit -m "docs: finalize onboarding, contribution, and release readiness"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure all gates linked; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (release docs complete; Windows onboarding reproducible)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
