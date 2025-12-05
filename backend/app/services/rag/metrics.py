"""
Retrieval metrics for evaluating multi-level retrieval quality.

Provides:
- Precision@K (fraction of top-K results that are relevant)
- Recall@K (fraction of relevant results in top-K)
- Mean Reciprocal Rank (MRR) - position of first relevant result
- Normalized Discounted Cumulative Gain (NDCG) - ranking quality
- Mean Average Precision (MAP)
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RetrievalMetrics:
    """Metrics for a single query evaluation."""

    query: str
    precision_at_5: float
    precision_at_10: float
    recall_at_5: float
    recall_at_10: float
    mrr: float  # Mean Reciprocal Rank
    ndcg_at_5: float
    ndcg_at_10: float
    map_at_5: float
    map_at_10: float
    num_relevant: int
    num_retrieved: int

    def __str__(self) -> str:
        return (
            f"P@5={self.precision_at_5:.3f} R@5={self.recall_at_5:.3f} "
            f"MRR={self.mrr:.3f} NDCG@5={self.ndcg_at_5:.3f}"
        )


class MetricsCalculator:
    """Calculate retrieval metrics for evaluation."""

    @staticmethod
    def calculate_precision_at_k(
        retrieved_ids: list[str],
        relevant_ids: set[str],
        k: int = 5,
    ) -> float:
        """
        Calculate Precision@K.

        Precision@K = (# relevant in top-K) / K

        Args:
            retrieved_ids: List of retrieved document IDs (ranked)
            relevant_ids: Set of relevant document IDs
            k: Number of top results to consider

        Returns:
            Precision score (0-1)
        """
        if k <= 0:
            return 0.0

        top_k = retrieved_ids[:k]
        num_relevant = sum(1 for doc_id in top_k if doc_id in relevant_ids)

        return num_relevant / k

    @staticmethod
    def calculate_recall_at_k(
        retrieved_ids: list[str],
        relevant_ids: set[str],
        k: int = 5,
    ) -> float:
        """
        Calculate Recall@K.

        Recall@K = (# relevant in top-K) / (# total relevant)

        Args:
            retrieved_ids: List of retrieved document IDs (ranked)
            relevant_ids: Set of relevant document IDs
            k: Number of top results to consider

        Returns:
            Recall score (0-1)
        """
        if len(relevant_ids) == 0:
            return 0.0

        top_k = retrieved_ids[:k]
        num_relevant = sum(1 for doc_id in top_k if doc_id in relevant_ids)

        return num_relevant / len(relevant_ids)

    @staticmethod
    def calculate_mrr(
        retrieved_ids: list[str],
        relevant_ids: set[str],
    ) -> float:
        """
        Calculate Mean Reciprocal Rank.

        MRR = 1 / (position of first relevant result)

        Args:
            retrieved_ids: List of retrieved document IDs (ranked)
            relevant_ids: Set of relevant document IDs

        Returns:
            MRR score (0-1)
        """
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_ids:
                return 1.0 / (i + 1)

        return 0.0

    @staticmethod
    def calculate_ndcg_at_k(
        retrieved_ids: list[str],
        relevant_ids: set[str],
        k: int = 5,
        relevance_scores: dict[str, float] | None = None,
    ) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain@K.

        NDCG@K = DCG@K / IDCG@K

        Where:
        - DCG = sum of (relevance / log2(position + 1))
        - IDCG = ideal DCG (all relevant docs at top)

        Args:
            retrieved_ids: List of retrieved document IDs (ranked)
            relevant_ids: Set of relevant document IDs
            k: Number of top results to consider
            relevance_scores: Optional dict of relevance scores (default: binary)

        Returns:
            NDCG score (0-1)
        """
        if len(relevant_ids) == 0:
            return 0.0

        # Calculate DCG
        dcg = 0.0
        for i, doc_id in enumerate(retrieved_ids[:k]):
            if doc_id in relevant_ids:
                # Binary relevance: 1 if relevant, 0 otherwise
                if relevance_scores:
                    relevance = relevance_scores.get(doc_id, 0.0)
                else:
                    relevance = 1.0

                dcg += relevance / (i + 1)  # log2(i + 2) for standard NDCG

        # Calculate IDCG (ideal ranking: all relevant at top)
        idcg = 0.0
        for i in range(min(k, len(relevant_ids))):
            idcg += 1.0 / (i + 1)

        if idcg == 0.0:
            return 0.0

        return dcg / idcg

    @staticmethod
    def calculate_map_at_k(
        retrieved_ids: list[str],
        relevant_ids: set[str],
        k: int = 5,
    ) -> float:
        """
        Calculate Mean Average Precision@K.

        MAP@K = (1/min(K, |relevant|)) * sum of (P@i for each relevant at position i)

        Args:
            retrieved_ids: List of retrieved document IDs (ranked)
            relevant_ids: Set of relevant document IDs
            k: Number of top results to consider

        Returns:
            MAP score (0-1)
        """
        if len(relevant_ids) == 0:
            return 0.0

        score = 0.0
        num_relevant_found = 0

        for i, doc_id in enumerate(retrieved_ids[:k]):
            if doc_id in relevant_ids:
                num_relevant_found += 1
                precision_at_i = num_relevant_found / (i + 1)
                score += precision_at_i

        return score / min(k, len(relevant_ids))

    @staticmethod
    def evaluate_query(
        query: str,
        retrieved_ids: list[str],
        relevant_ids: set[str],
    ) -> RetrievalMetrics:
        """
        Evaluate retrieval results for a single query.

        Args:
            query: Query text
            retrieved_ids: List of retrieved document IDs (ranked)
            relevant_ids: Set of relevant document IDs

        Returns:
            RetrievalMetrics object with all metrics
        """
        return RetrievalMetrics(
            query=query,
            precision_at_5=MetricsCalculator.calculate_precision_at_k(
                retrieved_ids, relevant_ids, k=5
            ),
            precision_at_10=MetricsCalculator.calculate_precision_at_k(
                retrieved_ids, relevant_ids, k=10
            ),
            recall_at_5=MetricsCalculator.calculate_recall_at_k(
                retrieved_ids, relevant_ids, k=5
            ),
            recall_at_10=MetricsCalculator.calculate_recall_at_k(
                retrieved_ids, relevant_ids, k=10
            ),
            mrr=MetricsCalculator.calculate_mrr(retrieved_ids, relevant_ids),
            ndcg_at_5=MetricsCalculator.calculate_ndcg_at_k(
                retrieved_ids, relevant_ids, k=5
            ),
            ndcg_at_10=MetricsCalculator.calculate_ndcg_at_k(
                retrieved_ids, relevant_ids, k=10
            ),
            map_at_5=MetricsCalculator.calculate_map_at_k(
                retrieved_ids, relevant_ids, k=5
            ),
            map_at_10=MetricsCalculator.calculate_map_at_k(
                retrieved_ids, relevant_ids, k=10
            ),
            num_relevant=len(relevant_ids),
            num_retrieved=len(retrieved_ids),
        )


class EvaluationHarness:
    """Harness for evaluating retrieval quality across multiple queries."""

    def __init__(self):
        """Initialize evaluation harness."""
        self.results: list[RetrievalMetrics] = []

    def add_result(self, metrics: RetrievalMetrics) -> None:
        """Add evaluation result."""
        self.results.append(metrics)

    def aggregate_metrics(self) -> dict[str, float]:
        """
        Aggregate metrics across all queries.

        Returns:
            Dictionary with average metrics
        """
        if not self.results:
            return {}

        num_queries = len(self.results)

        return {
            "num_queries": num_queries,
            "avg_precision_at_5": sum(r.precision_at_5 for r in self.results)
            / num_queries,
            "avg_precision_at_10": sum(r.precision_at_10 for r in self.results)
            / num_queries,
            "avg_recall_at_5": sum(r.recall_at_5 for r in self.results) / num_queries,
            "avg_recall_at_10": sum(r.recall_at_10 for r in self.results) / num_queries,
            "avg_mrr": sum(r.mrr for r in self.results) / num_queries,
            "avg_ndcg_at_5": sum(r.ndcg_at_5 for r in self.results) / num_queries,
            "avg_ndcg_at_10": sum(r.ndcg_at_10 for r in self.results) / num_queries,
            "avg_map_at_5": sum(r.map_at_5 for r in self.results) / num_queries,
            "avg_map_at_10": sum(r.map_at_10 for r in self.results) / num_queries,
        }

    def log_results(self) -> None:
        """Log evaluation results."""
        if not self.results:
            logger.warning("No results to log")
            return

        agg = self.aggregate_metrics()
        logger.info("=" * 60)
        logger.info("RETRIEVAL EVALUATION RESULTS")
        logger.info("=" * 60)
        logger.info(f"Queries evaluated: {agg['num_queries']}")
        logger.info(f"Avg Precision@5: {agg['avg_precision_at_5']:.3f}")
        logger.info(f"Avg Precision@10: {agg['avg_precision_at_10']:.3f}")
        logger.info(f"Avg Recall@5: {agg['avg_recall_at_5']:.3f}")
        logger.info(f"Avg Recall@10: {agg['avg_recall_at_10']:.3f}")
        logger.info(f"Avg MRR: {agg['avg_mrr']:.3f}")
        logger.info(f"Avg NDCG@5: {agg['avg_ndcg_at_5']:.3f}")
        logger.info(f"Avg NDCG@10: {agg['avg_ndcg_at_10']:.3f}")
        logger.info(f"Avg MAP@5: {agg['avg_map_at_5']:.3f}")
        logger.info(f"Avg MAP@10: {agg['avg_map_at_10']:.3f}")
        logger.info("=" * 60)

        # Log individual results
        logger.info("Individual query results:")
        for result in self.results:
            logger.info(f"  {result.query}: {result}")
