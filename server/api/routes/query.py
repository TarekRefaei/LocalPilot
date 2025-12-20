from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pathlib import Path

from server.api.dependencies import get_index_root, get_embedder
from server.indexing.query_service import QueryService

router = APIRouter()


class QueryRequest(BaseModel):
    project_id: str
    query: str
    top_k: int = 5


@router.post("/query")
def query_index(
    request: QueryRequest,
    index_root: Path = Depends(get_index_root),
    embedder = Depends(get_embedder),
):
    service = QueryService(
        index_root=index_root,
        project_id=request.project_id,
        embedder=embedder,
    )

    results = service.query(
        text=request.query,
        top_k=request.top_k,
    )

    return {"chunks": results}
