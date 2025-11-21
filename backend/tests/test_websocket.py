"""
Tests for WebSocket endpoint with handshake, heartbeat, and message routing.
"""

import json
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestWebSocketHandshake:
    """Tests for WebSocket handshake flow."""

    def test_websocket_handshake_flow(self):
        """WebSocket should complete handshake on connection."""
        with client.websocket_connect("/ws?client_id=test-client-1") as websocket:
            # Send handshake
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "test-client-1",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)

            # Receive handshake_ack
            response = websocket.receive_json()

            assert response["event"] == "handshake_ack"
            assert response["data"]["clientId"] == "test-client-1"
            assert response["data"]["serverVersion"] == "0.1.0"
            assert "capabilities" in response["data"]
            assert len(response["data"]["capabilities"]) > 0

    def test_websocket_handshake_ack_has_capabilities(self):
        """Handshake ACK should include server capabilities."""
        with client.websocket_connect("/ws?client_id=test-client-2") as websocket:
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "test-client-2",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)

            response = websocket.receive_json()
            capabilities = response["data"]["capabilities"]

            expected_capabilities = ["streaming", "indexing", "chat", "plan", "act", "vram"]
            for cap in expected_capabilities:
                assert cap in capabilities

    def test_websocket_handshake_preserves_correlation_id(self):
        """Handshake ACK should preserve correlation ID."""
        with client.websocket_connect("/ws?client_id=test-client-3") as websocket:
            corr_id = "corr-abc-123"
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "test-client-3",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": corr_id,
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)

            response = websocket.receive_json()
            assert response["correlationId"] == corr_id


class TestWebSocketHeartbeat:
    """Tests for WebSocket heartbeat/ping-pong."""

    def test_websocket_heartbeat_response(self):
        """WebSocket should respond to heartbeat with heartbeat_ack."""
        with client.websocket_connect("/ws?client_id=test-client-4") as websocket:
            # Complete handshake first
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "test-client-4",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)
            websocket.receive_json()  # Consume handshake_ack

            # Send heartbeat
            heartbeat = {
                "event": "heartbeat",
                "data": {
                    "clientId": "test-client-4",
                    "timestamp": "2025-01-15T10:30:30Z",
                },
                "timestamp": "2025-01-15T10:30:30Z",
                "correlationId": "hb-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(heartbeat)

            # Receive heartbeat_ack
            response = websocket.receive_json()

            assert response["event"] == "heartbeat_ack"
            assert "serverTime" in response["data"]
            assert "clientTime" in response["data"]
            assert response["data"]["clientTime"] == "2025-01-15T10:30:30Z"

    def test_websocket_heartbeat_preserves_correlation_id(self):
        """Heartbeat ACK should preserve correlation ID."""
        with client.websocket_connect("/ws?client_id=test-client-5") as websocket:
            # Complete handshake
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "test-client-5",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)
            websocket.receive_json()

            # Send heartbeat with specific correlation ID
            hb_corr_id = "hb-xyz-789"
            heartbeat = {
                "event": "heartbeat",
                "data": {
                    "clientId": "test-client-5",
                    "timestamp": "2025-01-15T10:30:30Z",
                },
                "timestamp": "2025-01-15T10:30:30Z",
                "correlationId": hb_corr_id,
                "contractVersion": "0.1.0",
            }
            websocket.send_json(heartbeat)

            response = websocket.receive_json()
            assert response["correlationId"] == hb_corr_id


