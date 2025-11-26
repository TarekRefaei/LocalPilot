import pytest

from app.api.retrieve import get_retriever
from app.services.rag.retriever import MultiLevelRetriever


@pytest.mark.asyncio
async def test_get_retriever_constructs_dependencies(monkeypatch):
    # Ensure vector store uses in-memory fake on Windows to avoid file locks
    monkeypatch.setenv("LOCALPILOT_CHROMA_FAKE", "1")

    retriever = await get_retriever()
    assert isinstance(retriever, MultiLevelRetriever)
    # basic sanity on constructed components
    assert retriever.vector_store is not None
    assert retriever.embedding_service is not None
    # MultiLevelRetriever exposes the cache as `cache`
    assert getattr(retriever, "cache", None) is not None
