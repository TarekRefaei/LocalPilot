"""
Integration tests for the /retrieve endpoint.
Uses mocks for retriever to avoid hitting Chroma or Ollama.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.retrieve import RetrieveRequest, RetrieveResponse


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_retriever():
    """Mock retriever with canned results."""
    mock = AsyncMock()
    mock.retrieve = AsyncMock(
        return_value=[
            {
                "id": "chunk_1",
                "file_path": "src/auth.py",
                "chunk_index": 0,
                "content": "def authenticate(user, password):\n    return verify_password(user, password)",
                "start_line": 10,
                "end_line": 12,
                "symbols": ["authenticate", "verify_password"],
                "score": 0.95,
                "diversity_adjusted_score": 0.92,
                "scores": {
                    "semantic_score": 0.95,
                    "symbol_score": 0.8,
                    "keyword_score": 0.7,
                    "summary_score": 0.0,
                    "fused_score": 0.85,
                },
            },
            {
                "id": "chunk_2",
                "file_path": "src/utils.py",
                "chunk_index": 5,
                "content": "def verify_password(user, pwd):\n    return hash(pwd) == user.password_hash",
                "start_line": 45,
                "end_line": 47,
                "symbols": ["verify_password"],
                "score": 0.88,
                "diversity_adjusted_score": 0.85,
                "scores": {
                    "semantic_score": 0.88,
                    "symbol_score": 0.9,
                    "keyword_score": 0.6,
                    "summary_score": 0.0,
                    "fused_score": 0.80,
                },
            },
        ]
    )
    return mock


def test_retrieve_endpoint_shape(client, mock_retriever):
    """Test that /retrieve returns correct response shape."""
    with patch("app.api.retrieve.get_retriever", return_value=mock_retriever):
        response = client.post(
            "/retrieve",
            json={
                "query": "authentication flow",
                "top_k": 5,
                "debug": True,
            },
        )

    assert response.status_code == 200
    data = response.json()

    # Check response shape
    assert "results" in data
    assert "total_count" in data
    assert "query" in data
    assert "top_k" in data
    assert "debug" in data

    # Check echoed parameters
    assert data["query"] == "authentication flow"
    assert data["top_k"] == 5
    assert data["debug"] is True
    assert data["total_count"] == 2

    # Check result shape
    assert len(data["results"]) == 2
    result = data["results"][0]
    assert "id" in result
    assert "file_path" in result
    assert "chunk_index" in result
    assert "content" in result
    assert "start_line" in result
    assert "end_line" in result
    assert "symbols" in result
    assert "score" in result
    assert "diversity_adjusted_score" in result
    assert "scores" in result

    # Check score breakdown shape
    scores = result["scores"]
    assert "semantic_score" in scores
    assert "symbol_score" in scores
    assert "keyword_score" in scores
    assert "summary_score" in scores
    assert "fused_score" in scores


def test_retrieve_debug_true_includes_scores(client, mock_retriever):
    """Test that debug=true includes scores and diversity_adjusted_score."""
    with patch("app.api.retrieve.get_retriever", return_value=mock_retriever):
        response = client.post(
            "/retrieve",
            json={
                "query": "authentication",
                "top_k": 5,
                "debug": True,
            },
        )

    assert response.status_code == 200
    data = response.json()

    # Scores should be present when debug=true
    for result in data["results"]:
        assert result["score"] is not None
        assert result["diversity_adjusted_score"] is not None
        assert result["scores"] is not None


def test_retrieve_debug_false_omits_scores(client, mock_retriever):
    """Test that debug=false omits scores and diversity_adjusted_score."""
    with patch("app.api.retrieve.get_retriever", return_value=mock_retriever):
        response = client.post(
            "/retrieve",
            json={
                "query": "authentication",
                "top_k": 5,
                "debug": False,
            },
        )

    assert response.status_code == 200
    data = response.json()

    # Scores should be omitted when debug=false
    for result in data["results"]:
        assert result["score"] is None
        assert result["diversity_adjusted_score"] is None
        assert result["scores"] is None


def test_retrieve_empty_query_returns_400(client):
    """Test that empty query returns 400."""
    response = client.post(
        "/retrieve",
        json={
            "query": "   ",  # Whitespace only
            "top_k": 5,
            "debug": False,
        },
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_retrieve_missing_query_returns_422(client):
    """Test that missing query returns 422 (validation error)."""
    response = client.post(
        "/retrieve",
        json={
            "top_k": 5,
            "debug": False,
        },
    )

    assert response.status_code == 422


def test_retrieve_top_k_validation(client):
    """Test that top_k is validated (1-50)."""
    # top_k too low
    response = client.post(
        "/retrieve",
        json={
            "query": "test",
            "top_k": 0,
            "debug": False,
        },
    )
    assert response.status_code == 422

    # top_k too high
    response = client.post(
        "/retrieve",
        json={
            "query": "test",
            "top_k": 51,
            "debug": False,
        },
    )
    assert response.status_code == 422


def test_retrieve_with_user_context(client, mock_retriever):
    """Test that user_context is passed to retriever."""
    with patch("app.api.retrieve.get_retriever", return_value=mock_retriever):
        response = client.post(
            "/retrieve",
            json={
                "query": "authentication",
                "top_k": 5,
                "debug": False,
                "user_context": {
                    "current_file": "src/auth.py",
                    "recent_files": ["src/utils.py", "src/models.py"],
                    "selected_text": "authenticate",
                },
            },
        )

    assert response.status_code == 200
    # Verify retriever was called with user_context
    mock_retriever.retrieve.assert_called_once()
    call_kwargs = mock_retriever.retrieve.call_args[1]
    assert call_kwargs["user_context"] is not None
    assert call_kwargs["user_context"]["current_file"] == "src/auth.py"


def test_retrieve_default_top_k(client, mock_retriever):
    """Test that default top_k is 5."""
    with patch("app.api.retrieve.get_retriever", return_value=mock_retriever):
        response = client.post(
            "/retrieve",
            json={
                "query": "authentication",
                "debug": False,
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["top_k"] == 5


def test_retrieve_default_debug_false(client, mock_retriever):
    """Test that default debug is false."""
    with patch("app.api.retrieve.get_retriever", return_value=mock_retriever):
        response = client.post(
            "/retrieve",
            json={
                "query": "authentication",
                "top_k": 5,
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["debug"] is False
    # Scores should be omitted
    for result in data["results"]:
        assert result["score"] is None


def test_retrieve_query_stripping(client, mock_retriever):
    """Test that query is stripped of whitespace."""
    with patch("app.api.retrieve.get_retriever", return_value=mock_retriever):
        response = client.post(
            "/retrieve",
            json={
                "query": "  authentication flow  ",
                "top_k": 5,
                "debug": False,
            },
        )

    assert response.status_code == 200
    data = response.json()
    # Query should be stripped in response
    assert data["query"] == "authentication flow"
    # Verify retriever was called with stripped query
    mock_retriever.retrieve.assert_called_once()
    call_kwargs = mock_retriever.retrieve.call_args[1]
    assert call_kwargs["query"] == "authentication flow"


def test_retrieve_response_model_validation():
    """Test that RetrieveResponse validates correctly."""
    # Valid response
    response = RetrieveResponse(
        results=[],
        total_count=0,
        query="test",
        top_k=5,
        debug=False,
    )
    assert response.query == "test"
    assert response.total_count == 0


def test_retrieve_request_model_validation():
    """Test that RetrieveRequest validates correctly."""
    # Valid request
    request = RetrieveRequest(
        query="test",
        top_k=5,
        debug=False,
    )
    assert request.query == "test"
    assert request.top_k == 5
    assert request.debug is False

    # Invalid: empty query
    with pytest.raises(ValueError):
        RetrieveRequest(query="", top_k=5, debug=False)

    # Invalid: top_k out of range
    with pytest.raises(ValueError):
        RetrieveRequest(query="test", top_k=0, debug=False)

    with pytest.raises(ValueError):
        RetrieveRequest(query="test", top_k=51, debug=False)
