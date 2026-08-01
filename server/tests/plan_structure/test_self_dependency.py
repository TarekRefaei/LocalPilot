from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.graph_validator import validate_plan_graph


def test_self_dependency_is_detected():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "title": "Self dependent",
                "filePath": "a.py",
                "actionType": "modify",
                "dependencies": ["t1"],
            }
        ],
    }

    graph = build_plan_graph(plan)
    issues = validate_plan_graph(graph)

    assert any(i.code == "self_dependency" and i.task_id == "t1" for i in issues)
