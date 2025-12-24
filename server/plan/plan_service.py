from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
import json

from server.chat.ollama_chat_client import OllamaChatClient

PLAN_MODE_SYSTEM = (
     "You are operating in PLAN MODE.\n\n"
     "Your task is to generate a structured implementation plan for a software project.\n\n"
     "────────────────────────────────────────\n"
     "CORE RULES\n"
     "────────────────────────────────────────\n"
     "1. You MUST generate a PLAN, not code.\n"
     "2. You MUST NOT write or suggest code implementations.\n"
     "3. You MUST NOT include shell commands or execution steps.\n"
     "4. You MUST NOT assume files or frameworks not present in the indexed project.\n"
     "5. You MUST base the plan ONLY on: Project Summary, Indexed Project Structure / Symbols, User Request.\n"
     "6. If information is missing, you MUST explicitly state it.\n\n"
     "────────────────────────────────────────\n"
     "PLAN REQUIREMENTS\n"
     "────────────────────────────────────────\n"
     "1. File-level tasks only (NOT function-level).\n"
     "2. Each task MUST specify:\n"
     "   - filePath\n"
     "   - actionType (create | modify | delete)\n"
     "3. Tasks MUST be ordered logically using orderIndex.\n"
     "4. Tasks MUST be descriptive but MUST NOT include implementation details.\n\n"
    "────────────────────────────────────────\n"
    "STRICT JSON SCHEMA (MANDATORY)\n"
    "────────────────────────────────────────\n"
    "You MUST embed ONE JSON block in the output.\n"
    "The JSON MUST be VALID and MUST MATCH THIS SCHEMA EXACTLY:\n\n"
    "{\n"
    '  "id": "string",\n'
    '  "title": "string",\n'
    '  "overview": "string",\n'
    '  "status": "draft",\n'
    '  "tasks": [\n'
    "    {\n"
    '      "id": "string",\n'
    '      "orderIndex": number,\n'
    '      "title": "string",\n'
    '      "description": "string",\n'
    '      "filePath": "string",\n'
    '      "actionType": "create | modify | delete",\n'
    '      "details": ["string"],\n'
    '      "dependencies": ["string"]\n'
    "    }\n"
    "  ]\n"
    "}\n\n"
    "RULES:\n"
    "- ALL fields are REQUIRED.\n"
    "- NO extra fields are allowed.\n"
    "- status MUST be \"draft\".\n"
    "- tasks array MUST NOT be empty.\n"
    "- orderIndex MUST start at 0 and be sequential.\n\n"
     "────────────────────────────────────────\n"
     "OUTPUT FORMAT (MANDATORY)\n"
     "────────────────────────────────────────\n"
     "1. Human-readable Markdown plan.\n"
     "2. ONE embedded JSON block that matches the schema exactly.\n\n"
     "────────────────────────────────────────\n"
     "FORBIDDEN\n"
     "────────────────────────────────────────\n"
     "- No code blocks except the embedded JSON.\n"
     "- No shell commands.\n"
     "- No file content.\n"
     "- No execution instructions.\n\n"
     "────────────────────────────────────────\n"
     "FAILURE HANDLING\n"
     "────────────────────────────────────────\n"
     "If you cannot produce a valid plan:\n"
     "- Explain what information is missing in Markdown.\n"
     "- STILL include a JSON block with empty tasks array.\n"
     "- NEVER hallucinate details.\n"
)


class PlanService:
    def __init__(self, index_root: Path, project_id: str, model: str, base_url: str = "http://127.0.0.1:11434"):
        self.index_root = index_root
        self.project_id = project_id
        self.model = model
        self.base_url = base_url.rstrip("/")

    def _extract_planning_intent(
        self, messages: List[Dict[str, str]]
    ) -> str:
        """
        Extract the most recent USER intent for planning.
        Assistant messages are intentionally ignored to
        avoid Chat-mode refusals poisoning Plan Mode.
        """
        for m in reversed(messages or []):
            if m.get("role") == "user" and m.get("content"):
                return m["content"]
        return ""

    def _read_json(self, path: Path) -> Any:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _build_messages(self, chat_messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        project_dir = self.index_root / self.project_id
        summary = self._read_json(project_dir / "summary.json") or {}
        symbols = self._read_json(project_dir / "symbols.json") or []

        preface = (
            "Project Summary:\n" + json.dumps(summary, indent=2) +
            "\n\nIndexed Symbols:\n" + json.dumps(symbols, indent=2)
        )

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": PLAN_MODE_SYSTEM},
            {"role": "user", "content": preface},
        ]
        # IMPORTANT:
        # Only pass the latest USER planning intent into Plan Mode.
        # Do NOT include assistant messages or full chat history.
        intent = self._extract_planning_intent(chat_messages)
        if intent:
            messages.append({"role": "user", "content": intent})
        return messages

    def generate(self, chat_messages: List[Dict[str, str]]) -> str:
        client = OllamaChatClient(base_url=self.base_url, model=self.model)
        messages = self._build_messages(chat_messages)
        return client.chat(messages)
