import re
from dataclasses import dataclass
from typing import List
from pathlib import Path

from server.execute_v2.models.execution_task import ExecutionTask
from server.execute_v2.validation.validation_errors import ContextMismatchViolation, DiffValidationError

from server.semantic.file_snapshot import snapshot_python_file
from server.execute_v2.validation.idempotency_validator import IdempotencyValidator


@dataclass
class ValidatedDiff:
    diff: str
    files_changed: List[str]

class DiffValidator:
    FILE_RE = re.compile(r"^\+\+\+\s+b/(.+)$", re.MULTILINE)
    HUNK_RE = re.compile(r"@@ -\d+(,\d+)? \+\d+(,\d+)? @@")
    FORBIDDEN_FILES = {
        # absolute hard blocks
        ".gitignore",
        ".env",
        ".vscode",
        ".idea",
    }

    def validate(self, diff: str, task: ExecutionTask, workspace: Path) -> ValidatedDiff:
        # Prevent hallucinated/empty diffs for modify tasks
        if task.action_type == "modify" and not diff.strip():
            raise ContextMismatchViolation(
                "Modify task produced no valid diff against existing file"
            )

        if not diff.strip():
            raise DiffValidationError("Empty diff")
        if not (diff.strip().startswith("diff --git") or diff.strip().startswith("--- ")):
            raise DiffValidationError("Diff must start with 'diff --git' or '---'")
        if not self.HUNK_RE.search(diff):
            raise DiffValidationError("Invalid or missing unified diff hunk header")

        files = self.FILE_RE.findall(diff)
        if not files:
            raise DiffValidationError("No files modified")
        if len(set(files)) != 1:
            raise DiffValidationError("Multiple files modified in a single task")

        for f in files:
            if f != task.file_path:
                raise DiffValidationError(
                    f"Illegal file modification: {f}"
                )
            if Path(f).name in self.FORBIDDEN_FILES:
                raise DiffValidationError(
                    f"Forbidden file modification: {f}"
                )
            resolved = (workspace / f).resolve()
            base = workspace.resolve()
            try:
                resolved.relative_to(base)
            except ValueError:
                raise DiffValidationError(
                    f"Path escape detected: {f}"
                )

        if task.action_type == "create" and "--- /dev/null" not in diff:
            raise DiffValidationError("Create task must add new file")

        if task.action_type == "delete" and "+++ /dev/null" not in diff:
            raise DiffValidationError("Delete task must remove file")

        # Workspace-aware checks
        target = workspace / task.file_path
        exists = target.exists()

        # P6.1 enforcement: unverified anchors must fail
        anchor = getattr(task, "anchor", None)
        if isinstance(anchor, dict) and anchor.get("verified") is False:
            raise DiffValidationError("Unverified anchor")

        if task.action_type == "create" and exists:
            raise DiffValidationError(
                f"Create task attempted on existing file: {task.file_path}"
            )

        if task.action_type == "modify" and not exists:
            raise DiffValidationError(
                f"Modify task attempted on missing file: {task.file_path}"
            )

        # P6.2 idempotency validation (best-effort for Python)
        try:
            snapshot = snapshot_python_file(str(target)) if exists else {"functions": [], "imports": []}
            IdempotencyValidator().validate(diff, snapshot)
        except ValueError as e:
            raise DiffValidationError(str(e))
        # Structural sanity checks
        if task.action_type == "modify" and task.file_path == "app.py":
            if re.search(r"^\+\s*return\b", diff, re.MULTILINE):
                raise DiffValidationError(
                    "Top-level return detected in script file"
                )
            if "subtract(" in diff and "from utils import subtract" not in diff:
                raise DiffValidationError(
                    "subtract used without import"
                )

        # Enforce script semantics regardless of filename
        if getattr(task, "file_role", "module") == "script":
            if re.search(r"^\+\s*return\b", diff, re.MULTILINE):
                raise DiffValidationError(
                    "Top-level return detected in script file"
                )

        # Generic guard: disallow top-level +return additions anywhere
        if task.action_type == "modify":
            for _ln in diff.splitlines():
                if _ln.startswith("+return"):
                    raise DiffValidationError(
                        "Top-level return detected (invalid Python structure)"
                    )

        return ValidatedDiff(diff=diff, files_changed=files)