from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException

try:
    from server.api.dependencies import get_index_root
except ImportError:
    from server.api.dependencies import get_index_root

router = APIRouter()


@router.get("/project/{project_id}/summary")
def get_project_summary(
    project_id: str,
    index_root: Path = Depends(get_index_root),
):
    summary_path = index_root / project_id / "summary.json"
    if not summary_path.exists():
        raise HTTPException(status_code=404, detail="summary not found")

    with open(summary_path, "r", encoding="utf-8") as f:
        return __import__("json").load(f)
