from app.services.rag.metrics import (
    EvaluationHarness,
    MetricsCalculator,
    RetrievalMetrics,
)


def test_precision_and_recall_edge_cases():
    # Precision with k=0 -> 0.0
    assert MetricsCalculator.calculate_precision_at_k(["a", "b"], {"a"}, k=0) == 0.0

    # Recall with no relevant -> 0.0
    assert MetricsCalculator.calculate_recall_at_k(["a", "b"], set(), k=5) == 0.0


def test_mrr_and_map_edge_cases():
    # MRR when no relevant -> 0.0
    assert MetricsCalculator.calculate_mrr(["a", "b", "c"], {"x", "y"}) == 0.0

    # MAP when no relevant -> 0.0
    assert MetricsCalculator.calculate_map_at_k(["a", "b", "c"], set(), k=5) == 0.0

    # MAP with some relevant -> >0
    m = MetricsCalculator.calculate_map_at_k(["a", "b", "c"], {"b"}, k=5)
    assert 0.0 < m <= 1.0


def test_ndcg_edge_cases_and_perfect_ranking():
    # NDCG when no relevant -> 0.0
    assert MetricsCalculator.calculate_ndcg_at_k(["a", "b"], set(), k=5) == 0.0

    # Perfect ranking yields NDCG of 1.0 regardless of discount base used
    retrieved = ["r1", "r2", "r3", "x", "y"]
    relevant = {"r1", "r2", "r3"}
    ndcg = MetricsCalculator.calculate_ndcg_at_k(retrieved, relevant, k=5)
    assert 0.99 <= ndcg <= 1.0


def test_evaluation_harness_and_metrics_object():
    metrics = MetricsCalculator.evaluate_query(
        query="q1",
        retrieved_ids=["a", "b", "c"],
        relevant_ids={"b"},
    )
    # Basic sanity checks
    assert isinstance(metrics, RetrievalMetrics)
    assert metrics.query == "q1"
    assert 0.0 <= metrics.precision_at_5 <= 1.0
    assert 0.0 <= metrics.recall_at_5 <= 1.0

    # Harness aggregation
    h = EvaluationHarness()
    h.add_result(metrics)
    agg = h.aggregate_metrics()
    assert agg["num_queries"] == 1
    assert "avg_mrr" in agg
