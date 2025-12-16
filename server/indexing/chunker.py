import hashlib
from typing import List

from .chunk import CodeChunk


class SemanticChunker:
    def chunk_file(
        self,
        file_path: str,
        language: str,
        source: str
    ) -> List[CodeChunk]:
        """
        Fallback semantic chunking:
        - Entire file = single chunk
        - Used until AST-aware chunkers are plugged in
        """

        lines = source.splitlines()
        content = source.strip()

        chunk_id = self._stable_id(file_path, content)

        return [
            CodeChunk(
                id=chunk_id,
                file_path=file_path,
                language=language,
                start_line=1,
                end_line=len(lines),
                content=content,
                symbol_type="file"
            )
        ]

    def _stable_id(self, file_path: str, content: str) -> str:
        h = hashlib.sha256()
        h.update(file_path.encode("utf-8"))
        h.update(content.encode("utf-8"))
        return h.hexdigest()
