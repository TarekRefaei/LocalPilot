from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from app.services.indexing.orchestrator import IndexingOrchestrator


class FakeManager:
    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []

    async def broadcast(self, message: dict) -> None:
        # Store envelope dicts
        self.messages.append(message)


@pytest.mark.asyncio
async def test_orchestrator_emits_progress_and_complete(tmp_path: Path) -> None:
    # Create tiny sample repo
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.ts").write_text("console.log(1)\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Title\nIntro\n", encoding="utf-8")

    mgr = FakeManager()
    orch = IndexingOrchestrator(mgr)  # type: ignore[arg-type]

    await orch.run(str(tmp_path))

    # There should be at least one progress and one complete envelope
    events = [m.get("event") for m in mgr.messages]
    assert "indexing.progress" in events
    assert "indexing.complete" in events

    # Validate complete payload shape
    complete = next(m for m in mgr.messages if m.get("event") == "indexing.complete")
    data = complete.get("data") or {}
    assert "indexing_id" in data
    assert "duration_seconds" in data
    stats = data.get("statistics") or {}
    assert "total_files" in stats
    assert stats.get("total_files", 0) >= 2
