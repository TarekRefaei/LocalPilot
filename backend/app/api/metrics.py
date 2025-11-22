from fastapi import APIRouter

from app.services.rag import retrieval_metrics

router = APIRouter(tags=["metrics"])


@router.get("/metrics/retrieval")
async def get_retrieval_metrics() -> dict:
    """Return retrieval metrics for observability (non-sensitive)."""
    return retrieval_metrics.get()
