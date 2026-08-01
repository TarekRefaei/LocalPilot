from __future__ import annotations

import ast
from typing import Dict, List


def snapshot_python_file(path: str) -> Dict[str, List[str]]:
    """
    Extract high-level semantic structure from a Python file.
    """

    try:
        with open(path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except Exception:
        return {"functions": [], "imports": []}

    functions: List[str] = []
    imports: List[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return {
        "functions": sorted(set(functions)),
        "imports": sorted(set(imports)),
    }
