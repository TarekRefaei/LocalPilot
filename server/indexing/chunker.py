import hashlib
import re
from typing import List

from .chunk import CodeChunk


class SemanticChunker:
    """
    Phase 2.5
    ----------
    Semantic, regex-based chunker.

    Guarantees:
    - File-level chunk always exists
    - Symbol-level chunks are non-overlapping
    - Chunk IDs are deterministic and UNIQUE
    """

    def chunk_file(
        self,
        file_path: str,
        language: str,
        source: str
    ) -> List[CodeChunk]:

        lines = source.splitlines()
        total_lines = len(lines)
        chunks: List[CodeChunk] = []

        # -------------------------
        # File-level chunk
        # -------------------------
        file_content = source.strip()
        if file_content:
            chunks.append(
                CodeChunk(
                    id=self._stable_id(
                        file_path,
                        1,
                        total_lines,
                        "file",
                        file_content,
                    ),
                    file_path=file_path,
                    language=language,
                    start_line=1,
                    end_line=total_lines,
                    content=file_content,
                    symbol_type="file",
                )
            )

        # -------------------------
        # Symbol-level chunking
        # -------------------------
        if language == "python":
            chunks.extend(self._chunk_python(source, file_path, language))
        elif language in {"typescript", "javascript"}:
            chunks.extend(self._chunk_js_ts(source, file_path, language))

        return chunks

    # ==========================================================
    # ID generation (CRITICAL)
    # ==========================================================
    def _stable_id(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        symbol_type: str,
        content: str,
    ) -> str:
        """
        Deterministic & unique chunk identity.
        """
        h = hashlib.sha256()
        h.update(file_path.encode("utf-8"))
        h.update(str(start_line).encode("utf-8"))
        h.update(str(end_line).encode("utf-8"))
        h.update(symbol_type.encode("utf-8"))
        h.update(content.encode("utf-8"))
        return h.hexdigest()

    # ==========================================================
    # Helpers
    # ==========================================================
    def _slice_content(self, src: str, start_line: int, end_line: int) -> str:
        lines = src.splitlines()
        return "\n".join(lines[start_line - 1 : end_line]).strip()

    # ==========================================================
    # Python chunking
    # ==========================================================
    def _chunk_python(
        self,
        source: str,
        file_path: str,
        language: str
    ) -> List[CodeChunk]:

        lines = source.splitlines()
        n = len(lines)
        chunks: List[CodeChunk] = []

        def indent(s: str) -> int:
            return len(s.replace("\t", "    ")) - len(s.lstrip(" "))

        symbols: List[tuple[int, str]] = []  # (line_no, type)

        for i, line in enumerate(lines, start=1):
            if indent(line) != 0:
                continue
            if re.match(r"^\s*class\s+\w+", line):
                symbols.append((i, "class"))
            elif re.match(r"^\s*def\s+\w+\s*\(", line):
                symbols.append((i, "function"))

        for idx, (start, symbol_type) in enumerate(symbols):
            end = n
            start_indent = indent(lines[start - 1])

            for j in range(idx + 1, len(symbols)):
                next_line = symbols[j][0]
                if indent(lines[next_line - 1]) <= start_indent:
                    end = next_line - 1
                    break

            content = self._slice_content(source, start, end)
            if not content or len(content.strip()) < 10:
                continue

            chunks.append(
                CodeChunk(
                    id=self._stable_id(
                        file_path,
                        start,
                        end,
                        symbol_type,
                        content,
                    ),
                    file_path=file_path,
                    language=language,
                    start_line=start,
                    end_line=end,
                    content=content,
                    symbol_type=symbol_type,
                )
            )

        return chunks

    # ==========================================================
    # JS / TS chunking
    # ==========================================================
    def _find_block_end(self, lines: List[str], start_idx: int) -> int:
        depth = 0
        for i in range(start_idx, len(lines)):
            depth += lines[i].count("{")
            depth -= lines[i].count("}")
            if depth == 0 and "{" in lines[start_idx]:
                return i + 1
        return len(lines)

    def _chunk_js_ts(
        self,
        source: str,
        file_path: str,
        language: str
    ) -> List[CodeChunk]:

        lines = source.splitlines()
        chunks: List[CodeChunk] = []

        patterns = {
            "class": re.compile(r"^\s*(export\s+)?class\s+\w+"),
            "function": re.compile(r"^\s*(export\s+)?function\s+\w+"),
            "interface": re.compile(r"^\s*(export\s+)?interface\s+\w+"),
        }

        i = 0
        while i < len(lines):
            line = lines[i]

            for symbol_type, pat in patterns.items():
                if pat.match(line):
                    start = i + 1
                    end = self._find_block_end(lines, i)
                    content = self._slice_content(source, start, end)

                    if content and len(content.strip()) >= 10:
                        chunks.append(
                            CodeChunk(
                                id=self._stable_id(
                                    file_path,
                                    start,
                                    end,
                                    symbol_type,
                                    content,
                                ),
                                file_path=file_path,
                                language=language,
                                start_line=start,
                                end_line=end,
                                content=content,
                                symbol_type=symbol_type,
                            )
                        )
                    i = end
                    break
            else:
                i += 1

        return chunks