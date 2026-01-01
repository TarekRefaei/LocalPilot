from pydantic import BaseModel
from typing import List, Literal


class ExecutionTask(BaseModel):
    task_id: str
    title: str
    file_path: str
    action_type: Literal["create", "modify", "delete"]
    dependencies: List[str]
    order_index: int
