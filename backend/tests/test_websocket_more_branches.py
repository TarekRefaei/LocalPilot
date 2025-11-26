"""
Additional tests to cover websocket API branches: error paths and helpers.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import websocket as ws_api
from app.main import app
from app.models.envelope import WebSocketEnvelope

client = TestClient(app)


def test_get_manager_returns_global_instance():
    m1 = ws_api.get_manager()
    m2 = ws_api.manager
    assert m1 is m2


def test_create_error_envelope_shape():
    env = ws_api.create_error_envelope(
        event="error",
        code="X",
        message="oops",
        details={"a": 1},
        correlationId="corr-1",
    )
    assert isinstance(env, WebSocketEnvelope)
    assert env.event == "error"
    assert env.data.get("code") == "X"
    assert env.data.get("message") == "oops"
    assert env.correlationId == "corr-1"


def test_handshake_validation_failure_sends_error():
    with client.websocket_connect("/ws?client_id=client-bad-hs") as websocket:
        # Missing required fields in handshake data -> validation error
        bad_handshake = {
            "event": "handshake",
            "data": {"foo": "bar"},  # invalid payload
            "timestamp": "2025-01-15T10:30:00Z",
            "correlationId": "corr-err-hs",
            "contractVersion": "0.1.0",
        }
        websocket.send_json(bad_handshake)
        resp = websocket.receive_json()
        assert resp["event"] == "error"
        assert resp["correlationId"] == "corr-err-hs"


def test_heartbeat_validation_failure_sends_error():
    with client.websocket_connect("/ws?client_id=client-bad-hb") as websocket:
        # Do a valid handshake first so manager has connection
        handshake = {
            "event": "handshake",
            "data": {"version": "0.1.0", "clientId": "client-bad-hb"},
            "timestamp": "2025-01-15T10:30:00Z",
            "correlationId": "corr-ok",
            "contractVersion": "0.1.0",
        }
        websocket.send_json(handshake)
        websocket.receive_json()

        # Send invalid heartbeat (missing required fields)
        bad_hb = {
            "event": "heartbeat",
            "data": {"clientId": "client-bad-hb"},  # missing timestamp
            "timestamp": "2025-01-15T10:30:30Z",
            "correlationId": "hb-bad",
            "contractVersion": "0.1.0",
        }
        websocket.send_json(bad_hb)
        resp = websocket.receive_json()
        assert resp["event"] == "error"
        assert resp["correlationId"] == "hb-bad"


def test_parse_envelope_general_exception_path_then_continue():
    with client.websocket_connect("/ws?client_id=client-parse") as websocket:
        # Send valid JSON that will fail pydantic validation for WebSocketEnvelope
        websocket.send_text("{" "not_an_envelope" ": 1}")
        # Connection should still be alive; now send a valid handshake
        handshake = {
            "event": "handshake",
            "data": {"version": "0.1.0", "clientId": "client-parse"},
            "timestamp": "2025-01-15T10:30:00Z",
            "correlationId": "corr-123",
            "contractVersion": "0.1.0",
        }
        websocket.send_json(handshake)
        resp = websocket.receive_json()
        assert resp["event"] == "handshake_ack"


def test_indexing_start_continues_broadcast_on_orchestrator_error():
    with patch.object(ws_api, "IndexingOrchestrator", side_effect=RuntimeError("fail")):
        with client.websocket_connect("/ws?client_id=client-idx") as websocket:
            # Complete handshake
            handshake = {
                "event": "handshake",
                "data": {"version": "0.1.0", "clientId": "client-idx"},
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-hs",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(handshake)
            websocket.receive_json()

            # Send indexing.start; even if orchestrator errors, event should be broadcast back
            indexing_event = {
                "event": "indexing.start",
                "data": {"workspace_path": "/tmp", "options": {}},
                "timestamp": "2025-01-15T10:31:00Z",
                "correlationId": "idx-corr",
                "contractVersion": "0.1.0",
            }
            websocket.send_json(indexing_event)
            resp = websocket.receive_json()
            assert resp["event"] == "indexing.start"
            assert resp["correlationId"] == "idx-corr"
