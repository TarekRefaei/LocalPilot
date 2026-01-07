import json
from typing import Dict, List

from server.prompts.execution.template import SYSTEM_PROMPT


def build_execution_prompt(context: Dict) -> str:
    """
    Builds the EXECUTION MODE system prompt by replacing placeholders
    in the template with values from the provided context. This function
    contains NO prompt text itself.
    """
    allowed_files: List[str] = context.get("allowed_files", []) or []
    error_feedback: str = context.get("error_feedback", "None") or "None"
    required_symbols: List[str] = context.get("required_symbols", []) or []
    action_type: str = context.get("action_type", "") or ""

    last_error: str = context.get("last_error") or (error_feedback or "None")

    system = (
        SYSTEM_PROMPT
        .replace("{{allowed_files}}", "\n".join(f"- {f}" for f in allowed_files))
        .replace("{{error_feedback}}", error_feedback or "None")
        .replace(
            "{{required_symbols}}",
            "\n".join(f"- {s}" for s in required_symbols) or "None",
        )
        .replace("{{file_structure}}", json.dumps(context.get("file_structure", {}), indent=2))
        .replace("{{file_role}}", context.get("file_role", "module"))
        .replace("{{insertion_mode}}", (context.get("insertion") or {}).get("mode", "append_eof"))
        .replace("{{insertion_symbol}}", str((context.get("insertion") or {}).get("symbol", "None")))
        .replace("{{action_type}}", action_type)
        .replace("{{last_error}}", last_error)
    )
    return system
