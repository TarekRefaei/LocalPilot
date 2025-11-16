# Agent 09 — Retrieval & Ranking

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Implement multi‑level retrieval (summary/symbol/semantic/lexical) and fusion with diversity re‑rank.”

## Role in This Project
Design the retrieval pipeline with multi-level strategies and fusion/reranking for high precision.

## Detailed Plan & TODOs
- [ ] Retrieval stages: summary, symbol, semantic, lexical.
- [ ] Fusion and diversity re-rank; scoring strategy.
- [ ] Evaluation harness and metrics logging.
- [ ] Integration tests with fixtures.
- [ ] TDD: failing precision@5 test against fixtures; implement.

## Milestones & Success Criteria
- Precision@5 ≥ 0.80 on fixture set.
- Integration tests pass on CI; metrics logged.

## Handoff
### To Agent 10 — Plan Mode
- Expose retrieval API used by Chat and Plan synthesis.

### To Supervisor
- Report on metrics, failure cases, and tuning recommendations.
- Fixture catalog and reproducibility steps.

## Orchestration Enhancements
- **Week alignment**: Week 6 — Retrieval Pipeline & Chat Integration
- **Dependencies**
  - Prev: Agent 08 (embeddings & vector)
  - Next: Agent 03 (chat integration), Agent 10 (plan synthesis)
- **Interfaces/Artifacts**
  - Retrieval API, fusion/rerank hooks, evaluators and metrics
- **Acceptance Gates & Checkpoints**
  - Precision@5 ≥ 0.80 on fixtures; integration tests green
- **Risks & Comms**
  - Guard against index quality drift; log metrics for nightly checks

## Git Workflow
- **Branch**: `feat/09-retrieval-ranking`
- **Scopes**: `feat(rag)`, `test`, `perf`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/09-retrieval-ranking origin/main
  git add -A
  git commit -m "feat(rag): multi-level retrieval and fusion re-rank"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure metrics meet gates; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (P@5 ≥ 0.80; integration tests)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
