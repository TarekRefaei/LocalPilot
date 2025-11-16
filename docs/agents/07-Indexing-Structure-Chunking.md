# Agent 07 — Indexing: Structure & Chunking

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“AST‑first chunking with Tree‑sitter; fallback lexical; symbol/import maps.”

## Role in This Project
Produce deterministic AST-first chunks with lexical fallback and symbol/import maps, emitting metadata for retrieval.

## Detailed Plan & TODOs
- [ ] Integrate Tree-sitter drivers for target languages; Windows prebuilt binaries.
- [ ] AST-first chunking rules; lexical fallback with precision checks.
- [ ] Build symbol/import maps for cross-file references.
- [ ] Pytest unit tests for chunk determinism and map correctness.
- [ ] TDD: failing tests around boundary precision; implement.

## Milestones & Success Criteria
- Deterministic chunk boundaries across runs.
- Tests pass; precision checks validated on fixtures.

## Handoff
### To Agent 08 — Embeddings & Vector Store
- Export chunk format and symbol map schema; provide sample corpora.

### To Supervisor
- Measurements for chunk size distribution; accuracy notes.
- Any Windows-specific build notes.

## Orchestration Enhancements
- **Week alignment**: Week 4 — Indexing II (Structure, Chunking)
- **Dependencies**
  - Prev: Agent 06 (discovery & docs)
  - Next: Agent 08 (embeddings & vector store)
- **Interfaces/Artifacts**
  - Chunk format, symbol/import maps, precision checks
- **Acceptance Gates & Checkpoints**
  - Deterministic boundaries; tests validate precision on fixtures
- **Risks & Comms**
  - Tree-sitter binaries on Windows; provide fallback notes

## Git Workflow
- **Branch**: `feat/07-indexing-chunking`
- **Scopes**: `feat(indexing)`, `test(py)`, `perf`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/07-indexing-chunking origin/main
  git add -A
  git commit -m "feat(indexing): AST-first chunking and symbol/import maps"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; tests must prove determinism; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (deterministic boundaries; precision checks)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
