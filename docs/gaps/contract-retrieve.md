Contract for POST /retrieve
Method: POST
Path: /retrieve
Purpose: Run multi-level retrieval (L2 symbols, L3 semantic, L4 BM25) and return fused, diversity re-ranked results.
Constraints: Retrieved context must not be displayed in the Chat UI. If debug=false, omit scoring breakdown fields from the response.
Request body
query: string (required)
top_k: int (default 5, 1–50 reasonable)
user_context: object (optional)
current_file?: string
recent_files?: string[]
current_directory?: string
debug: boolean (default false, when true include scoring breakdown)
Example:

json
{
  "query": "How does authentication work?",
  "top_k": 5,
  "user_context": {
    "current_file": "backend/app/services/rag/retriever.py",
    "recent_files": ["backend/app/services/rag/fusion.py"],
    "current_directory": "backend/app/services/rag/"
  },
  "debug": false
}
Response body
results: Array of result objects
id: string
content: string
metadata: object
score: number
fused_score: number
diversity_adjusted_score?: number
scores?: object
semantic?: number
symbol?: number
keyword?: number
summary?: number
Example (debug=false removes scores and diversity_adjusted_score):

json
{
  "results": [
    {
      "id": "auth_001",
      "content": "def authenticate(username, password): ...",
      "metadata": { "file_path": "backend/auth.py", "language": "python" },
      "score": 0.84,
      "fused_score": 0.76
    }
  ]
}
Usage snippet (FastAPI router)
Place in app/api/retrieve.py (Agent 05):

python
from typing import Any, Optional, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.services.rag.cache import QueryCache
from app.services.rag.embedding_service import EmbeddingService
from app.services.rag.retriever import MultiLevelRetriever
from app.services.rag.vector_store import VectorStore

router = APIRouter(tags=["retrieval"])

class UserContext(BaseModel):
    current_file: Optional[str] = None
    recent_files: Optional[List[str]] = None
    current_directory: Optional[str] = None

class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=50)
    user_context: Optional[UserContext] = None
    debug: bool = False

class ScoreBreakdown(BaseModel):
    semantic: Optional[float] = None
    symbol: Optional[float] = None
    keyword: Optional[float] = None
    summary: Optional[float] = None

class RetrieveResult(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    score: float
    fused_score: float
    diversity_adjusted_score: Optional[float] = None
    scores: Optional[ScoreBreakdown] = None

class RetrieveResponse(BaseModel):
    results: List[RetrieveResult]

def get_retriever() -> MultiLevelRetriever:
    # Defaults: VectorStore path from settings.vector_db_path
    cache = QueryCache(max_size=1000)
    embedding = EmbeddingService(query_cache=cache)
    store = VectorStore()
    return MultiLevelRetriever(
        vector_store=store,
        embedding_service=embedding,
        query_cache=cache,
        enable_keyword_level=True,  # Ablation flag; set False to disable L4
    )

@router.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_endpoint(
    req: RetrieveRequest,
    retriever: MultiLevelRetriever = Depends(get_retriever),
) -> RetrieveResponse:
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="query is required")

    uc = req.user_context.model_dump() if req.user_context else None
    results = await retriever.retrieve(q, top_k=req.top_k, user_context=uc)

    if not req.debug:
        for r in results:
            r.pop("scores", None)
            r.pop("diversity_adjusted_score", None)

    # UI must not display retrieved context; the API only returns data
    return RetrieveResponse(results=results)
Register router in 
app/main.py
:

python
from app.api.retrieve import router as retrieve_router
app.include_router(retrieve_router)
Example clients
curl:
bash
curl -s -X POST http://127.0.0.1:8765/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query":"authentication flow","top_k":5,"debug":false}'
Python:
python
import requests
resp = requests.post("http://127.0.0.1:8765/retrieve", json={
  "query": "authentication flow",
  "top_k": 5,
  "debug": False
})
print(resp.json())
Integration test outline (Agent 05)
Use a mock retriever to validate the route shape without hitting Chroma:

python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from app.api.retrieve import router, get_retriever

def test_retrieve_endpoint_shape(monkeypatch):
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    mock = AsyncMock()
    mock.retrieve.return_value = [
        {
            "id": "doc1",
            "content": "text",
            "metadata": {"file_path": "a.py"},
            "score": 0.9,
            "fused_score": 0.85,
            "scores": {"semantic": 0.8, "keyword": 0.2}
        }
    ]
    monkeypatch.setattr("app.api.retrieve.get_retriever", lambda: mock)

    # debug=false: scores omitted
    r = client.post("/retrieve", json={"query": "q", "top_k": 3, "debug": False})
    assert r.status_code == 200
    data = r.json()
    assert "results" in data and len(data["results"]) == 1
    assert "scores" not in data["results"][0]

    # debug=true: scores included
    r2 = client.post("/retrieve", json={"query": "q", "top_k": 3, "debug": True})
    assert r2.status_code == 200
    assert "scores" in r2.json()["results"][0]
