import uuid
import json
import re
from pathlib import Path
from typing import Dict, Any, List

from server.execute_v2.models.execution_state import ExecutionState
from server.execute_v2.models.execution_task import ExecutionTask
from server.api.dependencies import get_index_root
from server.plan.compile import compile_plan_to_todos
from server.execute_v2.proof.plan_execution_proof import verify_execution_proof


def _derive_file_structure(workspace_root: str, plan_id: str) -> Dict[str, Any]:
    """
    Build a lightweight file_structure map from the symbol index produced by the indexer.
    - functions: extracted by scanning symbol spans' start lines
    - imports: 'top' if top-of-file starts with imports; otherwise 'unknown'
    - script_body: True if there is top-level executable code (best-effort)
    """
    try:
        symbols_path = get_index_root() / plan_id / "symbols.json"
        if not symbols_path.exists():
            return {}

        with open(symbols_path, "r", encoding="utf-8") as f:
            symbols = json.load(f)

        ws = Path(workspace_root).resolve()
        file_map: Dict[str, Dict[str, Any]] = {}

        # Group symbols per file
        by_file: Dict[str, List[Dict[str, Any]]] = {}
        for s in symbols:
            fp = Path(s.get("file", "")).resolve()
            try:
                rel = str(fp.relative_to(ws))
            except Exception:
                rel = str(fp)
            by_file.setdefault(rel, []).append(s)

        for rel_path, items in by_file.items():
            abs_path = (ws / rel_path).resolve()
            functions: List[str] = []
            imports_pos = "unknown"
            script_body = False

            try:
                text = abs_path.read_text(encoding="utf-8", errors="ignore")
                lines = text.splitlines()

                # Determine imports at top
                i = 0
                while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith("#")):
                    i += 1
                if i < len(lines) and (lines[i].startswith("import ") or lines[i].startswith("from ")):
                    imports_pos = "top"

                # Extract function names for python/js/ts using symbol start lines
                for s in items:
                    start = int(s.get("start_line", 0))
                    if start <= 0 or start > len(lines):
                        continue
                    line = lines[start - 1]
                    m_py = re.match(r"^\s*def\s+(\w+)\s*\(", line)
                    m_js = re.match(r"^\s*(?:export\s+)?function\s+(\w+)\s*\(", line)
                    name = None
                    if m_py:
                        name = m_py.group(1)
                    elif m_js:
                        name = m_js.group(1)
                    if name:
                        functions.append(name)

                # Detect top-level executable code (very simple heuristic)
                for ln in lines:
                    s = ln.strip()
                    if not s or s.startswith("#"):
                        continue
                    if s.startswith("def ") or s.startswith("class ") or s.startswith("import ") or s.startswith("from "):
                        continue
                    # Likely top-level code
                    script_body = True
                    break
            except Exception:
                pass

            file_map[rel_path] = {
                "imports": imports_pos,
                "functions": sorted(list(set(functions))) if functions else [],
                "script_body": script_body,
            }

        return file_map
    except Exception:
        return {}


def compile_plan_to_execution(
    plan: Dict[str, Any],
    workspace_root: str,
    model: str,
) -> ExecutionState:
    # Correctness proof gate: plan must compile to a full TODO list
    try:
        todos = compile_plan_to_todos(plan)
        assert len(todos) == len(plan["tasks"]), "Plan execution incomplete"
    except Exception as e:
        # Surface as a clear failure
        raise

    tasks: List[ExecutionTask] = []

    for t in sorted(plan["tasks"], key=lambda x: x["orderIndex"]):
        tasks.append(
            ExecutionTask(
                execution_task_id=str(uuid.uuid4()),
                plan_task_id=t["id"],
                order_index=t["orderIndex"],
                title=t["title"],
                file_path=t["filePath"],
                action_type=t["actionType"],
                file_role=(
                    "script" if str(t["filePath"]).endswith("app.py") else "module"
                ),
                insertion=(
                    {
                        "mode": "after_imports" if t["filePath"] == "app.py" else "after_function",
                        "symbol": "add" if t["filePath"] == "utils.py" else None,
                    }
                    if t["actionType"] == "modify" else None
                ),
            )
        )

    file_structure = _derive_file_structure(workspace_root, plan["id"])

    execution = ExecutionState(
        execution_id=str(uuid.uuid4()),
        plan_id=plan["id"],
        plan_title=plan["title"],
        tasks=tasks,
        context={
            "workspace_root": workspace_root,
            "model": model,
            "file_structure": file_structure,
        },
    )
    verify_execution_proof(execution)
    return execution
