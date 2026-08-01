from pathlib import Path


def test_semantic_intent_gate_blocks_existing_function(tmp_path: Path):
    # Create a python file with an existing function
    (tmp_path / "utils.py").write_text("def subtract(a, b):\n    return a - b\n", encoding="utf-8")

    from server.execute_v2.compiler.plan_to_execution import compile_plan_to_execution

    plan = {
        "id": "p1",
        "title": "Test",
        "overview": "",
        "status": "approved",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "title": "Add function subtract",
                "description": "Add subtract function",
                "filePath": "utils.py",
                "actionType": "create",
                "details": ["Add function subtract"],
                "dependencies": [],
            }
        ],
    }

    execution = compile_plan_to_execution(plan=plan, workspace_root=str(tmp_path), model="mock")

    assert execution.status == "failed"
    assert len(execution.tasks) == 1
    assert execution.tasks[0].error.get("requires_plan_regeneration") is True
    assert execution.tasks[0].status == "failed"
    assert isinstance(execution.tasks[0].error, dict)
    assert execution.tasks[0].error.get("type") == "semantic"
    assert any("already exists" in str(m) for m in (execution.tasks[0].error.get("messages") or []))
    assert execution.tasks[0].error.get("requires_plan_regeneration") is True


def test_semantic_failure_is_terminal(tmp_path: Path):
    (tmp_path / "utils.py").write_text("def subtract(a, b):\n    return a - b\n", encoding="utf-8")

    from server.execute_v2.compiler.plan_to_execution import compile_plan_to_execution

    plan = {
        "id": "p1",
        "title": "Test",
        "overview": "",
        "status": "approved",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "title": "Add function subtract",
                "description": "Add function subtract",
                "filePath": "utils.py",
                "actionType": "create",
                "details": ["Add function subtract"],
                "dependencies": [],
            },
            {
                "id": "t2",
                "orderIndex": 1,
                "title": "Call subtract",
                "description": "",
                "filePath": "app.py",
                "actionType": "modify",
                "details": [],
                "dependencies": ["t1"],
            },
        ],
    }

    execution = compile_plan_to_execution(plan=plan, workspace_root=str(tmp_path), model="mock")

    assert execution.status == "failed"
    assert len(execution.tasks) == 1
