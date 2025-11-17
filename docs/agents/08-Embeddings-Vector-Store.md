# Agent 08 — Embeddings & Vector Store
[Kickoff prompt](./Agent_Prompts.md#agent-08)

## Engineering Principles
- TDD (Red → Green → Refactor)
- SOLID
- Clean Architecture (UI / Use-cases / Adapters / Infra)

## Ideal Prompt
“Integrate Ollama `bge‑m3`; Chroma upsert/query; ef settings; caching.”

## Role in This Project
Provide a robust embeddings service via Ollama and integrate Chroma for upsert/query with caching and filters.

## Detailed Plan & TODOs
- [ ] Implement embeddings service for `bge-m3` (pooling, batching, retries).
- [ ] Chroma integration for upsert, maintenance, and filtered queries.
- [ ] Cache recent embeddings and queries; LRU policy.
- [ ] Pytest unit and integration tests with fixtures.
- [ ] TDD: failing integration tests for vector search; implement.

## Milestones & Success Criteria
- Stable embeddings; vector search returns coherent neighbors.
- Unit+integration tests ≥ 80% for RAG infra components.

## Handoff
### To Agent 09 — Retrieval & Ranking
- Provide query APIs and scoring hooks; document filter capabilities.

### To Supervisor
- Benchmark results and resource usage notes (VRAM/RAM).
- Failure/timeout behavior documented.

## Orchestration Enhancements
- **Week alignment**: Week 5 — Embeddings & Vector Search
- **Dependencies**
  - Prev: Agent 07 (chunking & symbol maps)
  - Next: Agent 09 (retrieval & ranking)
- **Interfaces/Artifacts**
  - Embedding service API, Chroma collection schema, filter options
- **Acceptance Gates & Checkpoints**
  - Vector search returns coherent neighbors; unit+integration ≥ 80%
- **Risks & Comms**
  - VRAM constraints; implement backpressure and batching

## Git Workflow
- **Branch**: `feat/08-embeddings-vector-store`
- **Scopes**: `feat(rag)`, `test(py)`, `perf`, `docs`
- **Commands**
  ```sh
  git fetch origin
  git checkout -b feat/08-embeddings-vector-store origin/main
  git add -A
  git commit -m "feat(rag): bge-m3 embeddings and Chroma integration"
  git push -u origin HEAD
  git fetch origin && git rebase origin/main
  # open PR; ensure integration tests pass; squash merge
  git checkout main && git pull
  ```

 ## PR & Merge Checklist
 - [ ] Branch up to date with `main` (rebase preferred)
 - [ ] Required checks passed (lint, type, tests, coverage)
 - [ ] Acceptance gates satisfied (coherent neighbors; ≥80% tests)
 - [ ] ≥1 approval obtained; risks documented
 - [ ] Squash merge with Conventional Commit title; delete branch
 - [ ] Post-merge: `git checkout main && git pull`
