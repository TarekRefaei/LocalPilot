"""
Symbol and Import Maps for Cross-File References

Tracks symbols (functions, classes) across chunks and maintains
import relationships for retrieval context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .chunking import CodeChunk


@dataclass
class Symbol:
    """Symbol definition extracted from code."""

    name: str
    kind: str  # 'function', 'class', 'interface', 'type', 'variable'
    file_path: str
    start_line: int
    end_line: int
    chunk_id: str
    parent: str | None = None  # Parent class for methods
    is_exported: bool = False


@dataclass
class ImportLink:
    """Import relationship between files."""

    from_file: str
    to_module: str
    imports: list[str] = field(default_factory=list)  # Imported names
    line: int = 0


class SymbolMap:
    """Map of all symbols in the indexed codebase."""

    def __init__(self) -> None:
        """Initialize symbol map."""
        self.symbols: dict[str, list[Symbol]] = {}  # file_path -> [Symbol]
        self.symbol_index: dict[str, Symbol] = {}  # symbol_name -> Symbol (global)
        self.symbol_chunks: dict[str, set[str]] = {}  # symbol_name -> chunk_ids

    def add_symbol(self, symbol: Symbol) -> None:
        """Add a symbol to the map."""
        if symbol.file_path not in self.symbols:
            self.symbols[symbol.file_path] = []

        self.symbols[symbol.file_path].append(symbol)

        # Add to global index
        key = f"{symbol.file_path}:{symbol.name}"
        self.symbol_index[key] = symbol

        # Track chunks containing this symbol
        if symbol.name not in self.symbol_chunks:
            self.symbol_chunks[symbol.name] = set()
        self.symbol_chunks[symbol.name].add(symbol.chunk_id)

    def get_symbol(self, name: str, file_path: str | None = None) -> Symbol | None:
        """Get a symbol by name, optionally scoped to file."""
        if file_path:
            key = f"{file_path}:{name}"
            return self.symbol_index.get(key)

        # Search all scopes
        for symbol in self.symbol_index.values():
            if symbol.name == name:
                return symbol

        return None

    def get_symbols_in_file(self, file_path: str) -> list[Symbol]:
        """Get all symbols defined in a file."""
        return self.symbols.get(file_path, [])

    def get_chunk_ids_for_symbol(self, symbol_name: str) -> set[str]:
        """Get all chunk IDs that contain a symbol."""
        return self.symbol_chunks.get(symbol_name, set())

    def build_from_chunks(self, chunks: list[CodeChunk]) -> None:
        """Build symbol map from code chunks."""
        for chunk in chunks:
            for symbol_name in chunk.symbols:
                symbol = Symbol(
                    name=symbol_name,
                    kind=chunk.chunk_type,
                    file_path=chunk.file_path,
                    start_line=chunk.start_line,
                    end_line=chunk.end_line,
                    chunk_id=chunk.id,
                    parent=chunk.parent_context,
                    is_exported="export" in chunk.content.split("\n")[0],
                )
                self.add_symbol(symbol)

    def to_dict(self) -> dict[str, Any]:
        """Serialize symbol map to dictionary."""
        return {
            "symbols": {
                file_path: [
                    {
                        "name": s.name,
                        "kind": s.kind,
                        "line": s.start_line,
                        "parent": s.parent,
                        "exported": s.is_exported,
                    }
                    for s in symbols
                ]
                for file_path, symbols in self.symbols.items()
            },
            "total_symbols": len(self.symbol_index),
        }


class ImportMap:
    """Map of import relationships between files."""

    def __init__(self) -> None:
        """Initialize import map."""
        self.imports: list[ImportLink] = []
        self.file_imports: dict[str, list[ImportLink]] = {}  # file -> imports

    def add_import(self, link: ImportLink) -> None:
        """Add an import relationship."""
        self.imports.append(link)

        if link.from_file not in self.file_imports:
            self.file_imports[link.from_file] = []

        self.file_imports[link.from_file].append(link)

    def get_imports_in_file(self, file_path: str) -> list[ImportLink]:
        """Get all imports in a file."""
        return self.file_imports.get(file_path, [])

    def get_files_importing(self, module: str) -> list[str]:
        """Get all files that import a module."""
        files = set()
        for link in self.imports:
            if link.to_module == module:
                files.add(link.from_file)
        return list(files)

    def build_from_chunks(self, chunks: list[CodeChunk]) -> None:
        """Build import map from code chunks."""
        seen_imports: set[tuple[str, str]] = set()

        for chunk in chunks:
            for import_module in chunk.imports:
                key = (chunk.file_path, import_module)
                if key not in seen_imports:
                    link = ImportLink(
                        from_file=chunk.file_path,
                        to_module=import_module,
                        imports=[],  # Could be refined per chunk
                        line=chunk.start_line,
                    )
                    self.add_import(link)
                    seen_imports.add(key)

    def to_dict(self) -> dict[str, Any]:
        """Serialize import map to dictionary."""
        return {
            "imports": [
                {
                    "from": link.from_file,
                    "to": link.to_module,
                    "count": len(link.imports),
                }
                for link in self.imports
            ],
            "total_imports": len(self.imports),
        }


class SymbolImportMapBuilder:
    """Builder for symbol and import maps."""

    @staticmethod
    def build(chunks: list[CodeChunk]) -> tuple[SymbolMap, ImportMap]:
        """Build symbol and import maps from chunks.

        Returns:
            Tuple of (symbol_map, import_map)
        """
        symbol_map = SymbolMap()
        import_map = ImportMap()

        symbol_map.build_from_chunks(chunks)
        import_map.build_from_chunks(chunks)

        return symbol_map, import_map

    @staticmethod
    def validate_determinism(chunks1: list[CodeChunk], chunks2: list[CodeChunk]) -> bool:
        """Validate that chunking is deterministic across runs.

        Compares two runs and checks:
        - Same number of chunks
        - Same chunk boundaries (line numbers)
        - Same symbols extracted

        Returns:
            True if deterministic, False otherwise
        """
        if len(chunks1) != len(chunks2):
            return False

        for c1, c2 in zip(chunks1, chunks2):
            if (
                c1.file_path != c2.file_path
                or c1.start_line != c2.start_line
                or c1.end_line != c2.end_line
                or c1.symbols != c2.symbols
            ):
                return False

        return True
