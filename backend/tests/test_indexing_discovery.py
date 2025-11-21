from __future__ import annotations

from pathlib import Path

import pytest

from app.services.indexing.discovery import DiscoveryExecutor


@pytest.mark.asyncio
async def test_discovery_honors_gitignore_and_excludes(tmp_path: Path) -> None:
    # Layout
    (tmp_path / "src").mkdir()
    (tmp_path / "node_modules").mkdir()
    (tmp_path / ".git").mkdir()

    # Files
    (tmp_path / "README.md").write_text("# Title\n", encoding="utf-8")
    (tmp_path / "src" / "main.ts").write_text("console.log(1)\n", encoding="utf-8")
    (tmp_path / "src" / ".hidden.ts").write_text("console.log(2)\n", encoding="utf-8")
    (tmp_path / "node_modules" / "lib.js").write_text("ignored\n", encoding="utf-8")

    # Binary file
    (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00")

    # .gitignore exclude
    (tmp_path / ".gitignore").write_text("*.log\nsecret/\n", encoding="utf-8")
    (tmp_path / "build.log").write_text("log\n", encoding="utf-8")
    (tmp_path / "secret").mkdir()
    (tmp_path / "secret" / "note.txt").write_text("nope\n", encoding="utf-8")

    ex = DiscoveryExecutor()
    res = await ex.execute(str(tmp_path))

    # Validations
    # hidden file and node_modules and .git and binary and .gitignore patterns excluded
    file_names = {p.name for p in res.files}
    assert "main.ts" in file_names
    assert "README.md" in file_names
    assert "image.png" not in file_names
    assert "lib.js" not in file_names
    assert ".hidden.ts" not in file_names
    assert "build.log" not in file_names

    # Categorization
    assert res.files_by_type.get("typescript", 0) == 1
    assert res.files_by_type.get("markdown", 0) == 1

    # Root files detection
    assert "README.md" in res.root_files


@pytest.mark.asyncio
async def test_discovery_project_type_detection(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text('{"name":"x"}', encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "App.tsx").write_text("export {}", encoding="utf-8")

    ex = DiscoveryExecutor()
    res = await ex.execute(str(tmp_path))
    assert res.project_type in {"react", "generic"}
