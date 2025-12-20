import json
from pathlib import Path
from typing import List, Dict

from .chunk import CodeChunk


class SymbolIndex:
    def __init__(self, root: Path):
        self.path = root / "symbols.json"
        self._symbols: List[Dict] = []

    def add(self, file: str, symbol_type: str, start_line: int, end_line: int) -> None:
        self._symbols.append(
            {
                "file": file,
                "symbol_type": symbol_type,
                "start_line": start_line,
                "end_line": end_line,
            }
        )

    def add_chunk(self, chunk: CodeChunk) -> None:
        if chunk.symbol_type == "file":
            return
        self.add(
            file=chunk.file_path,
            symbol_type=chunk.symbol_type,
            start_line=chunk.start_line,
            end_line=chunk.end_line,
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._symbols, f, indent=2)
