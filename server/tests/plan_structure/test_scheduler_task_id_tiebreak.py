from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.scheduler import build_execution_schedule


def test_scheduler_uses_task_id_as_tie_breaker():
    plan = {
        "id": "p1",
        "tasks": [
            {
                "id": "b",
                "orderIndex": 0,
                "filePath": "b.py",
                "actionType": "create",
                "dependencies": [],
            },
            {
                "id": "a",
                "orderIndex": 0,
                "filePath": "a.py",
                "actionType": "create",
                "dependencies": [],
            },
        ],
    }

    graph = build_plan_graph(plan)
    schedule = build_execution_schedule(graph)
    task_ids = [t.task_id for t in schedule.ordered_tasks]

    assert task_ids == ["a", "b"]
