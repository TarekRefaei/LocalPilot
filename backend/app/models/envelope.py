"""
WebSocket envelope and message contracts.
Aligned with TypeScript contracts in extension/src/contracts/envelope.ts
"""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class WebSocketEnvelope(BaseModel):
    """WebSocket message envelope wrapping all messages."""

    event: str = Field(..., description="Event topic in dot-separated format")
    data: Any = Field(..., description="Payload data specific to the event type")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="ISO 8601 timestamp when message was created",
    )
    correlationId: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for request/response correlation",
    )
    contractVersion: str = Field(
        default="0.1.0", description="Contract version for forward compatibility"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "event": "handshake",
                "data": {"version": "0.1.0", "clientId": "client-123"},
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "550e8400-e29b-41d4-a716-446655440000",
                "contractVersion": "0.1.0",
            }
        }


class ErrorData(BaseModel):
    """Error payload for error events."""

    message: str
    code: str
    details: dict[str, Any] | None = None


class HandshakePayload(BaseModel):
    """Handshake payload sent by client on connection."""

    version: str
    clientId: str
    workspace: str | None = None


class HandshakeAckPayload(BaseModel):
    """Handshake acknowledgement from server."""

    serverVersion: str
    clientId: str
    capabilities: list[str]
    timestamp: str


class HeartbeatPayload(BaseModel):
    """Heartbeat/ping payload."""

    clientId: str
    timestamp: str


class HeartbeatAckPayload(BaseModel):
    """Heartbeat acknowledgement/pong payload."""

    serverTime: str
    clientTime: str


# Event topics for indexing, chat, plan, act, vram
class IndexingStartPayload(BaseModel):
    """Start indexing event payload."""

    workspace_path: str
    options: dict[str, Any] | None = None


class IndexingProgressPayload(BaseModel):
    """Indexing progress event payload."""

    indexing_id: str
    phase: str
    phase_number: int
    total_phases: int
    current_file: int
    total_files: int
    current_file_path: str | None = None
    percentage: float
    estimated_time_remaining_seconds: int
    message: str


class IndexingCompletePayload(BaseModel):
    """Indexing complete event payload."""

    indexing_id: str
    duration_seconds: int
    statistics: dict[str, Any]
    project_summary: str | None = None
    failed_files: list[dict[str, Any]] | None = None


class ChatMessagePayload(BaseModel):
    """Chat message event payload."""

    session_id: str
    message: str
    context: dict[str, Any] | None = None
    options: dict[str, Any] | None = None


class ChatStreamChunkPayload(BaseModel):
    """Chat stream chunk event payload."""

    message_id: str
    chunk: str
    index: int


class PlanGeneratePayload(BaseModel):
    """Plan generation event payload."""

    source: str
    chat_session_id: str | None = None
    plan_suggestion: dict[str, Any] | None = None
    workspace_path: str


class ActStartPayload(BaseModel):
    """Act/execution start event payload."""

    plan_id: str
    workspace_path: str
    options: dict[str, Any] | None = None


class VramWarningPayload(BaseModel):
    """VRAM warning event payload."""

    level: str  # "warning" | "critical"
    current_usage_gb: float
    total_vram_gb: float
    usage_percentage: float
    loaded_models: list[dict[str, Any]]
    recommendation: str
