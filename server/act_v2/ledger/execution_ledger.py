from typing import Dict, Optional
from threading import Lock
from server.act_v2.models.execution_state import ExecutionState
from pathlib import Path
import json
import uuid
from .models import ExecutionLedgerModel, TaskRecord


class ExecutionLedger:
    """
    In-memory authoritative execution registry.
    Persistent backend will replace this later.
    """

    def __init__(self):
        self._lock = Lock()
        self._executions: Dict[str, ExecutionState] = {}

    def create(self, state: ExecutionState) -> ExecutionState:
        with self._lock:
            self._executions[state.execution_id] = state
        return state

    def get(self, execution_id: str) -> Optional[ExecutionState]:
        return self._executions.get(execution_id)

    def update(self, execution_id: str, state: ExecutionState) -> None:
        with self._lock:
            self._executions[execution_id] = state


# Persistent ledger foundation (Phase 5.9)
LEDGER_ROOT = Path.home() / ".localpilot" / "executions"


class PersistentExecutionLedger:
    def __init__(self, plan_id: str):
        self.execution_id = str(uuid.uuid4())
        self.path = LEDGER_ROOT / f"{self.execution_id}.json"
        self.model = ExecutionLedgerModel(
            execution_id=self.execution_id,
            plan_id=plan_id,
            status="running",
        )

    def save(self):
        LEDGER_ROOT.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self.model.json(indent=2), encoding="utf-8")

    @classmethod
    def load(cls, execution_id: str):
        path = LEDGER_ROOT / f"{execution_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        ledger = cls(data["plan_id"])
        ledger.execution_id = execution_id
        ledger.path = path
        ledger.model = ExecutionLedgerModel(**data)
        return ledger

    def record_task(
        self,
        task_id: str,
        status: str,
        diff_hash: str | None = None,
        files_changed: list[str] | None = None,
    ):
        self.model.tasks.append(
            TaskRecord(
                task_id=task_id,
                status=status, 
                diff_hash=diff_hash,
                files_changed=files_changed or [],
            )
        )
        self.model.current_task = task_id
        self.save()

    def complete(self):
        self.model.status = "completed"
        self.save()
