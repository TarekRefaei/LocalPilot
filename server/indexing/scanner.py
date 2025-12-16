from pathlib import Path
from typing import List

EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "__pycache__",
    ".localpilot"
}

SUPPORTED_EXTENSIONS = {
    ".ts", ".js", ".py", ".json", ".md", ".dart"
}


class WorkspaceScanner:
    def scan(self, root: Path) -> List[Path]:
        files: List[Path] = []

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if any(part in EXCLUDED_DIRS for part in path.parts):
                continue

            if path.suffix not in SUPPORTED_EXTENSIONS:
                continue

            files.append(path)

        return sorted(files)
