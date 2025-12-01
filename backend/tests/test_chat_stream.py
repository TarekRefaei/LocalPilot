from fastapi.testclient import TestClient

from app.main import app


def test_chat_stream_endpoint_returns_text():
    client = TestClient(app)
    r = client.post("/chat/stream", json={"prompt": "Hello world", "model": "local"})
    assert r.status_code == 200
    # TestClient aggregates streaming response into text
    assert isinstance(r.text, str)
    assert len(r.text) > 0
