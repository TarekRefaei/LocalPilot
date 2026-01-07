from typing import Optional

from server.execute_v2.models.execution_state import ExecutionState
from server.execute_v2.models.execution_task import ExecutionTask


def get_current_task(state: ExecutionState) -> Optional[ExecutionTask]:
    while state.current_task_index < len(state.tasks):
        task = state.tasks[state.current_task_index]

        if task.status in ("done", "skipped"):
            state.current_task_index += 1
            continue

        # Block progression if task has an error (policy-free cursor)
        if getattr(task, "error", None):
            return None

        return task

    state.status = "completed"
    return None


def mark_running(task: ExecutionTask):
    task.status = "running"


def mark_done(task: ExecutionTask, diff: str):
    task.status = "done"
    task.last_diff = diff


def mark_failed(task: ExecutionTask, error: str):
    task.status = "failed"
    task.error = error


def mark_skipped(task: ExecutionTask):
    task.status = "skipped"
