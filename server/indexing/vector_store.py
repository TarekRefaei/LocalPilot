from typing import List, Optional, Dict, Any
import chromadb
from chromadb.config import Settings

from .chunk import CodeChunk


class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        chunks: List[CodeChunk],
        embeddings: List[List[float]],
    ) -> None:
        if not chunks:
            return

        self.collection.add(
            ids=[c.id for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[
                {
                    "file_path": c.file_path,
                    "language": c.language,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "symbol_type": c.symbol_type,
                }
                for c in chunks
            ],
            embeddings=embeddings,
        )
        # PersistentClient auto-persists

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        if self.collection.count() == 0:
            return []

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        hits: List[Dict] = []
        for i in range(len(result["ids"][0])):
            hits.append(
                {
                    "id": result["ids"][0][i],
                    "content": result["documents"][0][i],
                    "metadata": result["metadatas"][0][i],
                    "distance": result["distances"][0][i],
                }
            )

        return hits
