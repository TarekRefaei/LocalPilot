from typing import List

from server.plan.structure.graph_issues import GraphIssue


class StructuralPlanError(Exception):
    """
    Raised when a plan is structurally invalid and cannot be executed.
    """

    def __init__(self, issues: List[GraphIssue]):
        self.issues = issues
        self.codes = sorted({i.code for i in issues})
        super().__init__(self._format())

    def _format(self) -> str:
        return f"Plan is structurally invalid: {', '.join(self.codes)}"
