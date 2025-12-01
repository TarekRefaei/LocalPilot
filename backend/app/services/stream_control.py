from __future__ import annotations

import asyncio
import uuid

# A simple per-request cancel registry using asyncio.Event
_REGISTRY: dict[str, asyncio.Event] = {}


def new_request_id() -> str:
    rid = str(uuid.uuid4())
    ev = asyncio.Event()
    _REGISTRY[rid] = ev
    return rid


def get_event(request_id: str) -> asyncio.Event | None:
    return _REGISTRY.get(request_id)


def cancel_request(request_id: str) -> None:
    ev = _REGISTRY.get(request_id)
    if ev:
        ev.set()
        _REGISTRY.pop(request_id, None)


def cleanup(request_id: str) -> None:
    _REGISTRY.pop(request_id, None)


def ensure(request_id: str) -> None:
    """Ensure an asyncio.Event exists for the given request_id."""
    _REGISTRY.setdefault(request_id, asyncio.Event())
