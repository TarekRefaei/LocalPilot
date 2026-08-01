from typing import Literal, List
from pydantic import BaseModel


class ExecutionError(BaseModel):
    type: Literal["semantic", "diff", "runtime", "internal"]
    messages: List[str]
    retryable: bool = False
    requires_plan_regeneration: bool = False
    repair_hints: List[str] = []

    @property
    def is_terminal(self) -> bool:
        return self.type == "semantic"
