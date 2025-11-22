from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from app.services.act.diff_engine import DiffSummary, summarize_diff, unified_diff
from app.services.act.git_safety import GitSafetyContext, GitSafetyService

logger = logging.getLogger(__name__)


@dataclass
class OperationRequest:
    type: str  # create | modify | delete
    path: str
    content: str | None = None  # new content for create/modify


@dataclass
class OperationPreview:
    path: str
    type: str
    diff: str
    summary: DiffSummary


class ActExecutor:
    def __init__(self, git_safety: GitSafetyService):
        self.git_safety = git_safety

    def dry_run(self, root: Path, ops: Iterable[OperationRequest]) -> list[OperationPreview]:
        previews: list[OperationPreview] = []
        root = Path(root)
        for op in ops:
            file_path = (root / op.path).resolve()
            before = ""
            if file_path.exists() and file_path.is_file():
                before = file_path.read_text(encoding="utf-8", errors="ignore")
            after = before
            if op.type == "create":
                after = op.content or ""
            elif op.type == "modify":
                after = op.content or before
            elif op.type == "delete":
                after = ""
            else:
                raise ValueError(f"Unknown operation type: {op.type}")
            diff = unified_diff(op.path, before, after)
            summary = summarize_diff(op.path, diff)
            previews.append(
                OperationPreview(path=op.path, type=op.type, diff=diff, summary=summary)
            )
        return previews

    def apply(
        self,
        plan_id: str,
        todo_id: str,
        message: str,
        root: Path,
        ops: Iterable[OperationRequest],
    ) -> tuple[GitSafetyContext, list[Path]]:
        ctx = self.git_safety.prepare_workspace(plan_id)
        written: list[Path] = []
        root = Path(root)
        # Build audit diff while applying
        audit_chunks: list[str] = []
        for op in ops:
            path = root / op.path
            path.parent.mkdir(parents=True, exist_ok=True)
            before_text = ""
            if path.exists() and path.is_file():
                try:
                    before_text = path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    before_text = ""
            if op.type in ("create", "modify"):
                content = op.content or ""
                path.write_text(content, encoding="utf-8")
                written.append(path)
                logger.info("act.apply.write", extra={"path": str(path)})
            elif op.type == "delete":
                if path.exists():
                    path.unlink()
                    logger.info("act.apply.delete", extra={"path": str(path)})
            else:
                raise ValueError(f"Unknown operation type: {op.type}")
            # Append diff for audit
            after_text = ""
            if path.exists() and path.is_file():
                try:
                    after_text = path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    after_text = ""
            diff_txt = unified_diff(op.path, before_text, after_text)
            audit_chunks.append(diff_txt)
        # Commit per TODO when in repo
        self.git_safety.commit_todo(todo_id, message)
        logger.info("act.apply.commit", extra={"todo": todo_id})
        # Write audit file under .localpilot/audit
        try:
            audit_root = root / ".localpilot" / "audit"
            audit_root.mkdir(parents=True, exist_ok=True)
            ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            audit_file = audit_root / f"{ts}-plan-{plan_id}-todo-{todo_id}.diff"
            audit_text = "\n\n".join(audit_chunks)
            audit_file.write_text(audit_text, encoding="utf-8")
            logger.info("act.apply.audit", extra={"file": str(audit_file)})
        except Exception as e:
            logger.warning("act.apply.audit_failed", extra={"error": str(e)})
        return ctx, written

    def rollback_last(self) -> None:
        self.git_safety.rollback_last()

    def rollback_all(self, ctx: GitSafetyContext) -> None:
        self.git_safety.rollback_all(ctx)
