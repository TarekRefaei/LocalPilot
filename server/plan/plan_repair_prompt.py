from __future__ import annotations


def build_plan_repair_prompt(plan, warnings, workspace):
    return f"""
You are repairing a software implementation plan.

RULES (STRICT):
- Do NOT change the intent of the plan.
- Do NOT add or remove tasks.
- Do NOT change task order.
- ONLY fix the reported issues.
- Return ONLY valid JSON.
- Do NOT include explanations outside JSON.

Current Plan:
{plan}

Blocking Validation Errors:
{warnings}

Workspace Files:
{workspace.get('existingFiles', [])}

Your task:
Return a corrected version of the plan that fixes ONLY the listed errors.
"""
