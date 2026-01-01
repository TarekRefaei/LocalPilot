from pathlib import Path


def assert_path_allowed(root: Path, target: Path):
    root = root.resolve()
    target = target.resolve()

    if not str(target).startswith(str(root)):
        raise PermissionError(
            f"Write outside workspace blocked: {target}"
        )
