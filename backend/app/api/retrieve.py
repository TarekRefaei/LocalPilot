"""
Retrieval endpoint for semantic code search.
Exposes the MultiLevelRetriever via REST API with debug gating.
"""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.models.retrieve import RetrieveRequest, RetrieveResponse, RetrieveResult, ScoreBreakdown
from app.services.rag.cache import QueryCache
from app.services.rag.embedding_service import EmbeddingService
from app.services.rag.retriever import MultiLevelRetriever
from app.services.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/retrieve", tags=["retrieval"])


async def get_retriever() -> MultiLevelRetriever:
    """
    Dependency to construct and return a MultiLevelRetriever instance.

    Constructs:
    - QueryCache for embedding/search caching
    - EmbeddingService with query cache
    - VectorStore (defaults to settings.vector_db_path)
    - MultiLevelRetriever with enable_keyword_level=True

    Returns:
        MultiLevelRetriever instance
    """
    cache = QueryCache(max_size=1000)
    embedding_service = EmbeddingService(query_cache=cache)
    vector_store = VectorStore(persist_directory=settings.vector_db_path)
    retriever = MultiLevelRetriever(
        vector_store=vector_store,
        embedding_service=embedding_service,
        query_cache=cache,
        enable_keyword_level=True,
    )
    return retriever


@router.post("", response_model=RetrieveResponse)
async def retrieve(request: RetrieveRequest) -> RetrieveResponse:
    """
    Execute multi-level retrieval for semantic code search.

    Behavior:
    - Strips and validates query (non-empty)
    - Calls retriever.retrieve(query, top_k, user_context)
    - Applies debug gating: if debug=false, removes scores and diversity_adjusted_score

    Args:
        request: RetrieveRequest with query, top_k, debug flag, optional user_context

    Returns:
        RetrieveResponse with results, total_count, and echoed parameters

    Raises:
        HTTPException: 400 if query is empty after stripping
        HTTPException: 500 if retrieval fails
    """
    try:
        # Strip and validate query
        query = request.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        logger.info(f"Retrieve request: query='{query}', top_k={request.top_k}, debug={request.debug}")

        # Get retriever instance
        retriever = await get_retriever()

        # Call retriever
        raw_results = await retriever.retrieve(
            query=query,
            top_k=request.top_k,
            user_context=request.user_context.model_dump() if request.user_context else None,
        )

        # Convert raw results to RetrieveResult objects
        results: list[RetrieveResult] = []
        for raw_result in raw_results:
            # Extract score breakdown if present
            scores_dict = raw_result.get("scores", {})
            score_breakdown = None
            if scores_dict:
                score_breakdown = ScoreBreakdown(
                    semantic_score=scores_dict.get("semantic_score", 0.0),
                    symbol_score=scores_dict.get("symbol_score", 0.0),
                    keyword_score=scores_dict.get("keyword_score", 0.0),
                    summary_score=scores_dict.get("summary_score", 0.0),
                    fused_score=scores_dict.get("fused_score", 0.0),
                )

            result = RetrieveResult(
                id=raw_result.get("id", ""),
                file_path=raw_result.get("file_path", ""),
                chunk_index=raw_result.get("chunk_index", 0),
                content=raw_result.get("content", ""),
                start_line=raw_result.get("start_line", 0),
                end_line=raw_result.get("end_line", 0),
                symbols=raw_result.get("symbols", []),
                score=raw_result.get("score"),
                diversity_adjusted_score=raw_result.get("diversity_adjusted_score"),
                scores=score_breakdown,
            )

            # Apply debug gating: remove scores if debug=false
            if not request.debug:
                result.score = None
                result.diversity_adjusted_score = None
                result.scores = None

            results.append(result)

        response = RetrieveResponse(
            results=results,
            total_count=len(results),
            query=query,
            top_k=request.top_k,
            debug=request.debug,
        )

        logger.info(f"Retrieve response: {len(results)} results returned")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}") from e
