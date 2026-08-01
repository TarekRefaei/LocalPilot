from typing import Dict, Any, List, Set, Tuple

from server.plan.refinement.contracts import PlanRefinementProposal
from server.plan.refinement.applier import apply_repairs
from server.plan.structure.diagnostics import analyze_plan_structure


class RefinementValidationError(Exception):
    pass


def _repair_key(r: dict) -> Tuple:
    kind = r.get("kind")
    if kind == "remove_dependency":
        return (kind, r.get("taskId"), r.get("dependency"))
    if kind == "add_dependency":
        return (kind, r.get("taskId"), r.get("dependency"))
    if kind == "change_order_index":
        return (kind, r.get("taskId"), r.get("newOrderIndex"))
    if kind == "swap_order_index":
        a = r.get("taskA")
        b = r.get("taskB")
        return (kind, min(a, b), max(a, b))
    if kind == "remove_task":
        return (kind, r.get("taskId"))
    if kind == "rename_task_id":
        return (kind, r.get("oldId"), r.get("newId"))
    return (kind,)


def validate_and_apply_refinement(
    plan: Dict[str, Any],
    proposal: PlanRefinementProposal,
) -> Dict[str, Any]:
    if not proposal.repairs:
        raise RefinementValidationError("No safe structural repair possible")

    if not isinstance(plan, dict):
        raise RefinementValidationError("Invalid plan")

    original_plan_id = plan.get("id")
    original_tasks = plan.get("tasks")
    if not isinstance(original_tasks, list):
        raise RefinementValidationError("Invalid plan tasks")

    original_ids: List[str] = []
    for t in original_tasks:
        if isinstance(t, dict) and isinstance(t.get("id"), str):
            original_ids.append(t["id"])

    original_id_set: Set[str] = set(original_ids)
    if len(original_id_set) != len(original_ids):
        raise RefinementValidationError("Invalid plan: duplicate task IDs")

    repairs = [r.model_dump() for r in proposal.repairs]

    seen: Set[Tuple] = set()
    for r in repairs:
        key = _repair_key(r)
        if key in seen:
            raise RefinementValidationError("Duplicate repairs")
        seen.add(key)

    rename_map: Dict[str, str] = {}
    remove_ids: Set[str] = set()

    for r in repairs:
        kind = r.get("kind")

        if kind == "remove_dependency":
            task_id = r.get("taskId")
            dep = r.get("dependency")
            if task_id not in original_id_set:
                raise RefinementValidationError(f"Unknown taskId: {task_id}")
            task = next((t for t in original_tasks if isinstance(t, dict) and t.get("id") == task_id), None)
            deps = (task or {}).get("dependencies") or []
            if dep not in deps:
                raise RefinementValidationError("No-op repair")

        elif kind == "add_dependency":
            task_id = r.get("taskId")
            dep = r.get("dependency")
            if task_id not in original_id_set:
                raise RefinementValidationError(f"Unknown taskId: {task_id}")
            task = next((t for t in original_tasks if isinstance(t, dict) and t.get("id") == task_id), None)
            deps = (task or {}).get("dependencies") or []
            if dep in deps:
                raise RefinementValidationError("No-op repair")

        elif kind == "change_order_index":
            task_id = r.get("taskId")
            if task_id not in original_id_set:
                raise RefinementValidationError(f"Unknown taskId: {task_id}")
            task = next((t for t in original_tasks if isinstance(t, dict) and t.get("id") == task_id), None)
            if task is not None and task.get("orderIndex") == r.get("newOrderIndex"):
                raise RefinementValidationError("No-op repair")

        elif kind == "swap_order_index":
            a = r.get("taskA")
            b = r.get("taskB")
            if a not in original_id_set or b not in original_id_set:
                raise RefinementValidationError("Unknown taskId")
            if a == b:
                raise RefinementValidationError("No-op repair")
            ta = next((t for t in original_tasks if isinstance(t, dict) and t.get("id") == a), None)
            tb = next((t for t in original_tasks if isinstance(t, dict) and t.get("id") == b), None)
            if ta is not None and tb is not None and ta.get("orderIndex") == tb.get("orderIndex"):
                raise RefinementValidationError("No-op repair")

        elif kind == "remove_task":
            task_id = r.get("taskId")
            if task_id not in original_id_set:
                raise RefinementValidationError(f"Unknown taskId: {task_id}")
            remove_ids.add(task_id)

        elif kind == "rename_task_id":
            old = r.get("oldId")
            new = r.get("newId")
            if old not in original_id_set:
                raise RefinementValidationError(f"Unknown taskId: {old}")
            if not isinstance(new, str) or not new:
                raise RefinementValidationError("Invalid newId")
            if old == new:
                raise RefinementValidationError("No-op repair")
            if old in rename_map:
                raise RefinementValidationError("Duplicate repairs")
            rename_map[old] = new

        else:
            raise RefinementValidationError("Unsupported repair kind")

    new_ids = set(rename_map.values())
    forbidden = (original_id_set - set(rename_map.keys())) & new_ids
    if forbidden:
        raise RefinementValidationError("rename_task_id collision")

    if len(new_ids) != len(rename_map):
        raise RefinementValidationError("rename_task_id collision")

    effective_ids = (original_id_set - remove_ids - set(rename_map.keys())) | new_ids

    for r in repairs:
        if r.get("kind") == "add_dependency":
            dep = r.get("dependency")
            if dep not in effective_ids:
                raise RefinementValidationError(f"Unknown dependency target: {dep}")

    repaired = apply_repairs(plan, repairs)

    if repaired.get("id") != original_plan_id:
        raise RefinementValidationError("Plan ID is immutable")

    repaired_tasks = repaired.get("tasks")
    if not isinstance(repaired_tasks, list):
        raise RefinementValidationError("Invalid repaired plan tasks")

    repaired_ids: List[str] = []
    for t in repaired_tasks:
        if isinstance(t, dict) and isinstance(t.get("id"), str):
            repaired_ids.append(t["id"])

    repaired_id_set = set(repaired_ids)
    if len(repaired_ids) != len(repaired_id_set):
        raise RefinementValidationError("Invalid repaired plan: duplicate task IDs")

    expected_ids = (original_id_set - remove_ids - set(rename_map.keys())) | new_ids
    if repaired_id_set != expected_ids:
        raise RefinementValidationError("Task ID immutability violated")

    remove_count = len(remove_ids)
    expected_task_count = len(original_id_set) - remove_count
    if len(repaired_id_set) != expected_task_count:
        raise RefinementValidationError("Task count immutability violated")

    issues = analyze_plan_structure(repaired)
    if issues:
        codes = sorted({i.code for i in issues})
        raise RefinementValidationError(f"Refinement introduced structural issues: {codes}")

    return repaired
