from app.services.act.git_safety import GitSafetyService, GitSafetyError


class FakeGit:
    def __init__(self, repo: bool, dirty: bool):
        self._repo = repo
        self._dirty = dirty
        self.created = []
        self.checkouts = []
        self.commits = []
        self.reset_refs = []

    def is_repo(self) -> bool:
        return self._repo

    def has_uncommitted_changes(self) -> bool:
        return self._dirty

    def current_branch(self) -> str:
        return "main"

    def current_commit(self) -> str:
        return "abcdef"

    def create_branch(self, name: str) -> None:
        self.created.append(name)

    def checkout(self, name: str) -> None:
        self.checkouts.append(name)

    def add_all(self) -> None:
        pass

    def commit(self, message: str) -> None:
        self.commits.append(message)

    def reset_hard(self, ref: str) -> None:
        self.reset_refs.append(ref)


def test_strict_blocks_outside_git(monkeypatch):
    from app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "act_apply_safety", "strict", raising=False)

    svc = GitSafetyService(FakeGit(repo=False, dirty=False))
    try:
        svc.ensure_safe_to_apply()
        assert False, "should have raised"
    except GitSafetyError:
        assert True


def test_git_optional_allows_outside_git(monkeypatch):
    from app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "act_apply_safety", "git-optional", raising=False)

    svc = GitSafetyService(FakeGit(repo=False, dirty=False))
    svc.ensure_safe_to_apply()  # no exception


def test_dirty_tree_blocked_in_strict(monkeypatch):
    from app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "act_apply_safety", "strict", raising=False)

    svc = GitSafetyService(FakeGit(repo=True, dirty=True))
    try:
        svc.ensure_safe_to_apply()
        assert False
    except GitSafetyError:
        assert True


def test_prepare_workspace_creates_branch_in_repo(monkeypatch):
    from app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "act_apply_safety", "strict", raising=False)

    git = FakeGit(repo=True, dirty=False)
    svc = GitSafetyService(git)
    ctx = svc.prepare_workspace("123")
    assert ctx.original_branch == "main"
    assert ctx.safety_branch == "localpilot/plan-123"
    assert git.created == ["localpilot/plan-123"]
    assert git.checkouts[-1] == "localpilot/plan-123"
