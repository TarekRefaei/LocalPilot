from fastapi.testclient import TestClient

from app.main import app


def test_chat_echo_streams_text():
    client = TestClient(app)
    r = client.post('/chat/echo', json={'prompt': 'Hello', 'model': 'local'})
    assert r.status_code == 200
    # TestClient will consume the streaming response into text
    assert 'Echo (local): Hello' in r.text
