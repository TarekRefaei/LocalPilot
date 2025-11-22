"""
Query and embedding cache with LRU eviction policy.

Caches:
- Query embeddings (for repeated queries)
- Vector search results (for repeated queries)
"""

import logging
from collections import OrderedDict
from typing import Any, Optional

logger = logging.getLogger(__name__)


class QueryCache:
    """
    LRU cache for query embeddings and search results.

    Prevents re-embedding identical queries and re-searching identical vectors.
    """

    def __init__(self, max_size: int = 1000):
        """
        Initialize query cache.

        Args:
            max_size: Maximum number of cached items
        """
        self.max_size = max_size
        self._embedding_cache: OrderedDict[str, list[float]] = OrderedDict()
        self._search_cache: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
        self._hits = 0
        self._misses = 0

        logger.info(f"QueryCache initialized (max_size={max_size})")

    def get_embedding(self, query: str) -> Optional[list[float]]:
        """
        Get cached embedding for query.

        Args:
            query: Query text

        Returns:
            Embedding vector if cached, None otherwise
        """
        if query in self._embedding_cache:
            # Move to end (most recently used)
            self._embedding_cache.move_to_end(query)
            self._hits += 1
            logger.debug(f"Embedding cache hit: {query[:50]}...")
            return self._embedding_cache[query]

        self._misses += 1
        return None

    def set_embedding(self, query: str, embedding: list[float]) -> None:
        """
        Cache embedding for query.

        Args:
            query: Query text
            embedding: Embedding vector
        """
        if query in self._embedding_cache:
            # Remove and re-add to move to end
            del self._embedding_cache[query]
        else:
            # Check if we need to evict
            if len(self._embedding_cache) >= self.max_size:
                # Remove least recently used (first item)
                removed_query, _ = self._embedding_cache.popitem(last=False)
                logger.debug(f"Evicted embedding cache entry: {removed_query[:50]}...")

        self._embedding_cache[query] = embedding

    def get_search_results(
        self, query_vector_id: str
    ) -> Optional[list[dict[str, Any]]]:
        """
        Get cached search results for query vector.

        Args:
            query_vector_id: Hash or ID of query vector

        Returns:
            Search results if cached, None otherwise
        """
        if query_vector_id in self._search_cache:
            # Move to end (most recently used)
            self._search_cache.move_to_end(query_vector_id)
            self._hits += 1
            logger.debug(f"Search cache hit: {query_vector_id}")
            return self._search_cache[query_vector_id]

        self._misses += 1
        return None

    def set_search_results(
        self, query_vector_id: str, results: list[dict[str, Any]]
    ) -> None:
        """
        Cache search results for query vector.

        Args:
            query_vector_id: Hash or ID of query vector
            results: Search results
        """
        if query_vector_id in self._search_cache:
            # Remove and re-add to move to end
            del self._search_cache[query_vector_id]
        else:
            # Check if we need to evict
            if len(self._search_cache) >= self.max_size:
                # Remove least recently used (first item)
                removed_id, _ = self._search_cache.popitem(last=False)
                logger.debug(f"Evicted search cache entry: {removed_id}")

        self._search_cache[query_vector_id] = results

    def clear(self) -> None:
        """Clear all caches."""
        self._embedding_cache.clear()
        self._search_cache.clear()
        logger.info("QueryCache cleared")

    def get_statistics(self) -> dict[str, Any]:
        """Get cache statistics."""
        total_requests = self._hits + self._misses
        hit_rate = (
            self._hits / total_requests if total_requests > 0 else 0.0
        )

        return {
            "embedding_cache_size": len(self._embedding_cache),
            "search_cache_size": len(self._search_cache),
            "total_cache_size": len(self._embedding_cache) + len(self._search_cache),
            "cache_hits": self._hits,
            "cache_misses": self._misses,
            "cache_hit_rate": hit_rate,
            "max_size": self.max_size,
        }

    def reset_statistics(self) -> None:
        """Reset statistics counters."""
        self._hits = 0
        self._misses = 0
