"""
Deeper contract comparator:
- Expects JSON Schema files generated for TypeScript interfaces in schemas_ts/<Name>.json
- Compares top-level and nested property keys against Pydantic models' model_json_schema()
- Reports missing/extra property names recursively
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Dict, Set

ROOT = Path(__file__).resolve().parents[1]
TS_SCHEMA_DIR = ROOT / "schemas_ts"
PY_MODEL_DIR = ROOT / "backend" / "app" / "models"


def collect_prop_keys_from_schema(schema: Dict, prefix: str = "") -> Set[str]:
    keys: Set[str] = set()
    props = schema.get("properties", {})
    for k, v in props.items():
        path = f"{prefix}.{k}" if prefix else k
        keys.add(path)
        if v.get("properties"):
            keys |= collect_prop_keys_from_schema(v, prefix=path)
        if v.get("type") == "array":
            items = v.get("items", {})
            if items.get("properties"):
                keys |= collect_prop_keys_from_schema(items, prefix=path + "[]")
    return keys


def load_ts_schema_keys(name: str) -> Set[str]:
    p = TS_SCHEMA_DIR / f"{name}.json"
    if not p.exists():
        return set()
    schema = json.loads(p.read_text(encoding="utf-8"))
    return collect_prop_keys_from_schema(schema)


def load_py_model_keys(path: Path) -> Dict[str, Set[str]]:
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    out: Dict[str, Set[str]] = {}
    try:
        from pydantic import BaseModel
    except Exception:
        return out
    for k, v in vars(mod).items():
        try:
            if isinstance(v, type) and issubclass(v, BaseModel):
                schema = v.model_json_schema()
                keys = collect_prop_keys_from_schema(schema)
                out[k] = keys
        except Exception:
            continue
    return out


def main():
    errors = False
    for f in PY_MODEL_DIR.glob("*.py"):
        py_models = load_py_model_keys(f)
        for model_name, py_keys in py_models.items():
            ts_keys = load_ts_schema_keys(model_name)
            if not ts_keys:
                print(
                    f"[WARN] No TS schema for {model_name} (expected schemas_ts/{model_name}.json)"
                )
                continue
            missing = ts_keys - py_keys
            extra = py_keys - ts_keys
            if missing or extra:
                errors = True
                print(f"[MISMATCH] {model_name}:")
                if missing:
                    print("  Missing keys in Python model:", sorted(missing)[:30])
                if extra:
                    print("  Extra keys in Python model:", sorted(extra)[:30])
    if errors:
        print("Contract parity FAILED")
        sys.exit(2)
    print("Contract parity OK")


if __name__ == "__main__":
    main()
