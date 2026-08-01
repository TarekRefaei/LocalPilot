from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from server.api.dependencies import get_index_root
from server.plan.plan_service import PlanService
from server.plan.plan_parser import PlanParser
from server.plan.auto_fix import PlanAutoFixer
from server.plan.minimizer import minimize_plan
from server.plan.repair import repair_plan


router = APIRouter()


class PlanRequest(BaseModel):
    project_id: str
    model: str
    messages: List[Dict[str, str]]
    workspace_root: str | None = None


@router.post("/plan")
def generate_plan(request: PlanRequest, index_root: Path = Depends(get_index_root)) -> Dict[str, Any]:
    workspace_root = Path(request.workspace_root) if request.workspace_root else None
    service = PlanService(
        index_root=index_root,
        project_id=request.project_id,
        model=request.model,
        workspace_root=workspace_root,
    )
    markdown = service.generate(chat_messages=request.messages)
    parser = PlanParser()
    result = parser.parse(markdown)
    try:
        if result.get("plan"):
            result["plan"] = minimize_plan(result["plan"])  # type: ignore[arg-type]
    except Exception:
        pass
    return result


class AutoFixRequest(BaseModel):
    markdown: str
    workspace_root: str


class PlanRepairWorkspace(BaseModel):
    existingFiles: List[str] = []


class PlanRepairRequest(BaseModel):
    plan: Dict[str, Any]
    markdown: str
    blockingWarnings: List[Dict[str, Any]]
    workspace: PlanRepairWorkspace


@router.post("/plan/auto-fix")
def auto_fix_plan(request: AutoFixRequest) -> Dict[str, Any]:
    parser = PlanParser()
    parsed = parser.parse(request.markdown)
    if not parsed.get("plan"):
        # keep consistent 400 style used above
        raise HTTPException(status_code=400, detail="Invalid plan JSON")

    workspace = Path(request.workspace_root)
    if not workspace.exists() or not workspace.is_dir():
        raise HTTPException(status_code=400, detail="Invalid workspace root")
    fixer = PlanAutoFixer(workspace)
    result = fixer.auto_fix(parsed["plan"])  # type: ignore[arg-type]

    return {
        "fixedPlan": result.fixed_plan,
        "warnings": result.warnings,
        "diff": result.diff,
    }


@router.post("/plan/repair")
def repair_plan_endpoint(request: PlanRepairRequest) -> Dict[str, Any]:
    return repair_plan(request.dict())
