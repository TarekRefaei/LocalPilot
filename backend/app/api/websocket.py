"""
WebSocket endpoint for real-time communication.
Handles handshake, heartbeat, and message routing.
"""

import json
import logging
from datetime import datetime

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.models.envelope import (
    ErrorData,
    HandshakeAckPayload,
    HandshakePayload,
    HeartbeatAckPayload,
    HeartbeatPayload,
    WebSocketEnvelope,
)
from app.services.ws_manager import ConnectionManager

logger = logging.getLogger(__name__)
router = APIRouter()

# Global connection manager
manager = ConnectionManager()


def get_manager() -> ConnectionManager:
    """Get the global connection manager."""
    return manager


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str = Query(..., description="Unique client identifier"),
) -> None:
    """
    WebSocket endpoint for real-time communication.

    Handles:
    - Handshake and acknowledgement
    - Heartbeat/ping-pong for connection health
    - Message routing to subscribers
    - Error handling and recovery

    Args:
        websocket: WebSocket connection
        client_id: Unique client identifier (UUID)
    """
    await manager.connect(client_id, websocket)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            envelope = parse_envelope(data)

            if not envelope:
                continue

            logger.debug(f"Received from {client_id}: {envelope.event}")

            # Handle handshake
            if envelope.event == "handshake":
                await handle_handshake(client_id, envelope)

            # Handle heartbeat
            elif envelope.event == "heartbeat":
                await handle_heartbeat(client_id, envelope)

            # Route other events to all clients (broadcast)
            else:
                await manager.broadcast(envelope.model_dump())

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"Client disconnected: {client_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
        manager.disconnect(client_id)


async def handle_handshake(client_id: str, envelope: WebSocketEnvelope) -> None:
    """
    Handle handshake from client.

    Args:
        client_id: Client identifier
        envelope: Handshake envelope
    """
    try:
        # Validate handshake payload
        HandshakePayload(**envelope.data)

        # Create handshake acknowledgement
        ack_payload = HandshakeAckPayload(
            serverVersion="0.1.0",
            clientId=client_id,
            capabilities=[
                "streaming",
                "indexing",
                "chat",
                "plan",
                "act",
                "vram",
            ],
            timestamp=datetime.utcnow().isoformat(),
        )

        # Create response envelope
        response = WebSocketEnvelope(
            event="handshake_ack",
            data=ack_payload.model_dump(),
            correlationId=envelope.correlationId,
        )

        # Send acknowledgement
        await manager.send_personal(client_id, response.model_dump())
        logger.info(f"Handshake completed for {client_id}")

    except Exception as e:
        logger.error(f"Handshake error for {client_id}: {e}")
        error_response = create_error_envelope(
            "error",
            "HANDSHAKE_FAILED",
            str(e),
            correlationId=envelope.correlationId,
        )
        await manager.send_personal(client_id, error_response.model_dump())


async def handle_heartbeat(client_id: str, envelope: WebSocketEnvelope) -> None:
    """
    Handle heartbeat ping from client.

    Args:
        client_id: Client identifier
        envelope: Heartbeat envelope
    """
    try:
        # Validate heartbeat payload
        payload = HeartbeatPayload(**envelope.data)

        # Create heartbeat acknowledgement
        ack_payload = HeartbeatAckPayload(
            serverTime=datetime.utcnow().isoformat(),
            clientTime=payload.timestamp,
        )

        # Create response envelope
        response = WebSocketEnvelope(
            event="heartbeat_ack",
            data=ack_payload.model_dump(),
            correlationId=envelope.correlationId,
        )

        # Send acknowledgement
        await manager.send_personal(client_id, response.model_dump())

    except Exception as e:
        logger.error(f"Heartbeat error for {client_id}: {e}")
        error_response = create_error_envelope(
            "error",
            "HEARTBEAT_FAILED",
            str(e),
            correlationId=envelope.correlationId,
        )
        await manager.send_personal(client_id, error_response.model_dump())


def parse_envelope(data: str) -> WebSocketEnvelope | None:
    """
    Parse incoming message as WebSocket envelope.

    Args:
        data: Raw message data

    Returns:
        Parsed envelope or None if invalid
    """
    try:
        raw = json.loads(data)
        return WebSocketEnvelope(**raw)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Envelope parsing error: {e}")
        return None


def create_error_envelope(
    event: str,
    code: str,
    message: str,
    details: dict | None = None,
    correlationId: str | None = None,
) -> WebSocketEnvelope:
    """
    Create an error envelope.

    Args:
        event: Event name
        code: Error code
        message: Error message
        details: Additional error details
        correlationId: Correlation ID for request/response pairing

    Returns:
        Error envelope
    """
    error_data = ErrorData(
        message=message,
        code=code,
        details=details or {},
    )

    return WebSocketEnvelope(
        event=event,
        data=error_data.model_dump(),
        correlationId=correlationId or "",
    )
