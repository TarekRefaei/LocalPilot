from typing import Dict, Union
from uuid import uuid4


from server.plan.plan_parser import PlanSchema
from server.act_v2.models.execution_state import ExecutionState
from server.act_v2.compiler.task_graph import build_task_graph
from server.act_v2.errors import PlanCompilationError
from pathlib import Path



ALLOWED_ACTIONS = {"create", "modify", "delete"}


def compile_plan(plan: Union[PlanSchema, Dict], workspace_root: str) -> ExecutionState:
    """
    Deterministically compile a validated Plan into an executable task graph.
    Accepts either a PlanSchema or a dict conforming to PlanSchema.
    Only executable tasks (create/modify/delete with a non-empty filePath) are included.
    """
    if isinstance(plan, dict):
        plan = PlanSchema(**plan)

    executable_tasks = []

    for t in plan.tasks:
        if t.actionType not in ALLOWED_ACTIONS:
            continue
        if not t.filePath:
            continue
        executable_tasks.append(t)

    if not executable_tasks:
        raise PlanCompilationError("No executable tasks found in plan")

    tasks = build_task_graph(
        plan.copy(update={"tasks": executable_tasks})
    )

    # Enforce workspace-relative paths
    for t in tasks:
        if Path(t.file_path).is_absolute():
            raise PlanCompilationError(
                f"Illegal absolute path in plan task '{t.task_id}': {t.file_path}"
            )

    # Preflight existence checks — fail early before LLM invocation
    # Allow a modify if the plan includes a prior create of the same file
    workspace = Path(workspace_root)
    for t in tasks:
        target = workspace / t.file_path
        if t.action_type == "create" and target.exists():
            raise PlanCompilationError(
                f"Create task attempted on existing file: {t.file_path}"
            )
        if t.action_type == "modify":
            if target.exists():
                continue
            will_be_created_before = any(
                ct.action_type == "create"
                and ct.file_path == t.file_path
                and (ct.order_index < t.order_index or ct.task_id in (t.dependencies or []))
                for ct in tasks
            )
            if not will_be_created_before:
                raise PlanCompilationError(
                    f"Modify task attempted on missing file: {t.file_path}"
                )

    return ExecutionState(
        execution_id=str(uuid4()),
        plan_id=plan.id,
        workspace_root=workspace_root,
        status="pending",
        current_task_id=None,
        tasks=tasks,
    )
