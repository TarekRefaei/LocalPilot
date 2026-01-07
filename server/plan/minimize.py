from typing import Dict


def minimize_plan(plan: Dict) -> Dict:
    """
    Merge redundant tasks:
    - Same filePath
    - Same actionType
    - Sequential dependencies
    """
    tasks = list(plan.get("tasks", []))
    minimized = []
    last = None

    for task in sorted(tasks, key=lambda t: t.get("orderIndex", 0)):
        if (
            last
            and task.get("filePath") == last.get("filePath")
            and task.get("actionType") == last.get("actionType")
            and task.get("dependencies") == [last.get("id")]
        ):
            last["details"] = (last.get("details", []) + task.get("details", []))
            continue
        minimized.append(task)
        last = task

    plan["tasks"] = minimized
    return plan
