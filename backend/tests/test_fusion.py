"""
Unit tests for result fusion and diversity ranking.
"""

from app.services.rag.fusion import DiversityRanker, ResultFusion


class TestResultFusion:
    """Test result fusion from multiple levels."""

    def test_fusion_semantic_only(self):
        """Test fusion with only semantic results."""
        fusion = ResultFusion()

        semantic_results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "score": 0.9,
            },
            {
                "id": "doc2",
                "content": "content2",
                "metadata": {"file_path": "file2.py"},
                "score": 0.8,
            },
        ]

        fused = fusion.fuse(semantic_results=semantic_results)

        assert len(fused) == 2
        assert fused[0]["id"] == "doc1"
        assert fused[0]["fused_score"] > 0

    def test_fusion_multiple_levels(self):
        """Test fusion with results from multiple levels."""
        fusion = ResultFusion(
            semantic_weight=0.6,
            symbol_weight=0.2,
            keyword_weight=0.15,
            summary_weight=0.05,
        )

        semantic_results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "score": 0.9,
            },
        ]

        symbol_results = [
            {
                "id": "doc2",
                "content": "content2",
                "metadata": {"file_path": "file2.py"},
                "score": 0.8,
            },
        ]

        keyword_results = [
            {
                "id": "doc3",
                "content": "content3",
                "metadata": {"file_path": "file3.py"},
                "score": 0.7,
            },
        ]

        fused = fusion.fuse(
            semantic_results=semantic_results,
            symbol_results=symbol_results,
            keyword_results=keyword_results,
        )

        assert len(fused) == 3
        # Semantic should have highest fused score
        assert fused[0]["id"] == "doc1"

    def test_fusion_deduplication(self):
        """Test that fusion deduplicates results."""
        fusion = ResultFusion()

        semantic_results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "score": 0.9,
            },
        ]

        symbol_results = [
            {
                "id": "doc1",  # Same doc from different level
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "score": 0.8,
            },
        ]

        fused = fusion.fuse(
            semantic_results=semantic_results,
            symbol_results=symbol_results,
        )

        # Should have only 1 result (deduplicated)
        assert len(fused) == 1
        assert fused[0]["id"] == "doc1"
        # Fused score should combine both levels (0.6*0.9 + 0.2*0.8 = 0.7)
        assert abs(fused[0]["fused_score"] - 0.7) < 0.01

    def test_fusion_scoring(self):
        """Test that fusion scores are weighted correctly."""
        fusion = ResultFusion(
            semantic_weight=0.5,
            symbol_weight=0.5,
            keyword_weight=0.0,
            summary_weight=0.0,
        )

        semantic_results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "score": 1.0,
            },
        ]

        symbol_results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "score": 0.5,
            },
        ]

        fused = fusion.fuse(
            semantic_results=semantic_results,
            symbol_results=symbol_results,
        )

        # Fused score should be 0.5 * 1.0 + 0.5 * 0.5 = 0.75
        assert abs(fused[0]["fused_score"] - 0.75) < 0.01

    def test_fusion_empty_results(self):
        """Test fusion with empty results."""
        fusion = ResultFusion()

        fused = fusion.fuse(semantic_results=[])

        assert len(fused) == 0

    def test_fusion_preserves_metadata(self):
        """Test that fusion preserves metadata."""
        fusion = ResultFusion()

        semantic_results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py", "language": "python"},
                "score": 0.9,
            },
        ]

        fused = fusion.fuse(semantic_results=semantic_results)

        assert fused[0]["metadata"]["file_path"] == "file1.py"
        assert fused[0]["metadata"]["language"] == "python"


