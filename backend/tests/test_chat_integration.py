from fastapi.testclient import TestClient

from app.main import app


def test_chat_flow_with_mocked_components(monkeypatch):
    # Patch get_retriever in the chat module namespace
    import app.api.chat as chat_module

    async def fake_get_retriever():
        class DummyRetriever:
            async def retrieve(self, query: str, top_k: int = 5):
                return [{"content": "Evidence A"}, {"content": "Evidence B"}]

        return DummyRetriever()

    monkeypatch.setattr(chat_module, "get_retriever", fake_get_retriever)

    # Patch the model adapter function referenced by the chat module

    async def fake_stream(prompt: str, model: str = "llama2"):
        for p in ("Hello ", "from ", "mocked ", "model"):
            yield p

    monkeypatch.setattr(chat_module, "stream_from_ollama_safe", fake_stream)

    client = TestClient(app)
    r = client.post("/chat/stream", json={"prompt": "Test prompt", "model": "llama2"})
    assert r.status_code == 200
    # TestClient aggregates streaming output in .text
    assert "Hello" in r.text
    assert "mocked" in r.text
