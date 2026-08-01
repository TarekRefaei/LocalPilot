from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Set
import os
import re
from server.plan.constants import ACTION_TYPES
from server.plan.validation_codes import (
    EMPTY_PLAN,
    NO_TASKS,
    MISSING_FILE_PATH,
    ABSOLUTE_PATH,
    WINDOWS_PATH,
    DIRECTORY_PATH,
    MULTI_FILE_REFERENCE,
    MISSING_ACTION_TYPE,
    INVALID_ACTION_TYPE,
    ORDER_INDEX_TYPE,
    ORDER_INDEX_SEQUENCE,
)
from server.plan.path_rules import (
    is_absolute_path,
    has_windows_separators,
    is_directory_path,
    is_multi_file_reference,
)

from pydantic import ValidationError
from server.plan.plan_parser import PlanSchema


def validate_plan(plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    if not plan:
        issues.append({
            "code": EMPTY_PLAN,
            "field": "",
            "message": "Plan object is empty",
            "fix": "Return a valid plan JSON per schema"
        })
        return issues

    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        issues.append({
            "code": NO_TASKS,
            "field": "tasks",
            "message": "Plan has no tasks",
            "fix": "Provide at least one task"
        })
        return issues

    valid_actions = ACTION_TYPES

    for idx, t in enumerate(tasks):
        tid = t.get("id", f"tasks[{idx}]")
        fp = t.get("filePath")
        if not fp or not isinstance(fp, str):
            issues.append({
                "code": MISSING_FILE_PATH,
                "field": f"tasks[{idx}].filePath",
                "taskId": tid,
                "message": "Task is missing filePath",
                "fix": "Set filePath to a project-relative POSIX path (e.g. utils.py)"
            })
        else:
            # Absolute path
            try:
                if is_absolute_path(fp):
                    issues.append({
                        "code": ABSOLUTE_PATH,
                        "field": f"tasks[{idx}].filePath",
                        "taskId": tid,
                        "message": "Absolute path detected",
                        "fix": "Use project-relative path only (e.g. utils.py)"
                    })
            except Exception:
                pass

            # Windows separators
            if has_windows_separators(fp):
                issues.append({
                    "code": WINDOWS_PATH,
                    "field": f"tasks[{idx}].filePath",
                    "taskId": tid,
                    "message": "Windows path separators detected",
                    "fix": "Use POSIX-style forward slashes (e.g. src/main.py)"
                })

            # Directory path (ends with slash)
            if is_directory_path(fp):
                issues.append({
                    "code": DIRECTORY_PATH,
                    "field": f"tasks[{idx}].filePath",
                    "taskId": tid,
                    "message": "filePath points to a directory",
                    "fix": "Specify a file, not a directory"
                })

            # Multiple references (comma)
            if is_multi_file_reference(fp):
                issues.append({
                    "code": MULTI_FILE_REFERENCE,
                    "field": f"tasks[{idx}].filePath",
                    "taskId": tid,
                    "message": "filePath appears to reference multiple files",
                    "fix": "Use one file per task"
                })

        at = t.get("actionType")
        if not at:
            issues.append({
                "code": MISSING_ACTION_TYPE,
                "field": f"tasks[{idx}].actionType",
                "taskId": tid,
                "message": "Task is missing actionType",
                "fix": "Set actionType to create | modify | delete"
            })
        elif at not in valid_actions:
            issues.append({
                "code": INVALID_ACTION_TYPE,
                "field": f"tasks[{idx}].actionType",
                "taskId": tid,
                "message": f"Invalid actionType: {at}",
                "fix": "Use one of: create | modify | delete"
            })

    # Simple check for contiguous orderIndex
    try:
        order = [t.get("orderIndex") for t in tasks]
        if any(not isinstance(x, int) for x in order):
            issues.append({
                "code": ORDER_INDEX_TYPE,
                "field": "tasks[].orderIndex",
                "message": "orderIndex must be integers",
                "fix": "Ensure orderIndex are integers starting at 0"
            })
        else:
            sorted_order = sorted(order)
            if sorted_order != list(range(len(order))):
                issues.append({
                    "code": ORDER_INDEX_SEQUENCE,
                    "field": "tasks[].orderIndex",
                    "message": "orderIndex must be contiguous starting at 0",
                    "fix": "Normalize orderIndex to 0..N-1"
                })
    except Exception:
        pass

    return issues


def validate_plan_schema(plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    try:
        PlanSchema(**(plan or {}))
        return []
    except ValidationError as e:
        try:
            return e.errors()
        except Exception:
            return [{"message": str(e)}]


class PlanValidationError(Exception):
    pass


def validate_plan_files(plan: Dict[str, Any], existing_files: Set[str]) -> None:
    tasks = (plan or {}).get("tasks", [])
    ef = set(existing_files or set())
    for t in tasks:
        fp = t.get("filePath")
        at = t.get("actionType")
        if not isinstance(fp, str) or not isinstance(at, str):
            continue
        if fp in ef and at == "create":
            raise PlanValidationError(
                f"Invalid plan: file '{fp}' exists but actionType is 'create'"
            )
        if fp not in ef and at == "modify":
            raise PlanValidationError(
                f"Invalid plan: file '{fp}' does not exist but actionType is 'modify'"
            )
