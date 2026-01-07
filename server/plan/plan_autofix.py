from __future__ import annotations
import json
from typing import Any, Dict, List


def repair_plan_if_needed(plan: Dict[str, Any], issues: List[Dict[str, Any]], llm) -> Dict[str, Any]:
    """
    Ask the LLM to repair the plan given a list of structured issues.
    Returns the corrected plan dict if successful; otherwise returns the original plan.
    """
    if not issues:
        return plan

    prompt = {
        "role": "system",
        "content": """
You are repairing a PLAN.

The plan below has VALIDATION ERRORS.
You MUST fix ALL issues listed.

RULES:
- DO NOT change plan intent
- DO NOT add new tasks
- DO NOT remove tasks
- ONLY fix the reported issues
- Output the FULL corrected plan JSON
- Ensure the plan passes validation
"""
    }

    user = {
        "role": "user",
        "content": json.dumps({
            "plan": plan,
            "issues": issues,
        }, indent=2),
    }

    try:
        # Support either chat(messages) or invoke(messages)
        raw = llm.chat([prompt, user]) if hasattr(llm, "chat") else llm.invoke([prompt, user])
        fixed = json.loads(raw)
        if isinstance(fixed, dict):
            return fixed
    except Exception:
        pass

    return plan
