from typing import Optional, Any

from server.execute_v2.models.execution_state import ExecutionState
from server.execute_v2.models.execution_task import ExecutionTask


def get_current_task(state: ExecutionState) -> Optional[ExecutionTask]:
    if state.status == "failed":
        return None

    while state.current_task_index < len(state.tasks):
        task = state.tasks[state.current_task_index]

        # Skip tasks that already mutated files (replay-safe)
        if task.status == "done" and getattr(task, "changed_files", None):
            state.current_task_index += 1
            continue

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


def mark_failed(task: ExecutionTask, error: Any):
    task.status = "failed"
    task.error = error


def mark_skipped(task: ExecutionTask):
    task.status = "skipped"
