"""
Multi-level retriever for semantic code search.

Implements 4-level retrieval strategy:
1. Project Summary - High-level project overview
2. Symbol/Metadata Search - Exact matches on symbols, files, functions
3. Semantic Vector Search - Embedding-based similarity
4. Keyword/Lexical Search - BM25-style keyword matching

Results are fused and re-ranked with diversity penalty.
"""

import hashlib
import json
import logging
import re
import time
from typing import Any

from rank_bm25 import BM25Okapi

from . import retrieval_metrics
from .cache import QueryCache
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
        query_cache: QueryCache | None = None,
        enable_keyword_level: bool = True,
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
            enable_keyword_level: Flag to enable or disable keyword search level
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
        self.cache = query_cache or QueryCache(max_size=1000)
        self.enable_keyword_level = enable_keyword_level

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
        semantic_results = await self._level3_semantic_search(query, user_context, top_k=top_k * 2)

        # Level 4: Keyword/Lexical Search (ablatable)
        keyword_results: list[dict[str, Any]] = []
        l4_ms = 0.0
        if self.enable_keyword_level:
            l4_start = time.time()
            candidates = []
            seen_ids: set[str] = set()
            for r in semantic_results + symbol_results:
                if r["id"] not in seen_ids:
                    seen_ids.add(r["id"])
                    candidates.append(r)
            keyword_results = await self._level4_keyword_search(
                query, candidates=candidates, top_k=10
            )
            l4_ms = (time.time() - l4_start) * 1000.0

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

        try:
            cache_stats = self.cache.get_statistics()
            # Publish metrics for observability
            retrieval_metrics.update(
                l4_enabled=self.enable_keyword_level,
                l4_ms=l4_ms,
                cache_stats=cache_stats,
            )
            logger.debug(
                f"L4_enabled={self.enable_keyword_level} l4_ms={l4_ms:.1f} "
                f"cache_hit_rate={cache_stats.get('cache_hit_rate', 0.0):.2f} "
                f"cache_hits={cache_stats.get('cache_hits', 0)} "
                f"cache_misses={cache_stats.get('cache_misses', 0)}"
            )
        except Exception:
            pass

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
            cached_embedding = self.cache.get_embedding(query)
            if cached_embedding is not None:
                query_embedding = cached_embedding
            else:
                query_embedding = await self.embedding_service.embed_query(query)
                self.cache.set_embedding(query, query_embedding)

            cache_key = self._make_search_cache_key(query_embedding, None, top_k)
            cached_results = self.cache.get_search_results(cache_key)
            if cached_results is not None:
                results = cached_results
            else:
                results = await self.vector_store.search(
                    query_embedding=query_embedding,
                    top_k=top_k,
                    min_score=0.3,
                )
                self.cache.set_search_results(cache_key, results)

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
        candidates: list[dict[str, Any]] | None = None,
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
        if not candidates:
            return []

        docs = []
        id_order: list[str] = []
        by_id: dict[str, dict[str, Any]] = {}

        for r in candidates:
            doc_id = r["id"]
            if doc_id in by_id:
                continue
            text = r.get("content", "")
            docs.append(self._tokenize(text))
            id_order.append(doc_id)
            by_id[doc_id] = r

        if not docs:
            return []

        bm25 = BM25Okapi(docs)
        query_tokens = self._tokenize(query)
        scores_arr = bm25.get_scores(query_tokens)
        # Avoid boolean evaluation of numpy arrays
        scores_list = list(scores_arr)

        if len(scores_list) == 0:
            return []

        max_score = float(max(scores_list))
        if max_score <= 0.0:
            return []

        results: list[dict[str, Any]] = []
        for idx, s in enumerate(scores_list):
            norm = float(s) / float(max_score)
            base = by_id[id_order[idx]]
            results.append(
                {
                    "id": base["id"],
                    "content": base.get("content", ""),
                    "metadata": base.get("metadata", {}),
                    "score": round(norm, 4),
                }
            )

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def _tokenize(self, text: str) -> list[str]:
        tokens = re.findall(r"\b\w+\b", text.lower())
        return tokens

    def _make_search_cache_key(
        self,
        embedding: list[float],
        filters: dict[str, Any] | None,
        top_k: int,
    ) -> str:
        rounded = [round(x, 4) for x in embedding]
        payload = json.dumps({"e": rounded, "f": filters or {}, "k": top_k}, sort_keys=True)
        return hashlib.sha1(payload.encode("utf-8")).hexdigest()

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
