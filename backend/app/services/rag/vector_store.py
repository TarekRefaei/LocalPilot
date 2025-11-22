"""
Vector store using ChromaDB with HNSW indexing.

Provides:
- Upsert chunks with embeddings and metadata
- Semantic search with filters
- Metadata-only search
- Collection management
"""

import logging
import time
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings
from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Vector store using ChromaDB with HNSW indexing.

    Stores code chunks with embeddings and metadata for semantic search.
    """

    def __init__(
        self,
        persist_directory: str | None = None,
        collection_name: str = "localpilot_codebase",
        ef_construction: int = 200,
        ef_search: int = 200,
        m: int = 16,
    ):
        """
        Initialize vector store.

        Args:
            persist_directory: Directory for persistent storage
            collection_name: Name of the collection
            ef_construction: HNSW construction parameter (higher = better quality)
            ef_search: HNSW search parameter (higher = better recall)
            m: HNSW M parameter (connections per layer)
        """
        # Resolve persist directory from settings if not provided
        self.persist_directory = persist_directory or settings.vector_db_path
        self.collection_name = collection_name

        # Create directory if needed
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )

        # Get or create collection with HNSW settings
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "cosine",
                "hnsw:construction_ef": ef_construction,
                "hnsw:M": m,
            },
        )

        # Statistics
        self._upsert_count = 0
        self._search_count = 0
        self._total_search_time = 0.0

        logger.info(
            f"VectorStore initialized: {collection_name} "
            f"(ef_construction={ef_construction}, ef_search={ef_search}, m={m})"
        )
        logger.info(f"Collection has {self.collection.count()} documents")

    async def upsert_chunks(
        self,
        chunks: list[dict[str, Any]],
    ) -> int:
        """
        Upsert code chunks with embeddings.

        Args:
            chunks: List of chunks with 'id', 'content', 'embedding', 'metadata'

        Returns:
            Number of chunks upserted
        """
        if not chunks:
            return 0

        # Prepare data for Chroma
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:
            ids.append(chunk["id"])
            documents.append(chunk["content"])
            embeddings.append(chunk["embedding"])

            # Prepare metadata (flatten for Chroma)
            metadata = chunk.get("metadata", {})
            # Ensure all metadata values are strings or numbers (Chroma requirement)
            flattened_metadata = {}
            for key, value in metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    flattened_metadata[key] = value
                elif isinstance(value, list):
                    # Convert lists to comma-separated strings
                    flattened_metadata[key] = ",".join(str(v) for v in value)
                else:
                    flattened_metadata[key] = str(value)

            metadatas.append(flattened_metadata)

        # Upsert to collection
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        self._upsert_count += len(chunks)
        logger.info(f"Upserted {len(chunks)} chunks (total: {self._upsert_count})")

        return len(chunks)

    async def search(
        self,
        query_embedding: list[float],
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
        min_score: float = 0.0,
    ) -> list[dict[str, Any]]:
        """
        Search for similar chunks.

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Metadata filters (e.g., {'language': 'typescript'})
            min_score: Minimum similarity score (0-1)

        Returns:
            List of results with content, metadata, and scores
        """
        start_time = time.time()

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters,
            include=["documents", "metadatas", "distances"],
        )

        elapsed = time.time() - start_time
        self._search_count += 1
        self._total_search_time += elapsed

        # Format results
        formatted_results = []

        if results["ids"] and len(results["ids"]) > 0:
            for i in range(len(results["ids"][0])):
                # Convert distance to similarity score
                # ChromaDB returns cosine distance: distance = 1 - similarity
                distance = results["distances"][0][i]
                similarity = 1.0 - distance

                # Filter by minimum score
                if similarity < min_score:
                    continue

                formatted_results.append(
                    {
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "score": round(similarity, 4),
                    }
                )

        logger.debug(
            f"Search completed in {elapsed:.3f}s: "
            f"found {len(formatted_results)} results (score >= {min_score})"
        )

        return formatted_results

    async def search_by_metadata(
        self,
        filters: dict[str, Any],
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Search by metadata only (no semantic search).

        Args:
            filters: Metadata filters
            limit: Maximum results to return

        Returns:
            List of matching chunks
        """
        results = self.collection.get(
            where=filters,
            limit=limit,
            include=["documents", "metadatas"],
        )

        formatted = []
        for i in range(len(results["ids"])):
            formatted.append(
                {
                    "id": results["ids"][i],
                    "content": results["documents"][i],
                    "metadata": results["metadatas"][i],
                    "score": 1.0,  # Exact match
                }
            )

        logger.debug(f"Metadata search found {len(formatted)} results")

        return formatted

    async def delete_chunks(self, chunk_ids: list[str]) -> int:
        """
        Delete chunks by ID.

        Args:
            chunk_ids: List of chunk IDs to delete

        Returns:
            Number of chunks deleted
        """
        if not chunk_ids:
            return 0

        self.collection.delete(ids=chunk_ids)
        logger.info(f"Deleted {len(chunk_ids)} chunks")

        return len(chunk_ids)

    async def clear_collection(self) -> None:
        """Clear all chunks from collection."""
        # Delete all by getting all IDs first
        all_data = self.collection.get(limit=100000)
        if all_data["ids"]:
            self.collection.delete(ids=all_data["ids"])
            logger.info(f"Cleared collection: deleted {len(all_data['ids'])} chunks")

    def get_statistics(self) -> dict[str, Any]:
        """Get vector store statistics."""
        count = self.collection.count()

        # Sample some documents to analyze
        sample_limit = min(100, count)
        if count > 0:
            sample = self.collection.peek(limit=sample_limit)

            languages = {}
            chunk_types = {}

            for metadata in sample["metadatas"]:
                lang = metadata.get("language", "unknown")
                languages[lang] = languages.get(lang, 0) + 1

                chunk_type = metadata.get("chunk_type", "unknown")
                chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
        else:
            languages = {}
            chunk_types = {}

        avg_search_time = (
            self._total_search_time / self._search_count if self._search_count > 0 else 0.0
        )

        return {
            "total_chunks": count,
            "collection_name": self.collection_name,
            "persist_directory": self.persist_directory,
            "languages": languages,
            "chunk_types": chunk_types,
            "total_upserts": self._upsert_count,
            "total_searches": self._search_count,
            "total_search_time_seconds": self._total_search_time,
            "average_search_time_seconds": avg_search_time,
        }

    def reset_statistics(self) -> None:
        """Reset statistics counters."""
        self._upsert_count = 0
        self._search_count = 0
        self._total_search_time = 0.0
