"""
Unit tests for QueryCache.

Tests:
- Embedding cache get/set
- Search result cache get/set
- LRU eviction
- Statistics tracking
- Cache clearing
"""

import pytest

from app.services.rag.cache import QueryCache


@pytest.fixture
def query_cache():
    """Create QueryCache instance for testing."""
    return QueryCache(max_size=3)


class TestQueryCacheBasics:
    """Test basic cache functionality."""

    def test_initialization(self, query_cache):
        """Test cache initialization."""
        assert query_cache.max_size == 3
        assert len(query_cache._embedding_cache) == 0
        assert len(query_cache._search_cache) == 0

    def test_embedding_cache_set_get(self, query_cache):
        """Test setting and getting embedding."""
        embedding = [0.1, 0.2, 0.3]
        query_cache.set_embedding("test query", embedding)

        result = query_cache.get_embedding("test query")

        assert result == embedding

    def test_embedding_cache_miss(self, query_cache):
        """Test cache miss for embedding."""
        result = query_cache.get_embedding("nonexistent")

        assert result is None

    def test_search_cache_set_get(self, query_cache):
        """Test setting and getting search results."""
        results = [{"id": "1", "score": 0.9}]
        query_cache.set_search_results("query_vector_1", results)

        cached = query_cache.get_search_results("query_vector_1")

        assert cached == results

    def test_search_cache_miss(self, query_cache):
        """Test cache miss for search results."""
        result = query_cache.get_search_results("nonexistent")

        assert result is None

    def test_lru_eviction_embeddings(self, query_cache):
        """Test LRU eviction for embeddings."""
        # Fill cache to max_size
        for i in range(3):
            query_cache.set_embedding(f"query_{i}", [0.1 * i])

        assert len(query_cache._embedding_cache) == 3

        # Add one more, should evict oldest
        query_cache.set_embedding("query_3", [0.3])

        assert len(query_cache._embedding_cache) == 3
        # query_0 should be evicted
        assert query_cache.get_embedding("query_0") is None
        # query_3 should be present
        assert query_cache.get_embedding("query_3") is not None

    def test_lru_eviction_search(self, query_cache):
        """Test LRU eviction for search results."""
        # Fill cache to max_size
        for i in range(3):
            query_cache.set_search_results(f"vector_{i}", [{"id": str(i)}])

        assert len(query_cache._search_cache) == 3

        # Add one more, should evict oldest
        query_cache.set_search_results("vector_3", [{"id": "3"}])

        assert len(query_cache._search_cache) == 3
        # vector_0 should be evicted
        assert query_cache.get_search_results("vector_0") is None
        # vector_3 should be present
        assert query_cache.get_search_results("vector_3") is not None

    def test_lru_move_to_end_on_access(self, query_cache):
        """Test that accessing item moves it to end (most recently used)."""
        # Fill cache
        for i in range(3):
            query_cache.set_embedding(f"query_{i}", [0.1 * i])

        # Access query_0 (should move to end)
        query_cache.get_embedding("query_0")

        # Add new item, should evict query_1 (now oldest)
        query_cache.set_embedding("query_3", [0.3])

        assert query_cache.get_embedding("query_0") is not None
        assert query_cache.get_embedding("query_1") is None
        assert query_cache.get_embedding("query_3") is not None

    def test_cache_hit_tracking(self, query_cache):
        """Test cache hit statistics."""
        query_cache.set_embedding("query_1", [0.1])

        # Hit
        query_cache.get_embedding("query_1")
        # Miss
        query_cache.get_embedding("nonexistent")

        stats = query_cache.get_statistics()

        assert stats["cache_hits"] == 1
        assert stats["cache_misses"] == 1
        assert stats["cache_hit_rate"] == 0.5

    def test_cache_statistics(self, query_cache):
        """Test cache statistics."""
        query_cache.set_embedding("query_1", [0.1])
        query_cache.set_search_results("vector_1", [{"id": "1"}])

        stats = query_cache.get_statistics()

        assert stats["embedding_cache_size"] == 1
        assert stats["search_cache_size"] == 1
        assert stats["total_cache_size"] == 2
        assert stats["max_size"] == 3

    def test_clear_cache(self, query_cache):
        """Test clearing cache."""
        query_cache.set_embedding("query_1", [0.1])
        query_cache.set_search_results("vector_1", [{"id": "1"}])

        assert len(query_cache._embedding_cache) == 1
        assert len(query_cache._search_cache) == 1

        query_cache.clear()

        assert len(query_cache._embedding_cache) == 0
        assert len(query_cache._search_cache) == 0

    def test_statistics_reset(self, query_cache):
        """Test resetting statistics."""
        query_cache.set_embedding("query_1", [0.1])
        query_cache.get_embedding("query_1")  # Hit
        query_cache.get_embedding("nonexistent")  # Miss

        stats_before = query_cache.get_statistics()
        assert stats_before["cache_hits"] == 1

        query_cache.reset_statistics()

        stats_after = query_cache.get_statistics()
        assert stats_after["cache_hits"] == 0
        assert stats_after["cache_misses"] == 0


