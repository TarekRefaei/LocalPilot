from typing import Dict, List


def compile_plan_to_todos(plan: Dict) -> List[Dict]:
    """
    Converts plan into a linear, provable TODO list.
    Ensures dependencies are respected and detects cycles.
    """
    tasks = plan.get("tasks", []) or []
    id_to_task = {t["id"]: t for t in tasks if "id" in t}

    todos: List[Dict] = []
    resolved = set()

    while len(todos) < len(tasks):
        progress = False
        for task in sorted(tasks, key=lambda t: t.get("orderIndex", 0)):
            tid = task.get("id")
            if not tid or tid in resolved:
                continue
            deps = task.get("dependencies", []) or []
            if all(dep in resolved for dep in deps):
                todos.append({
                    "task_id": tid,
                    "file": task.get("filePath"),
                    "action": task.get("actionType"),
                })
                resolved.add(tid)
                progress = True
        if not progress:
            raise ValueError("Dependency cycle detected")

    return todos
