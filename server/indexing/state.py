import json
from pathlib import Path
from typing import Dict


class IndexState:
    def __init__(self, root: Path):
        self.path = root / "state.json"
        self.file_hashes: Dict[str, str] = {}

    def load(self) -> None:
        if not self.path.exists():
            return
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.file_hashes = data.get("file_hashes", {})

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                {"file_hashes": self.file_hashes},
                f,
                indent=2
            )
