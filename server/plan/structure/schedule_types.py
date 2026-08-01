from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ScheduledTask:
    task_id: str
    order_index: int


@dataclass(frozen=True)
class PlanSchedule:
    ordered_tasks: List[ScheduledTask]
