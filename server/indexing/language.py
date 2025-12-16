from pathlib import Path


EXTENSION_LANGUAGE_MAP = {
    ".ts": "typescript",
    ".js": "javascript",
    ".py": "python",
    ".dart": "dart",
    ".json": "json",
    ".md": "markdown"
}


def detect_language(path: Path) -> str | None:
    return EXTENSION_LANGUAGE_MAP.get(path.suffix)
