import json
from pathlib import Path
from typing import List, Dict

import requests

from .scanner import WorkspaceScanner
from .language import detect_language


class SummaryService:
    """
    Phase 2.5 (FINAL)
    -----------------
    Deterministic project summary generator with OPTIONAL LLM refinement.
    Indexing MUST NOT fail if LLM misbehaves.
    """

    def __init__(
        self,
        workspace: Path,
        index_root: Path,
        ollama_base_url: str = "http://127.0.0.1:11434",
        model: str = "qwen2.5-coder:7b-instruct-q4_K_M",
    ):
        self.workspace = workspace
        self.index_root = index_root
        self.base_url = ollama_base_url.rstrip("/")
        self.model = model
        self.scanner = WorkspaceScanner()

    # ==========================================================
    # Deterministic facts
    # ==========================================================
    def _scan_files(self) -> List[Dict]:
        files = []
        for p in self.scanner.scan(self.workspace):
            files.append({
                "file": str(p.relative_to(self.workspace)),
                "language": detect_language(p) or "unknown"
            })
        return files

    def _load_symbols(self) -> List[Dict]:
        path = self.index_root / "symbols.json"
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    # ==========================================================
    # Deterministic fallback summary (ALWAYS VALID)
    # ==========================================================
    def _deterministic_summary(self) -> Dict:
        files = self._scan_files()
        symbols = self._load_symbols()

        languages = sorted({f["language"] for f in files})
        key_files = [f["file"] for f in files[:10]]

        return {
            "project_name": self.workspace.name,
            "description": "Indexed software project.",
            "main_languages": languages,
            "key_files": key_files,
            "architecture": "Workspace indexed into semantic code chunks and symbols.",
            "frameworks": [],
        }

    # ==========================================================
    # Optional LLM refinement (best-effort)
    # ==========================================================
    def _try_llm_summary(self, base_summary: Dict) -> Dict | None:
        system = (
            "You refine project summaries.\n"
            "Return ONLY valid JSON.\n"
            "No explanations.\n"
            "Schema must remain identical."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(base_summary, indent=2)},
        ]

        try:
            resp = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0},
                },
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            content = (data.get("message") or {}).get("content", "").strip()
            if not content.startswith("{"):
                return None
            return json.loads(content)
        except Exception:
            return None

    # ==========================================================
    # Public API
    # ==========================================================
    def generate_and_save(self) -> Path:
        summary = self._deterministic_summary()

        # Try LLM enhancement, but NEVER fail indexing
        refined = self._try_llm_summary(summary)
        if isinstance(refined, dict):
            summary = refined

        out = self.index_root / "summary.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        return out
