from dataclasses import dataclass


@dataclass(frozen=True)
class CodeChunk:
    id: str
    file_path: str
    language: str
    start_line: int
    end_line: int
    content: str
    symbol_type: str  # function, class, module, block
