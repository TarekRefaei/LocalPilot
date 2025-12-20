from typing import Callable, Optional


class ProgressTracker:
    """
    Phase 2.5
    ----------
    Lightweight progress reporter used by indexing services.
    """

    def __init__(self, callback: Callable[[str, int, int], None]):
        self._callback = callback

    def report(self, phase: str, current: int, total: int) -> None:
        if self._callback:
            self._callback(phase, current, total)
