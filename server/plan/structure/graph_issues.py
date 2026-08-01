from dataclasses import dataclass
from typing import Literal

IssueLevel = Literal["error", "warning"]


@dataclass(frozen=True)
class GraphIssue:
    code: str
    message: str
    level: IssueLevel = "error"
    task_id: str | None = None
