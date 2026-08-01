from pathlib import Path


def test_idempotent_diff_is_blocked(tmp_path: Path):
    (tmp_path / "utils.py").write_text(
        "def subtract(a, b):\n    return a - b\n", encoding="utf-8"
    )

    from server.execute_v2.validation.idempotency_validator import IdempotencyValidator

    diff = """
+def subtract(a, b):
+    return a - b
"""

    snapshot = {"functions": ["subtract"]}

    try:
        IdempotencyValidator().validate(diff, snapshot)
        assert False, "Expected idempotency violation"
    except ValueError as e:
        assert "already exists" in str(e)
