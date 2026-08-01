from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Set

NodeKind = Literal["task"]
EdgeKind = Literal["depends_on", "file_order"]


@dataclass(frozen=True)
class PlanNode:
    id: str
    order_index: int
    file_path: str
    action_type: str
    depends_on: Set[str]


@dataclass(frozen=True)
class PlanEdge:
    source: str
    target: str
    kind: EdgeKind


@dataclass
class PlanGraph:
    nodes: Dict[str, PlanNode]
    edges: List[PlanEdge]

    def get_node(self, node_id: str) -> Optional[PlanNode]:
        return self.nodes.get(node_id)
