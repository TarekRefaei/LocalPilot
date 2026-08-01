import pytest

from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.scheduler import build_execution_schedule


def test_scheduler_refuses_cyclic_graph():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "a",
                "orderIndex": 0,
                "filePath": "a.py",
                "actionType": "modify",
                "dependencies": ["b"],
            },
            {
                "id": "b",
                "orderIndex": 1,
                "filePath": "b.py",
                "actionType": "modify",
                "dependencies": ["a"],
            },
        ],
    }

    graph = build_plan_graph(plan)

    with pytest.raises(RuntimeError):
        build_execution_schedule(graph)
