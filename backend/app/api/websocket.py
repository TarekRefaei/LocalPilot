"""
WebSocket endpoint for real-time communication.
Handles handshake, heartbeat, and message routing.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.models.act import (
    ApplyPayload,
    ApplyResult,
    ApprovalOperation,
    DryRunPayload,
    DryRunResult,
)
from app.models.envelope import (
    ErrorData,
    HandshakeAckPayload,
    HandshakePayload,
    HeartbeatAckPayload,
    HeartbeatPayload,
    IndexingStartPayload,
    WebSocketEnvelope,
)
from app.services.act.approval import (
    FileOperation as ApproveOp,
)
from app.services.act.approval import (
    categorize_operations,
)
from app.services.act.executor import ActExecutor
from app.services.act.executor import OperationRequest as ExecOp
from app.services.act.git_safety import GitSafetyError, GitSafetyService
from app.services.indexing.orchestrator import IndexingOrchestrator
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

            # Indexing start: validate and kick off orchestrator, then broadcast
            elif envelope.event == "indexing.start":
                try:
                    payload = IndexingStartPayload(**envelope.data)
                    # Start orchestrator in background
                    orchestrator = IndexingOrchestrator(manager)
                    # Fire-and-forget
                    import asyncio as _asyncio

                    _asyncio.create_task(
                        orchestrator.run(
                            workspace_path=payload.workspace_path,
                            options=payload.options or {},
                        )
                    )
                except Exception as e:
                    logger.error(f"Failed to start indexing: {e}")
                # Always broadcast the original event to all clients (tests rely on this)
                await manager.broadcast(envelope.model_dump())

            # Act: request approval (dry-run)
            elif envelope.event == "act.request_approval":
                try:
                    payload = DryRunPayload(**envelope.data)
                    root = Path(payload.workspace_path)
                    exe = ActExecutor(make_git_safety(root))
                    # Compute previews
                    previews = exe.dry_run(
                        root,
                        [
                            ExecOp(type=op.type, path=op.path, content=op.content)
                            for op in payload.operations
                        ],
                    )
                    # Categorize requiresApproval
                    ops_for_approval = [
                        ApproveOp(type=p.type, path=p.path, diff=p.diff, content=None)
                        for p in previews
                    ]
                    auto, review = categorize_operations(ops_for_approval)
                    auto_set = {o.path for o in auto}
                    result = DryRunResult(
                        operations=[
                            ApprovalOperation(
                                path=p.path,
                                type=p.type,
                                diff=p.diff,
                                additions=p.summary.additions,
                                deletions=p.summary.deletions,
                                requiresApproval=(p.path not in auto_set),
                            )
                            for p in previews
                        ],
                        autoApprovedPaths=sorted(list(auto_set)),
                        requiresReviewCount=len(review),
                    )
                    await manager.send_personal(
                        client_id,
                        WebSocketEnvelope(
                            event="act.request_approval",
                            data=result.model_dump(),
                            correlationId=envelope.correlationId,
                        ).model_dump(),
                    )
                except Exception as e:
                    logger.error(f"act.request_approval failed: {e}")
                    await manager.send_personal(
                        client_id,
                        create_error_envelope(
                            "act.error",
                            "ACT_DRYRUN_FAILED",
                            str(e),
                            correlationId=envelope.correlationId,
                        ).model_dump(),
                    )

            # Act: apply approved operations
            elif envelope.event == "act.apply":
                try:
                    payload = ApplyPayload(**envelope.data)
                    if not payload.approved:
                        await manager.send_personal(
                            client_id,
                            create_error_envelope(
                                "act.error",
                                "ACT_APPROVAL_REQUIRED",
                                "Apply requires approval.",
                                correlationId=envelope.correlationId,
                            ).model_dump(),
                        )
                        continue
                    root = Path(payload.workspace_path)
                    exe = ActExecutor(make_git_safety(root))
                    ctx, written = exe.apply(
                        plan_id=payload.plan_id,
                        todo_id=payload.todo_id,
                        message=payload.message,
                        root=root,
                        ops=[
                            ExecOp(type=o.type, path=o.path, content=o.content)
                            for o in payload.operations
                        ],
                    )
                    result = ApplyResult(
                        written=[str(p) for p in written],
                        todo_id=payload.todo_id,
                        plan_id=payload.plan_id,
                    )
                    await manager.broadcast(
                        WebSocketEnvelope(
                            event="act.apply_result",
                            data=result.model_dump(),
                            correlationId=envelope.correlationId,
                        ).model_dump()
                    )
                except GitSafetyError as e:
                    await manager.send_personal(
                        client_id,
                        create_error_envelope(
                            "act.error",
                            "ACT_SAFETY_BLOCKED",
                            str(e),
                            correlationId=envelope.correlationId,
                        ).model_dump(),
                    )
                except Exception as e:
                    logger.error(f"act.apply failed: {e}")
                    await manager.send_personal(
                        client_id,
                        create_error_envelope(
                            "act.error",
                            "ACT_APPLY_FAILED",
                            str(e),
                            correlationId=envelope.correlationId,
                        ).model_dump(),
                    )

            # Act: rollback last commit
            elif envelope.event == "act.rollback":
                try:
                    # No payload schema yet; rollback last by default
                    exe = ActExecutor(make_git_safety(Path.cwd()))
                    exe.rollback_last()
                    await manager.broadcast(
                        WebSocketEnvelope(
                            event="act.apply_result",
                            data={"written": [], "todo_id": "", "plan_id": ""},
                            correlationId=envelope.correlationId,
                        ).model_dump()
                    )
                except Exception as e:
                    logger.error(f"act.rollback failed: {e}")
                    await manager.send_personal(
                        client_id,
                        create_error_envelope(
                            "act.error",
                            "ACT_ROLLBACK_FAILED",
                            str(e),
                            correlationId=envelope.correlationId,
                        ).model_dump(),
                    )

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


def make_git_safety(root: Path):
    import subprocess  # local import to avoid unused at module level

    class _GitAdapter:
        def __init__(self, cwd: Path):
            self.cwd = cwd

        def _run(self, *args: str) -> tuple[int, str]:
            try:
                out = subprocess.run(
                    ["git", *args],
                    cwd=str(self.cwd),
                    check=False,
                    text=True,
                    capture_output=True,
                )
                return out.returncode, (out.stdout or out.stderr)
            except Exception as e:  # pragma: no cover
                return 1, str(e)

        def is_repo(self) -> bool:
            code, _ = self._run("rev-parse", "--is-inside-work-tree")
            return code == 0

        def has_uncommitted_changes(self) -> bool:
            code, out = self._run("status", "--porcelain")
            return code == 0 and bool(out.strip())

        def current_branch(self) -> str:
            _, out = self._run("rev-parse", "--abbrev-ref", "HEAD")
            return out.strip() or "HEAD"

        def current_commit(self) -> str:
            _, out = self._run("rev-parse", "HEAD")
            return out.strip()

        def create_branch(self, name: str) -> None:
            self._run("branch", name)

        def checkout(self, name: str) -> None:
            self._run("checkout", name)

        def add_all(self) -> None:
            self._run("add", "-A")

        def commit(self, message: str) -> None:
            self._run("commit", "-m", message)

        def reset_hard(self, ref: str) -> None:
            self._run("reset", "--hard", ref)

    return GitSafetyService(_GitAdapter(root))
