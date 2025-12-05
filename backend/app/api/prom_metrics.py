from __future__ import annotations

import logging
import os

from fastapi import APIRouter, Header, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter()

# Try to import the VRAM/model configuration validator
try:
    from app.services.llm.validator import validate_config_on_startup  # type: ignore
except Exception:  # pragma: no cover - fallback path
    try:
        from services.llm.validator import validate_config_on_startup  # type: ignore
    except Exception:  # pragma: no cover - if unavailable, skip registration
        validate_config_on_startup = None  # type: ignore

logger = logging.getLogger(__name__)


def register_validator_startup(app):
    """
    Register a FastAPI startup hook to validate model config early.

    Idempotent: safe to call multiple times.
    """
    if validate_config_on_startup is None:
        logger.debug("validate_config_on_startup not available, skipping registration")
        return

    if getattr(app, "_validator_startup_registered", False):
        logger.debug("Validator startup already registered")
        return

    @app.on_event("startup")
    async def _validate_models_on_startup() -> (
        None
    ):  # pragma: no cover - exercised in app startup
        cfg: dict[str, str | None] = {
            "embedding": os.getenv("MODEL_EMBEDDING")
            or os.getenv("MODEL_EMBED")
            or os.getenv("MODEL_EMB"),
            "chat": os.getenv("MODEL_CHAT") or os.getenv("MODEL_CH"),
            "planning": os.getenv("MODEL_PLANNING"),
            "coding": os.getenv("MODEL_CODING"),
        }
        if not any(cfg.values()):
            logger.debug("No MODEL_* env vars set - skipping model config validation")
            return
        try:
            validate_config_on_startup(cfg)  # type: ignore[misc]
            logger.info("Model configuration validated successfully at startup")
        except RuntimeError as exc:  # pragma: no cover
            msg = (
                f"Model configuration invalid at startup: {exc}. "
                "To override and force start (risky), set env FORCE_START=true."
            )
            logging.getLogger("uvicorn.error").error(msg)
            raise

    app._validator_startup_registered = True
    logger.debug("Registered model validator startup handler")


_METRICS_TOKEN = os.environ.get("METRICS_BEARER_TOKEN")


@router.get("/metrics")
async def metrics_endpoint(authorization: str | None = Header(None)):
    if _METRICS_TOKEN:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization required")
        token = authorization.split(" ", 1)[1]
        if token != _METRICS_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")
    try:
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)
    except Exception:
        return Response(content=b"", media_type=CONTENT_TYPE_LATEST)
