from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DocumentChunk:
    id: str
    content: str
    source_file: str
    chunk_type: str  # 'markdown' | 'jsdoc' | 'docstring'
    title: str | None = None
    section: str | None = None


class DocumentationExtractor:
    def find_markdown_files(self, files: list[Path]) -> list[Path]:
        return [f for f in files if f.suffix.lower() in {".md", ".markdown", ".rst"}]

    def find_code_files(self, files: list[Path]) -> list[Path]:
        code_exts = {".ts", ".tsx", ".js", ".jsx", ".py"}
        return [f for f in files if f.suffix.lower() in code_exts]

    def process_markdown(
        self, filepath: Path, workspace_path: str
    ) -> list[DocumentChunk]:
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return []

        sections = self._split_markdown_sections(content)
        chunks: list[DocumentChunk] = []
        for i, sec in enumerate(sections):
            if not sec["content"].strip():
                continue
            chunks.append(
                DocumentChunk(
                    id=f"{filepath.stem}-{i}",
                    content=sec["content"],
                    source_file=str(
                        Path(filepath)
                        .resolve()
                        .relative_to(Path(workspace_path).resolve())
                    ),
                    chunk_type="markdown",
                    title=sec.get("title"),
                    section=sec.get("section"),
                )
            )
        return chunks

    def _split_markdown_sections(self, content: str) -> list[dict]:
        sections: list[dict] = []
        current = {"content": "", "title": None, "section": None}
        for line in content.splitlines():
            m = re.match(r"^(#{1,6})\s+(.+)$", line)
            if m:
                if current["content"]:
                    sections.append(current)
                level = len(m.group(1))
                current = {
                    "content": line + "\n",
                    "title": m.group(2),
                    "section": f"h{level}",
                }
            else:
                current["content"] += line + "\n"
        if current["content"]:
            sections.append(current)
        return sections

    def extract_jsdoc(self, content: str) -> list[dict]:
        pattern = r"/\*\*\s*(.*?)\s*\*/"
        matches = re.finditer(pattern, content, re.DOTALL)
        docs: list[dict] = []
        for m in matches:
            raw = m.group(1)
            lines = raw.split("\n")
            cleaned_lines = [re.sub(r"^\s*\*\s?", "", ln) for ln in lines]
            cleaned = "\n".join(cleaned_lines).strip()
            if len(cleaned) <= 10:
                continue
            after = content[m.end() : m.end() + 200]
            func = re.search(r"(?:function\s+)?(\w+)\s*\(", after)
            docs.append(
                {"content": cleaned, "function_name": func.group(1) if func else None}
            )
        return docs

    def extract_python_docstrings(self, content: str) -> list[dict]:
        pattern = r'(?:"""|\'\'\')(.*?)(?:"""|\'\'\')'
        matches = re.finditer(pattern, content, re.DOTALL)
        docs: list[dict] = []
        for m in matches:
            doc = m.group(1).strip()
            if len(doc) <= 10:
                continue
            before = content[max(0, m.start() - 200) : m.start()]
            func = re.search(r"(?:def|class)\s+(\w+)", before)
            docs.append(
                {"content": doc, "function_name": func.group(1) if func else None}
            )
        return docs

    def extract_docstrings(
        self, filepath: Path, workspace_path: str
    ) -> list[DocumentChunk]:
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return []

        chunks: list[DocumentChunk] = []
        if filepath.suffix.lower() in {".ts", ".tsx", ".js", ".jsx"}:
            docs = self.extract_jsdoc(content)
            for i, d in enumerate(docs):
                chunks.append(
                    DocumentChunk(
                        id=f"{filepath.stem}-jsdoc-{i}",
                        content=d["content"],
                        source_file=str(
                            Path(filepath)
                            .resolve()
                            .relative_to(Path(workspace_path).resolve())
                        ),
                        chunk_type="jsdoc",
                        title=d.get("function_name"),
                    )
                )
        elif filepath.suffix.lower() == ".py":
            docs = self.extract_python_docstrings(content)
            for i, d in enumerate(docs):
                chunks.append(
                    DocumentChunk(
                        id=f"{filepath.stem}-docstring-{i}",
                        content=d["content"],
                        source_file=str(
                            Path(filepath)
                            .resolve()
                            .relative_to(Path(workspace_path).resolve())
                        ),
                        chunk_type="docstring",
                        title=d.get("function_name"),
                    )
                )
        return chunks
