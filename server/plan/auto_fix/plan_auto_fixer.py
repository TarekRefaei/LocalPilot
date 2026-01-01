from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from copy import deepcopy
import json
import difflib


class PlanAutoFixResult:
    def __init__(self, fixed_plan: Dict[str, Any], warnings: List[str], diff: str):
        self.fixed_plan = fixed_plan
        self.warnings = warnings
        self.diff = diff


class PlanAutoFixer:
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()

    def auto_fix(self, plan: Dict[str, Any]) -> PlanAutoFixResult:
        original = deepcopy(plan)
        fixed = deepcopy(plan)
        warnings: List[str] = []

        tasks = fixed.get("tasks", []) or []
        for task in tasks:
            file_path = task.get("filePath")
            if not file_path:
                continue

            # Rule A — Absolute Paths → Relative Paths
            p = Path(file_path)
            if p.is_absolute():
                try:
                    task["filePath"] = str(p.resolve().relative_to(self.workspace_root))
                except Exception:
                    warnings.append(
                        f"Task '{task.get('id', '?')}' uses illegal absolute path: {file_path}"
                    )
                    # leave as-is; surfaced to user
                    continue

            # Normalize separators to POSIX style for consistency
            task["filePath"] = task["filePath"].replace("\\", "/")

            # Rule C — Directory in filePath → error (no auto-fix)
            if task["filePath"].endswith("/"):
                warnings.append(
                    f"Task '{task.get('id', '?')}' filePath points to a directory"
                )

            # Rule D — Multi-file paths in single task → warning only
            if "," in task["filePath"]:
                warnings.append(
                    f"Task '{task.get('id', '?')}' filePath appears to reference multiple files"
                )

            # Rule B — Modify on missing file → Create
            target = self.workspace_root / task["filePath"]
            if task.get("actionType") == "modify" and not target.exists():
                task["actionType"] = "create"
                warnings.append(
                    f"Task '{task.get('id', '?')}': actionType changed modify → create (file not found)"
                )

            # Rule F — Create on existing file → Modify
            if task.get("actionType") == "create" and target.exists():
                task["actionType"] = "modify"
                warnings.append(
                    f"Task '{task.get('id', '?')}': actionType changed create → modify (file already exists)"
                )

        # Rule E — Task ordering normalization (contiguous 0..N)
        try:
            tasks.sort(key=lambda t: t.get("orderIndex", 0))
            for i, t in enumerate(tasks):
                t["orderIndex"] = i
        except Exception:
            # if tasks not sortable, leave as-is
            pass

        diff = self._generate_diff(original, fixed)
        return PlanAutoFixResult(fixed, warnings, diff)

    def _generate_diff(self, before: Dict[str, Any], after: Dict[str, Any]) -> str:
        before_json = json.dumps(before, indent=2).splitlines(keepends=True)
        after_json = json.dumps(after, indent=2).splitlines(keepends=True)
        return "".join(
            difflib.unified_diff(
                before_json,
                after_json,
                fromfile="plan.json (original)",
                tofile="plan.json (auto-fixed)",
            )
        )
