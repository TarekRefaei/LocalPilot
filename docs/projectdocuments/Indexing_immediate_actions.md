# LocalPilot — Indexing Immediate Actions & Defaults

This document captures the immediate actions, default decisions, and concrete artifacts requested:

- **Model-selection mapping (defaults + VRAM thresholds)**
- **WebSocket contract & TypeScript interfaces** (indexing events)
- **Chunking rules table & config defaults**
- **Soft "docs-only" read-only UX state** for the side-panel
- **Embedding A/B test harness (pytest) plan and sample test**

---

## 1. Defaults (chosen)

- Discovery: **Smart hybrid** (default excludes + editable whitelist + presets per project type)
- Chunking: **Hybrid AST-first** with token-size fallback
- Embeddings: **Default: bge-m3:latest**; fallbacks: `mxbai-embed-large:latest` then `jina/jina-embeddings-v2-base-en:latest`
- Chat / Coding LLMs: default `qwen2.5-coder:7b-instruct-q4_K_M`; fallback `qwen2.5-coder:14b-instruct-q4_K_M` when VRAM allows
- Vector DB: **ChromaDB + HNSW (M=16, ef_construction=200)**; search `ef_search=50` default
- Retrieval: **Multi-level**: Project summary → Symbol/metadata → Semantic vectors → Keyword lexical
- Context assembly: **Context-budget optimizer** (summary + diverse chunks + import lines)
- Index freshness: **Incremental on save** (file-hash & chunk-hash diffing)
- Edge cases: Skip binaries; cap large text files; sample & chunk very large files
- UI: Side-panel with Chat / Plan / Act tabs; **Docs-only soft-mode** allowed during indexing (read-only, docs-scoped chat)

---

## 2. Model-selection mapping (defaults)

| Task | Primary model | Fallback(s) | VRAM threshold (approx) |
|---|---:|---|---:|
| Embeddings | `bge-m3:latest` | `mxbai-embed-large:latest`, `jina-embeddings-v2-base-en` | 2–4 GB |
| Chat (general) | `qwen2.5-coder:7b-instruct-q4_K_M` | `qwen-custom:latest` | 6–8 GB |
| Plan-generation (long-form) | `qwen2.5-coder:14b-instruct-q4_K_M` | `qwen2.5-coder:7b` | 12+ GB |
| Code generation / Act-mode edits | `qwen2.5-coder:7b-instruct-q4_K_M` | `qwen2.5-coder:14b` | 6–12 GB |

> _Notes:_ The VRAM thresholds are conservative approximations to drive the runtime auto-suggester. You can tune based on real hardware profiling.

---

## 3. WebSocket contract & TypeScript interfaces

**Events (direction: server -> client unless noted)**

- `indexing.start` — indicates indexing started
- `indexing.progress` — progress updates (phase, percentage, current_file, stats)
- `indexing.complete` — indexing finished with result summary
- `indexing.error` — error state
- `indexing.partial_ready` — docs-only partial index available (enable soft-mode)

**Sample event payloads & TypeScript interfaces**

```ts
// shared/types/indexing.ts
export type IndexingPhase =
  | 'discovery'
  | 'analysis'
  | 'chunking'
  | 'embedding'
  | 'summarization'
  | 'complete'
  | 'error';

export interface IndexingProgress {
  jobId: string; // uuid
  phase: IndexingPhase;
  percent: number; // 0-100
  currentFile?: string; // path
  filesScanned?: number;
  filesIndexed?: number;
  estimatedRemainingSeconds?: number;
  message?: string;
  timestamp: string; // ISO
}

export interface IndexingResult {
  jobId: string;
  indexedFiles: number;
  indexedChunks: number;
  vectorSize: number; // total vectors
  durationSeconds: number;
  summaryPath?: string; // path to generated project summary
  partialDocsReady?: boolean; // if docs-only is available before complete
}

export interface IndexingError {
  jobId: string;
  errorCode: string;
  message: string;
  details?: Record<string, any>;
}
```

**WebSocket example (JSON)**

```json
{ "event": "indexing.progress", "data": { "jobId": "...", "phase": "embedding", "percent": 57, "currentFile": "src/app/main.py", "filesScanned": 234, "filesIndexed": 87, "estimatedRemainingSeconds": 42, "timestamp": "2025-11-15T02:12:00Z" } }
```

---

## 4. Chunking rules table & config defaults

- **Primary strategy:** AST-first chunking. For supported languages (Python, JavaScript/TypeScript, Kotlin, Dart, Swift, Java, C#, C++) extract logical units:
  - Function/method body (include signature and docstring)
  - Class definition (full class)
  - Module-level constants & imports
- **Fallback:** For files that fail AST parse or exceed token length: token-slice with overlap.

**Config defaults**
- `maxTokensPerChunk`: 1024
- `chunkOverlapTokens`: 64
- `maxFileSizeMB`: 5 (skip or sample if larger)
- `minChunkSizeTokens`: 64
- `maxChunksPerFile`: 200

**Chunk metadata** (store with each vector):
```json
{ "file_path": "src/foo.py", "start_line": 120, "end_line": 160, "language": "python", "chunk_type": "function", "symbols": ["do_stuff"] }
```

---

## 5. Docs-only soft-mode UX state (side-panel)

- State: `indexing.initial` → `indexing.partial_docs_ready` → `indexing.complete`
- When server emits `indexing.partial_ready`, the client enables a **Docs-only** read-only Chat tab that only queries documentation & README-level vectors. Chat/Plan/Act other modes remain disabled until full index or user override.
- UI copy example (short): "Partial docs indexed — you can ask about README and docs while full indexing continues. Some answers may be incomplete."

---

## 6. Embedding A/B test harness (pytest plan)

- Objective: Compare `bge-m3:latest` vs `mxbai-embed-large:latest` vs `jina/jina-embeddings-v2-base-en` on Retrieval Precision@5 and latency
- Components:
  - Small fixture repo (10–30 files) with curated queries + ground-truth relevant chunks
  - Test runner script that: (1) builds embeddings for fixture repo, (2) stores in temporary vectordb, (3) runs queries, (4) computes Precision@5 and average embed time.

**Sample pytest test (pseudocode)**

```py
def test_embedding_quality(tmp_path):
    repo = tmp_path / "fixture_repo"
    # ... create files, queries, ground_truth mapping ...
    for model in ["bge-m3", "mxbai", "jina-v2"]:
        vectors = embed_repo(repo, model=model)
        db = build_chroma(vectors)
        precision = compute_precision_at_k(db, queries, k=5)
        assert precision >= 0.8, f"{model} below target: {precision}"
```

---

## 7. Next actions I will take (if you confirm)

- Produce `ws-contract.md` and `shared/types/indexing.ts` as separate files for the repo (ready to paste)
- Add the **Model-selection mapping** to `Model_Management_spec.md`
- Add **Chunking rules table** to `Indexing_System_Spec.md`
- Add the **Docs-only state** to `UI_Design_System.md`
- Create the **pytest A/B harness** test file under `tests/integration/test_embedding_ab.py`

If you confirm, I will create these files/content now.

---

*End of document.*

