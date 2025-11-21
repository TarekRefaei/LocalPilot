from __future__ import annotations

from pathlib import Path

from app.services.indexing.documentation import DocumentationExtractor


def test_markdown_sectioning(tmp_path: Path) -> None:
    md = tmp_path / "README.md"
    md_content = (
        "# Title\n" "\n" "Intro\n" "\n" "## Section A\n" "Text A\n" "\n" "### Sub A1\n" "Text A1\n"
    )
    md.write_text(md_content, encoding="utf-8")

    ex = DocumentationExtractor()
    chunks = ex.process_markdown(md, str(tmp_path))

    # At least 2 sections (Title, Section A)
    assert len(chunks) >= 2
    assert chunks[0].chunk_type == "markdown"
    assert chunks[0].title == "Title"
    assert chunks[0].source_file == "README.md"


def test_jsdoc_extraction() -> None:
    src = (
        "/**\n"
        " * Adds two numbers.\n"
        " * @param a first\n"
        " * @param b second\n"
        " */\n"
        "function add(a, b) { return a + b }\n"
    )
    ex = DocumentationExtractor()
    docs = ex.extract_jsdoc(src)
    assert len(docs) >= 1
    assert "Adds two numbers" in docs[0]["content"]
    # function name captured or None
    assert docs[0].get("function_name") in {"add", None}


def test_python_docstring_extraction() -> None:
    src = '''
class C:
    """A class docstring."""
    def f(self):
        """Function docstring."""
        return 1
'''
    ex = DocumentationExtractor()
    docs = ex.extract_python_docstrings(src)
    assert any("class docstring" in d["content"] for d in docs)
    assert any("Function docstring" in d["content"] for d in docs)
