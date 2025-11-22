"""
Result fusion and re-ranking for multi-level retrieval.

Provides:
- Fusion of results from multiple retrieval levels
- Diversity-aware re-ranking
- Score normalization and weighting
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ResultFusion:
    """Fuse results from multiple retrieval levels."""

    def __init__(
        self,
        semantic_weight: float = 0.6,
        symbol_weight: float = 0.2,
        keyword_weight: float = 0.15,
        summary_weight: float = 0.05,
    ):
        """
        Initialize result fusion.

        Args:
            semantic_weight: Weight for semantic search results
            symbol_weight: Weight for symbol/metadata search results
            keyword_weight: Weight for keyword/lexical search results
            summary_weight: Weight for project summary results
        """
        total = semantic_weight + symbol_weight + keyword_weight + summary_weight
        self.semantic_weight = semantic_weight / total
        self.symbol_weight = symbol_weight / total
        self.keyword_weight = keyword_weight / total
        self.summary_weight = summary_weight / total

        logger.debug(
            f"ResultFusion weights: semantic={self.semantic_weight:.2f}, "
            f"symbol={self.symbol_weight:.2f}, keyword={self.keyword_weight:.2f}, "
            f"summary={self.summary_weight:.2f}"
        )

    def fuse(
        self,
        semantic_results: list[dict[str, Any]],
        symbol_results: list[dict[str, Any]] | None = None,
        keyword_results: list[dict[str, Any]] | None = None,
        summary_results: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fuse results from multiple levels.

        Args:
            semantic_results: Results from semantic search
            symbol_results: Results from symbol/metadata search
            keyword_results: Results from keyword/lexical search
            summary_results: Results from project summary

        Returns:
            Fused and ranked results
        """
        # Initialize score map
        score_map: dict[str, dict[str, Any]] = {}

        # Add semantic results
        for result in semantic_results:
            doc_id = result["id"]
            score = result.get("score", 0.0)
            if doc_id not in score_map:
                score_map[doc_id] = {
                    "id": doc_id,
                    "content": result.get("content", ""),
                    "metadata": result.get("metadata", {}),
                    "scores": {},
                    "fused_score": 0.0,
                }
            score_map[doc_id]["scores"]["semantic"] = score

        # Add symbol results
        if symbol_results:
            for result in symbol_results:
                doc_id = result["id"]
                score = result.get("score", 0.0)
                if doc_id not in score_map:
                    score_map[doc_id] = {
                        "id": doc_id,
                        "content": result.get("content", ""),
                        "metadata": result.get("metadata", {}),
                        "scores": {},
                        "fused_score": 0.0,
                    }
                score_map[doc_id]["scores"]["symbol"] = score

        # Add keyword results
        if keyword_results:
            for result in keyword_results:
                doc_id = result["id"]
                score = result.get("score", 0.0)
                if doc_id not in score_map:
                    score_map[doc_id] = {
                        "id": doc_id,
                        "content": result.get("content", ""),
                        "metadata": result.get("metadata", {}),
                        "scores": {},
                        "fused_score": 0.0,
                    }
                score_map[doc_id]["scores"]["keyword"] = score

        # Add summary results
        if summary_results:
            for result in summary_results:
                doc_id = result["id"]
                score = result.get("score", 0.0)
                if doc_id not in score_map:
                    score_map[doc_id] = {
                        "id": doc_id,
                        "content": result.get("content", ""),
                        "metadata": result.get("metadata", {}),
                        "scores": {},
                        "fused_score": 0.0,
                    }
                score_map[doc_id]["scores"]["summary"] = score

        # Calculate fused scores
        for doc_id, result in score_map.items():
            scores = result["scores"]
            fused_score = (
                scores.get("semantic", 0.0) * self.semantic_weight
                + scores.get("symbol", 0.0) * self.symbol_weight
                + scores.get("keyword", 0.0) * self.keyword_weight
                + scores.get("summary", 0.0) * self.summary_weight
            )
            result["fused_score"] = fused_score

        # Sort by fused score
        fused_results = sorted(
            score_map.values(),
            key=lambda x: x["fused_score"],
            reverse=True,
        )

        logger.debug(f"Fused {len(fused_results)} results from multiple levels")

        return fused_results


class DiversityRanker:
    """Re-rank results to promote diversity across files."""

    def __init__(self, diversity_weight: float = 0.3):
        """
        Initialize diversity ranker.

        Args:
            diversity_weight: Weight for diversity penalty (0-1)
        """
        self.diversity_weight = diversity_weight

    def rerank(
        self,
        results: list[dict[str, Any]],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Re-rank results with diversity penalty.

        Penalizes results from files already selected to promote diversity.

        Args:
            results: Ranked results from fusion
            top_k: Number of results to return

        Returns:
            Re-ranked results with diversity penalty applied
        """
        if len(results) <= top_k:
            return results

        selected = []
        remaining = list(results)
        file_counts: dict[str, int] = {}

        while len(selected) < top_k and remaining:
            # Score remaining results with diversity penalty
            scored = []
            for result in remaining:
                file_path = result.get("metadata", {}).get("file_path", "unknown")
                file_count = file_counts.get(file_path, 0)

                # Apply diversity penalty
                diversity_penalty = file_count * self.diversity_weight
                adjusted_score = result.get("fused_score", 0.0) - diversity_penalty

                scored.append((adjusted_score, result))

            # Select best
            scored.sort(key=lambda x: x[0], reverse=True)
            best_score, best_result = scored[0]

            # Add to selected
            best_result["diversity_adjusted_score"] = best_score
            selected.append(best_result)
            remaining.remove(best_result)

            # Update file count
            file_path = best_result.get("metadata", {}).get("file_path", "unknown")
            file_counts[file_path] = file_counts.get(file_path, 0) + 1

        logger.debug(
            f"Re-ranked {len(selected)} results with diversity penalty "
            f"(weight={self.diversity_weight})"
        )

        return selected
