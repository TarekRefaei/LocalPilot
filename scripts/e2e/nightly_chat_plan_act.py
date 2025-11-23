#!/usr/bin/env python3
"""
LocalPilot E2E: Chat → Plan → Act nightly scenario (Windows-friendly).

Steps (deterministic):
1) Start backend on 127.0.0.1:8765 (uvicorn app.main:app)
2) Health 200
3) WebSocket handshake + heartbeat
4) indexing.start broadcast round-trip
5) REST chat echo smoke
6) act.request_approval (create docs/E2E_README.md) -> preview
7) act.apply (approved) -> apply_result and verify file written

Artifacts written under ./artifacts/e2e/:
- backend.log         (backend stdout/stderr)
- e2e-result.json     (summary result)
- ws-trace.jsonl      (optional WS messages logged)

Exit code: 0 on success; 1 on failure.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional

import httpx
import websockets

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
ARTIFACTS_DIR = REPO_ROOT / "artifacts" / "e2e"
BACKEND_LOG = ARTIFACTS_DIR / "backend.log"
RESULT_JSON = ARTIFACTS_DIR / "e2e-result.json"
WS_TRACE = ARTIFACTS_DIR / "ws-trace.jsonl"

HOST = "127.0.0.1"
PORT = 8765
HTTP_BASE = f"http://{HOST}:{PORT}"
WS_URL_BASE = f"ws://{HOST}:{PORT}/ws"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
ENABLE_OFFLINE_RETRIEVAL = os.environ.get("E2E_OFFLINE_RETRIEVAL", "0") == "1"

CLIENT_ID = "e2e-client-01"
PLAN_ID = "plan-e2e-0001"
TODO_ID = "todo-e2e-0001"
EXECUTION_ID = "exec-e2e-0001"
TARGET_FILE = "docs/E2E_README.md"
TARGET_CONTENT = "E2E seeded content\n"

# E2E scenario identification and flake control
SCENARIO_ID = "chat-plan-act"
FLAKY_CONFIG = REPO_ROOT / "scripts" / "e2e" / ".flaky.json"


def ensure_artifacts_dir() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def read_flaky_config() -> dict:
    """Read flake quarantine configuration."""
    try:
        if FLAKY_CONFIG.exists():
            return json.loads(FLAKY_CONFIG.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"skip": []}


def is_transient_error(e: Exception) -> bool:
    """Heuristic to detect likely transient errors suitable for a single retry."""
    msg = str(e)
    transient_markers = [
        "ConnectionRefusedError",
        "connect",  # generic connect error substring
        "Timed out waiting for event",
        "health check failed",
        "Cannot connect to host",
        "TimeoutError",
    ]
    return isinstance(e, TimeoutError) or any(m.lower() in msg.lower() for m in transient_markers)


async def is_ollama_online() -> bool:
    """Check if Ollama endpoint is reachable by probing /api/tags."""
    url = f"{OLLAMA_HOST}/api/tags"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get(url)
            return r.status_code == 200
    except Exception:
        return False


# Enable importing backend modules for seeding
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


async def seed_retrieval_fixture() -> None:
    """Seed Chroma collection with one deterministic chunk for symbol search.

    Uses VectorStore to upsert a chunk with metadata including symbols: 'E2E_Symbol'.
    Embedding vector is zeros (not used by symbol search).
    """
    try:
        from app.core.config import settings as _settings  # type: ignore
        from app.services.rag.vector_store import VectorStore  # type: ignore

        vs = VectorStore(persist_directory=_settings.vector_db_path)
        chunk = {
            "id": "e2e_chunk_001",
            "content": "def E2E_Symbol():\n    return 'ok'\n",
            "embedding": [0.0] * 1024,
            "metadata": {
                "file_path": "e2e/seed.py",
                "symbols": "E2E_Symbol",
                "chunk_type": "function",
                "language": "python",
                "chunk_index": 0,
                "start_line": 1,
                "end_line": 2,
            },
        }
        await vs.upsert_chunks([chunk])
    except Exception:
        # Seeding failures should not break the harness
        pass


def start_backend() -> subprocess.Popen:
    """Start uvicorn backend on PORT, log to backend.log."""
    ensure_artifacts_dir()
    logf = open(BACKEND_LOG, "w", encoding="utf-8")
    # Use python -m uvicorn so environment python is used
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        HOST,
        "--port",
        str(PORT),
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=str(BACKEND_DIR),
        stdout=logf,
        stderr=subprocess.STDOUT,
        shell=False,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
    )
    return proc


def stop_backend(proc: subprocess.Popen) -> None:
    try:
        if os.name == "nt":
            proc.send_signal(2)  # CTRL+C equivalent for new process group
        else:
            proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    except Exception:
        pass


def run(cmd: list[str], cwd: Optional[Path] = None) -> tuple[int, str]:
    try:
        out = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            check=False,
            text=True,
            capture_output=True,
            shell=False,
        )
        return out.returncode, (out.stdout or out.stderr)
    except Exception as e:
        return 1, str(e)


def init_git_repo(root: Path) -> None:
    run(["git", "init"], cwd=root)
    # Ensure user identity for commit on CI
    run(["git", "config", "user.email", "ci@example.com"], cwd=root)
    run(["git", "config", "user.name", "LocalPilot CI"], cwd=root)
    (root / ".gitignore").write_text(".venv\n__pycache__\n", encoding="utf-8")
    (root / "README.md").write_text("# E2E workspace\n", encoding="utf-8")
    run(["git", "add", "-A"], cwd=root)
    run(["git", "commit", "-m", "chore(e2e): init repo"], cwd=root)


def ensure_clean_git(root: Path) -> None:
    """Commit any outstanding changes to satisfy strict safety before apply."""
    code, out = run(["git", "status", "--porcelain"], cwd=root)
    if code == 0 and out.strip():
        # There are changes; commit them
        run(["git", "add", "-A"], cwd=root)
        run(["git", "commit", "-m", "chore(e2e): pre-apply clean"], cwd=root)


async def wait_for_health(timeout_s: float = 30.0) -> None:
    deadline = time.time() + timeout_s
    last_err: Optional[Exception] = None
    async with httpx.AsyncClient(timeout=5.0) as client:
        while time.time() < deadline:
            try:
                r = await client.get(f"{HTTP_BASE}/health")
                if r.status_code == 200:
                    return
            except Exception as e:  # noqa: BLE001
                last_err = e
            await asyncio.sleep(0.3)
    raise RuntimeError(f"Backend health check failed: {last_err}")


def make_envelope(event: str, data: Dict[str, Any], correlation_id: Optional[str] = None) -> Dict[str, Any]:
    env = {
        "event": event,
        "data": data,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "contractVersion": "0.1.0",
    }
    if correlation_id:
        env["correlationId"] = correlation_id
    return env


async def ws_send_recv_until(ws, want_event: str, send_first: Optional[Dict[str, Any]] = None, timeout_s: float = 10.0) -> Dict[str, Any]:
    if send_first is not None:
        await ws.send(json.dumps(send_first))
    deadline = time.time() + timeout_s
    with WS_TRACE.open("a", encoding="utf-8") as f:
        while time.time() < deadline:
            raw = await asyncio.wait_for(ws.recv(), timeout=timeout_s)
            f.write(raw + "\n")
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(msg, dict) and msg.get("event") == want_event:
                return msg
    raise TimeoutError(f"Timed out waiting for event: {want_event}")


async def run_scenario() -> Dict[str, Any]:
    ensure_artifacts_dir()
    # Create temp workspace (no spaces on Windows path if possible)
    tmp_root = Path(tempfile.mkdtemp(prefix="lp-e2e-"))
    workspace = tmp_root / "ws"
    workspace.mkdir(parents=True, exist_ok=True)
    init_git_repo(workspace)

    # Use isolated vector DB path per run to avoid file locks on Windows
    vec_dir = tmp_root / "vectordb"
    vec_dir.mkdir(parents=True, exist_ok=True)
    os.environ["VECTOR_DB_PATH"] = str(vec_dir)

    # 1) Start backend
    proc = start_backend()
    try:
        timings: Dict[str, float] = {}

        # 2) Health
        _t0 = time.time(); await wait_for_health(); timings["health_ms"] = (time.time() - _t0) * 1000

        # 3) WebSocket handshake + heartbeat
        ws_url = f"{WS_URL_BASE}?client_id={CLIENT_ID}"
        async with websockets.connect(ws_url) as ws:
            hs = make_envelope("handshake", {"version": "0.1.0", "clientId": CLIENT_ID})
            msg = await ws_send_recv_until(ws, "handshake_ack", send_first=hs, timeout_s=10.0)
            assert msg["data"]["clientId"] == CLIENT_ID

            hb = make_envelope("heartbeat", {"clientId": CLIENT_ID, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
            hb_msg = await ws_send_recv_until(ws, "heartbeat_ack", send_first=hb, timeout_s=10.0)
            assert "serverTime" in hb_msg.get("data", {})

            # 4) indexing.start broadcast round-trip
            idx = make_envelope(
                "indexing.start",
                {"workspace_path": str(workspace), "options": {}},
            )
            # server broadcasts original event; we wait to see it echoed
            _t = time.time()
            echo = await ws_send_recv_until(ws, "indexing.start", send_first=idx, timeout_s=10.0)
            timings["indexing_broadcast_ms"] = (time.time() - _t) * 1000
            assert echo.get("event") == "indexing.start"

            # 5) REST chat echo smoke (short prompt)
            _t = time.time()
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.post(f"{HTTP_BASE}/chat/echo", json={"prompt": "E2E", "model": "local"})
                r.raise_for_status()
            timings["chat_echo_ms"] = (time.time() - _t) * 1000

            # 5b) Retrieval smoke
            if await is_ollama_online():
                # Semantic path (requires Ollama)
                _t = time.time()
                async with httpx.AsyncClient(timeout=15.0) as client:
                    rr = await client.post(
                        f"{HTTP_BASE}/retrieve",
                        json={
                            "query": "E2E retrieval smoke",
                            "top_k": 1,
                            "debug": False,
                            "user_context": {},
                        },
                    )
                    rr.raise_for_status()
                timings["retrieve_semantic_ms"] = (time.time() - _t) * 1000
            else:
                # Offline path: optionally seed symbol fixture for deterministic query
                if ENABLE_OFFLINE_RETRIEVAL:
                    _t = time.time()
                    await seed_retrieval_fixture()
                    async with httpx.AsyncClient(timeout=15.0) as client:
                        rr = await client.post(
                            f"{HTTP_BASE}/retrieve",
                            json={
                                "query": "E2E_Symbol",
                                "top_k": 1,
                                "debug": False,
                                "user_context": {},
                            },
                        )
                        rr.raise_for_status()
                    timings["retrieve_offline_ms"] = (time.time() - _t) * 1000

            # 6) act.request_approval
            op = {"type": "create", "path": TARGET_FILE, "content": TARGET_CONTENT}
            _t = time.time(); dry = make_envelope(
                "act.request_approval",
                {
                    "workspace_path": str(workspace),
                    "plan_id": PLAN_ID,
                    "todo_id": TODO_ID,
                    "operations": [op],
                },
                correlation_id=EXECUTION_ID,
            )
            preview = await ws_send_recv_until(ws, "act.request_approval", send_first=dry, timeout_s=20.0)
            data = preview.get("data", {})
            ops = data.get("operations", [])
            assert isinstance(ops, list) and len(ops) == 1
            timings["act_dry_run_ms"] = (time.time() - _t) * 1000

            # 7) act.apply (approved)
            # Ensure workspace is clean to satisfy strict safety policy
            ensure_clean_git(workspace)
            _t = time.time(); apply_env = make_envelope(
                "act.apply",
                {
                    "workspace_path": str(workspace),
                    "plan_id": PLAN_ID,
                    "todo_id": TODO_ID,
                    "message": "Apply approved operations",
                    "operations": [op],
                    "approved": True,
                },
                correlation_id=EXECUTION_ID,
            )
            apply_res = await ws_send_recv_until(ws, "act.apply_result", send_first=apply_env, timeout_s=20.0)
            written = apply_res.get("data", {}).get("written", [])
            assert any(p.endswith(TARGET_FILE.replace("\\", "/")) for p in written)
            timings["act_apply_create_ms"] = (time.time() - _t) * 1000

        # Verify file on disk
        target = workspace / TARGET_FILE
        assert target.exists(), f"File not found: {target}"
        assert target.read_text(encoding="utf-8") == TARGET_CONTENT

        # Assert audit file was written
        audit_dir = workspace / ".localpilot" / "audit"
        assert audit_dir.exists()
        audit_files = sorted(audit_dir.glob("*.diff"))
        assert audit_files, "No audit diff written"
        latest_audit = audit_files[-1]
        audit_text = latest_audit.read_text(encoding="utf-8")
        assert "E2E seeded content" in audit_text

        # 8) act.modify then act.delete, and verify
        # Modify
        mod_content = "E2E modified\n"
        mod_op = {"type": "modify", "path": TARGET_FILE, "content": mod_content}
        ensure_clean_git(workspace)
        _t = time.time(); mod_env = make_envelope(
            "act.apply",
            {
                "workspace_path": str(workspace),
                "plan_id": PLAN_ID,
                "todo_id": TODO_ID,
                "message": "Modify file",
                "operations": [mod_op],
                "approved": True,
            },
            correlation_id=EXECUTION_ID,
        )
        async with websockets.connect(f"{WS_URL_BASE}?client_id={CLIENT_ID}") as ws2:
            _ = await ws_send_recv_until(ws2, "act.apply_result", send_first=mod_env, timeout_s=20.0)
        timings["act_apply_modify_ms"] = (time.time() - _t) * 1000
        assert target.read_text(encoding="utf-8") == mod_content

        # Delete
        del_op = {"type": "delete", "path": TARGET_FILE, "content": None}
        ensure_clean_git(workspace)
        _t = time.time(); del_env = make_envelope(
            "act.apply",
            {
                "workspace_path": str(workspace),
                "plan_id": PLAN_ID,
                "todo_id": TODO_ID,
                "message": "Delete file",
                "operations": [del_op],
                "approved": True,
            },
            correlation_id=EXECUTION_ID,
        )
        async with websockets.connect(f"{WS_URL_BASE}?client_id={CLIENT_ID}") as ws3:
            _ = await ws_send_recv_until(ws3, "act.apply_result", send_first=del_env, timeout_s=20.0)
        timings["act_apply_delete_ms"] = (time.time() - _t) * 1000
        assert not target.exists()

        # 9) Local rollback one commit (simulating rollback) then verify file restored absent/present as expected
        # Roll back delete -> file should reappear with modified content
        run(["git", "reset", "--hard", "HEAD~1"], cwd=workspace)
        assert target.exists()
        assert target.read_text(encoding="utf-8") == mod_content

        result = {
            "ok": True,
            "workspace": str(workspace),
            "written": [str(target)],
            "timings_ms": timings,
            "vector_db_path": str(vec_dir),
        }
        return result
    finally:
        stop_backend(proc)
        # Persist minimal tree snapshot for diagnostics
        try:
            (ARTIFACTS_DIR / "tree.txt").write_text("\n".join(str(p.relative_to(REPO_ROOT)) for p in REPO_ROOT.rglob("*")), encoding="utf-8")
        except Exception:
            pass


def main() -> None:
    ensure_artifacts_dir()
    # Flake quarantine: allow skipping this scenario
    flaky_cfg = read_flaky_config()
    skip_list = set(map(str, flaky_cfg.get("skip", [])))
    if SCENARIO_ID in skip_list:
        result = {"ok": True, "skipped": True, "scenario": SCENARIO_ID}
        RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("E2E skipped (quarantined):", json.dumps(result))
        sys.exit(0)

    retry_used = False
    try:
        result = asyncio.run(run_scenario())
        result.update({"scenario": SCENARIO_ID, "retry": False, "flaky": False})
        RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("E2E success:", json.dumps(result))
        sys.exit(0)
    except Exception as first_err:  # noqa: BLE001
        if is_transient_error(first_err):
            retry_used = True
            time.sleep(3)
            try:
                result = asyncio.run(run_scenario())
                # Mark flaky but successful on retry
                result.update({"scenario": SCENARIO_ID, "retry": True, "flaky": True})
                RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
                print("E2E success after retry (flaky):", json.dumps(result))
                sys.exit(0)
            except Exception as second_err:  # noqa: BLE001
                err = {
                    "ok": False,
                    "scenario": SCENARIO_ID,
                    "retry": True,
                    "flaky": False,
                    "error": f"{first_err} | after-retry: {second_err}",
                    "error_type": type(second_err).__name__,
                }
                RESULT_JSON.write_text(json.dumps(err, indent=2), encoding="utf-8")
                print("E2E failure after retry:", err, file=sys.stderr)
                sys.exit(1)
        # Non-transient failure: no retry
        err = {
            "ok": False,
            "scenario": SCENARIO_ID,
            "retry": False,
            "flaky": False,
            "error": str(first_err),
            "error_type": type(first_err).__name__,
        }
        RESULT_JSON.write_text(json.dumps(err, indent=2), encoding="utf-8")
        print("E2E failure:", err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
