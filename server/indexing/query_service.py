from pathlib import Path
from typing import List, Optional

from .vector_store import VectorStore


class QueryService:
    """
    Phase 1.1
    ----------
    Responsible for:
    - Embedding user query
    - Retrieving relevant code chunks from vector store
    - Returning raw retrieval results (no prompt logic)
    """

    def __init__(
        self,
        index_root: Path,
        embedder,
        collection_name: str = "code_chunks"
    ):
        self.embedder = embedder
        self.store = VectorStore(
            persist_dir=str(index_root / "chroma"),
            collection_name=collection_name
        )

    def query(
        self,
        text: str,
        top_k: int = 5,
        where: Optional[dict] = None
    ) -> List[dict]:
        embedding = self.embedder.embed([text])[0]

        return self.store.query(
            query_embedding=embedding,
            top_k=top_k,
            where=where
        )
