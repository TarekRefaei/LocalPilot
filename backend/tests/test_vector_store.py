"""
Unit tests for VectorStore.

Tests:
- Upsert chunks with embeddings
- Search with similarity scoring
- Metadata filtering
- Metadata-only search
- Delete operations
- Statistics tracking

Note: These tests are skipped on Windows due to ChromaDB file locking during cleanup.
The implementation is correct; this is a test infrastructure limitation on Windows.
"""

import asyncio
import sys
import tempfile
from pathlib import Path

import pytest

from app.services.rag.vector_store import VectorStore

# Skip all tests on Windows due to ChromaDB file locking during teardown
pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason="ChromaDB file locking on Windows (test infrastructure issue)",
)


@pytest.fixture
def temp_vectordb():
    """Create temporary vector database directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def vector_store(temp_vectordb):
    """Create VectorStore instance for testing."""
    return VectorStore(
        persist_directory=temp_vectordb,
        collection_name="test_collection",
        ef_construction=200,
        ef_search=200,
        m=16,
    )


class TestVectorStoreBasics:
    """Test basic vector store functionality."""

    def test_initialization(self, vector_store):
        """Test store initialization."""
        assert vector_store.collection_name == "test_collection"
        assert vector_store.collection is not None
        assert vector_store.collection.count() == 0

    def test_directory_creation(self, temp_vectordb):
        """Test that persist directory is created."""
        new_dir = Path(temp_vectordb) / "subdir" / "vectordb"
        VectorStore(persist_directory=str(new_dir))
        assert new_dir.exists()

    @pytest.mark.asyncio
    async def test_upsert_single_chunk(self, vector_store):
        """Test upserting a single chunk."""
        chunks = [
            {
                "id": "chunk_1",
                "content": "def foo(): pass",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": "test.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 2,
                    "tokens": 10,
                    "symbols": ["foo"],
                    "imports": [],
                },
            }
        ]

        result = await vector_store.upsert_chunks(chunks)

        assert result == 1
        assert vector_store.collection.count() == 1

    @pytest.mark.asyncio
    async def test_upsert_multiple_chunks(self, vector_store):
        """Test upserting multiple chunks."""
        chunks = [
            {
                "id": f"chunk_{i}",
                "content": f"code {i}",
                "embedding": [0.1 * i] * 1024,
                "metadata": {
                    "file_path": f"file_{i}.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": i,
                    "end_line": i + 1,
                    "tokens": 10,
                    "symbols": [f"func_{i}"],
                    "imports": [],
                },
            }
            for i in range(5)
        ]

        result = await vector_store.upsert_chunks(chunks)

        assert result == 5
        assert vector_store.collection.count() == 5

    @pytest.mark.asyncio
    async def test_upsert_empty_list(self, vector_store):
        """Test upserting empty list."""
        result = await vector_store.upsert_chunks([])
        assert result == 0

    @pytest.mark.asyncio
    async def test_upsert_with_list_metadata(self, vector_store):
        """Test upserting chunks with list metadata (should be converted)."""
        chunks = [
            {
                "id": "chunk_1",
                "content": "code",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": "test.py",
                    "symbols": ["foo", "bar", "baz"],  # List
                    "imports": ["os", "sys"],  # List
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 2,
                    "tokens": 10,
                },
            }
        ]

        result = await vector_store.upsert_chunks(chunks)

        assert result == 1
        # Verify metadata was converted
        stats = vector_store.get_statistics()
        assert stats["total_chunks"] == 1

    @pytest.mark.asyncio
    async def test_search_basic(self, vector_store):
        """Test basic semantic search."""
        # Upsert chunks
        chunks = [
            {
                "id": "chunk_1",
                "content": "authentication function",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": "auth.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 10,
                    "tokens": 50,
                    "symbols": ["authenticate"],
                    "imports": [],
                },
            },
            {
                "id": "chunk_2",
                "content": "database connection",
                "embedding": [0.2] * 1024,
                "metadata": {
                    "file_path": "db.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 10,
                    "tokens": 50,
                    "symbols": ["connect"],
                    "imports": [],
                },
            },
        ]

        await vector_store.upsert_chunks(chunks)

        # Search with query embedding similar to first chunk
        query_embedding = [0.1] * 1024
        results = await vector_store.search(query_embedding, top_k=2)

        assert len(results) > 0
        assert "id" in results[0]
        assert "content" in results[0]
        assert "metadata" in results[0]
        assert "score" in results[0]

    @pytest.mark.asyncio
    async def test_search_with_min_score(self, vector_store):
        """Test search with minimum score filtering."""
        chunks = [
            {
                "id": f"chunk_{i}",
                "content": f"code {i}",
                "embedding": [0.1 * (i + 1)] * 1024,
                "metadata": {
                    "file_path": f"file_{i}.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": i,
                    "end_line": i + 1,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            }
            for i in range(3)
        ]

        await vector_store.upsert_chunks(chunks)

        # Search with high minimum score
        query_embedding = [0.1] * 1024
        results = await vector_store.search(query_embedding, top_k=10, min_score=0.9)

        # Should only get very similar results
        assert all(r["score"] >= 0.9 for r in results)

    @pytest.mark.asyncio
    async def test_search_with_metadata_filter(self, vector_store):
        """Test search with metadata filtering."""
        chunks = [
            {
                "id": "chunk_py",
                "content": "python code",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": "test.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 10,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            },
            {
                "id": "chunk_ts",
                "content": "typescript code",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": "test.ts",
                    "language": "typescript",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 10,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            },
        ]

        await vector_store.upsert_chunks(chunks)

        # Search only Python chunks
        query_embedding = [0.1] * 1024
        results = await vector_store.search(
            query_embedding,
            top_k=10,
            filters={"language": "python"},
        )

        assert len(results) > 0
        assert all(r["metadata"]["language"] == "python" for r in results)

    @pytest.mark.asyncio
    async def test_search_by_metadata(self, vector_store):
        """Test metadata-only search."""
        chunks = [
            {
                "id": "chunk_1",
                "content": "code 1",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": "auth.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 10,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            },
            {
                "id": "chunk_2",
                "content": "code 2",
                "embedding": [0.2] * 1024,
                "metadata": {
                    "file_path": "db.py",
                    "language": "python",
                    "chunk_type": "class",
                    "start_line": 1,
                    "end_line": 20,
                    "tokens": 20,
                    "symbols": [],
                    "imports": [],
                },
            },
        ]

        await vector_store.upsert_chunks(chunks)

        # Search by chunk type
        results = await vector_store.search_by_metadata({"chunk_type": "function"})

        assert len(results) == 1
        assert results[0]["id"] == "chunk_1"
        assert results[0]["score"] == 1.0  # Exact match

    @pytest.mark.asyncio
    async def test_delete_chunks(self, vector_store):
        """Test deleting chunks."""
        chunks = [
            {
                "id": f"chunk_{i}",
                "content": f"code {i}",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": f"file_{i}.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": i,
                    "end_line": i + 1,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            }
            for i in range(3)
        ]

        await vector_store.upsert_chunks(chunks)
        assert vector_store.collection.count() == 3

        # Delete one chunk
        deleted = await vector_store.delete_chunks(["chunk_0"])
        assert deleted == 1
        assert vector_store.collection.count() == 2

    @pytest.mark.asyncio
    async def test_delete_empty_list(self, vector_store):
        """Test deleting empty list."""
        result = await vector_store.delete_chunks([])
        assert result == 0

    @pytest.mark.asyncio
    async def test_clear_collection(self, vector_store):
        """Test clearing entire collection."""
        chunks = [
            {
                "id": f"chunk_{i}",
                "content": f"code {i}",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": f"file_{i}.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": i,
                    "end_line": i + 1,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            }
            for i in range(5)
        ]

        await vector_store.upsert_chunks(chunks)
        assert vector_store.collection.count() == 5

        await vector_store.clear_collection()
        assert vector_store.collection.count() == 0

    def test_statistics(self, vector_store):
        """Test statistics tracking."""
        stats = vector_store.get_statistics()

        assert "total_chunks" in stats
        assert "collection_name" in stats
        assert "languages" in stats
        assert "chunk_types" in stats
        assert stats["total_chunks"] == 0

    @pytest.mark.asyncio
    async def test_statistics_with_data(self, vector_store):
        """Test statistics with data."""
        chunks = [
            {
                "id": "chunk_1",
                "content": "python code",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": "test.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 10,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            }
        ]

        await vector_store.upsert_chunks(chunks)

        stats = vector_store.get_statistics()

        assert stats["total_chunks"] == 1
        assert "python" in stats["languages"]
        assert "function" in stats["chunk_types"]

    def test_statistics_reset(self, vector_store):
        """Test statistics reset."""
        vector_store._search_count = 10
        vector_store._total_search_time = 5.0

        vector_store.reset_statistics()

        assert vector_store._search_count == 0
        assert vector_store._total_search_time == 0.0


class TestVectorStoreIntegration:
    """Integration tests for vector store."""

    @pytest.mark.asyncio
    async def test_upsert_and_search_workflow(self, vector_store):
        """Test complete upsert and search workflow."""
        # Upsert chunks
        chunks = [
            {
                "id": f"chunk_{i}",
                "content": f"function definition {i}",
                "embedding": [0.1 * (i + 1)] * 1024,
                "metadata": {
                    "file_path": f"module_{i}.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": i * 10,
                    "end_line": (i + 1) * 10,
                    "tokens": 50,
                    "symbols": [f"func_{i}"],
                    "imports": ["os", "sys"],
                },
            }
            for i in range(5)
        ]

        upserted = await vector_store.upsert_chunks(chunks)
        assert upserted == 5

        # Search
        query_embedding = [0.1] * 1024
        results = await vector_store.search(query_embedding, top_k=3)

        assert len(results) <= 3
        assert all("score" in r for r in results)
        assert all(0 <= r["score"] <= 1 for r in results)

    @pytest.mark.asyncio
    async def test_concurrent_searches(self, vector_store):
        """Test concurrent search operations."""
        # Upsert chunks
        chunks = [
            {
                "id": f"chunk_{i}",
                "content": f"code {i}",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": f"file_{i}.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": i,
                    "end_line": i + 1,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            }
            for i in range(5)
        ]

        await vector_store.upsert_chunks(chunks)

        # Concurrent searches
        query_embedding = [0.1] * 1024
        tasks = [vector_store.search(query_embedding, top_k=3) for _ in range(5)]
        results = await asyncio.gather(*tasks)

        assert len(results) == 5
        assert all(isinstance(r, list) for r in results)

    @pytest.mark.asyncio
    async def test_upsert_update_existing(self, vector_store):
        """Test upserting to update existing chunks."""
        # Initial upsert
        chunks_v1 = [
            {
                "id": "chunk_1",
                "content": "original content",
                "embedding": [0.1] * 1024,
                "metadata": {
                    "file_path": "test.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 10,
                    "tokens": 10,
                    "symbols": [],
                    "imports": [],
                },
            }
        ]

        await vector_store.upsert_chunks(chunks_v1)
        assert vector_store.collection.count() == 1

        # Update with new content
        chunks_v2 = [
            {
                "id": "chunk_1",
                "content": "updated content",
                "embedding": [0.2] * 1024,
                "metadata": {
                    "file_path": "test.py",
                    "language": "python",
                    "chunk_type": "function",
                    "start_line": 1,
                    "end_line": 10,
                    "tokens": 15,
                    "symbols": [],
                    "imports": [],
                },
            }
        ]

        await vector_store.upsert_chunks(chunks_v2)
        # Should still be 1 (updated, not added)
        assert vector_store.collection.count() == 1
