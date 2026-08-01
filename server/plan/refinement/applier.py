from copy import deepcopy
from typing import Dict, Any, List


def apply_repairs(plan: Dict[str, Any], repairs: List[dict]) -> Dict[str, Any]:
    plan = deepcopy(plan)
    tasks = plan.get("tasks", [])

    task_map = {t.get("id"): t for t in tasks if isinstance(t, dict) and t.get("id") is not None}

    for r in repairs:
        kind = r["kind"]

        if kind == "remove_dependency":
            task = task_map[r["taskId"]]
            deps = task.get("dependencies")
            if deps is None:
                deps = []
                task["dependencies"] = deps
            deps.remove(r["dependency"])

        elif kind == "add_dependency":
            task = task_map[r["taskId"]]
            deps = task.get("dependencies")
            if deps is None:
                deps = []
                task["dependencies"] = deps
            deps.append(r["dependency"])

        elif kind == "change_order_index":
            task_map[r["taskId"]]["orderIndex"] = r["newOrderIndex"]

        elif kind == "swap_order_index":
            a = task_map[r["taskA"]]
            b = task_map[r["taskB"]]
            a["orderIndex"], b["orderIndex"] = b.get("orderIndex"), a.get("orderIndex")

        elif kind == "remove_task":
            remove_id = r["taskId"]
            tasks[:] = [t for t in tasks if t.get("id") != remove_id]
            task_map.pop(remove_id, None)

        elif kind == "rename_task_id":
            old = r["oldId"]
            new = r["newId"]

            task = task_map.pop(old)
            task["id"] = new
            task_map[new] = task

            for t in tasks:
                deps = t.get("dependencies") or []
                t["dependencies"] = [new if d == old else d for d in deps]

        else:
            raise ValueError(f"Unsupported repair kind: {kind}")

    plan["tasks"] = tasks
    return plan
