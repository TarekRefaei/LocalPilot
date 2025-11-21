"""
LocalPilot Backend - FastAPI application.
Exposes REST and WebSocket APIs for the VS Code extension.
"""

import asyncio
import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api import health, websocket

# Setup logging
setup_logging()
logger = get_logger("localpilot.backend")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


# Startup and shutdown events
@app.on_event("startup")
async def startup_event() -> None:
    """Initialize on startup."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    health.set_startup_time(datetime.utcnow())


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Cleanup on shutdown."""
    logger.info("Shutting down backend")


# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(websocket.router, tags=["websocket"])


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
