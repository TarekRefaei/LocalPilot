from __future__ import annotations

from typing import Dict, List


def validate_semantics(intent: Dict, snapshot: Dict) -> List[str]:
    """
    Compare intent against semantic snapshot.
    Returns list of error messages.
    """

    errors: List[str] = []

    if not intent or not snapshot:
        return errors

    kind = intent.get("kind")
    fn = intent.get("functionName")
    functions = snapshot.get("functions") or []

    if kind == "add_function" and fn:
        if fn in functions:
            errors.append(f"Function '{fn}' already exists")

    if kind == "modify_function" and fn:
        if fn not in functions:
            errors.append(f"Function '{fn}' does not exist")

    if kind == "call_function" and fn:
        if fn not in functions:
            errors.append(f"Function '{fn}' is not defined or imported")

    return errors
