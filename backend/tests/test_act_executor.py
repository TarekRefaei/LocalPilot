from pathlib import Path
from app.services.act.executor import ActExecutor, OperationRequest
from app.services.act.git_safety import GitSafetyService


class FakeGit:
    def __init__(self):
        self.created = []
        self.checkouts = []
        self.added = 0
        self.commits = []
        self.resets = []

    def is_repo(self) -> bool:
        return True

    def has_uncommitted_changes(self) -> bool:
        return False

    def current_branch(self) -> str:
        return "main"

    def current_commit(self) -> str:
        return "abcdef"

    def create_branch(self, name: str) -> None:
        self.created.append(name)

    def checkout(self, name: str) -> None:
        self.checkouts.append(name)

    def add_all(self) -> None:
        self.added += 1

    def commit(self, message: str) -> None:
        self.commits.append(message)

    def reset_hard(self, ref: str) -> None:
        self.resets.append(ref)


def test_apply_writes_files_and_audit(tmp_path: Path, monkeypatch):
    # prepare
    from app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "act_apply_safety", "strict", raising=False)

    git = FakeGit()
    exe = ActExecutor(GitSafetyService(git))

    ops = [
        OperationRequest(type="create", path="docs/readme.md", content="# Title\n"),
        OperationRequest(type="modify", path="docs/readme.md", content="# Title\nMore\n"),
    ]

    # dry run
    previews = exe.dry_run(tmp_path, ops)
    assert any(p.path == "docs/readme.md" and p.diff for p in previews)

    # apply
    ctx, written = exe.apply(
        plan_id="p1",
        todo_id="t1",
        message="Create docs",
        root=tmp_path,
        ops=ops,
    )
    assert ctx.safety_branch.startswith("localpilot/plan-")
    assert (tmp_path / "docs/readme.md").exists()
    # audit exists
    audit_dir = tmp_path / ".localpilot" / "audit"
    files = list(audit_dir.glob("*.diff"))
    assert files, "expected audit diff file to be written"
    # per-TODO commit happened
    assert any("TODO: t1" in m for m in git.commits)
