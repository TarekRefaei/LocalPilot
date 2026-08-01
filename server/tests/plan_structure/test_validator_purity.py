from copy import deepcopy

from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.graph_validator import validate_plan_graph


def test_validator_is_pure_function():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "t1",
                "orderIndex": 0,
                "filePath": "a.py",
                "actionType": "create",
                "dependencies": [],
            }
        ],
    }

    graph = build_plan_graph(plan)
    snapshot = deepcopy(graph.__dict__)

    validate_plan_graph(graph)

    assert graph.__dict__ == snapshot
