from typing import List, Literal
from pydantic import BaseModel
import time


TaskStatus = Literal["pending", "done", "failed", "skipped"]
ExecutionStatus = Literal["running", "paused", "failed", "completed"]


class TaskRecord(BaseModel):
    task_id: str
    status: TaskStatus
    diff_hash: str | None = None
    files_changed: List[str] = []
    timestamp: float = time.time()


class ExecutionLedgerModel(BaseModel):
    execution_id: str
    plan_id: str
    status: ExecutionStatus
    current_task: str | None = None
    tasks: List[TaskRecord] = []
