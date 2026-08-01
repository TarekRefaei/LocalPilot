from typing import Dict, Any, List


def diagnose_execution_failure(error: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Translate execution errors into plan-level repair proposals.
    This function must NEVER mutate execution or workspace state.
    """

    if not isinstance(error, dict):
        return []

    if error.get("type") == "semantic":
        return [
            {
                "kind": "change_action_type",
                "from": "create",
                "to": "modify",
                "reason": "Target symbol already exists",
            },
            {
                "kind": "rename_symbol",
                "reason": "Avoid name collision with existing symbol",
            },
            {
                "kind": "remove_task",
                "reason": "Task duplicates existing functionality",
            },
        ]

    return []
