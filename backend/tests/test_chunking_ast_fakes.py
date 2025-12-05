from pathlib import Path

import pytest

from app.services.indexing.chunking import CodeChunk, SemanticChunker


class FakeNode:
    def __init__(
        self,
        type_: str,
        name_text: str | None = None,
        start=(0, 0),
        end=(0, 0),
        children=None,
    ):
        self.type = type_
        self._name_text = name_text
        self.start_point = start
        self.end_point = end
        self.children = children or []

    # Tree-sitter API compatibility used by code under test
    def child_by_field_name(self, field: str):
        if field == "name" and self._name_text is not None:
            # Return another FakeNode representing the name node
            return FakeNode("identifier", name_text=self._name_text)
        return None


@pytest.mark.asyncio
async def test_get_node_type_and_declaration_name_and_make_chunk_id(
    tmp_path: Path, monkeypatch
):
    ch = SemanticChunker()

    # Monkeypatch _get_node_text to return the name for identifier nodes
    monkeypatch.setattr(ch, "_get_node_text", lambda node, fp: (node._name_text or ""))

    fp = tmp_path / "file.ts"
    fp.write_text("// x\n", encoding="utf-8")

    # function_declaration
    fn = FakeNode("function_declaration", name_text="hello", start=(1, 0), end=(3, 0))
    assert ch._get_node_type(fn) == "function"
    assert ch._get_declaration_name(fn, fp) == "hello"
    cid = ch._make_chunk_id(fp, str(tmp_path), fn)
    assert cid.endswith("1-3")

    # class_declaration
    cls = FakeNode("class_declaration", name_text="Greeter", start=(5, 0), end=(10, 0))
    assert ch._get_node_type(cls) == "class"
    assert ch._get_declaration_name(cls, fp) == "Greeter"


@pytest.mark.asyncio
async def test_split_python_class_with_methods(tmp_path: Path, monkeypatch):
    ch = SemanticChunker()

    # Ensure short text counts as tokens
    monkeypatch.setattr(ch, "_estimate_tokens", lambda text: 5)
    monkeypatch.setattr(ch, "_get_node_text", lambda node, fp: "def body\n")
    monkeypatch.setattr(
        ch, "_get_declaration_name", lambda node, fp: (node._name_text or "")
    )

    fp = tmp_path / "c.py"
    fp.write_text("# py\n", encoding="utf-8")

    m1 = FakeNode("function_definition", name_text="m1", start=(2, 0), end=(4, 0))
    m2 = FakeNode("function_definition", name_text="m2", start=(5, 0), end=(7, 0))
    cls = FakeNode(
        "class_definition", name_text="C", start=(1, 0), end=(8, 0), children=[m1, m2]
    )

    chunks = ch._split_python_class(cls, fp, str(tmp_path), imports=["os"])  # type: ignore[arg-type]
    assert len(chunks) == 2
    assert all(isinstance(c, CodeChunk) for c in chunks)
    assert all(c.chunk_type == "method" for c in chunks)
    assert any("C" in c.symbols for c in chunks)


@pytest.mark.asyncio
async def test_split_ts_class_fallback_methods(tmp_path: Path, monkeypatch):
    ch = SemanticChunker()

    # For TS path: provide class_body with method_definition child
    method = FakeNode("method_definition", name_text="g", start=(2, 0), end=(3, 0))
    body = FakeNode("class_body", children=[method])
    cls = FakeNode(
        "class_declaration", name_text="A", start=(1, 0), end=(5, 0), children=[body]
    )

    monkeypatch.setattr(
        ch, "_get_declaration_name", lambda node, fp: (node._name_text or "")
    )
    monkeypatch.setattr(ch, "_get_node_text", lambda node, fp: "body\n")
    monkeypatch.setattr(ch, "_estimate_tokens", lambda text: 5)

    fp = tmp_path / "a.ts"
    fp.write_text("// ts\n", encoding="utf-8")

    chunks = ch._split_class_declaration(cls, fp, str(tmp_path), imports=["lodash"])  # type: ignore[arg-type]
    assert any(c.chunk_type == "method" for c in chunks)
    assert any("A" in c.symbols for c in chunks)
