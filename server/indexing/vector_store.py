from typing import List, Optional

import chromadb

from .chunk import CodeChunk


class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.Client(
            settings=chromadb.Settings(
                persist_directory=persist_dir,
                anonymized_telemetry=False
            )
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        chunks: List[CodeChunk],
        embeddings: List[List[float]]
    ) -> None:
        self.collection.add(
            ids=[c.id for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[
                {
                    "file_path": c.file_path,
                    "language": c.language,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "symbol_type": c.symbol_type
                }
                for c in chunks
            ],
            embeddings=embeddings
        )
        self.client.persist()

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[dict] = None
    ) -> List[dict]:
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )

        hits = []
        for i in range(len(result["ids"][0])):
            hits.append({
                "id": result["ids"][0][i],
                "content": result["documents"][0][i],
                "metadata": result["metadatas"][0][i],
                "distance": result["distances"][0][i]
            })

        return hits
