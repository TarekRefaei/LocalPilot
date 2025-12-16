from typing import List, Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    project_id: str
    query: str
    top_k: int = 5
    filters: Optional[dict] = None


class RetrievedChunk(BaseModel):
    id: str
    content: str
    metadata: dict
    distance: float


class QueryResponse(BaseModel):
    chunks: List[RetrievedChunk]
