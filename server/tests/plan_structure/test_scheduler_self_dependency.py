from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.graph_validator import validate_plan_graph
from server.plan.structure.readiness import is_plan_structurally_executable


def test_scheduler_refuses_self_dependency():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "filePath": "a.py",
                "actionType": "modify",
                "dependencies": ["t1"],
            }
        ],
    }

    graph = build_plan_graph(plan)
    issues = validate_plan_graph(graph)

    assert any(i.code == "self_dependency" for i in issues)
    assert is_plan_structurally_executable(issues) is False
