"""
Health check and status endpoints.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.models.health import (
    ConfigResponse,
    HealthResponse,
    OllamaHealthResponse,
    ResourceUsage,
    ServiceStatus,
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Track startup time
_startup_time: datetime | None = None


def set_startup_time(time: datetime) -> None:
    """Set the application startup time."""
    global _startup_time
    _startup_time = time


def get_uptime_seconds() -> int:
    """Get uptime in seconds."""
    if _startup_time is None:
        return 0
    return int((datetime.utcnow() - _startup_time).total_seconds())


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Check if backend is running and healthy.

    Returns:
        HealthResponse: Health status with service details and resource usage.
    """
    try:
        # Check Ollama connectivity (mock for now)
        ollama_status = ServiceStatus(
            status="connected",
            details={"host": settings.ollama_host},
        )

        # Check vector DB (mock for now)
        vector_db_status = ServiceStatus(
            status="ready",
            details={"collections": 0, "total_vectors": 0},
        )

        # Resource usage (mock for now)
        resources = ResourceUsage(
            vram_usage_gb=0.0,
            vram_total_gb=8.0,
            ram_usage_gb=0.0,
            ram_total_gb=16.0,
        )

        return HealthResponse(
            status="healthy",
            version=settings.app_version,
            uptime_seconds=get_uptime_seconds(),
            services={
                "ollama": ollama_status,
                "vector_db": vector_db_status,
            },
            resources=resources,
            timestamp=datetime.utcnow().isoformat(),
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable") from e


@router.get("/health/ollama", response_model=OllamaHealthResponse)
async def ollama_health() -> OllamaHealthResponse:
    """
    Check Ollama service connectivity.

    Returns:
        OllamaHealthResponse: Ollama status and available models.
    """
    try:
        # Mock response - in production, would call actual Ollama API
        return OllamaHealthResponse(
            status="connected",
            host=settings.ollama_host,
            version="0.1.20",
            models=[
                {
                    "name": "qwen2.5-coder:7b-instruct-q4_K_M",
                    "size_gb": 4.5,
                    "loaded": True,
                },
                {
                    "name": "qwen2.5-coder:14b-instruct-q4_K_M",
                    "size_gb": 9.0,
                    "loaded": False,
                },
                {
                    "name": "bge-m3",
                    "size_gb": 1.5,
                    "loaded": True,
                },
            ],
        )
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")
        raise HTTPException(status_code=503, detail="Ollama unavailable") from e


@router.get("/config", response_model=ConfigResponse)
async def get_config() -> ConfigResponse:
    """
    Get current configuration.

    Returns:
        ConfigResponse: Application configuration.
    """
    return ConfigResponse(
        app_name=settings.app_name,
        app_version=settings.app_version,
        debug=settings.debug,
        host=settings.host,
        port=settings.port,
        ollama_host=settings.ollama_host,
        log_level=settings.log_level,
        timestamp=datetime.utcnow().isoformat(),
    )
