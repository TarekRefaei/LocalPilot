import asyncio
import json
import types

import pytest

from app.services import model_adapter


class DummyResponse:
    def __init__(self, chunks):
        self._chunks = chunks

    async def aiter_text(self):
        for c in self._chunks:
            await asyncio.sleep(0)
            yield c

    def raise_for_status(self):
        return None


class DummyStreamCtx:
    def __init__(self, response):
        self._resp = response

    async def __aenter__(self):
        return self._resp

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FakeAsyncClient:
    def __init__(self, response):
        self._resp = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    def stream(self, method, url, json=None, headers=None):
        return DummyStreamCtx(self._resp)


@pytest.mark.asyncio
async def test_stream_from_ollama_safe_parses_ndjson(monkeypatch):
    ndjson_lines = [
        json.dumps({"response": "Hello"}) + "\n",
        json.dumps({"response": " world!"}) + "\n",
    ]
    resp = DummyResponse(ndjson_lines)

    # Patch httpx.AsyncClient to our fake
    fake_module = types.SimpleNamespace(
        AsyncClient=lambda *a, **k: FakeAsyncClient(resp)
    )
    monkeypatch.setattr(model_adapter, "httpx", fake_module)

    pieces = []
    async for piece in model_adapter.stream_from_ollama_safe("hi", model="llama2"):
        pieces.append(piece)

    joined = "".join(pieces)
    assert "Hello" in joined
    assert "world!" in joined
