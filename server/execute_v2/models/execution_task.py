from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel
from server.execute_v2.constants import TASK_STATUS


class ExecutionTask(BaseModel):
    execution_task_id: str
    plan_task_id: str
    order_index: int

    title: str
    file_path: str
    action_type: Literal["create", "modify", "delete"]
    file_role: Literal["script", "module"] = "module"

    status: TASK_STATUS = "pending"

    last_diff: Optional[str] = None
    error: Optional[str] = None
    changed_files: Optional[List[str]] = None
    insertion: Optional[Dict[str, Any]] = None
