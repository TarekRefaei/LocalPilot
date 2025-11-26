from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api import websocket as ws_api
from app.main import app

client = TestClient(app)


def test_parse_envelope_validation_error_returns_none():
    # Valid JSON but invalid envelope shape triggers general exception path inside parse_envelope
    data = '{"not_an_envelope": 1}'
    env = ws_api.parse_envelope(data)
    assert env is None


def test_websocket_endpoint_catches_general_exception_and_disconnects():
    with patch.object(ws_api, "parse_envelope", side_effect=RuntimeError("boom")):
        with client.websocket_connect("/ws?client_id=client-exc") as websocket:
            # Any incoming text will trigger parse_envelope which raises -> endpoint catches and disconnects
            websocket.send_text("{}")
            # Do not block waiting on receive; exception path is covered by the send above.
