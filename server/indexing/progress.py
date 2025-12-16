from typing import Callable, Literal

Phase = Literal[
    "scan",
    "chunk",
    "embed",
    "store",
    "complete"
]


class ProgressTracker:
    def __init__(self, callback: Callable[[Phase, int, int], None]):
        self.callback = callback

    def report(self, phase: Phase, current: int, total: int) -> None:
        self.callback(phase, current, total)
