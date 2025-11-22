Agent 09 — Retrieval & Ranking: Decisions Finalized and Gap‑Fix Plan
Go‑Ahead
Proceed to implement the steps below as the next incremental PR.
Scope: Level 4 (lexical BM25) + QueryCache wiring + VectorStore path unification + retrieval API contract handoff.
Constraint: Keep the UI unchanged (retrieved context remains invisible).
Decisions Finalized
Endpoint strategy
Choose: Dedicated POST /retrieve now.
Why: Separation of concerns, reusability for Chat and Plan, easier metrics/benchmarks; later, /chat/answer can orchestrate retrieval + LLM.
Lexical Level 4 approach
Choose: Add lightweight dependency rank_bm25.
Why: Higher quality and faster delivery than re‑implementing BM25; small footprint; can be feature‑flagged.
VectorStore persistence path
Choose: Unify VectorStore.persist_directory to settings.vector_db_path now.
Why: Single source of truth via config; avoids drift; aligns with RAG spec.
UI treatment of retrieved context
Choose: Keep context invisible in the extension UI (per your request).
Note: Allow optional diagnostic metadata in API responses behind a debug flag (not displayed in UI).
Gap‑Fix Document (Agent 09)
Ideal Prompt (For Agent 09)
“Complete multi‑level retrieval by implementing Level 4 lexical (BM25) and wiring LRU caching for query embeddings and vector search results. Align VectorStore persistence with settings.vector_db_path. Maintain Precision
5
 ≥ 0.80 on the existing fixture set and keep current tests green. Coordinate with Agent 05 to expose a dedicated POST /retrieve endpoint that returns fused and diversity‑re‑ranked results. Do not change the Chat UI (context remains invisible).”

Detailed TODOs
[L4 Keyword/Lexical — BM25]
Add dependency: rank_bm25 to 
backend/requirements.txt
.
Implement 
_level4_keyword_search(query, top_k=10)
 in 
retriever.py
:
Build a simple corpus over chunk contents (via vector store pulls or retained candidates).
Tokenize (lowercase, basic punctuation strip) and score with BM25.
Normalize BM25 scores to [0, 1] before fusion.
Return top results with {id, content, metadata, score}.
Tests:
Unit tests for BM25 path (deterministic tokenization and scoring).
Fusion test to ensure L4 contributes signal without overpowering semantic L3.
[Caching — Wire QueryCache]
Embedding cache:
Before 
EmbeddingService.embed_query
, check 
QueryCache.get_embedding(query)
.
After successful embed, 
QueryCache.set_embedding(query, embedding)
.
Search results cache:
Compute a stable key for 
search
 calls: SHA1 of JSON with rounded embedding (e.g., 4 decimals), filters, top_k.
Check 
QueryCache.get_search_results(key)
 before 
VectorStore.search
.
After search, 
QueryCache.set_search_results(key, results)
.
Tests:
Cache hit/miss behavior for embeddings and searches.
Idempotence: cached vs uncached returns identical results.
[Config — Unify VectorStore path]
Default VectorStore.persist_directory = settings.vector_db_path.
Ensure all constructors use settings by default (allow explicit override).
Test: Instantiate VectorStore and assert internal path equals settings.vector_db_path.
[Quality Gates & Observability]
Re‑run fixture evaluation ensuring avg Precision
5
 ≥ 0.80.
Log L4 latency and cache hit rates at DEBUG.
Add an ablation flag to disable L4 for diagnosis (env or constructor arg).
[API Handoff — Agent 05]
Contract proposal for POST /retrieve:
Request:
query: str
top_k: int = 5
user_context?: { current_file?: str, recent_files?: str[], current_directory?: str }
debug?: bool (if true, include scoring breakdown)
Response: results: Array<{ id, content, metadata, score, fused_score, diversity_adjusted_score?, scores?: { semantic?, symbol?, keyword?, summary? } }>
Agent 05 adds the router and integration test; Agent 09 provides usage snippet._
Implementation Guidance
BM25 normalization
Normalize BM25 scores per query using min‑max or divide by max to [0,1].
Keep keyword_weight at 0.15 initially. If P
5
 regresses, tune weights or raise min score thresholds.
Tokenization
Keep simple: lowercase, split on whitespace, strip basic punctuation.
Avoid heavy NLP deps; deterministic behavior is preferable.
Cache keys
Embedding cache key: raw query string.
Search cache key: sha1(json.dumps({vec: round(embedding,4), filters, top_k}, sort_keys=True)).
Diversity & fusion
Preserve metadata.file_path end‑to‑end for diversity penalties.
Do not change default fusion weights unless fixture P
5
 drops.
Rollout plan
Step 1: Implement BM25 + caching, run all retrieval/fusion tests + fixtures.
Step 2: Unify VectorStore path; smoke test init.
Step 3: Hand off /retrieve to Agent 05; validate route with retriever mocks.
Step 4: Land PR after CI green and P
5
 gate verified.