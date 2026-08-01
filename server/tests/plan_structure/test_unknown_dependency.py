from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.graph_validator import validate_plan_graph


def test_unknown_dependency_is_reported():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "title": "Task 1",
                "filePath": "a.py",
                "actionType": "create",
                "dependencies": ["ghost"],
            }
        ],
    }

    graph = build_plan_graph(plan)
    issues = validate_plan_graph(graph)

    assert any(i.code == "unknown_dependency" and i.task_id == "t1" for i in issues)
