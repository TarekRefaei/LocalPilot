"""
Tests for /retrieve error path (500) when retriever raises.
"""

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_retrieve_internal_error_returns_500_and_message():
    # Mock get_retriever to return an object whose retrieve raises
    mock_retriever = AsyncMock()
    mock_retriever.retrieve = AsyncMock(side_effect=RuntimeError("boom"))

    with patch("app.api.retrieve.get_retriever", return_value=mock_retriever):
        resp = client.post(
            "/retrieve",
            json={
                "query": "something",
                "top_k": 5,
                "debug": False,
            },
        )

    assert resp.status_code == 500
    body = resp.json()
    assert "Retrieval failed" in body.get("detail", "")
