"""
Basic contract parity checker:
- Extracts 'export interface <Name> { ... }' fields from TypeScript contract files under extension/src/contracts
- Imports Pydantic models under backend/app/models (by filename) and compares field names
- Prints mismatches and returns non-zero exit code if parity fails

Limitations:
 - This script only checks presence of field names (no types)
 - TS parsing uses simple regex; it expects fairly standard 'export interface' blocks
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TS_CONTRACT_DIR = ROOT / "extension" / "src" / "contracts"
PY_MODEL_DIR = ROOT / "backend" / "app" / "models"

INTERFACE_RE = re.compile(r"export\s+interface\s+([A-Za-z0-9_]+)\s*{([^}]*)}", re.S)
FIELD_RE = re.compile(r"([A-Za-z0-9_]+)\s*[:?]")


def parse_ts_interfaces(path: Path):
    text = path.read_text(encoding="utf-8")
    out: dict[str, set[str]] = {}
    for m in INTERFACE_RE.finditer(text):
        name = m.group(1)
        body = m.group(2)
        fields = set(FIELD_RE.findall(body))
        out[name] = fields
    return out


def load_pydantic_model_fields(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    if spec is None or spec.loader is None:
        return {}
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[assignment]
    out: dict[str, set[str]] = {}
    for k, v in vars(mod).items():
        try:
            from pydantic import BaseModel

            if isinstance(v, type) and issubclass(v, BaseModel):
                fields: set[str] = set()
                if hasattr(v, "__fields__"):
                    fields = set(getattr(v, "__fields__").keys())  # pydantic v1
                elif hasattr(v, "model_fields"):
                    fields = set(getattr(v, "model_fields").keys())  # pydantic v2
                out[k] = fields
        except Exception:
            continue
    return out


def main() -> int:
    ts_map: dict[str, set[str]] = {}
    if TS_CONTRACT_DIR.exists():
        for f in TS_CONTRACT_DIR.glob("*.ts"):
            ts_map.update(parse_ts_interfaces(f))

    py_map: dict[str, set[str]] = {}
    if PY_MODEL_DIR.exists():
        for f in PY_MODEL_DIR.glob("*.py"):
            try:
                py_map.update(load_pydantic_model_fields(f))
            except Exception:
                continue

    ok = True
    for name, ts_fields in ts_map.items():
        if name in py_map:
            py_fields = py_map[name]
            missing = ts_fields - py_fields
            extra = py_fields - ts_fields
            if missing or extra:
                ok = False
                print(f"Contract mismatch for {name}:")
                if missing:
                    print("  Missing in Python model:", missing)
                if extra:
                    print("  Extra in Python model:", extra)
        else:
            print(f"TS interface {name} has no corresponding Python model (skipping)")

    if not ok:
        print("Contract parity check failed")
        return 2
    print("Contract parity check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
