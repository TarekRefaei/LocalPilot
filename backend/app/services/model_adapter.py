from __future__ import annotations

import json
import logging
import os
import re
import time
from collections.abc import AsyncIterator

import httpx
from prometheus_client import Counter, Histogram, Info

from app.services import stream_control

try:
    from app.core.config import settings
except Exception:  # pragma: no cover - fallback for import-time issues
    settings = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


def _get_ollama_url() -> str:
    """
    Resolve the Ollama server URL. Prefer settings.OLLAMA_URL if present,
    otherwise settings.ollama_host, otherwise env OLLAMA_URL, otherwise default.
    """
    if settings is not None:
        # Prefer explicit OLLAMA_URL
        if getattr(settings, "OLLAMA_URL", None):
            return settings.OLLAMA_URL  # type: ignore[attr-defined]
        # Fallback to existing config key used elsewhere
        if getattr(settings, "ollama_host", None):
            return settings.ollama_host  # type: ignore[attr-defined]
    import os

    return os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")


def _get_ollama_api_key() -> str | None:
    if settings is not None and getattr(settings, "OLLAMA_API_KEY", None):
        return settings.OLLAMA_API_KEY  # type: ignore[attr-defined]
    return os.environ.get("OLLAMA_API_KEY")


def _get_ssl_verify() -> bool:
    if settings is not None and getattr(settings, "OLLAMA_VERIFY_SSL", None) is not None:
        return bool(settings.OLLAMA_VERIFY_SSL)  # type: ignore[arg-type]
    val = os.environ.get("OLLAMA_VERIFY_SSL", "1")
    return val not in ("0", "false", "False")


# Prometheus metrics
MODEL_REQUESTS = Counter("localpilot_model_requests_total", "Total model requests")
MODEL_ERRORS = Counter("localpilot_model_errors_total", "Total model stream errors")
MODEL_LATENCY = Histogram(
    "localpilot_model_request_latency_seconds", "Model request latency seconds"
)
MODEL_PER_MODEL_LATENCY = Histogram(
    "localpilot_model_latency_seconds", "Model latency per model", ["model"]
)
APP_INFO = Info("localpilot_app_info", "LocalPilot application info")
APP_INFO.info({"version": "0.1.0", "instance": "localpilot-backend"})


async def _iter_stream_text(resp: httpx.Response) -> AsyncIterator[str]:
    """
    Iterate streamed HTTP response body as text chunks.
    """
    async for chunk in resp.aiter_text():
        if chunk:
            yield chunk


_JSON_LIKE = re.compile(r"^\s*(\{.*\}|\[.*\])\s*$", re.S)


async def _try_parse_json_line(line: str):
    try:
        return json.loads(line)
    except Exception:
        m = re.search(r"(\{.*\}|\[.*\])", line)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                return None
    return None


def _extract_texts_from_json(obj) -> list[str]:
    pieces: list[str] = []
    try:
        if isinstance(obj, str):
            pieces.append(obj)
            return pieces
        if not isinstance(obj, dict):
            return pieces
        # choices (OpenAI-style) with delta/content
        if "choices" in obj and isinstance(obj["choices"], list):
            for choice in obj["choices"]:
                if isinstance(choice, dict):
                    if "delta" in choice and isinstance(choice["delta"], dict):
                        for k in ("content", "text", "token"):
                            if k in choice["delta"] and isinstance(choice["delta"][k], str):
                                pieces.append(choice["delta"][k])
                    if "text" in choice and isinstance(choice["text"], str):
                        pieces.append(choice["text"])
        # common top-level fields
        for k in ("response", "content", "text", "output", "token", "delta"):
            if k in obj:
                v = obj[k]
                if isinstance(v, str):
                    pieces.append(v)
                elif isinstance(v, list):
                    for e in v:
                        if isinstance(e, str):
                            pieces.append(e)
                elif isinstance(v, dict):
                    for subk in ("text", "content"):
                        if subk in v and isinstance(v[subk], str):
                            pieces.append(v[subk])
        if "result" in obj and isinstance(obj["result"], dict):
            for kk in ("content", "text"):
                if kk in obj["result"] and isinstance(obj["result"][kk], str):
                    pieces.append(obj["result"][kk])
    except Exception:
        logger.debug("Failed to extract texts from json fragment", exc_info=True)
    return pieces


