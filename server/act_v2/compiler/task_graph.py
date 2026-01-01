from typing import List
from server.plan.plan_parser import PlanSchema
from server.act_v2.models.execution_task import ExecutionTask
from pathlib import Path


def build_task_graph(plan: PlanSchema) -> List[ExecutionTask]:
    """
    Converts plan.tasks into a strictly ordered, dependency-safe graph.
    """
    sorted_tasks = sorted(plan.tasks, key=lambda t: t.orderIndex)

    graph: List[ExecutionTask] = []

    for t in sorted_tasks:
        rel_path = Path(t.filePath).as_posix()
        graph.append(
            ExecutionTask(
                task_id=t.id,
                title=t.title,
                file_path=rel_path,
                action_type=t.actionType,
                dependencies=t.dependencies or [],
                order_index=t.orderIndex,
            )
        )

    return graph
