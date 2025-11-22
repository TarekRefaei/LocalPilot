from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from app.core.config import settings


@dataclass
class FileOperation:
    type: str  # create | modify | delete
    path: str
    content: str | None = None
    diff: str | None = None
    requiresApproval: bool = True


SAFE_DOC_EXT = {".md", ".mdx", ".txt", ".rst"}


def _lower_unix(path: str) -> str:
    return path.replace("\\", "/").lower()


def _is_safe_create(path: str) -> bool:
    p = _lower_unix(path)
    if p.startswith(".localpilot/"):
        return True
    if p.startswith("docs/"):
        return any(p.endswith(ext) for ext in SAFE_DOC_EXT)
    if p.startswith("tests/") or p.startswith("__tests__/") or "/__tests__/" in p:
        return ".test." in p or ".spec." in p
    return False


def categorize_operations(
    ops: Iterable[FileOperation],
) -> tuple[list[FileOperation], list[FileOperation]]:
    auto: list[FileOperation] = []
    review: list[FileOperation] = []

    allow_safe = bool(settings.act_autoapprove_safe_creates)

    for op in ops:
        if op.type == "create" and allow_safe and _is_safe_create(op.path):
            auto.append(op)
        else:
            review.append(op)

    return auto, review