async def _parse_ollama_stream(
    chunks: AsyncIterator[str],
    request_id: str | None = None,
    model_label: str | None = None,
) -> AsyncIterator[str]:
    """
    Robust parse for Ollama stream supporting NDJSON, SSE 'data:' lines, and raw text.
    Extracts from choices/delta/content as well as common fields.
    """
    buffer = ""
    async for chunk in chunks:
        # cancellation check
        if request_id:
            ev = stream_control.get_event(request_id)
            if ev and ev.is_set():
                return
        buffer += chunk
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()
            if not line:
                continue
            if line.startswith("data:"):
                line = line[len("data:") :].strip()
            # cancellation check
            if request_id:
                ev = stream_control.get_event(request_id)
                if ev and ev.is_set():
                    return
            parsed = await _try_parse_json_line(line)
            if parsed is not None:
                if isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict | str):
                            for t in _extract_texts_from_json(item):
                                yield t
                else:
                    for t in _extract_texts_from_json(parsed):
                        yield t
                continue
            # not JSON → raw line
            # cancellation check before yielding
            if request_id:
                ev = stream_control.get_event(request_id)
                if ev and ev.is_set():
                    return
            yield line

    # flush remainder
    trimmed = buffer.strip()
    if trimmed:
        parsed = await _try_parse_json_line(trimmed)
        if parsed is not None:
            if isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict | str):
                        for t in _extract_texts_from_json(item):
                            yield t
            else:
                for t in _extract_texts_from_json(parsed):
                    if request_id:
                        ev = stream_control.get_event(request_id)
                        if ev and ev.is_set():
                            return
                    yield t
        else:
            if request_id:
                ev = stream_control.get_event(request_id)
                if ev and ev.is_set():
                    return
            yield trimmed


async def stream_from_ollama(
    prompt: str,
    model: str = "llama2",
    temperature: float = 0.2,
    request_timeout: float | None = None,
    request_id: str | None = None,
) -> AsyncIterator[str]:
    """
    Stream text from an Ollama-like REST API. Yields textual chunks as they arrive.

    Notes:
    - Adjust the endpoint path and payload to match your model host if needed.
    - Ollama's API semantics may differ; adapt parsing of streamed events accordingly.
    """
    url = _get_ollama_url().rstrip("/") + "/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": float(temperature),
        "stream": True,
    }
    headers = {"Content-Type": "application/json"}

    # httpx default timeout can break long-lived streams; allow None or configured value
    timeout = None if request_timeout is None else request_timeout

    MODEL_REQUESTS.inc()
    start = time.time()
    api_key = _get_ollama_api_key()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    verify = _get_ssl_verify()

    try:
        async with httpx.AsyncClient(timeout=timeout, verify=verify) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as resp:
                resp.raise_for_status()
                async for parsed in _parse_ollama_stream(
                    _iter_stream_text(resp), request_id=request_id, model_label=model
                ):
                    # check cancellation before yielding to caller
                    if request_id:
                        ev = stream_control.get_event(request_id)
                        if ev and ev.is_set():
                            return
                    yield parsed
    except Exception:
        MODEL_ERRORS.inc()
        raise
    finally:
        dur = time.time() - start
        MODEL_LATENCY.observe(dur)
        try:
            MODEL_PER_MODEL_LATENCY.labels(model=model).observe(dur)
        except Exception:
            pass


async def stream_from_ollama_safe(
    prompt: str, model: str = "llama2", request_id: str | None = None
) -> AsyncIterator[str]:
    """
    Convenience wrapper that catches exceptions and yields an error message as a final chunk.
    """
    try:
        async for piece in stream_from_ollama(prompt, model=model, request_id=request_id):
            yield piece
    except Exception as exc:  # pragma: no cover - network/host dependent
        logger.exception("Model adapter failed: %s", exc)
        yield "\n\n[Model adapter error: unable to contact the model backend]\n\n"
