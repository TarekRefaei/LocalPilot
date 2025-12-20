from pathlib import Path
from .vector_store import VectorStore

class QueryService:
    def __init__(
        self,
        index_root: Path,
        project_id: str,
        embedder,
    ):
        self.index_root = index_root
        self.project_id = project_id
        self.embedder = embedder

        self.store = VectorStore(
            persist_dir=str(index_root / project_id / "chroma"),
            collection_name="code_chunks",
        )

    def query(self, text: str, top_k: int = 5):
        embedding = self.embedder.embed([text])[0]
        return self.store.query(embedding, top_k=top_k)
