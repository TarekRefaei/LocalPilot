from pathlib import Path

import pytest

from app.services.indexing.chunking import ChunkingExecutor, SemanticChunker


def test_extract_all_imports_python_from_and_import():
    lines = [
        "from collections import defaultdict",
        "import os",
        "print('x')",
    ]
    ch = SemanticChunker()
    imports = ch._extract_all_imports(lines, "python")
    assert "collections" in imports
    assert "os" in imports


def test_extract_all_imports_ts_require():
    lines = [
        "require('fs')",
        "function f() { return 1 }",
    ]
    ch = SemanticChunker()
    imports = ch._extract_all_imports(lines, "typescript")
    assert "fs" in imports


def test_find_closing_brace_no_match_returns_start():
    lines = [
        "export const a = 1;",
        "// no braces here",
    ]
    ch = SemanticChunker()
    assert ch._find_closing_brace(lines, 0) == 0


def test_make_lexical_chunk_id_and_estimate_tokens(tmp_path: Path):
    ws = tmp_path / "ws"
    ws.mkdir()
    nested = ws / "dir" / "subdir"
    nested.mkdir(parents=True)
    fp = nested / "file.ts"
    fp.write_text("export function f() { return 1; }\n", encoding="utf-8")

    ch = SemanticChunker()
    cid = ch._make_lexical_chunk_id(fp, str(ws), 0, 0)
    # Always forward slashes
    assert "/" in cid and "\\" not in cid

    tokens = ch._estimate_tokens("one two three four")
    assert tokens >= 1


@pytest.mark.asyncio
async def test_executor_execute_mixed_files(monkeypatch, tmp_path: Path):
    # Lower to ensure chunks for small snippets
    monkeypatch.setattr(SemanticChunker, "MIN_CHUNK_SIZE", 1, raising=False)

    ws = tmp_path / "ws2"
    ws.mkdir()

    py = ws / "a.py"
    py.write_text("def f():\n    return 1\n", encoding="utf-8")

    ts = ws / "b.ts"
    ts.write_text("export function g() { return 2; }\n", encoding="utf-8")

    other = ws / "c.txt"
    other.write_text("ignored\n", encoding="utf-8")

    execu = ChunkingExecutor()
    chunks, metrics = await execu.execute(str(ws), [py, ts, other])

    # Only .py and .ts counted
    assert metrics["total_files"] == 3
    assert metrics["files_chunked"] == 2
    assert metrics["total_chunks"] == len(chunks)
    assert metrics["avg_tokens"] > 0
    # Chunk types should include function
    assert any(c.chunk_type == "function" for c in chunks)


def test_find_python_block_end_start_ge_len():
    ch = SemanticChunker()
    lines = ["def a():", "    pass"]
    assert ch._find_python_block_end(lines, len(lines)) == len(lines)


@pytest.mark.asyncio
async def test_ts_class_and_es_imports(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(SemanticChunker, "MIN_CHUNK_SIZE", 1, raising=False)

    content = (
        "import { map as fmap } from 'lodash'\n\n" "export class A {\n" "  m() { return; }\n" "}\n"
    )
    fp = tmp_path / "cls.ts"
    fp.write_text(content, encoding="utf-8")

    ch = SemanticChunker()
    chunks = ch.chunk_file(fp, "typescript", str(tmp_path))
    types = {c.chunk_type for c in chunks}
    assert "class" in types
    assert any("lodash" in c.imports for c in chunks)


@pytest.mark.asyncio
async def test_python_class_and_top_level_func(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(SemanticChunker, "MIN_CHUNK_SIZE", 1, raising=False)

    content = "class A:\n" "    def x(self):\n" "        return 1\n\n" "def y():\n" "    return 2\n"
    fp = tmp_path / "mix.py"
    fp.write_text(content, encoding="utf-8")

    ch = SemanticChunker()
    chunks = ch.chunk_file(fp, "python", str(tmp_path))
    types = {c.chunk_type for c in chunks}
    assert "class" in types and "function" in types
    names = [s for c in chunks for s in c.symbols]
    assert "A" in names or "y" in names


@pytest.mark.asyncio
async def test_ts_interface_multiline(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(SemanticChunker, "MIN_CHUNK_SIZE", 1, raising=False)

    content = "interface Foo {\n" "  x: number;\n" "  y: string;\n" "}\n"
    fp = tmp_path / "iface.ts"
    fp.write_text(content, encoding="utf-8")

    ch = SemanticChunker()
    chunks = ch.chunk_file(fp, "typescript", str(tmp_path))
    assert any(c.chunk_type == "interface" for c in chunks)
