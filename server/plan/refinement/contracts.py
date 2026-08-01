from typing import List, Optional, Literal, Union

from pydantic import BaseModel, Field

from server.plan.refinement.refinement_types import RepairKind


class BaseRepair(BaseModel):
    kind: RepairKind
    reason: str = Field(min_length=3, max_length=200)


class RemoveDependencyRepair(BaseRepair):
    kind: Literal["remove_dependency"]
    taskId: str
    dependency: str


class AddDependencyRepair(BaseRepair):
    kind: Literal["add_dependency"]
    taskId: str
    dependency: str


class ChangeOrderIndexRepair(BaseRepair):
    kind: Literal["change_order_index"]
    taskId: str
    newOrderIndex: int


class SwapOrderIndexRepair(BaseRepair):
    kind: Literal["swap_order_index"]
    taskA: str
    taskB: str


class RemoveTaskRepair(BaseRepair):
    kind: Literal["remove_task"]
    taskId: str


class RenameTaskIdRepair(BaseRepair):
    kind: Literal["rename_task_id"]
    oldId: str
    newId: str


RepairOperation = Union[
    RemoveDependencyRepair,
    AddDependencyRepair,
    ChangeOrderIndexRepair,
    SwapOrderIndexRepair,
    RemoveTaskRepair,
    RenameTaskIdRepair,
]


class PlanRefinementProposal(BaseModel):
    repairs: List[RepairOperation]

    class Config:
        extra = "forbid"


class StructuralIssueInput(BaseModel):
    code: str
    message: str
    taskId: Optional[str] = None


class PlanRefinementInput(BaseModel):
    plan: dict
    structuralIssues: List[StructuralIssueInput]
    constraints: dict


SYSTEM_PROMPT = """You are a structural plan refinement engine.

Your task is to propose STRUCTURAL REPAIRS ONLY.

You MUST:
- Output VALID JSON ONLY
- Follow the provided schema exactly
- Use ONLY the allowed repair kinds
- Preserve all task IDs unless explicitly renaming
- Never invent tasks
- Never modify files or code
- Never explain your reasoning

You MUST NOT:
- Execute anything
- Generate diffs
- Change plan semantics
- Output markdown or text

If no safe repair exists, output:

{ \"repairs\": [] }
"""


USER_PROMPT_TEMPLATE = """PLAN:
{{PLAN_JSON}}

STRUCTURAL ISSUES:
{{STRUCTURAL_ISSUES_JSON}}

CONSTRAINTS:
{{CONSTRAINTS_JSON}}

Propose the minimal set of structural repairs
required to eliminate ALL structural issues.

Return JSON ONLY.
"""
