from typing import List

from server.plan.structure.graph_types import PlanGraph
from server.plan.structure.graph_issues import GraphIssue


def _detect_cycles(graph: PlanGraph) -> List[GraphIssue]:
    issues: List[GraphIssue] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node_id: str, stack: List[str]) -> None:
        if node_id in visiting:
            cycle = " -> ".join(stack + [node_id])
            issues.append(
                GraphIssue(
                    code="dependency_cycle",
                    message=f"Dependency cycle detected: {cycle}",
                    level="error",
                    task_id=node_id,
                )
            )
            return

        if node_id in visited:
            return

        node = graph.nodes.get(node_id)
        if node is None:
            # Unknown nodes are handled by unknown_dependency; don't traverse.
            visited.add(node_id)
            return

        visiting.add(node_id)
        stack.append(node_id)

        for dep in node.depends_on:
            if dep in graph.nodes:
                dfs(dep, stack)

        stack.pop()
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in graph.nodes:
        if node_id not in visited:
            dfs(node_id, [])

    return issues


def _validate_order_index(graph: PlanGraph) -> List[GraphIssue]:
    issues: List[GraphIssue] = []

    order_map: dict[int, list[str]] = {}
    for node in graph.nodes.values():
        order_map.setdefault(node.order_index, []).append(node.id)

    for idx, ids in order_map.items():
        if len(ids) > 1:
            issues.append(
                GraphIssue(
                    code="duplicate_order_index",
                    message=f"orderIndex {idx} is used by multiple tasks: {ids}",
                    level="error",
                )
            )

    expected = list(range(len(graph.nodes)))
    actual = sorted(order_map.keys())
    if actual != expected:
        issues.append(
            GraphIssue(
                code="non_contiguous_order_index",
                message=(
                    "orderIndex must be contiguous starting at 0 "
                    f"(expected {expected}, got {actual})"
                ),
                level="error",
            )
        )

    return issues


def _validate_dependency_order(graph: PlanGraph) -> List[GraphIssue]:
    issues: List[GraphIssue] = []

    for node in graph.nodes.values():
        for dep_id in node.depends_on:
            dep = graph.nodes.get(dep_id)
            if not dep:
                continue

            if dep.order_index >= node.order_index:
                issues.append(
                    GraphIssue(
                        code="dependency_order_violation",
                        message=(
                            f"Task '{node.id}' depends on '{dep_id}' "
                            f"which has orderIndex {dep.order_index} ≥ {node.order_index}"
                        ),
                        level="error",
                        task_id=node.id,
                    )
                )

    return issues


def validate_plan_graph(graph: PlanGraph) -> List[GraphIssue]:
    """
    Phase 8.x validator.
    P8.1 Patch 2: self-dependency detection.
    """

    issues: List[GraphIssue] = []

    issues.extend(_detect_cycles(graph))
    issues.extend(_validate_order_index(graph))
    issues.extend(_validate_dependency_order(graph))

    known_ids = set(graph.nodes.keys())
    for node in graph.nodes.values():
        for dep in node.depends_on:
            if dep == node.id:
                issues.append(
                    GraphIssue(
                        code="self_dependency",
                        message=f"Task '{node.id}' depends on itself",
                        level="error",
                        task_id=node.id,
                    )
                )
                continue
            if dep not in known_ids:
                issues.append(
                    GraphIssue(
                        code="unknown_dependency",
                        message=f"Task '{node.id}' depends on unknown task '{dep}'",
                        level="error",
                        task_id=node.id,
                    )
                )

    return issues
