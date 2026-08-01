from typing import Dict, Any
import re


class IdempotencyValidator:
    def validate(self, diff: str, snapshot: Dict[str, Any]) -> None:
        functions = snapshot.get("functions", [])

        for fn in functions:
            if re.search(rf"def\s+{re.escape(fn)}\s*\(", diff):
                raise ValueError(
                    f"Idempotency violation: function '{fn}' already exists"
                )
