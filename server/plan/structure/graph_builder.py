from typing import Dict, Any

from server.plan.structure.graph_types import PlanGraph, PlanNode, PlanEdge


def build_plan_graph(plan: Dict[str, Any]) -> PlanGraph:
    """
    Build a structural DAG from a plan.
    No validation, no execution, no semantics.
    """

    nodes: Dict[str, PlanNode] = {}
    edges: list[PlanEdge] = []

    for task in plan.get("tasks", []) or []:
        try:
            task_id = task.get("id")
            if not task_id:
                continue

            deps = set(task.get("dependencies", []) or [])
            order_index = task.get("orderIndex")
            file_path = task.get("filePath")
            action_type = task.get("actionType")

            if order_index is None:
                continue

            if file_path is None:
                file_path = ""
            if action_type is None:
                action_type = ""

            nodes[task_id] = PlanNode(
                id=task_id,
                order_index=order_index,
                file_path=file_path,
                action_type=action_type,
                depends_on=deps,
            )

            for dep in deps:
                edges.append(
                    PlanEdge(
                        source=dep,
                        target=task_id,
                        kind="depends_on",
                    )
                )
        except Exception:
            continue

    return PlanGraph(nodes=nodes, edges=edges)
