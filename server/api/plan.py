from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from server.api.dependencies import get_index_root
from server.plan.plan_service import PlanService
from server.plan.plan_parser import PlanParser


router = APIRouter()


class PlanRequest(BaseModel):
    project_id: str
    model: str
    messages: List[Dict[str, str]]


@router.post("/plan")
def generate_plan(request: PlanRequest, index_root: Path = Depends(get_index_root)) -> Dict[str, Any]:
    service = PlanService(index_root=index_root, project_id=request.project_id, model=request.model)
    markdown = service.generate(chat_messages=request.messages)
    parser = PlanParser()
    result = parser.parse(markdown)
    return result
