"""
LocalPilot Backend - FastAPI application.
Exposes REST and WebSocket APIs for the VS Code extension.
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.api import chat as chat_api
from app.api import health, metrics, prom_metrics, retrieve, websocket
from app.api import models as models_api
from app.core.config import settings
from app.core.logging import get_logger, setup_logging

# Setup logging
setup_logging()
logger = get_logger("localpilot.backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context to handle startup/shutdown."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    health.set_startup_time(datetime.utcnow())
    try:
        yield
    finally:
        logger.info("Shutting down backend")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)


# Register model validator on startup (idempotent)
try:
    prom_metrics.register_validator_startup(app)
except Exception as e:  # pragma: no cover
    logger.debug(f"Could not register validator startup hook: {e}")


# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(websocket.router, tags=["websocket"])
app.include_router(metrics.router, tags=["metrics"])
app.include_router(retrieve.router, tags=["retrieval"])
app.include_router(models_api.router, tags=["models"])
app.include_router(chat_api.router, tags=["chat"])
app.include_router(prom_metrics.router)


# Legacy endpoints for compatibility
class ChatRequest(BaseModel):
    prompt: str
    model: str | None = None


@app.post("/chat/echo")
async def chat_echo(req: ChatRequest):
    logger.info(f"Chat request: prompt={req.prompt[:50]}..., model={req.model or 'local'}")

    async def gen():
        try:
            # Stream back the prompt as a demo
            text = f"Echo ({req.model or 'local'}): " + req.prompt
            for ch in text:
                yield ch
                await asyncio.sleep(0.01)
            logger.info("Chat stream completed successfully")
        except Exception as e:
            logger.error(f"Chat stream error: {e}")
            raise

    return StreamingResponse(gen(), media_type="text/plain")
