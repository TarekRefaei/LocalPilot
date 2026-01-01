from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any
from .execution_task import ExecutionTask


class ExecutionState(BaseModel):
    execution_id: str
    plan_id: str
    workspace_root: str
    status: Literal[
        "pending",
        "ready",
        "context_ready",
        "validated",
        "running",
        "awaiting_human",
        "failed",
        "completed",
    ]
    current_task_id: Optional[str]
    tasks: List[ExecutionTask]
    context: Optional[Dict[str, Any]] = None
    last_error: Optional[str] = None
    last_diff: Optional[str] = None
    baseline_hash: Optional[str] = None
