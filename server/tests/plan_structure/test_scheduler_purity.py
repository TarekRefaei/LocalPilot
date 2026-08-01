from copy import deepcopy

from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.scheduler import build_execution_schedule


def test_scheduler_is_pure_function():
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

    build_execution_schedule(graph)

    assert graph.__dict__ == snapshot
