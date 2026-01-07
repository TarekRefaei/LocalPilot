from pathlib import Path
from server.execute_v2.llm.ollama_client import OllamaClient
from server.execute_v2.llm.confined_prompt import build_confined_prompt
from server.execute_v2.validation.diff_parser import extract_diff
from server.execute_v2.validation.diff_validator import DiffValidator


class InvocationService:
    def __init__(self, client: OllamaClient):
        self.client = client

    def invoke_task(self, task, context: dict) -> str:
        if not context:
            raise RuntimeError("Context missing")

        # Compute required symbols from task intent
        required_symbols = []
        try:
            if getattr(task, "action_type", None) in ("create", "modify"):
                title = (getattr(task, "title", "") or "").lower()
                if "subtract" in title:
                    required_symbols.append("subtract")
        except Exception:
            pass

        # 🔒 STRICT FILE SCOPE
        context = {
            **context,
            "allowed_files": [task.file_path],
            "required_symbols": required_symbols,
            "error_feedback": getattr(task, "error", None),
            "last_error": getattr(task, "error", None),
            "action_type": getattr(task, "action_type", None) or "",
            "insertion": getattr(task, "insertion", None),
            "file_role": getattr(task, "file_role", "module"),
        }

        # Inject semantic correction hint for known structural failures
        try:
            err = getattr(task, "error", None) or ""
            if isinstance(err, str) and "Top-level return" in err:
                context["error_fix_hint"] = "Remove any return statements. Use print() instead."
        except Exception:
            pass

        messages = build_confined_prompt(context)
        raw = self.client.invoke(messages)

        # Safety net for CREATE: wrap raw content into a valid unified diff if needed
        try:
            action = getattr(task, "action_type", None) or getattr(task, "action", None)
            file_path = getattr(task, "file_path", None)
        except Exception:
            action = None
            file_path = None
        if action == "create" and isinstance(raw, str):
            stripped = raw.lstrip()
            if not stripped.startswith("---") and file_path:
                raw = (
                    f"--- /dev/null\n"
                    f"+++ b/{file_path}\n"
                    f"@@\n"
                    + "\n".join("+" + line for line in raw.splitlines())
                )

        diff = extract_diff(raw)
        workspace = Path(context.get("workspace_root", "."))
        DiffValidator().validate(diff, task, workspace)
        return diff
