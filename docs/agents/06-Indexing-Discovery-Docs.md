# Agent 06 — Indexing: Discovery & Docs
 
[Kickoff prompt](./Agent_Prompts.md#agent-06)
 
## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Implement discovery, ignore rules, doc extraction, file hash cache, progress events.”

## Role in This Project
Implement the first phase of indexing: discover files, apply ignore rules, extract docs, maintain file-hash metadata, and emit progress events.

## Detailed Plan & TODOs
- [ ] Discovery walkers honoring .gitignore and project rules.
- [ ] Doc/markdown extraction with metadata.
- [ ] File-hash cache for change detection.
- [ ] Progress events to `Indexing` view via WS.
- [ ] Pytest unit tests for walkers/parsers/cache.
- [ ] TDD: failing tests for cache invalidation + event emission; implement.

## Milestones & Success Criteria
- Small repo indexes reliably; progress visible in the UI.
- Unit tests pass with good coverage.

## Handoff
### To Agent 07 — Indexing: Structure & Chunking
- Provide metadata schema and sample outputs; define extension points for AST parsing.

### To Supervisor
- Report on indexing speed and coverage; risks for large repos.
- Fixtures saved for regression.

## Orchestration Enhancements
- **Week alignment**: Week 3 — Indexing I (Discovery, Documentation)
- **Dependencies**
  - Prev: Agent 05 (backend gateway)
  - Next: Agent 07 (structure & chunking)
- **Interfaces/Artifacts**
  - Discovery outputs, doc metadata schema, file-hash cache
  - Progress event topics and payloads
- **Acceptance Gates & Checkpoints**
  - Index a small repo; UI shows progress; tests ≥ 75%
- **Risks & Comms**
  - .gitignore nuances on Windows; path case-sensitivity

## Git Workflow
- **Branch**: `feat/06-indexing-discovery`
- **Scopes**: `feat(indexing)`, `test(py)`, `docs`, `perf`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/06-indexing-discovery origin/main
  git add -A
  git commit -m "feat(indexing): discovery, doc extraction, and progress events"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure unit tests pass; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (index small repo; progress visible; tests ≥ 75%)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
