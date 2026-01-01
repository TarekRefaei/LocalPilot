from pathlib import Path
from typing import Dict


class WorkspaceReader:
    """
    Read-only, allowlist-based workspace access.
    """

    def __init__(self, workspace_root: Path):
        self.root = workspace_root.resolve()

    def read_file(self, relative_path: str) -> str:
        path = (self.root / relative_path).resolve()

        if not path.exists() or not path.is_file():
            raise FileNotFoundError(relative_path)

        if self.root not in path.parents:
            raise PermissionError("Path escape attempt detected")

        return path.read_text(encoding="utf-8", errors="ignore")
