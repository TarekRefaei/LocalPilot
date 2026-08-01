from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from pathlib import Path
from time import time
from fastapi.responses import JSONResponse

from server.execute_v2.compiler.plan_to_execution import compile_plan_to_execution
from server.execute_v2.engine.execution_cursor import (
    get_current_task,
    mark_running,
    mark_done,
    mark_failed,
)
from server.execute_v2.store import save_execution, get_execution

from server.execute_v2.llm.invocation_service import InvocationService
from server.execute_v2.llm.ollama_client import OllamaClient
from server.execute_v2.validation.diff_parser import extract_diff
from server.execute_v2.apply_engine import ApplyEngine
from server.execute_v2.index_hook import reindex_files
from server.execute_v2.validation.diff_validator import DiffValidator
from server.execute_v2.validation.validation_errors import DiffValidationError

from server.plan.repair_diagnostics import diagnose_execution_failure


router = APIRouter(prefix="/api/execute_v2", tags=["execute_v2"])


class StartExecutionRequest(BaseModel):
    plan: Dict[str, Any]
    workspace_root: str
    model: str


@router.post("/plan")
def start_execution(payload: StartExecutionRequest):
    execution = compile_plan_to_execution(
        plan=payload.plan,
        workspace_root=payload.workspace_root,
        model=payload.model,
    )
    save_execution(execution)
    return execution.model_dump()


@router.get("/{execution_id}")
def get_execution_state(execution_id: str):
    """
    Phase 5.3
    ----------
    Read-only execution state endpoint.
    Used by Execution Timeline UI.
    """
    try:
        state = get_execution(execution_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Execution not found")

    return JSONResponse(
        content={
            "executionId": state.execution_id,
            "planTitle": state.plan_title,
            "status": state.status,
            "currentTaskIndex": state.current_task_index,
            "tasks": [
                {
                    "executionTaskId": t.execution_task_id,
                    "planTaskId": t.plan_task_id,
                    "orderIndex": t.order_index,
                    "title": t.title,
                    "filePath": t.file_path,
                    "actionType": t.action_type,
                    "status": t.status,
                    "lastDiff": t.last_diff,
                    "error": t.error,
                }
                for t in state.tasks
            ],
            "repairProposals": (
                diagnose_execution_failure(state.tasks[state.current_task_index].error)
                if state.status == "failed"
                and state.current_task_index < len(state.tasks)
                and state.tasks[state.current_task_index].error
                else []
            ),
        }
    )


@router.post("/{execution_id}/next")
def execute_next(execution_id: str):
    try:
        state = get_execution(execution_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Execution not found")

    task = get_current_task(state)

    if not task:
        return {"status": "completed"}

    mark_running(task)
    # Mutation guard timestamp
    state.updated_at = time()
    save_execution(state)

    try:
        model_name = state.context.get("model") if isinstance(state.context, dict) else None
        if not isinstance(model_name, str) or not model_name:
            model_name = "qwen2.5-coder:7b-instruct-q4_K_M"
        client = OllamaClient(base_url="http://127.0.0.1:11434", model=model_name)
        invoker = InvocationService(client)
        raw = invoker.invoke_task(task, state.context or {})
        diff = extract_diff(raw)
        task.last_diff = diff
        save_execution(state)
        return {
            "status": "awaiting_apply",
            "task": {
                "id": task.execution_task_id,
                "title": task.title,
                "diff": diff,
            },
        }
    except DiffValidationError as e:
        mark_failed(task, str(e))
        state.status = "running"
        state.updated_at = time()
        save_execution(state)
        return {
            "status": "task_failed",
            "error": task.error,
            "task": {
                "id": task.execution_task_id,
                "title": task.title,
            },
        }
    except Exception as e:
        mark_failed(task, str(e))
        state.status = "failed"
        state.updated_at = time()
        try:
            save_execution(state)
        except Exception:
            pass
        raise


@router.post("/{execution_id}/apply")
def apply_diff(execution_id: str):
    try:
        state = get_execution(execution_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Execution not found")

    if state.current_task_index >= len(state.tasks):
        raise HTTPException(status_code=400, detail="No task to apply")

    task = state.tasks[state.current_task_index]

    if not task.last_diff or not task.last_diff.strip():
        raise HTTPException(status_code=400, detail="No diff to apply")

    workspace_root = state.context.get("workspace_root") if isinstance(state.context, dict) else None
    if not workspace_root:
        raise HTTPException(status_code=400, detail="workspace_root missing from context")

    engine = ApplyEngine(Path(workspace_root))
    sanitized = extract_diff(task.last_diff)
    # Defense-in-depth: re-validate before destructive apply
    DiffValidator().validate(sanitized, task, Path(workspace_root))
    changed_files = engine.apply(
        sanitized,
        is_script=(getattr(task, "file_role", "module") == "script"),
    )

    mark_done(task, task.last_diff)
    # Advance the cursor immediately after successful apply
    state.current_task_index += 1
    # Persist changed files for future selective reindex/audit
    try:
        task.changed_files = changed_files
    except Exception:
        pass
    # Mutation guard timestamp
    state.updated_at = time()
    save_execution(state)
    return {"status": "applied"}


@router.post("/{execution_id}/reindex")
def reindex_after_apply(execution_id: str):
    try:
        state = get_execution(execution_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Execution not found")

    workspace_root = state.context.get("workspace_root") if isinstance(state.context, dict) else None
    if not workspace_root:
        raise HTTPException(status_code=400, detail="workspace_root missing from context")

    # Trigger incremental reindex (no changed files tracking at this layer in Phase 5.1)
    reindex_files(state.plan_id, [], Path(workspace_root))
    return {"status": "indexed"}


@router.post("/{execution_id}/resume")
def resume_execution(execution_id: str):
    try:
        state = get_execution(execution_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Execution not found")

    # Semantic failures are terminal
    if state.status == "failed":
        raise HTTPException(
            status_code=400,
            detail="Execution failed due to semantic errors and cannot be resumed",
        )

    if state.status in ("completed",):
        return {"status": state.status}

    state.status = "running"
    state.updated_at = time()
    save_execution(state)
    return {"status": "resumed"}


@router.post("/{execution_id}/skip")
def skip_task(execution_id: str):
    try:
        state = get_execution(execution_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Execution not found")

    task = get_current_task(state)
    if not task:
        return {"status": "completed"}

    task.status = "skipped"
    state.current_task_index += 1
    state.updated_at = time()
    save_execution(state)
    return {"status": "skipped"}


@router.post("/{execution_id}/retry")
def retry_task(execution_id: str):
    try:
        state = get_execution(execution_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Execution not found")

    idx = state.current_task_index
    if idx >= len(state.tasks):
        raise HTTPException(status_code=400, detail="No task to retry")

    task = state.tasks[idx]
    if task.status != "failed":
        raise HTTPException(status_code=400, detail="Task is not failed")

    if isinstance(task.error, dict):
        if task.error.get("type") == "semantic":
            raise HTTPException(
                status_code=400,
                detail="Semantic failure cannot be retried. Regenerate or repair the plan.",
            )

    task.status = "pending"
    task.error = None
    task.last_diff = None
    
    # IMPORTANT:
    # Retry must re-run execution, not just reset state.
    state.status = "running"
    state.updated_at = time()
    save_execution(state)
    
    # Re-execute the task immediately
    return execute_next(execution_id)
