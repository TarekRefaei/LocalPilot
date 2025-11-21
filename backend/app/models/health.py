"""
Health check and status models.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel


class ServiceStatus(BaseModel):
    """Status of a service."""

    status: str  # "connected", "ready", "error"
    details: Optional[Dict[str, Any]] = None


class ResourceUsage(BaseModel):
    """Resource usage information."""

    vram_usage_gb: float
    vram_total_gb: float
    ram_usage_gb: float
    ram_total_gb: float


class HealthResponse(BaseModel):
    """Health check response."""

    status: str  # "healthy", "degraded", "unhealthy"
    version: str
    uptime_seconds: int
    services: Dict[str, ServiceStatus]
    resources: ResourceUsage
    timestamp: str


class OllamaHealthResponse(BaseModel):
    """Ollama service health response."""

    status: str
    host: str
    version: Optional[str] = None
    models: Optional[list[Dict[str, Any]]] = None


class ConfigResponse(BaseModel):
    """Configuration response."""

    app_name: str
    app_version: str
    debug: bool
    host: str
    port: int
    ollama_host: str
    log_level: str
    timestamp: str
