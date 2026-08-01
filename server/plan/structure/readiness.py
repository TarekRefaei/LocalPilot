from typing import List

from server.plan.structure.graph_issues import GraphIssue


BLOCKING_CODES = {
    "dependency_cycle",
    "duplicate_order_index",
    "non_contiguous_order_index",
    "dependency_order_violation",
    "self_dependency",
    "unknown_dependency",
}


def is_plan_structurally_executable(
    issues: List[GraphIssue],
) -> bool:
    return not any(i.code in BLOCKING_CODES for i in issues)
