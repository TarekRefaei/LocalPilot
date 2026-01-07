from pathlib import Path
import json
from typing import Dict

from server.execute_v2.models.execution_state import ExecutionState
from server.config.paths import EXECUTION_ROOT

EXECUTION_ROOT.mkdir(parents=True, exist_ok=True)


_EXECUTIONS: Dict[str, ExecutionState] = {}


def _execution_path(execution_id: str) -> Path:
    return EXECUTION_ROOT / f"{execution_id}.json"


def save_execution(state: ExecutionState):
    _EXECUTIONS[state.execution_id] = state
    path = _execution_path(state.execution_id)
    # Defense-in-depth: ensure directory exists on every save (handles rare runtime deletions)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    path.write_text(state.model_dump_json(indent=2), encoding="utf-8")


def get_execution(execution_id: str) -> ExecutionState:
    if execution_id in _EXECUTIONS:
        return _EXECUTIONS[execution_id]

    path = _execution_path(execution_id)
    if not path.exists():
        raise KeyError(execution_id)

    state = ExecutionState.model_validate_json(path.read_text(encoding="utf-8"))
    _EXECUTIONS[execution_id] = state
    return state


def load_all_executions() -> Dict[str, ExecutionState]:
    # Ensure directory exists even if initialization was bypassed or folder removed at runtime
    try:
        EXECUTION_ROOT.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    for p in EXECUTION_ROOT.glob("*.json"):
        try:
            state = ExecutionState.model_validate_json(p.read_text(encoding="utf-8"))
            _EXECUTIONS[state.execution_id] = state
        except Exception:
            continue
    return _EXECUTIONS
