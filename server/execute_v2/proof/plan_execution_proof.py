from typing import List
from server.execute_v2.models.execution_state import ExecutionState


class ExecutionProofError(Exception):
    pass


def verify_execution_proof(state: ExecutionState):
    """
    Ensures execution tasks:
    - Match plan tasks 1:1 (no duplicates)
    - Are ordered correctly (order_index equals position)
    - (Extension point) Respect dependencies — not enforced here due to plan schema locality
    """
    plan_ids: List[str] = [t.plan_task_id for t in state.tasks]

    if len(plan_ids) != len(set(plan_ids)):
        raise ExecutionProofError("Duplicate execution tasks detected")

    for i, task in enumerate(state.tasks):
        if task.order_index != i:
            raise ExecutionProofError(
                f"Execution order mismatch at task {task.execution_task_id}"
            )
