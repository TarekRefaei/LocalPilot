from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import json
import queue
import threading

from server.api.dependencies import get_index_root, get_embedder
from server.indexing.service import IndexingService
from server.indexing.progress import ProgressTracker

router = APIRouter()


@router.get("/index/{project_id}")
def index_project(
    project_id: str,
    workspace_root: str,
    index_root: Path = Depends(get_index_root),
    embedder = Depends(get_embedder),
):
    # Early validation of workspace path
    workspace = Path(workspace_root)
    if not workspace.exists() or not workspace.is_dir():
        raise HTTPException(status_code=400, detail="Invalid workspace root")

    q: queue.Queue = queue.Queue()

    def run_indexing():
        try:

            def on_progress(phase: str, current: int, total: int):
                q.put({
                    "type": "index:progress",
                    "phase": phase,
                    "current": current,
                    "total": total,
                })

            tracker = ProgressTracker(on_progress)

            service = IndexingService(
                workspace=workspace,
                index_root=index_root / project_id,
                embedder=embedder,
                progress=tracker,
            )

            service.run()

            q.put({ "type": "index:done" })

        except Exception as e:
            q.put({
                "type": "error",
                "message": str(e),
            })

    threading.Thread(target=run_indexing, daemon=True).start()

    def event_stream():
        while True:
            event = q.get()
            yield f"data: {json.dumps(event)}\n\n"
            if event["type"] in ("index:done", "error"):
                break

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )
