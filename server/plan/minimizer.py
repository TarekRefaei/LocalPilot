from typing import Dict, List
from copy import deepcopy


def minimize_plan(plan: Dict) -> Dict:
    """
    Merge redundant tasks that:
    - Target the same filePath
    - Share the same actionType
    - Have linear dependencies
    """
    plan = deepcopy(plan)
    tasks = plan.get("tasks", [])

    merged: List[Dict] = []
    seen = {}

    for task in tasks:
        key = (task["filePath"], task["actionType"])
        if key not in seen:
            seen[key] = task
            merged.append(task)
        else:
            existing = seen[key]
            existing.setdefault("details", [])
            existing["details"].extend(task.get("details", []))
            existing["dependencies"] = list(set(existing.get("dependencies", [])))

    # Re-index
    for i, t in enumerate(merged):
        t["orderIndex"] = i

    plan["tasks"] = merged
    return plan
