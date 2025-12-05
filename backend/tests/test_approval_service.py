from app.services.act.approval import FileOperation, categorize_operations


def test_auto_approve_safe_creates_docs_tests_localpilot(monkeypatch):
    from app.core import config as cfg

    monkeypatch.setattr(
        cfg.settings, "act_autoapprove_safe_creates", True, raising=False
    )

    ops = [
        FileOperation(type="create", path="docs/readme.md"),
        FileOperation(type="create", path="tests/unit/foo.test.ts"),
        FileOperation(type="create", path="__tests__/bar.spec.ts"),
        FileOperation(type="create", path=".localpilot/audit/1.diff"),
        FileOperation(type="create", path="src/app.ts"),
        FileOperation(type="modify", path="src/app.ts"),
    ]

    auto, review = categorize_operations(ops)
    auto_paths = {o.path for o in auto}

    assert "docs/readme.md" in auto_paths
    assert "tests/unit/foo.test.ts" in auto_paths
    assert "__tests__/bar.spec.ts" in auto_paths
    assert ".localpilot/audit/1.diff" in auto_paths
    assert any(o.path == "src/app.ts" for o in review)
