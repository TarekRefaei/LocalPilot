from typing import Literal

EXECUTION_STATUS = Literal[
    "running",
    "paused",
    "completed",
    "failed",
]

TASK_STATUS = Literal[
    "pending",
    "running",
    "done",
    "failed",
    "skipped",
]
