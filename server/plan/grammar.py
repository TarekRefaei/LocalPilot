from typing import Dict, List


ALLOWED_ACTIONS = {"create", "modify", "delete"}


def enforce_plan_grammar(plan: Dict):
    """
    Enforces hard grammar rules.
    Raises ValueError on violation.
    """
    if "tasks" not in plan or not isinstance(plan["tasks"], list):
        raise ValueError("Plan must contain a tasks[] array")

    seen_ids = set()

    for i, task in enumerate(plan["tasks"]):
        if "id" not in task:
            raise ValueError(f"Task[{i}] missing id")

        if task["id"] in seen_ids:
            raise ValueError(f"Duplicate task id: {task['id']}")
        seen_ids.add(task["id"])

        if task.get("actionType") not in ALLOWED_ACTIONS:
            raise ValueError(
                f"Invalid actionType in task {task['id']}"
            )

        if not isinstance(task.get("filePath"), str):
            raise ValueError(
                f"Invalid filePath in task {task['id']}"
            )

        if task["filePath"].startswith(("/", "\\")) or ":" in task["filePath"]:
            raise ValueError(
                f"Absolute path forbidden: {task['filePath']}"
            )

        if ".." in task["filePath"]:
            raise ValueError(
                f"Path traversal forbidden: {task['filePath']}"
            )
