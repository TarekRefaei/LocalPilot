from __future__ import annotations

import logging
import os
from typing import Any

import httpx
from fastapi import APIRouter, Header, HTTPException

try:
    from app.core.config import settings
except Exception:  # pragma: no cover
    settings = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/models", tags=["models"])


def _get_ollama_url() -> str:
    if settings is not None and getattr(settings, "OLLAMA_URL", None):
        return settings.OLLAMA_URL  # type: ignore[attr-defined]
    return os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")


def _get_ollama_api_key() -> str | None:
    if settings is not None and getattr(settings, "OLLAMA_API_KEY", None):
        return settings.OLLAMA_API_KEY  # type: ignore[attr-defined]
    return os.environ.get("OLLAMA_API_KEY")


def _get_models_bearer_token() -> str | None:
    if settings is not None and getattr(settings, "MODELS_BEARER_TOKEN", None):
        return settings.MODELS_BEARER_TOKEN  # type: ignore[attr-defined]
    return os.environ.get("MODELS_BEARER_TOKEN")


@router.get("/", summary="List models available on Ollama")
async def list_models(authorization: str | None = Header(None)) -> Any:
    base = _get_ollama_url().rstrip("/")
    headers: dict[str, str] = {}
    api_key = _get_ollama_api_key()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Optional bearer protection for this endpoint
    token = _get_models_bearer_token()
    if token:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization required")
        provided = authorization.split(" ", 1)[1]
        if provided != token:
            raise HTTPException(status_code=403, detail="Invalid token")

    # TLS verify toggle via settings or env OLLAMA_VERIFY_SSL
    verify = True
    if settings is not None and getattr(settings, "OLLAMA_VERIFY_SSL", None) is not None:
        verify = bool(settings.OLLAMA_VERIFY_SSL)  # type: ignore[arg-type]
    else:
        verify = os.environ.get("OLLAMA_VERIFY_SSL", "1") not in ("0", "false", "False")

    async with httpx.AsyncClient(timeout=10.0, verify=verify) as client:
        # Try /api/models first
        try:
            resp = await client.get(f"{base}/api/models", headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                return data
        except Exception:
            pass
        # Fallback to /api/tags (Ollama classic)
        try:
            resp = await client.get(f"{base}/api/tags", headers=headers)
            resp.raise_for_status()
            data = resp.json()
            # Normalize to { models: [name, ...] }
            if isinstance(data, dict) and isinstance(data.get("models"), list):
                names = []
                for m in data.get("models", []):
                    name = (m or {}).get("name")
                    if isinstance(name, str):
                        names.append(name)
                return {"models": names}
            if isinstance(data, list):
                names = []
                for m in data:
                    if isinstance(m, dict) and isinstance(m.get("name"), str):
                        names.append(m["name"])
                    elif isinstance(m, str):
                        names.append(m)
                return {"models": names}
        except Exception as e:  # pragma: no cover - network dependent
            logger.exception("Failed to fetch ollama tags/models: %s", e)
            return {"error": "failed_fetch_models", "detail": str(e)}
    return {"models": []}
