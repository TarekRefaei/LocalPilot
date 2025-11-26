from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_retrieval_metrics_endpoint_returns_dict():
    resp = client.get("/metrics/retrieval")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict)
    # basic shape keys present per retrieval_metrics.get()
    assert "l4_enabled" in body
    assert "cache_stats" in body
    assert "timestamp" in body