class TestQueryCacheAdvanced:
    """Advanced cache tests."""

    def test_multiple_embeddings(self, query_cache):
        """Test caching multiple different embeddings."""
        embeddings = {
            "query_1": [0.1, 0.2, 0.3],
            "query_2": [0.4, 0.5, 0.6],
            "query_3": [0.7, 0.8, 0.9],
        }

        for query, embedding in embeddings.items():
            query_cache.set_embedding(query, embedding)

        for query, embedding in embeddings.items():
            assert query_cache.get_embedding(query) == embedding

    def test_multiple_search_results(self, query_cache):
        """Test caching multiple different search results."""
        results = {
            "vector_1": [{"id": "1", "score": 0.9}],
            "vector_2": [{"id": "2", "score": 0.8}, {"id": "3", "score": 0.7}],
            "vector_3": [{"id": "4", "score": 0.95}],
        }

        for vector_id, result in results.items():
            query_cache.set_search_results(vector_id, result)

        for vector_id, result in results.items():
            assert query_cache.get_search_results(vector_id) == result

    def test_update_existing_embedding(self, query_cache):
        """Test updating existing embedding."""
        query_cache.set_embedding("query_1", [0.1])
        result1 = query_cache.get_embedding("query_1")
        assert result1 == [0.1]

        # Update
        query_cache.set_embedding("query_1", [0.2])
        result2 = query_cache.get_embedding("query_1")
        assert result2 == [0.2]

        # Should still be 1 item in cache
        assert len(query_cache._embedding_cache) == 1

    def test_update_existing_search_results(self, query_cache):
        """Test updating existing search results."""
        query_cache.set_search_results("vector_1", [{"id": "1"}])
        result1 = query_cache.get_search_results("vector_1")
        assert result1 == [{"id": "1"}]

        # Update
        query_cache.set_search_results("vector_1", [{"id": "2"}])
        result2 = query_cache.get_search_results("vector_1")
        assert result2 == [{"id": "2"}]

        # Should still be 1 item in cache
        assert len(query_cache._search_cache) == 1

    def test_hit_rate_calculation(self, query_cache):
        """Test hit rate calculation."""
        query_cache.set_embedding("query_1", [0.1])

        # 3 hits
        for _ in range(3):
            query_cache.get_embedding("query_1")

        # 2 misses
        for _ in range(2):
            query_cache.get_embedding("nonexistent")

        stats = query_cache.get_statistics()

        # 3 hits / (3 hits + 2 misses) = 0.6
        assert stats["cache_hit_rate"] == 0.6

    def test_zero_hit_rate(self, query_cache):
        """Test hit rate when no requests."""
        stats = query_cache.get_statistics()
        assert stats["cache_hit_rate"] == 0.0

    def test_perfect_hit_rate(self, query_cache):
        """Test hit rate when all hits."""
        query_cache.set_embedding("query_1", [0.1])

        for _ in range(5):
            query_cache.get_embedding("query_1")

        stats = query_cache.get_statistics()
        assert stats["cache_hit_rate"] == 1.0


class TestQueryCacheSeparation:
    """Test separation between embedding and search caches."""

    def test_caches_are_separate(self, query_cache):
        """Test that embedding and search caches are separate."""
        query_cache.set_embedding("query_1", [0.1])
        query_cache.set_search_results("query_1", [{"id": "1"}])

        # Both should be retrievable
        embedding = query_cache.get_embedding("query_1")
        search = query_cache.get_search_results("query_1")

        assert embedding == [0.1]
        assert search == [{"id": "1"}]

    def test_separate_max_sizes(self, query_cache):
        """Test that each cache respects max_size independently."""
        # Fill embedding cache
        for i in range(3):
            query_cache.set_embedding(f"query_{i}", [0.1 * i])

        # Fill search cache
        for i in range(3):
            query_cache.set_search_results(f"vector_{i}", [{"id": str(i)}])

        assert len(query_cache._embedding_cache) == 3
        assert len(query_cache._search_cache) == 3

        # Add to embedding cache, should evict from embedding cache only
        query_cache.set_embedding("query_3", [0.3])

        assert len(query_cache._embedding_cache) == 3
        assert len(query_cache._search_cache) == 3
        assert query_cache.get_embedding("query_0") is None
        assert query_cache.get_search_results("vector_0") is not None