class TestWebSocketMessageRouting:
    """Tests for WebSocket message routing to subscribers."""

    def test_websocket_message_broadcast(self):
        """Messages should be routed to all connected clients."""
        # Create two connections
        with client.websocket_connect("/ws?client_id=client-a") as ws_a:
            with client.websocket_connect("/ws?client_id=client-b") as ws_b:
                # Complete handshakes
                for ws, client_id in [(ws_a, "client-a"), (ws_b, "client-b")]:
                    handshake = {
                        "event": "handshake",
                        "data": {
                            "version": "0.1.0",
                            "clientId": client_id,
                        },
                        "timestamp": "2025-01-15T10:30:00Z",
                        "correlationId": "corr-123",
                        "contractVersion": "0.1.0",
                    }
                    ws.send_json(handshake)
                    ws.receive_json()  # Consume handshake_ack

                # Send indexing.start from client-a
                indexing_event = {
                    "event": "indexing.start",
                    "data": {
                        "workspace_path": "/home/user/project",
                        "options": {},
                    },
                    "timestamp": "2025-01-15T10:30:00Z",
                    "correlationId": "idx-123",
                    "contractVersion": "0.1.0",
                }
                ws_a.send_json(indexing_event)

                # Both clients should receive the event (broadcast)
                response_a = ws_a.receive_json()
                response_b = ws_b.receive_json()

                assert response_a["event"] == "indexing.start"
                assert response_b["event"] == "indexing.start"
                assert response_a["data"]["workspace_path"] == "/home/user/project"
                assert response_b["data"]["workspace_path"] == "/home/user/project"

    def test_websocket_chat_event_routing(self):
        """Chat events should be routed correctly."""
        with client.websocket_connect("/ws?client_id=client-chat") as websocket:
            # Complete handshake
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "client-chat",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)
            websocket.receive_json()

            # Send chat message
            chat_event = {
                "event": "chat.message",
                "data": {
                    "session_id": "session-123",
                    "message": "Hello, how does auth work?",
                    "context": {},
                    "options": {},
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "chat-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(chat_event)

            # Should receive the same event back (broadcast to self)
            response = websocket.receive_json()
            assert response["event"] == "chat.message"
            assert response["data"]["message"] == "Hello, how does auth work?"

    def test_websocket_plan_event_routing(self):
        """Plan events should be routed correctly."""
        with client.websocket_connect("/ws?client_id=client-plan") as websocket:
            # Complete handshake
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "client-plan",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)
            websocket.receive_json()

            # Send plan.generate
            plan_event = {
                "event": "plan.generate",
                "data": {
                    "source": "chat",
                    "workspace_path": "/home/user/project",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "plan-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(plan_event)

            # Should receive the same event back (broadcast to self)
            response = websocket.receive_json()
            assert response["event"] == "plan.generate"
            assert response["data"]["source"] == "chat"

    def test_websocket_act_event_routing(self):
        """Act events should be routed correctly."""
        with client.websocket_connect("/ws?client_id=client-act") as websocket:
            # Complete handshake
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "client-act",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)
            websocket.receive_json()

            # Send act.start
            act_event = {
                "event": "act.start",
                "data": {
                    "plan_id": "plan-123",
                    "workspace_path": "/home/user/project",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "act-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(act_event)

            # Should receive the same event back (broadcast to self)
            response = websocket.receive_json()
            assert response["event"] == "act.start"
            assert response["data"]["plan_id"] == "plan-123"


class TestWebSocketEnvelopeValidation:
    """Tests for WebSocket envelope validation."""

    def test_websocket_invalid_json_handling(self):
        """WebSocket should handle invalid JSON gracefully."""
        with client.websocket_connect("/ws?client_id=client-invalid") as websocket:
            # Send invalid JSON
            websocket.send_text("not valid json")

            # Connection should remain open (no crash)
            # Send a valid message to verify connection is still alive
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "client-invalid",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)

            # Should receive handshake_ack
            response = websocket.receive_json()
            assert response["event"] == "handshake_ack"

    def test_websocket_envelope_has_contract_version(self):
        """All responses should include contractVersion."""
        with client.websocket_connect("/ws?client_id=client-version") as websocket:
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "client-version",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)

            response = websocket.receive_json()
            assert "contractVersion" in response
            assert response["contractVersion"] == "0.1.0"

    def test_websocket_envelope_has_timestamp(self):
        """All responses should include timestamp."""
        with client.websocket_connect("/ws?client_id=client-ts") as websocket:
            handshake = {
                "event": "handshake",
                "data": {
                    "version": "0.1.0",
                    "clientId": "client-ts",
                },
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-123",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)

            response = websocket.receive_json()
            assert "timestamp" in response
            # Should be ISO 8601 format
            assert "T" in response["timestamp"]
