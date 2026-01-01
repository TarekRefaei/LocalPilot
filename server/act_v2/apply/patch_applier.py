import subprocess
from pathlib import Path

from .apply_errors import PatchApplyFailed


def apply_patch(diff: str, workspace_root: Path) -> None:
    if not diff.strip():
        return

    # Safety: ensure git repo exists
    if not (workspace_root / ".git").exists():
        raise PatchApplyFailed("Workspace is not a git repository")

    # Dry-run first
    dry = subprocess.run(
        ["git", "apply", "--check"],
        input=diff,
        cwd=workspace_root,
        text=True,
        capture_output=True,
    )

    if dry.returncode != 0:
        raise PatchApplyFailed(dry.stderr)

    # Apply for real
    apply = subprocess.run(
        ["git", "apply"],
        input=diff,
        cwd=workspace_root,
        text=True,
        capture_output=True,
    )

    if apply.returncode != 0:
        raise PatchApplyFailed(apply.stderr)
