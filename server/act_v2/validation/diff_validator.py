import re

from server.act_v2.models.execution_task import ExecutionTask
from .validation_errors import (
    FileScopeViolation,
    ActionTypeViolation,
    EmptyDiffNotAllowed,
)


FILE_HEADER = re.compile(r"^\+\+\+\s+b/(.+)", re.MULTILINE)


def validate_diff(diff: str, task: ExecutionTask) -> None:
    if not diff.strip():
        if task.action_type != "create":
            raise EmptyDiffNotAllowed("Task requires changes but diff is empty")
        return

    files = FILE_HEADER.findall(diff)
    if not files:
        raise FileScopeViolation("No target files detected")

    for f in files:
        if f != task.file_path:
            raise FileScopeViolation(
                f"Diff modifies unauthorized file: {f}"
            )

    if task.action_type == "delete":
        if not re.search(r"^---\s+b/", diff, re.MULTILINE):
            raise ActionTypeViolation("Delete action missing file removal")