Summary
Contract and usage snippet for POST /retrieve provided.
Response includes fused and diversity-aware scores; debug controls scoring breakdown visibility.
Router wiring and integration test example included.
Keeps UI unchanged (context not displayed).


# Agent 05 — Implementation Brief (Prompts, TODOs, Criteria)

## Ideal Prompt (Copy-Paste for Agent 05)

"Implement a dedicated POST /retrieve endpoint that calls the MultiLevelRetriever and returns fused, diversity re‑ranked results. Use the provided request/response contract. Respect debug gating (omit scores when debug=false). Register the router in app/main.py. Add an integration test that mocks the retriever and asserts response shape. Do not change the extension UI (retrieved context remains invisible)."

## Detailed TODOs

- **Create router**
  - File: `app/api/retrieve.py`.
  - Define models: `UserContext`, `RetrieveRequest`, `ScoreBreakdown`, `RetrieveResult`, `RetrieveResponse`.
  - Dependency `get_retriever()` constructs `QueryCache`, `EmbeddingService(query_cache=cache)`, `VectorStore()` (defaults to `settings.vector_db_path`), and `MultiLevelRetriever(enable_keyword_level=True)`.
  - Endpoint: `@router.post("/retrieve", response_model=RetrieveResponse)`.
  - Behavior: strip query; validate non-empty; call `retriever.retrieve(query, top_k, user_context)`.
  - Gating: if `debug` is false remove `scores` and `diversity_adjusted_score` fields before returning.

- **Register router**
  - In `app/main.py`, `from app.api.retrieve import router as retrieve_router` and `app.include_router(retrieve_router)`.

- **Integration test**
  - Use `fastapi.testclient.TestClient`.
  - Monkeypatch `get_retriever()` to return an `AsyncMock` with a canned `retrieve` result.
  - Assert: 200, contains `results`, honors debug gating: when `debug=false` `scores` absent; when `debug=true` scores present.

- **Observability (optional but recommended)**
  - GET `/metrics/retrieval` returns retrieval metrics (L4 latency, cache stats). Already implemented and registered.
  - Add a simple test to assert it returns a dict with keys: `l4_enabled`, `last_l4_ms`, `cache_stats`.

- **Config sanity**
  - No need to pass `persist_directory`; `VectorStore` defaults to `settings.vector_db_path`.
  - Ensure indexing is run at least once so Chroma DB has data before calling `/retrieve`.

- **Non-functional checks**
  - Input validation: `top_k` 1–50; non-empty `query`.
  - Performance: rely on `QueryCache` to avoid redundant embedding/search.
  - Logging: minimal INFO for request receipt; DEBUG for diagnostics only.

## Acceptance Criteria

- `POST /retrieve` returns HTTP 200 with shape matching `RetrieveResponse`.
- `debug=false` omits `scores` and `diversity_adjusted_score`; `debug=true` includes them.
- Router is registered and visible in OpenAPI when `settings.debug=True`.
- Integration test for route passes and does not hit Chroma or Ollama (uses mocks).
- No changes to the extension UI; no leakage of retrieved context to UI.
- Existing tests remain green.

## Verification Steps

- Run focused route test:
```bash
.venv/Scripts/pytest -q tests -k retrieve_endpoint_shape
```

- Smoke the retrieval API (service running):
```bash
curl -s -X POST http://127.0.0.1:8765/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query":"authentication flow","top_k":5,"debug":false}'
```

- Check observability endpoint:
```bash
curl -s http://127.0.0.1:8765/metrics/retrieval | jq .
```

Sample response:
```json
{
  "l4_enabled": true,
  "last_l4_ms": 12.3,
  "cache_stats": {
    "embedding_cache_size": 0,
    "search_cache_size": 0,
    "total_cache_size": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "cache_hit_rate": 0.0,
    "max_size": 1000
  },
  "timestamp": 1732260000.123
}
```

## Notes

- Retrieval levels and fusion are already implemented (L2 symbols, L3 semantic, L4 BM25 with ablation flag). No UI changes required.
- VectorStore persistence path is unified to `settings.vector_db_path`.
- If fixture precision regresses in future changes, consider tuning fusion weights or disabling L4 via `enable_keyword_level=False`.