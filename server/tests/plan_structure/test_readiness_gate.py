from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.graph_validator import validate_plan_graph
from server.plan.structure.readiness import is_plan_structurally_executable


def test_readiness_gate_blocks_on_blocking_issues():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "filePath": "a.py",
                "actionType": "create",
                "dependencies": ["t2"],
            },
            {
                "id": "t2",
                "orderIndex": 1,
                "filePath": "b.py",
                "actionType": "create",
                "dependencies": ["t1"],
            },
        ],
    }

    graph = build_plan_graph(plan)
    issues = validate_plan_graph(graph)

    assert is_plan_structurally_executable(issues) is False
