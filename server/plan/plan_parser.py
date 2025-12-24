from __future__ import annotations
import json
import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Literal


class TaskSchema(BaseModel):
    id: str
    orderIndex: int
    title: str
    description: str
    filePath: str
    actionType: Literal["create", "modify", "delete"]
    details: List[str]
    dependencies: List[str]

    class Config:
        extra = "forbid"


class PlanSchema(BaseModel):
    id: str
    title: str
    overview: str
    status: Literal["draft"]
    tasks: List[TaskSchema]

    class Config:
        extra = "forbid"


class PlanParser:
    def _extract_json(self, markdown: str) -> Optional[str]:
        fence = re.compile(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", re.IGNORECASE)
        m = fence.search(markdown)
        if m:
            return m.group(1)
        start = markdown.find("{")
        end = markdown.rfind("}")
        if start != -1 and end != -1 and end > start:
            return markdown[start : end + 1]
        return None

    def parse(self, markdown: str) -> Dict[str, Any]:
        raw = self._extract_json(markdown or "")
        if raw is None:
            return {"markdown": markdown, "plan": None}
        try:
            data = json.loads(raw)
            plan = PlanSchema(**data)
            return {"markdown": markdown, "plan": plan.dict()}
        except (json.JSONDecodeError, ValidationError):
            return {"markdown": markdown, "plan": None}
