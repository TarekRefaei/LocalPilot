"""
Multi-level retriever for semantic code search.

Implements 4-level retrieval strategy:
1. Project Summary - High-level project overview
2. Symbol/Metadata Search - Exact matches on symbols, files, functions
3. Semantic Vector Search - Embedding-based similarity
4. Keyword/Lexical Search - BM25-style keyword matching

Results are fused and re-ranked with diversity penalty.
"""

import logging
from typing import Any

from .embedding_service import EmbeddingService
from .fusion import DiversityRanker, ResultFusion
from .vector_store import VectorStore

logger = logging.getLogger(__name__)


class MultiLevelRetriever:
    """Multi-level retrieval combining semantic, symbol, and keyword search."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        semantic_weight: float = 0.6,
        symbol_weight: float = 0.2,
        keyword_weight: float = 0.15,
        summary_weight: float = 0.05,
        diversity_weight: float = 0.3,
    ):
        """
        Initialize multi-level retriever.

        Args:
            vector_store: VectorStore instance for semantic search
            embedding_service: EmbeddingService for query embedding
            semantic_weight: Weight for semantic search results
            symbol_weight: Weight for symbol/metadata search results
            keyword_weight: Weight for keyword/lexical search results
            summary_weight: Weight for project summary results
            diversity_weight: Weight for diversity penalty in re-ranking
        """
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.fusion = ResultFusion(
            semantic_weight=semantic_weight,
            symbol_weight=symbol_weight,
            keyword_weight=keyword_weight,
            summary_weight=summary_weight,
        )
        self.ranker = DiversityRanker(diversity_weight=diversity_weight)

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        user_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Execute multi-level retrieval.

        Args:
            query: User query
            top_k: Number of results to return
            user_context: Optional user context (current_file, recent_files, etc.)

        Returns:
            List of top-K results with fused scores
        """
        logger.info(f"Retrieving for query: {query}")

        # Level 1: Project Summary (placeholder - would need project summary index)
        summary_results = await self._level1_project_summary(query)

        # Level 2: Symbol/Metadata Search
        symbol_results = await self._level2_symbol_search(query)

        # Level 3: Semantic Vector Search (PRIMARY)
        semantic_results = await self._level3_semantic_search(
            query, user_context, top_k=top_k * 2
        )

        # Level 4: Keyword/Lexical Search
        keyword_results = await self._level4_keyword_search(query, top_k=10)

        # Fuse results
        fused_results = self.fusion.fuse(
            semantic_results=semantic_results,
            symbol_results=symbol_results,
            keyword_results=keyword_results,
            summary_results=summary_results,
        )

        # Re-rank with diversity
        final_results = self.ranker.rerank(fused_results, top_k=top_k)

        logger.info(
            f"Retrieved {len(final_results)} results "
            f"(semantic={len(semantic_results)}, "
            f"symbol={len(symbol_results)}, "
            f"keyword={len(keyword_results)})"
        )

        return final_results

    async def _level1_project_summary(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        """
        Level 1: Project Summary Retrieval.

        Checks if query is about project-level concepts.
        Placeholder for future implementation with project summary index.

        Args:
            query: User query

        Returns:
            List of project summary results
        """
        # TODO: Implement project summary search
        # For now, return empty list
        return []

    async def _level2_symbol_search(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        """
        Level 2: Symbol/Metadata Search.

        Searches for exact matches on:
        - Function/class names
        - File paths
        - Module names

        Args:
            query: User query

        Returns:
            List of symbol search results
        """
        # Extract potential symbols from query
        # Simple heuristic: look for CamelCase or snake_case words
        symbols = self._extract_symbols(query)

        if not symbols:
            return []

        results = []

        # Search for each symbol
        for symbol in symbols:
            try:
                # Search by symbol in metadata
                symbol_results = await self.vector_store.search_by_metadata(
                    filters={"symbols": symbol},
                    limit=5,
                )
                results.extend(symbol_results)
            except Exception as e:
                logger.debug(f"Symbol search failed for '{symbol}': {e}")

        # Deduplicate by ID
        seen = set()
        deduped = []
        for result in results:
            if result["id"] not in seen:
                seen.add(result["id"])
                deduped.append(result)

        logger.debug(f"Symbol search found {len(deduped)} results")
        return deduped

    async def _level3_semantic_search(
        self,
        query: str,
        user_context: dict[str, Any] | None = None,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Level 3: Semantic Vector Search (PRIMARY).

        Embeds query and searches vector store for similar chunks.

        Args:
            query: User query
            user_context: Optional user context for boosting
            top_k: Number of results to return

        Returns:
            List of semantic search results
        """
        try:
            # Embed query
            query_embedding = await self.embedding_service.embed_query(query)

            # Search vector store
            results = await self.vector_store.search(
                query_embedding=query_embedding,
                top_k=top_k,
                min_score=0.3,  # Minimum similarity threshold
            )

            # Apply user context boosting if provided
            if user_context:
                results = self._apply_context_boost(results, user_context)

            logger.debug(f"Semantic search found {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []

    async def _level4_keyword_search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Level 4: Keyword/Lexical Search.

        Searches for exact keyword matches in chunk content.
        Placeholder for BM25-style implementation.

        Args:
            query: User query
            top_k: Number of results to return

        Returns:
            List of keyword search results
        """
        # TODO: Implement BM25 keyword search
        # For now, return empty list
        return []

    def _extract_symbols(self, query: str) -> list[str]:
        """
        Extract potential symbols from query.

        Looks for CamelCase or snake_case words.

        Args:
            query: User query

        Returns:
            List of potential symbols
        """
        symbols = []
        words = query.split()

        for word in words:
            # Check for CamelCase (e.g., MyClass, myFunction)
            if any(c.isupper() for c in word[1:]):
                symbols.append(word)
            # Check for snake_case with underscores
            elif "_" in word:
                symbols.append(word)

        return symbols[:5]  # Limit to 5 symbols

    def _apply_context_boost(
        self,
        results: list[dict[str, Any]],
        user_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Apply user context boosting to results.

        Boosts results from:
        - Currently open file
        - Recently edited files
        - Files in same directory

        Args:
            results: Search results
            user_context: User context dict

        Returns:
            Results with boosted scores
        """
        for result in results:
            boost = 1.0
            file_path = result.get("metadata", {}).get("file_path", "")

            # Boost if current file
            if "current_file" in user_context:
                if file_path == user_context["current_file"]:
                    boost *= 1.5
                    logger.debug(f"Current file boost: {file_path}")

            # Boost if recently edited
            if "recent_files" in user_context:
                if file_path in user_context["recent_files"]:
                    boost *= 1.3
                    logger.debug(f"Recent file boost: {file_path}")

            # Boost if same directory
            if "current_directory" in user_context:
                current_dir = user_context["current_directory"]
                if file_path.startswith(current_dir):
                    boost *= 1.2
                    logger.debug(f"Same directory boost: {file_path}")

            # Apply boost
            result["original_score"] = result.get("score", 0.0)
            result["score"] = result.get("score", 0.0) * boost
            result["context_boost"] = boost

        # Re-sort by boosted score
        results.sort(key=lambda x: x["score"], reverse=True)

        return results
