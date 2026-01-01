from pathlib import Path
from server.act_v2.llm.ollama_client import OllamaClient
from server.act_v2.llm.confined_prompt import build_confined_prompt
from server.act_v2.validation.diff_parser import extract_diff
from server.act_v2.diff_validator import DiffValidator


class InvocationService:
    def __init__(self, client: OllamaClient):
        self.client = client

    def invoke_task(self, task, context: dict) -> str:
        if not context:
            raise RuntimeError("Context missing")

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
