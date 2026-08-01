from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from time import time

from .execution_task import ExecutionTask
from server.execute_v2.constants import EXECUTION_STATUS


class ExecutionState(BaseModel):
    execution_id: str
    plan_id: str
    plan_title: str

    status: EXECUTION_STATUS = "running"

    current_task_index: int = 0
    tasks: List[ExecutionTask]

    context: Dict[str, Any]

    proof: Optional[Dict[str, Any]] = None

    created_at: float = time()
    updated_at: float = time()
