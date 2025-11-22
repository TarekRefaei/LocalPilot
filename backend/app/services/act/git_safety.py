from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.core.config import settings


class GitAdapter(Protocol):
    def is_repo(self) -> bool: ...
    def has_uncommitted_changes(self) -> bool: ...
    def current_branch(self) -> str: ...
    def current_commit(self) -> str: ...
    def create_branch(self, name: str) -> None: ...
    def checkout(self, name: str) -> None: ...
    def add_all(self) -> None: ...
    def commit(self, message: str) -> None: ...
    def reset_hard(self, ref: str) -> None: ...


@dataclass
class GitSafetyContext:
    original_branch: str
    safety_branch: str
    base_commit: str


class GitSafetyError(RuntimeError):
    pass


class GitSafetyService:
    def __init__(self, git: GitAdapter):
        self.git = git

    def _apply_allowed(self) -> str:
        # mirrors extension setting: strict | git-optional | unsafe
        mode = settings.act_apply_safety.strip().lower()
        if mode not in {"strict", "git-optional", "unsafe"}:
            mode = "strict"
        return mode

    def ensure_safe_to_apply(self) -> None:
        mode = self._apply_allowed()
        in_repo = self.git.is_repo()
        dirty = self.git.has_uncommitted_changes() if in_repo else False

        if mode == "strict":
            if not in_repo:
                raise GitSafetyError("Workspace is not a Git repository. Initialize Git or change applySafety.")
            if dirty:
                raise GitSafetyError("Workspace has uncommitted changes. Commit or stash before applying.")
        elif mode == "git-optional":
            if in_repo and dirty:
                raise GitSafetyError("Uncommitted changes present. Clean working tree required.")
        else:
            # unsafe: allowed, but no-op
            pass

    def prepare_workspace(self, plan_id: str) -> GitSafetyContext:
        self.ensure_safe_to_apply()
        in_repo = self.git.is_repo()
        if not in_repo:
            # Outside Git and allowed by safety; create a synthetic context
            return GitSafetyContext(original_branch="", safety_branch="", base_commit="")

        original = self.git.current_branch()
        base = self.git.current_commit()
        branch = f"localpilot/plan-{plan_id}"
        self.git.create_branch(branch)
        self.git.checkout(branch)
        return GitSafetyContext(original_branch=original, safety_branch=branch, base_commit=base)

    def commit_todo(self, todo_id: str, message: str) -> None:
        if not self.git.is_repo():
            return
        self.git.add_all()
        self.git.commit(f"[LocalPilot] {message}\n\nTODO: {todo_id}")

    def rollback_last(self) -> None:
        if not self.git.is_repo():
            return
        self.git.reset_hard("HEAD~1")

    def rollback_all(self, ctx: GitSafetyContext) -> None:
        if not self.git.is_repo():
            return
        if ctx.base_commit:
            self.git.reset_hard(ctx.base_commit)
        if ctx.original_branch:
            self.git.checkout(ctx.original_branch)
