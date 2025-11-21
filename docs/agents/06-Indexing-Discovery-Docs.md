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
- [x] Discovery walkers honoring .gitignore and project rules.
- [x] Doc/markdown extraction with metadata.
- [x] File-hash cache for change detection.
- [x] Progress events to `Indexing` view via WS.
- [x] Pytest unit tests for walkers/parsers/cache.
- [x] TDD: failing tests for cache invalidation + event emission; implement.

## Milestones & Success Criteria
- Small repo indexes reliably; progress visible in the UI.
- Unit tests pass with good coverage.

## Handoff documents
### To Agent 07 — Indexing: Structure & Chunking document (follow docs\agents\_templates\Agent_Handoff_Template.md)
- Provide metadata schema and sample outputs; define extension points for AST parsing.
- Include module boundaries and extension points:
  - Backend: `app/services/indexing/*` (discovery, documentation, cache, orchestrator)
  - Event contracts: `indexing.start`, `indexing.progress`, `indexing.complete`
  - Extensibility: add AST-based extractors (TS/JS/py) and semantic chunkers
- Attach example outputs (sample `DocumentChunk` lists) and stats JSON from orchestrator
- List test fixtures and guidelines for new extractor tests

### To Supervisor documents
- Report on indexing speed and coverage; risks for large repos.
- Fixtures saved for regression.
- Outline performance considerations and next-phase scope (Agent 07)

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
    - Mitigation: `pathspec` for gitignore semantics; normalize paths to forward-slash and use `os.path.normcase`
  - Large repo performance; binary/large files
    - Mitigation: binary sniff + default excludes; stream hashing; incremental cache updates
  - Hidden/system files indexing accidentally
    - Mitigation: skip hidden by default; allow explicit overrides later
  - CRLF vs LF and encoding
    - Mitigation: read text as UTF-8 with fallback; tests include Windows-style paths

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

## Implementation Summary (Agent 06)

### Extractors
- Markdown: Split by headers (h1–h6), preserve code fences, attach `title` and `section`. Source file path recorded relative to workspace.
- JSDoc: Extract `/** ... */` blocks, clean `*` prefix, associate nearest function when available.
- Python docstrings: Triple-quoted blocks, associate preceding `def|class` when available.

### Store Design (File-Hash Cache)
- SQLite at `.localpilot/index_cache.sqlite` inside workspace.
- Tables
  - `files(file_path, hash, size, mtime, language, last_indexed, doc_extracted, error)`
  - `runs(id, started, ended, status, stats_json)`
  - `run_files(run_id, file_path, status)`
- Hash algorithm: `sha256` (stdlib). Normalized workspace-relative paths.

### Progress Events and Orchestration
- Extension sends `indexing.start` with workspace path.
- Backend orchestrator phases:
  - Discovery → `indexing.progress` (counts, ETA)
  - Documentation extraction → incremental `indexing.progress`
  - Completion → `indexing.complete` with statistics
- WebSocket endpoint validates `indexing.start`, starts orchestrator in background, and broadcasts events.

### Event Topics & Payloads
- `indexing.start`
  - Data: `{ workspace_path: string, options?: object }`
- `indexing.progress`
  - Data: `{ indexing_id: string, phase: string, phase_number: number, total_phases: number, current_file: number, total_files: number, current_file_path?: string, percentage: number, estimated_time_remaining_seconds: number, message: string }`
- `indexing.complete`
  - Data: `{ indexing_id: string, duration_seconds: number, statistics: object, project_summary?: string, failed_files?: object[] }`

### Example Outputs
- Sample `DocumentChunk[]`
```json
[
  {
    "id": "README-0",
    "content": "# Title\nIntro...",
    "source_file": "README.md",
    "chunk_type": "markdown",
    "title": "Title",
    "section": "h1"
  },
  {
    "id": "main-docstring-0",
    "content": "Function docstring.",
    "source_file": "src/main.py",
    "chunk_type": "docstring",
    "title": "main"
  }
]
```

- Sample `statistics` from `indexing.complete`
```json
{
  "total_files": 12,
  "files_by_type": { "markdown": 2, "python": 5, "typescript": 3, "other": 2 },
  "project_type": "python",
  "docs_chunks": 9,
  "added": 7,
  "modified": 1,
  "deleted": 0,
  "estimated_seconds": 4
}
```

### Test Fixtures & Guidelines
- Prefer `tmp_path` and create small trees with `.gitignore`, `node_modules/`, hidden files, and a binary sentinel.
- Verify Windows path normalization and `.gitignore` negation patterns.
- Keep docstrings/comments >10 chars to avoid trivial skip filter.
- Measure coverage in CI; keep baseline ≥ 75% and expand as Agent 07 adds AST parsing.

### Tests
- Discovery: honors `.gitignore`, excludes defaults/hidden/binaries, categorization, project markers.
- Cache: detects added/modified/deleted; stable hashing; path normalization.
- Documentation: markdown sectioning; JSDoc and Python docstring extraction.
- Orchestrator: emits `indexing.progress` and `indexing.complete` envelopes with expected shape.

### Acceptance
- Indexes a tiny sample repo in tests; progress events surfaced to the extension Indexing view.
- Coverage target ≥ 75% (baseline on unit tests).

### Acceptance Demo Steps
1. Start backend: `uvicorn app.main:app --port 8765`
2. In VS Code, open a workspace with a few files (README.md, small src/)
3. Run command: "LocalPilot: Start Indexing"
4. Observe Indexing view: status switches to Running; after completion, shows Idle and a toast "Indexing: Complete"
5. Verify WS logs carry `indexing.progress` and `indexing.complete` events

## PR & Merge Checklist
- [ ] Branch up to date with `main` (rebase preferred)
- [ ] Required checks passed (lint, type, tests, coverage)
- [ ] Acceptance gates satisfied (index small repo; progress visible; tests ≥ 75%)
- [ ] ≥1 approval obtained; risks documented
- [ ] Squash merge with Conventional Commit title; delete branch
- [ ] Post-merge: `git checkout main && git pull`
