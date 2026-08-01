from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from server.plan.structure.diagnostics import analyze_plan_structure

router = APIRouter(prefix="/api/plan/structure", tags=["plan-structure"])


@router.post("/analyze")
def analyze_structure(payload: Dict[str, Any]):
    plan = payload.get("plan")
    if not isinstance(plan, dict):
        raise HTTPException(status_code=400, detail="Invalid plan")

    issues = analyze_plan_structure(plan)

    return {
        "issues": [
            {
                "code": i.code,
                "message": i.message,
                "level": i.level,
                "taskId": i.task_id,
            }
            for i in issues
        ]
    }
