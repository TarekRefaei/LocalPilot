from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.graph_validator import validate_plan_graph


def test_order_index_mismatch_is_detected():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "filePath": "a.py",
                "actionType": "create",
                "dependencies": [],
            },
            {
                "id": "t2",
                "orderIndex": 2,
                "filePath": "b.py",
                "actionType": "create",
                "dependencies": [],
            },
        ],
    }

    graph = build_plan_graph(plan)
    issues = validate_plan_graph(graph)

    assert any(i.code == "non_contiguous_order_index" for i in issues)
