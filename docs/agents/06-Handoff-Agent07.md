# Agent Handoff: Agent 06 → Agent 07 (Indexing: Structure & Chunking)

## Handoff Summary
- From Agent: Agent 06 — Indexing: Discovery & Docs → To Agent: Agent 07 — Indexing: Structure & Chunking
- Date: 2025-11-21
- Milestone: Week 3
- Scope delivered: Discovery walker honoring .gitignore, documentation extractors (Markdown, JSDoc, Python docstrings), file-hash cache (SQLite + sha256), indexing orchestrator with progress/complete events, and VS Code extension hooks to start indexing and reflect progress.

## Artifacts
- Code branches/dirs:
  - Backend: app/services/indexing/{discovery.py, documentation.py, cache.py, orchestrator.py}
  - Backend WS: app/api/websocket.py (handles indexing.start)
  - Extension: src/services/realtime.ts, wiring in src/commands.ts
  - Docs: docs/agents/06-Indexing-Discovery-Docs.md (updated with contracts and examples)
- Test results:
  - Backend: pytest green for discovery/cache/doc/orchestrator
  - Extension: Jest green; baseline coverage ≥ 75%
- Deps added: backend/requirements.txt → pathspec

## Interfaces & Contracts
- WebSocket events (payloads):
  - indexing.start → { workspace_path: string, options?: object }
  - indexing.progress → { indexing_id: string, phase: string, phase_number: number, total_phases: number, current_file: number, total_files: number, current_file_path?: string, percentage: number, estimated_time_remaining_seconds: number, message: string }
  - indexing.complete → { indexing_id: string, duration_seconds: number, statistics: object, project_summary?: string, failed_files?: object[] }
- DocumentChunk shape (for extractors):
  - { id: string, content: string, source_file: string, chunk_type: 'markdown'|'jsdoc'|'docstring', title?: string, section?: string }
- Cache schema (SQLite at .localpilot/index_cache.sqlite):
  - files(file_path TEXT PK, hash TEXT, size INTEGER, mtime REAL, language TEXT, last_indexed TEXT, doc_extracted INTEGER, error TEXT)
  - runs(id TEXT PK, started TEXT, ended TEXT, status TEXT, stats_json TEXT)
  - run_files(run_id TEXT, file_path TEXT, status TEXT, PK(run_id, file_path))

## Validation & Demos
- Local demo:
  1) Start backend: uvicorn app.main:app --port 8765
  2) VS Code → run command "LocalPilot: Start Indexing"
  3) Observe Indexing view switches to Running, then "Indexing: Complete" toast
- Tests:
  - Backend: python -m venv .venv && .venv/Scripts/python -m pip install -r requirements-dev.txt && .venv/Scripts/pytest -q
  - Extension: npm ci && npm test
- Known caveats:
  - Orchestrator emits progress with simple ETA (placeholder); improve once chunking/embeddings are added
  - .gitignore semantics from pathspec; additional project-specific rules may be introduced later

## Open Items
- Follow-ups:
  - Implement AST-based structural parsing & symbol extraction per language (TS/JS/Python) and produce structured chunks
  - Define chunking strategy (by symbols, by sections, token limits) and metadata (anchors, IDs)
  - Extend statistics to include symbols/chunks per language, and error logs per file
  - Incremental re-index on file change events leveraging the hash cache
- Deferred decisions:
  - Vector DB choice and schema (Agent 08)
  - Chunk granularity defaults and per-language heuristics
- Risks to track:
  - Performance on very large repos; consider parallelism and IO throttling
  - Windows path edge cases; continue normalizing with forward slashes and normcase

## Next Steps Guidance
- Priorities for Agent 07:
  - Build structure extractors (AST) and semantic chunker interface
  - Emit refined progress per sub-phase (parse, structure, chunk)
  - Prepare outputs consumable by embeddings pipeline (Agent 08)
- Acceptance reminders:
  - Structured chunks produced for small sample; enriched statistics; tests ≥ 75%

## Sign-off
- Acceptance by receiving agent: __________________________ (name/date)
