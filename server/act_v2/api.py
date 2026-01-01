from fastapi import APIRouter, HTTPException
from typing import Dict
from pathlib import Path

from server.act_v2.compiler.plan_compiler import compile_plan
from server.act_v2.ledger.execution_ledger import ExecutionLedger
from server.act_v2.context.task_context_builder import build_task_context
from server.act_v2.llm.invocation_service import InvocationService
from server.act_v2.llm.ollama_client import OllamaClient
from server.act_v2.validation.validation_errors import DiffValidationError
from server.act_v2.diff_validator import DiffValidationError as StrictDiffValidationError
from server.act_v2.apply.apply_errors import ApplyError
from server.act_v2.apply_engine import ApplyEngine
from server.act_v2.index_hook import reindex_files
from server.act_v2.errors import PlanCompilationError
from server.act_v2.validation.diff_parser import extract_diff


router = APIRouter(prefix="/api/execute", tags=["act_v2"])

ledger = ExecutionLedger()

client = OllamaClient(
    base_url="http://127.0.0.1:11434",
    model="qwen2.5-coder:7b-instruct-q4_K_M",
)
invoker = InvocationService(client)


@router.post("/plan")
def compile_plan_endpoint(payload: Dict):
    """
    Compile an APPROVED plan into an execution graph.
    """
    try:
        plan_id = payload.get("planId")
        plan = payload.get("plan")
        workspace_root = payload.get("workspaceRoot")

        if not workspace_root:
            raise HTTPException(status_code=400, detail="workspaceRoot required")

        if not plan_id or not plan:
            raise HTTPException(
                status_code=400,
                detail="planId and compiled plan object are required",
            )

        # Enforce approved plan contract
        if plan.get("status") != "approved":
            raise HTTPException(
                status_code=400,
                detail="Only approved plans may be executed",
            )

        execution = compile_plan(plan, workspace_root)
        execution.plan_id = plan_id  # canonical identity

        # Persist and set explicit initial status
        created = ledger.create(execution)
        created.status = "ready"
        # Optional: baseline workspace hash for drift detection
        try:
            created.baseline_hash = ApplyEngine.compute_hash(Path(workspace_root))
        except Exception:
            created.baseline_hash = None
        ledger.update(created.execution_id, created)
        return created.model_dump()

    except PlanCompilationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{execution_id}")
def get_execution_state(execution_id: str):
    state = ledger.get(execution_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution not found")
    return state.dict()


@router.post("/{execution_id}/prepare/{task_id}")
def prepare_task_context(execution_id: str, task_id: str):
    state = ledger.get(execution_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution not found")

    task = next((t for t in state.tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Enforce state machine: only from 'ready' we can prepare context
    if state.status != "ready":
        raise HTTPException(status_code=400, detail="Execution not ready")

    workspace = Path(state.workspace_root)
    context = build_task_context(task, workspace)
    context["workspace_root"] = str(workspace)

    state.status = "context_ready"
    state.current_task_id = task_id
    state.context = context
    ledger.update(execution_id, state)

    return {
        "execution_id": execution_id,
        "task_id": task_id,
        "context": context,
    }


@router.post("/{execution_id}/invoke/{task_id}")
def invoke_task(execution_id: str, task_id: str):
    state = ledger.get(execution_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution not found")

    task = next((t for t in state.tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if state.status != "context_ready":
        raise HTTPException(status_code=400, detail="Context not prepared")

    try:
        diff = invoker.invoke_task(task, state.context or {})
        state.status = "awaiting_human"
        state.last_diff = diff
        state.last_error = None
        ledger.update(execution_id, state)
        return {
            "status": "awaiting_human",
            "diff": diff,
        }

    except (DiffValidationError, StrictDiffValidationError) as e:
        state.status = "failed"
        state.last_error = str(e)
        ledger.update(execution_id, state)
        raise HTTPException(
            status_code=422,
            detail=f"Execution blocked by safety rule: {e}",
        )
    except ValueError as e:
        state.status = "failed"
        state.last_error = str(e)
        ledger.update(execution_id, state)
        raise HTTPException(
            status_code=422,
            detail=f"Invalid execution output: {e}",
        )


@router.post("/{execution_id}/apply")
def apply_execution(execution_id: str):
    state = ledger.get(execution_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution not found")

    if state.status != "awaiting_human":
        raise HTTPException(
            status_code=400,
            detail="Execution not awaiting approval",
        )

    try:
        workspace = Path(state.context["workspace_root"])  # type: ignore[index]

        # Drift detection: ensure workspace hasn't changed since compilation
        if getattr(state, "baseline_hash", None):
            current_hash = ApplyEngine.compute_hash(workspace)
            if current_hash != state.baseline_hash:
                raise ApplyError("Workspace changed since plan compilation. Regenerate plan.")

        engine = ApplyEngine(workspace)
        # sanitize diff to avoid trailing prose/ellipses/markdown
        sanitized = extract_diff(state.last_diff or "") if (state.last_diff or "").strip() else ""
        changed = engine.apply(sanitized)
        reindex_files(state.plan_id, changed, workspace)

        state.status = "completed"
        ledger.update(execution_id, state)

        return {"status": "applied"}

    except ApplyError as e:
        state.status = "failed"
        state.last_error = str(e)
        ledger.update(execution_id, state)
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/{execution_id}/reindex")
def reindex_after_apply(execution_id: str):
    state = ledger.get(execution_id)
    if not state or state.status != "completed":
        raise HTTPException(status_code=400, detail="Execution not completed")

    workspace = Path(state.context["workspace_root"])  # type: ignore[index]
    reindex_files(state.plan_id, [], workspace)

    return {"status": "indexed"}


# Human Gate (Final)
act_router = APIRouter(prefix="/api/act", tags=["act_v2"])

@act_router.post("/approve")
def approve_task(task_id: str):
    # block until user approval recorded (placeholder)
    return {"approved": True}
