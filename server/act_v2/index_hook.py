from server.indexing.service import IndexingService
from server.api.dependencies import get_embedder, get_index_root
from pathlib import Path


def reindex_files(project_id: str, files: list[str], workspace: Path):
    service = IndexingService(
        workspace=workspace,
        index_root=get_index_root() / project_id,
        embedder=get_embedder(),
    )
    service.run()
