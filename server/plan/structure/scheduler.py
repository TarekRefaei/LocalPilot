from typing import List, Dict, Set

from server.plan.structure.graph_types import PlanGraph
from server.plan.structure.schedule_types import PlanSchedule, ScheduledTask


def build_execution_schedule(graph: PlanGraph) -> PlanSchedule:
    """
    Build a deterministic execution order from a structurally valid plan graph.

    Assumptions:
    - Graph is already validated (no cycles, no unknown deps, etc.)
    - order_index is contiguous and unique

    This function is PURE.
    """

    # Defensive invariant: scheduler must never accept invalid graphs
    for node in graph.nodes.values():
        if node.id in node.depends_on:
            raise RuntimeError("Scheduler received invalid graph (self dependency)")

    # Step 1: build dependency map
    deps: Dict[str, Set[str]] = {
        node_id: set(node.depends_on) for node_id, node in graph.nodes.items()
    }

    # Step 2: stable candidate pool
    # Sorted by (order_index, task_id) to guarantee determinism
    candidates = sorted(
        graph.nodes.values(),
        key=lambda n: (n.order_index, n.id),
    )

    schedule: List[ScheduledTask] = []
    completed: Set[str] = set()

    while candidates:
        progressed = False

        for node in list(candidates):
            if deps[node.id].issubset(completed):
                schedule.append(
                    ScheduledTask(
                        task_id=node.id,
                        order_index=node.order_index,
                    )
                )
                completed.add(node.id)
                candidates.remove(node)
                progressed = True
                break

        if not progressed:
            # This should never happen if validation ran correctly
            raise RuntimeError("Scheduler deadlock: unresolved dependencies")

    return PlanSchedule(ordered_tasks=schedule)