class TestDiversityRanker:
    """Test diversity-aware re-ranking."""

    def test_rerank_no_penalty(self):
        """Test re-ranking with no diversity penalty."""
        ranker = DiversityRanker(diversity_weight=0.0)

        results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "fused_score": 0.9,
            },
            {
                "id": "doc2",
                "content": "content2",
                "metadata": {"file_path": "file2.py"},
                "fused_score": 0.8,
            },
            {
                "id": "doc3",
                "content": "content3",
                "metadata": {"file_path": "file3.py"},
                "fused_score": 0.7,
            },
        ]

        reranked = ranker.rerank(results, top_k=3)

        # Should maintain original order
        assert reranked[0]["id"] == "doc1"
        assert reranked[1]["id"] == "doc2"
        assert reranked[2]["id"] == "doc3"

    def test_rerank_with_penalty(self):
        """Test re-ranking with diversity penalty."""
        ranker = DiversityRanker(diversity_weight=0.3)

        results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "fused_score": 0.9,
            },
            {
                "id": "doc2",
                "content": "content2",
                "metadata": {"file_path": "file1.py"},  # Same file
                "fused_score": 0.85,
            },
            {
                "id": "doc3",
                "content": "content3",
                "metadata": {"file_path": "file2.py"},
                "fused_score": 0.8,
            },
        ]

        reranked = ranker.rerank(results, top_k=2)

        # Should select doc1 and doc3 (different files)
        assert reranked[0]["id"] == "doc1"
        assert reranked[1]["id"] == "doc3"

    def test_rerank_top_k(self):
        """Test that re-ranking respects top_k."""
        ranker = DiversityRanker()

        results = [
            {
                "id": f"doc{i}",
                "content": f"content{i}",
                "metadata": {"file_path": f"file{i}.py"},
                "fused_score": 1.0 - (i * 0.1),
            }
            for i in range(10)
        ]

        reranked = ranker.rerank(results, top_k=5)

        assert len(reranked) == 5

    def test_rerank_small_result_set(self):
        """Test re-ranking with fewer results than top_k."""
        ranker = DiversityRanker()

        results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "fused_score": 0.9,
            },
            {
                "id": "doc2",
                "content": "content2",
                "metadata": {"file_path": "file2.py"},
                "fused_score": 0.8,
            },
        ]

        reranked = ranker.rerank(results, top_k=5)

        # Should return all results
        assert len(reranked) == 2

    def test_rerank_diversity_adjusted_score(self):
        """Test that diversity-adjusted scores are calculated."""
        ranker = DiversityRanker(diversity_weight=0.3)

        results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "fused_score": 0.9,
            },
            {
                "id": "doc2",
                "content": "content2",
                "metadata": {"file_path": "file2.py"},
                "fused_score": 0.8,
            },
            {
                "id": "doc3",
                "content": "content3",
                "metadata": {"file_path": "file3.py"},
                "fused_score": 0.7,
            },
        ]

        reranked = ranker.rerank(results, top_k=2)

        # All results should have diversity_adjusted_score
        for result in reranked:
            assert "diversity_adjusted_score" in result

    def test_rerank_multiple_files(self):
        """Test re-ranking promotes diversity across files."""
        ranker = DiversityRanker(diversity_weight=0.5)

        results = [
            {
                "id": "doc1",
                "content": "content1",
                "metadata": {"file_path": "file1.py"},
                "fused_score": 0.95,
            },
            {
                "id": "doc2",
                "content": "content2",
                "metadata": {"file_path": "file1.py"},
                "fused_score": 0.94,
            },
            {
                "id": "doc3",
                "content": "content3",
                "metadata": {"file_path": "file1.py"},
                "fused_score": 0.93,
            },
            {
                "id": "doc4",
                "content": "content4",
                "metadata": {"file_path": "file2.py"},
                "fused_score": 0.80,
            },
            {
                "id": "doc5",
                "content": "content5",
                "metadata": {"file_path": "file3.py"},
                "fused_score": 0.75,
            },
        ]

        reranked = ranker.rerank(results, top_k=3)

        # Should select from different files
        file_paths = [r["metadata"]["file_path"] for r in reranked]
        assert len(set(file_paths)) >= 2  # At least 2 different files
