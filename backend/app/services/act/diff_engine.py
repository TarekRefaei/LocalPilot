from __future__ import annotations

import difflib
from dataclasses import dataclass


@dataclass
class DiffSummary:
    path: str
    additions: int
    deletions: int


def unified_diff(path: str, before: str, after: str) -> str:
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)
    diff = difflib.unified_diff(
        before_lines,
        after_lines,
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
        lineterm="",
        n=3,
    )
    return "\n".join(diff)


def summarize_diff(path: str, diff_text: str) -> DiffSummary:
    additions = 0
    deletions = 0
    for line in diff_text.splitlines():
        if not line:
            continue
        # skip headers
        if (
            line.startswith("+++")
            or line.startswith("---")
            or line.startswith("@@")
            or line.startswith("diff ")
        ):
            continue
        if line.startswith("+"):
            additions += 1
        elif line.startswith("-"):
            deletions += 1
    return DiffSummary(path=path, additions=additions, deletions=deletions)
