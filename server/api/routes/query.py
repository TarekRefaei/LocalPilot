from pathlib import Path
from fastapi import APIRouter, Depends

try:
    from ..schemas.query import QueryRequest, QueryResponse
    from ...indexing.query_service import QueryService
    from ..dependencies import get_embedder, get_index_root
except ImportError:
    from api.schemas.query import QueryRequest, QueryResponse
    from indexing.query_service import QueryService
    from api.dependencies import get_embedder, get_index_root

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_index(
    request: QueryRequest,
    embedder = Depends(get_embedder),
    index_root: Path = Depends(get_index_root),
):
    service = QueryService(
        index_root=index_root / request.project_id,
        embedder=embedder
    )

    results = service.query(
        text=request.query,
        top_k=request.top_k,
        where=request.filters
    )

    return {"chunks": results}
