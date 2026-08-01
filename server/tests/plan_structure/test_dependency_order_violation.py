from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.graph_validator import validate_plan_graph


def test_dependency_order_violation_is_detected():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 1,
                "filePath": "a.py",
                "actionType": "modify",
                "dependencies": ["t2"],
            },
            {
                "id": "t2",
                "orderIndex": 2,
                "filePath": "b.py",
                "actionType": "modify",
                "dependencies": [],
            },
        ],
    }

    graph = build_plan_graph(plan)
    issues = validate_plan_graph(graph)

    assert any(i.code == "dependency_order_violation" and i.task_id == "t1" for i in issues)
