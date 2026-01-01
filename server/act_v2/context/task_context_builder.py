from typing import Dict
from pathlib import Path


from server.act_v2.models.execution_task import ExecutionTask
from .workspace_reader import WorkspaceReader


MAX_CONTEXT_CHARS = 12_000


def build_task_context(
    task: ExecutionTask,
    workspace_root: Path
) -> Dict:
    """
    Builds the minimal deterministic context for ONE task.
    """

    reader = WorkspaceReader(workspace_root)

    context_files: Dict[str, str] = {}

    # Only the task-declared file is allowed
    if Path(task.file_path).is_absolute():
        raise RuntimeError(
            f"Absolute paths are forbidden: {task.file_path}"
        )

    try:
        content = reader.read_file(task.file_path)
        context_files[task.file_path] = content[:MAX_CONTEXT_CHARS]
    except FileNotFoundError:
        # File may not exist yet (create action)
        context_files[task.file_path] = ""
    except PermissionError:
        raise RuntimeError("Illegal file access attempted")

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "action": task.action_type,
            "file_path": task.file_path,
            "dependencies": task.dependencies,
        },
        "files": context_files,
        "rules": {
            "allowed_files": [task.file_path],
            "action_type": task.action_type,
        }
    }
