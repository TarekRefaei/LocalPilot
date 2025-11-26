from pathlib import Path

import pytest

from app.services.indexing.chunking import SemanticChunker


@pytest.mark.asyncio
async def test_chunking_python_definitions_and_imports(monkeypatch, tmp_path: Path):
    # Lower threshold to force chunk creation for small fixtures
    monkeypatch.setattr(SemanticChunker, "MIN_CHUNK_SIZE", 1, raising=False)

    content = (
        "import os\n"
        "from math import sqrt\n\n"
        "def foo(x):\n"
        "    return x + 1\n\n"
        "class Bar:\n"
        "    def baz(self, y):\n"
        "        return y * 2\n"
    )
    f = tmp_path / "sample.py"
    f.write_text(content, encoding="utf-8")

    chunker = SemanticChunker()
    chunks = chunker.chunk_file(f, "python", str(tmp_path))

    # Expect at least function and class chunks
    types = {c.chunk_type for c in chunks}
    assert "function" in types or "method" in types
    assert "class" in types

    # Imports should be attached to chunks
    assert any("math" in c.imports for c in chunks)

    # Symbols captured on chunks
    all_symbols = [s for c in chunks for s in c.symbols]
    assert any(sym in all_symbols for sym in ["foo", "Bar"])  # either symbol present


@pytest.mark.asyncio
async def test_chunking_typescript_function_and_class(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(SemanticChunker, "MIN_CHUNK_SIZE", 1, raising=False)

    content = (
        "import _ from 'lodash';\n\n"
        "export function hello(name) {\n"
        "  return `hi ${name}`;\n"
        "}\n\n"
        "export class Greeter {\n"
        "  greet(who) {\n"
        "    return 'hello ' + who;\n"
        "  }\n"
        "}\n"
    )
    f = tmp_path / "greeter.ts"
    f.write_text(content, encoding="utf-8")

    chunker = SemanticChunker()
    chunks = chunker.chunk_file(f, "typescript", str(tmp_path))

    # Expect function and class chunks
    types = {c.chunk_type for c in chunks}
    assert "function" in types
    assert "class" in types or "method" in types

    # Imports captured
    assert any("lodash" in c.imports for c in chunks)


@pytest.mark.asyncio
async def test_chunking_no_definitions_fallback_module(tmp_path: Path):
    content = "# just comments and small content\n" "import os\n\n" "print('hello')\n"
    f = tmp_path / "minimal.py"
    f.write_text(content, encoding="utf-8")

    chunker = SemanticChunker()
    chunks = chunker.chunk_file(f, "python", str(tmp_path))

    # Without lowering MIN_CHUNK_SIZE, small defs won't form; expect whole-file module chunk
    assert len(chunks) == 1
    assert chunks[0].chunk_type == "module"
    assert chunks[0].start_line == 1
    # end_line equals total split-by-"\n" lines (includes trailing blank if any)
    assert chunks[0].end_line == len(content.split("\n"))
