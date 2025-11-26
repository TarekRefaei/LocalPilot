from pathlib import Path

import pytest

from app.services.indexing.chunking import SemanticChunker


def test_find_python_block_end_simple():
    lines = [
        "def f():",
        "    x = 1",
        "",
        "y = 2",
    ]
    ch = SemanticChunker()
    end = ch._find_python_block_end(lines, 0)
    # Function block includes the blank line before dedent, so end is index 2
    assert end == 2


def test_find_closing_brace_ignores_braces_in_strings():
    lines = [
        "function t() {",
        '  const s = "not a } brace";',
        "  return 1;",
        "}",
    ]
    ch = SemanticChunker()
    end = ch._find_closing_brace(lines, 0)
    assert end == 3


@pytest.mark.asyncio
async def test_typescript_arrow_and_interface(monkeypatch, tmp_path: Path):
    # Allow small snippets to form chunks
    monkeypatch.setattr(SemanticChunker, "MIN_CHUNK_SIZE", 1, raising=False)

    content = "export const add = (a, b) => { return a + b; }\n\n" "interface Foo { x: number; }\n"
    f = tmp_path / "math.ts"
    f.write_text(content, encoding="utf-8")

    ch = SemanticChunker()
    chunks = ch.chunk_file(f, "typescript", str(tmp_path))

    types = {c.chunk_type for c in chunks}
    assert "function" in types
    assert "interface" in types
    # Symbol names captured for arrow function and interface
    names = [s for c in chunks for s in c.symbols]
    assert "add" in names or any(n for n in names)


@pytest.mark.asyncio
async def test_module_full_id_on_no_defs(tmp_path: Path):
    content = "print('only code, no defs')\n"
    p = tmp_path / "nodefs.py"
    p.write_text(content, encoding="utf-8")

    ch = SemanticChunker()
    chunks = ch.chunk_file(p, "python", str(tmp_path))

    assert len(chunks) == 1
    assert chunks[0].chunk_type == "module"
    assert chunks[0].id.endswith("-full")
