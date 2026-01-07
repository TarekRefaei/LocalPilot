import ast


class PythonStructureError(Exception):
    pass


def validate_python_structure(source: str, *, is_script: bool):
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise PythonStructureError(str(e))

    if is_script:
        for node in tree.body:
            if isinstance(node, ast.Return):
                raise PythonStructureError(
                    "Top-level return is forbidden in script files"
                )
            if isinstance(node, ast.FunctionDef):
                raise PythonStructureError(
                    "Function definitions are forbidden in script files"
                )
