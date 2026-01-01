import re
from dataclasses import dataclass
from typing import List
from pathlib import Path

from server.act_v2.models.execution_task import ExecutionTask
from server.act_v2.validation.validation_errors import ContextMismatchViolation


@dataclass
class ValidatedDiff:
    diff: str
    files_changed: List[str]


class DiffValidationError(Exception):
    pass


class DiffValidator:
    FILE_RE = re.compile(r"^\+\+\+\s+b/(.+)$", re.MULTILINE)

    def validate(self, diff: str, task: ExecutionTask, workspace: Path) -> ValidatedDiff:
        # Prevent hallucinated/empty diffs for modify tasks
        if task.action_type == "modify" and not diff.strip():
            raise ContextMismatchViolation(
                "Modify task produced no valid diff against existing file"
            )

        if not diff.strip():
            raise DiffValidationError("Empty diff")

        files = self.FILE_RE.findall(diff)
        if not files:
            raise DiffValidationError("No files modified")

        for f in files:
            if f != task.file_path:
                raise DiffValidationError(
                    f"Illegal file modification: {f}"
                )

        if task.action_type == "create" and "--- /dev/null" not in diff:
            raise DiffValidationError("Create task must add new file")

        if task.action_type == "delete" and not any("+++ /dev/null" in diff for _ in [0]):
            raise DiffValidationError("Delete task must remove file")

        # Workspace-aware checks
        target = workspace / task.file_path
        exists = target.exists()

        if task.action_type == "create" and exists:
            raise DiffValidationError(
                f"Create task attempted on existing file: {task.file_path}"
            )

        if task.action_type == "modify" and not exists:
            raise DiffValidationError(
                f"Modify task attempted on missing file: {task.file_path}"
            )

        return ValidatedDiff(diff=diff, files_changed=files)
