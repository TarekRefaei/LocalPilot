from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
import json

from server.chat.ollama_chat_client import OllamaChatClient

PLAN_MODE_SYSTEM = (
    "You are operating in PLAN MODE.\n\n"

    "Your task is to output ONE VALID IMPLEMENTATION PLAN.\n"
    "You MUST output EXACTLY ONE JSON object inside a fenced ```json block.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "ABSOLUTE RULES (NO EXCEPTIONS)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "1. Output ONE and ONLY ONE JSON object.\n"
    "2. JSON MUST be syntactically valid.\n"
    "3. JSON MUST match the schema EXACTLY.\n"
    "4. ALL fields are REQUIRED.\n"
    "5. NO extra fields are allowed.\n"
    "6. status MUST be \"draft\".\n"
    "7. orderIndex MUST start at 0 and increment by 1.\n"
    "8. tasks MUST NOT be empty.\n"
    "9. filePath MUST NEVER be empty.\n"
    "10. actionType MUST be create | modify | delete.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "STRICT JSON SCHEMA\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "{\n"
    "  \"id\": \"string\",\n"
    "  \"title\": \"string\",\n"
    "  \"overview\": \"string\",\n"
    "  \"status\": \"draft\",\n"
    "  \"tasks\": [\n"
    "    {\n"
    "      \"id\": \"string\",\n"
    "      \"orderIndex\": number,\n"
    "      \"title\": \"string\",\n"
    "      \"description\": \"string\",\n"
    "      \"filePath\": \"string\",\n"
    "      \"actionType\": \"create | modify | delete\",\n"
    "      \"details\": [\"string\"],\n"
    "      \"dependencies\": [\"string\"]\n"
    "    }\n"
    "  ]\n"
    "}\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "SELF-CHECK LOOP (MANDATORY)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "- Validate JSON against the schema.\n"
    "- Fix ALL errors BEFORE responding.\n"
    "- Do NOT explain.\n"
    "- Do NOT apologize.\n"
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

        output = ""
        for attempt in range(3):  # increase to 3 attempts
            output = client.chat(messages)

            # Validate JSON via parser
            from server.plan.plan_parser import PlanParser
            parser = PlanParser()
            parsed = parser.parse(output)

            if parsed.get("plan"):
                return output

            # Self-repair instruction for the model
            messages.append({
                "role": "system",
                "content": (
                    "The previous output was INVALID.\n"
                    "You MUST fix ALL schema violations.\n"
                    "Output ONLY a valid JSON plan."
                )
            })

        return output  # last attempt (will fail validation visibly)
