from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import health
from app.main import app

client = TestClient(app)


def test_set_startup_time_and_get_uptime_seconds():
    # Explicitly set startup time and verify uptime returns an int >= 0
    import datetime as dt

    health.set_startup_time(dt.datetime.utcnow())
    uptime = health.get_uptime_seconds()
    assert isinstance(uptime, int)
    assert uptime >= 0


def test_health_responds_503_when_healthresponse_raises():
    with patch.object(health, "HealthResponse", side_effect=RuntimeError("fail")):
        resp = client.get("/health")
        assert resp.status_code == 503
        assert "Service unavailable" in resp.text


def test_ollama_health_responds_503_when_ollamahealthresponse_raises():
    with patch.object(health, "OllamaHealthResponse", side_effect=RuntimeError("fail")):
        resp = client.get("/health/ollama")
        assert resp.status_code == 503
        assert "Ollama unavailable" in resp.text
