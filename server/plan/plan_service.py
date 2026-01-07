from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from server.chat.ollama_chat_client import OllamaChatClient
from server.plan.plan_validator import (
    validate_plan,
    PlanValidationError,
    validate_plan_files,
)
from server.plan.plan_autofix import repair_plan_if_needed
from server.plan.grammar import enforce_plan_grammar
from server.plan.minimize import minimize_plan
from server.plan.compile import compile_plan_to_todos

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

    "STRICT RULES:\n"
    "- actionType MUST be one of: create | modify | delete\n"
    "- NEVER use actionType \"run\", \"test\", \"execute\", or similar\n"
    "- Tasks that describe running tests must be expressed as code changes\n"
    "  (e.g. adding test files), not execution steps\n"
    "- filePath MUST NEVER be empty\n\n"

    "\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "FILE SYSTEM GROUND TRUTH (MANDATORY)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "\n"
    "You are given the current workspace file state.\n\n"
    "This information is AUTHORITATIVE.\n"
    "You MUST NOT guess or infer file existence.\n\n"
    "\n"
    "EXISTING FILES:\n"
    "{{existing_files}}\n\n"
    "\n"
    "MISSING FILES:\n"
    "{{missing_files}}\n\n"
    "\n"
    "STRICT RULES (NON-NEGOTIABLE):\n\n"
    "\n"
    "1. If a file is listed under EXISTING FILES:\n"
    "   - You MUST use actionType: \"modify\"\n"
    "   - You MUST NEVER use actionType: \"create\" for that file\n\n"
    "\n"
    "2. If a file is listed under MISSING FILES:\n"
    "   - You MUST use actionType: \"create\"\n"
    "   - You MUST NOT use actionType: \"modify\"\n\n"
    "\n"
    "3. If a file is NOT listed in either section:\n"
    "   - You MUST NOT reference it at all\n\n"
    "\n"
    "4. Violating these rules makes the plan INVALID and it will be rejected.\n\n"
    "\n"
    "You are expected to self-correct before outputting the final plan.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "FILE PATH RULES (MANDATORY)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "\n"
    "- ALL task.filePath values MUST be:\n"
    "  - Relative to the project root\n"
    "  - POSIX-style paths (no backslashes)\n"
    "\n"
    "VALID:\n"
    "  - \"utils.py\"\n"
    "  - \"app.py\"\n"
    "  - \"src/main.py\"\n"
    "\n"
    "INVALID:\n"
    "  - Absolute paths\n"
    "  - Windows paths (C:\\...)\n"
    "  - Paths containing workspace names\n"
    "\n"
    "If you generate an absolute path, the plan is INVALID.\n"
    "You MUST correct it.\n\n"

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
    "MANDATORY SELF-CHECK BEFORE OUTPUT\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "\n"
    "Before producing the final plan, you MUST verify:\n\n"
    "\n"
    "- Every task.filePath exists in EXACTLY ONE of:\n"
    "  - EXISTING FILES\n"
    "  - MISSING FILES\n\n"
    "\n"
    "- actionType correctness:\n"
    "  - EXISTING FILE → modify\n"
    "  - MISSING FILE → create\n\n"
    "\n"
    "If ANY violation is found:\n"
    "- You MUST FIX the plan\n"
    "- You MUST NOT output an invalid plan\n\n"
    "\n"
    "DO NOT explain the fix.\n"
    "ONLY output a corrected plan.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "PLAN SELF-CHECK (MANDATORY)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "\n"
    "Before finalizing the plan:\n"
    "\n"
    "1. Validate the plan against the JSON schema.\n"
    "2. Ensure ALL filePath values are relative paths.\n"
    "3. Ensure NO task modifies more than one file.\n"
    "4. Ensure dependency order is acyclic.\n"
    "\n"
    "If ANY rule fails:\n"
    "- Fix the plan\n"
    "- Re-validate\n"
    "- Repeat until valid\n"
    "\n"
    "ONLY output the FINAL VALID plan JSON.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "SELF-CHECK LOOP (MANDATORY)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "- Validate JSON against the schema.\n"
    "- Fix ALL errors BEFORE responding.\n"
    "- Do NOT explain.\n"
    "- Do NOT apologize.\n"
)


