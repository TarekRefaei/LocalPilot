import pytest
from pathlib import Path

from server.execute_v2.compiler.plan_to_execution import compile_plan_to_execution


def _assert_blocked(plan, tmp_path: Path, expected_code: str):
    with pytest.raises(Exception) as e:
        compile_plan_to_execution(
            plan=plan,
            workspace_root=str(tmp_path),
            model="mock",
        )

    err = e.value
    if hasattr(err, "codes"):
        assert expected_code in err.codes
    else:
        assert expected_code in str(err)


def test_execution_blocked_on_dependency_cycle(tmp_path: Path):
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "t1", "orderIndex": 0, "filePath": "a.py", "actionType": "create", "dependencies": ["t2"]},
            {"id": "t2", "orderIndex": 1, "filePath": "b.py", "actionType": "create", "dependencies": ["t1"]},
        ],
    }

    _assert_blocked(plan, tmp_path, "dependency_cycle")


def test_execution_blocked_on_duplicate_order_index(tmp_path: Path):
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "t1", "orderIndex": 0, "filePath": "a.py", "actionType": "create", "dependencies": []},
            {"id": "t2", "orderIndex": 0, "filePath": "b.py", "actionType": "create", "dependencies": []},
        ],
    }

    _assert_blocked(plan, tmp_path, "duplicate_order_index")


def test_execution_blocked_on_non_contiguous_order_index(tmp_path: Path):
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "t1", "orderIndex": 0, "filePath": "a.py", "actionType": "create", "dependencies": []},
            {"id": "t2", "orderIndex": 2, "filePath": "b.py", "actionType": "create", "dependencies": []},
        ],
    }

    _assert_blocked(plan, tmp_path, "non_contiguous_order_index")


def test_execution_blocked_on_self_dependency(tmp_path: Path):
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "t1", "orderIndex": 0, "filePath": "a.py", "actionType": "modify", "dependencies": ["t1"]},
        ],
    }

    _assert_blocked(plan, tmp_path, "self_dependency")


def test_execution_blocked_on_unknown_dependency(tmp_path: Path):
    plan = {
        "id": "p1",
        "tasks": [
            {"id": "t1", "orderIndex": 0, "filePath": "a.py", "actionType": "create", "dependencies": ["ghost"]},
        ],
    }

    _assert_blocked(plan, tmp_path, "unknown_dependency")
