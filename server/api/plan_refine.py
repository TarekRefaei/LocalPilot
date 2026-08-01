from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from server.plan.refinement.contracts import PlanRefinementProposal
from server.plan.refinement.validator import validate_and_apply_refinement
from server.llm.refinement_client import invoke_refinement_llm

router = APIRouter(prefix="/api/plan/refine", tags=["plan-refine"])


@router.post("")
def refine_plan(payload: Dict[str, Any]):
    plan = payload.get("plan")
    issues = payload.get("structuralIssues")

    if not isinstance(plan, dict) or not isinstance(issues, list) or not issues:
        raise HTTPException(status_code=400, detail="Invalid payload")

    try:
        proposal_json = invoke_refinement_llm(plan, issues)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))

    proposal = PlanRefinementProposal.model_validate(proposal_json)

    try:
        repaired = validate_and_apply_refinement(plan, proposal)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    print(
        f"[plan-refine] plan={plan.get('id')} "
        f"repairs={[r.kind for r in proposal.repairs]}"
    )

    return {
        "originalPlanId": plan.get("id"),
        "repairedPlan": repaired,
        "repairs": proposal.repairs,
    }