class PlanService:
    def __init__(
        self,
        index_root: Path,
        project_id: str,
        model: str,
        workspace_root: Optional[Path] = None,
        base_url: str = "http://127.0.0.1:11434",
    ):
        self.index_root = index_root
        self.project_id = project_id
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.workspace_root = workspace_root

    def _collect_workspace_files(self) -> List[str]:
        root = self.workspace_root
        files: List[str] = []
        try:
            if root and root.exists() and root.is_dir():
                for p in root.rglob("*"):
                    if p.is_file():
                        try:
                            files.append(p.relative_to(root).as_posix())
                        except Exception:
                            pass
        except Exception:
            return []
        return sorted(set(files))

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

        # Build file system ground truth placeholders
        # Prefer live workspace scan if provided, otherwise fall back to index artifacts
        scanned = self._collect_workspace_files()
        existing_files: List[str] = scanned.copy()
        try:
            # Prefer summary if it enumerates files
            if not existing_files and isinstance(summary, dict):
                for key in ("files", "file_list", "fileList"):
                    if isinstance(summary.get(key), list):
                        existing_files = [str(p).replace("\\", "/") for p in summary.get(key) or []]
                        break
        except Exception:
            pass
        if not existing_files and isinstance(symbols, list):
            try:
                paths = set()
                for s in symbols:
                    p = s.get("filePath") or s.get("path") or s.get("file")
                    if isinstance(p, str) and p.strip():
                        paths.add(p.replace("\\", "/"))
                existing_files = sorted(paths)
            except Exception:
                existing_files = []

        missing_files: List[str] = []

        existing_block = "\n".join(f"- {p}" for p in existing_files) or "None"
        missing_block = "\n".join(f"- {p}" for p in missing_files) or "None"

        system_content = (
            PLAN_MODE_SYSTEM
            .replace("{{existing_files}}", existing_block)
            .replace("{{missing_files}}", missing_block)
        )

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_content},
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
                # Structured validation
                plan_dict = parsed["plan"]
                issues = validate_plan(plan_dict)
                candidate = plan_dict
                if issues:
                    # Try LLM-based repair loop (max 2 attempts)
                    repaired = plan_dict
                    for _ in range(2):
                        try:
                            repaired = repair_plan_if_needed(repaired, issues, client)
                        except Exception:
                            break
                        issues = validate_plan(repaired)
                        if not issues:
                            candidate = repaired
                            break

                # If we have a candidate (possibly repaired), enforce grammar/minimize/proof
                if candidate and not issues:
                    try:
                        # Hard validator: file existence vs actionType
                        ef_list = self._collect_workspace_files()
                        if not ef_list:
                            # fall back to index-derived file set
                            ef_list = []
                            try:
                                if isinstance(summary, dict):
                                    for key in ("files", "file_list", "fileList"):
                                        if isinstance(summary.get(key), list):
                                            ef_list = [str(p).replace("\\", "/") for p in summary.get(key) or []]
                                            break
                            except Exception:
                                pass
                            if not ef_list and isinstance(symbols, list):
                                try:
                                    paths = set()
                                    for s in symbols:
                                        p = s.get("filePath") or s.get("path") or s.get("file")
                                        if isinstance(p, str) and p.strip():
                                            paths.add(p.replace("\\", "/"))
                                    ef_list = sorted(paths)
                                except Exception:
                                    ef_list = []

                        validate_plan_files(candidate, set(ef_list))

                        enforce_plan_grammar(candidate)
                        candidate = minimize_plan(candidate)
                        todos = compile_plan_to_todos(candidate)
                        assert len(todos) == len(candidate["tasks"]), "Plan execution incomplete"
                        # Return the authoritative corrected JSON
                        return "```json\n" + json.dumps(candidate, indent=2) + "\n```"
                    except PlanValidationError as e:
                        # Provide specific error feedback for self-healing
                        messages.append({
                            "role": "system",
                            "content": (
                                "PREVIOUS PLAN ERROR:\n" + str(e) + "\n\nYou MUST correct this."
                            ),
                        })
                    except Exception:
                        # Fall through to self-repair instruction
                        pass

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
