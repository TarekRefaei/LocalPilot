from typing import Literal

RepairKind = Literal[
    "remove_dependency",
    "add_dependency",
    "change_order_index",
    "swap_order_index",
    "remove_task",
    "rename_task_id",
]
