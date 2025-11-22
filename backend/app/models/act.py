from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class OperationRequest(BaseModel):
    type: Literal["create", "modify", "delete"]
    path: str
    content: str | None = None


class DryRunPayload(BaseModel):
    workspace_path: str
    plan_id: str
    todo_id: str
    operations: list[OperationRequest]


class ApplyPayload(BaseModel):
    workspace_path: str
    plan_id: str
    todo_id: str
    message: str
    operations: list[OperationRequest]
    approved: bool = False


class ApprovalOperation(BaseModel):
    path: str
    type: str
    diff: str
    additions: int
    deletions: int
    requiresApproval: bool


class DryRunResult(BaseModel):
    operations: list[ApprovalOperation]
    autoApprovedPaths: list[str] = []
    requiresReviewCount: int = 0


class ApplyResult(BaseModel):
    written: list[str]
    todo_id: str
    plan_id: str
