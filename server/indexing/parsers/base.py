from pathlib import Path
from typing import Any


class ParseResult:
    def __init__(self, ast: Any, source: str):
        self.ast = ast
        self.source = source


class BaseParser:
    language: str

    def parse(self, path: Path) -> ParseResult:
        raise NotImplementedError("Parser must implement parse()")
