from __future__ import annotations

import time
from typing import Any

_state: dict[str, Any] = {
    "l4_enabled": False,
    "last_l4_ms": 0.0,
    "cache_stats": {
        "embedding_cache_size": 0,
        "search_cache_size": 0,
        "total_cache_size": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "cache_hit_rate": 0.0,
        "max_size": 0,
    },
    "timestamp": 0.0,
}


def update(l4_enabled: bool, l4_ms: float, cache_stats: dict[str, Any]) -> None:
    _state["l4_enabled"] = bool(l4_enabled)
    _state["last_l4_ms"] = float(l4_ms)
    _state["cache_stats"] = dict(cache_stats or {})
    _state["timestamp"] = time.time()


def get() -> dict[str, Any]:
    return dict(_state)
