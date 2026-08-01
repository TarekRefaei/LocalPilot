from typing import Dict, Any, List

from server.plan.structure.graph_builder import build_plan_graph
from server.plan.structure.graph_validator import validate_plan_graph
from server.plan.structure.graph_issues import GraphIssue


def analyze_plan_structure(plan: Dict[str, Any]) -> List[GraphIssue]:
    """
    Read-only structural analysis.
    MUST NOT mutate plan or execution.
    """

    graph = build_plan_graph(plan)
    return validate_plan_graph(graph)
