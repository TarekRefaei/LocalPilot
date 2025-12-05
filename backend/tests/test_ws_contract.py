# backend/tests/test_ws_contract.py
import os


def test_ws_event_names_present():
    """
    Basic presence test: ensure common WS event names appear somewhere in backend source/docs.
    This is a heuristic guard to catch accidental renames/removals.
    """
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    target = os.path.join(repo_root, "backend")

    required = [
        "indexing.start",
        "indexing.progress",
        "indexing.complete",
        "chat.message",
        "plan.generate",
        "act.start",
        "act.request_approval",
        "act.apply_result",
        "act.error",
        "heartbeat_ack",  # response event
        "handshake_ack",  # response event
    ]

    misses = []
    for r in required:
        found = False
        for subdir, _dirs, files in os.walk(target):
            for f in files:
                if not f.endswith((".py", ".md", ".json", ".yml", ".yaml")):
                    continue
                path = os.path.join(subdir, f)
                try:
                    with open(path, encoding="utf-8", errors="ignore") as fh:
                        if r in fh.read():
                            found = True
                            break
                except Exception:
                    continue
            if found:
                break
        if not found:
            misses.append(r)

    assert not misses, f"Missing WS event names in repository: {misses}"
