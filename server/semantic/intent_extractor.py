from __future__ import annotations

from typing import Dict, Optional


def extract_intent(task: Dict) -> Optional[Dict]:
    """
    Infer semantic intent from a plan task.
    Returns a SemanticIntent dict or None if intent is unclear.
    """

    if not isinstance(task, dict):
        return None

    action = task.get("actionType")
    file_path = task.get("filePath")
    title = (task.get("title") or "").lower()
    desc = (task.get("description") or "").lower()
    details = " ".join(task.get("details") or []).lower()

    text = f"{title} {desc} {details}"

    # Add function intent
    if action == "create" and "function" in text:
        name = _extract_function_name(text)
        return {
            "kind": "add_function",
            "functionName": name,
            "targetFile": file_path,
        }

    # Modify function intent
    if action == "modify" and "function" in text:
        name = _extract_function_name(text)
        return {
            "kind": "modify_function",
            "functionName": name,
            "targetFile": file_path,
        }

    # Call function intent
    if action == "modify" and ("call" in text or "invoke" in text):
        name = _extract_function_name(text)
        return {
            "kind": "call_function",
            "functionName": name,
            "targetFile": file_path,
        }

    return None


def _extract_function_name(text: str) -> Optional[str]:
    tokens = text.replace("(", " ").replace(")", " ").split()
    for i, t in enumerate(tokens):
        if t == "function" and i + 1 < len(tokens):
            return tokens[i + 1]
    return None
