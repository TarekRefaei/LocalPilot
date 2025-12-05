from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_act_request_approval_returns_previews(tmp_path: Path):
    client = TestClient(app)
    with client.websocket_connect("/ws?client_id=act-client-1") as ws:
        # handshake
        ws.send_json(
            {
                "event": "handshake",
                "data": {"version": "0.1.0", "clientId": "act-client-1"},
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-001",
                "contractVersion": "0.1.0",
            }
        )
        ws.receive_json()

        ws.send_json(
            {
                "event": "act.request_approval",
                "data": {
                    "workspace_path": str(tmp_path),
                    "plan_id": "p1",
                    "todo_id": "t1",
                    "operations": [
                        {
                            "type": "create",
                            "path": "docs/readme.md",
                            "content": "# Title\n",
                        }
                    ],
                },
                "timestamp": "2025-01-15T10:31:00Z",
                "correlationId": "act-001",
                "contractVersion": "0.1.0",
            }
        )

        resp = ws.receive_json()
        assert resp["event"] == "act.request_approval"
        ops = resp["data"]["operations"]
        assert isinstance(ops, list) and len(ops) == 1
        op0 = ops[0]
        assert op0["path"].endswith("docs/readme.md")
        assert op0["requiresApproval"] is False  # safe create


def test_act_apply_requires_approval(tmp_path: Path):
    client = TestClient(app)
    with client.websocket_connect("/ws?client_id=act-client-2") as ws:
        # handshake
        ws.send_json(
            {
                "event": "handshake",
                "data": {"version": "0.1.0", "clientId": "act-client-2"},
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-002",
                "contractVersion": "0.1.0",
            }
        )
        ws.receive_json()

        ws.send_json(
            {
                "event": "act.apply",
                "data": {
                    "workspace_path": str(tmp_path),
                    "plan_id": "p1",
                    "todo_id": "t1",
                    "message": "Apply",
                    "operations": [
                        {
                            "type": "create",
                            "path": "docs/readme.md",
                            "content": "# Title\n",
                        }
                    ],
                },
                "timestamp": "2025-01-15T10:32:00Z",
                "correlationId": "act-002",
                "contractVersion": "0.1.0",
            }
        )

        resp = ws.receive_json()
        assert resp["event"] == "act.error"
        assert resp["data"]["code"] == "ACT_APPROVAL_REQUIRED"


def test_act_apply_approved_outside_git_allowed_in_git_optional(
    tmp_path: Path, monkeypatch
):
    from app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "act_apply_safety", "git-optional", raising=False)

    client = TestClient(app)
    with client.websocket_connect("/ws?client_id=act-client-3") as ws:
        # handshake
        ws.send_json(
            {
                "event": "handshake",
                "data": {"version": "0.1.0", "clientId": "act-client-3"},
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-003",
                "contractVersion": "0.1.0",
            }
        )
        ws.receive_json()

        ws.send_json(
            {
                "event": "act.apply",
                "data": {
                    "workspace_path": str(tmp_path),
                    "plan_id": "p2",
                    "todo_id": "t2",
                    "message": "Apply",
                    "approved": True,
                    "operations": [
                        {
                            "type": "create",
                            "path": "docs/readme.md",
                            "content": "# Title\n",
                        }
                    ],
                },
                "timestamp": "2025-01-15T10:32:00Z",
                "correlationId": "act-003",
                "contractVersion": "0.1.0",
            }
        )

        resp = ws.receive_json()
        assert resp["event"] == "act.apply_result"
        assert any(
            p.endswith("docs/readme.md") for p in resp["data"]["written"]
        )  # created


def test_act_rollback_broadcasts_result():
    client = TestClient(app)
    with client.websocket_connect("/ws?client_id=act-client-4") as ws:
        # handshake
        ws.send_json(
            {
                "event": "handshake",
                "data": {"version": "0.1.0", "clientId": "act-client-4"},
                "timestamp": "2025-01-15T10:30:00Z",
                "correlationId": "corr-004",
                "contractVersion": "0.1.0",
            }
        )
        ws.receive_json()

        ws.send_json(
            {
                "event": "act.rollback",
                "data": {},
                "timestamp": "2025-01-15T10:33:00Z",
                "correlationId": "act-004",
                "contractVersion": "0.1.0",
            }
        )

        resp = ws.receive_json()
        assert resp["event"] == "act.apply_result"
