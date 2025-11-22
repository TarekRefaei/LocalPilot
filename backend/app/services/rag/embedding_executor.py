"""
Phase 5: Embeddings & Vector Store Executor

Orchestrates embedding generation and vector store upsert for code chunks.
Emits progress events via WebSocket.
"""

import asyncio
import logging
import time
from typing import Any, Callable, Optional

from ..indexing.chunking import CodeChunk
from .embedding_service import EmbeddingService
from .vector_store import VectorStore

logger = logging.getLogger(__name__)


class EmbeddingExecutor:
    """
    Execute Phase 5: Generate embeddings and upsert to vector store.

    Responsibilities:
    - Batch chunks for efficient embedding
    - Generate embeddings via Ollama
    - Upsert to ChromaDB with metadata
    - Emit progress events
    - Handle errors gracefully
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        batch_size: int = 32,
    ):
        """
        Initialize embedding executor.

        Args:
            embedding_service: EmbeddingService instance
            vector_store: VectorStore instance
            batch_size: Number of chunks to embed per batch
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.batch_size = batch_size

        # Statistics
        self._total_chunks = 0
        self._embedded_chunks = 0
        self._failed_chunks = 0
        self._total_time = 0.0

        logger.info(
            f"EmbeddingExecutor initialized (batch_size={batch_size})"
        )

    async def execute(
        self,
        chunks: list[CodeChunk],
        progress_callback: Optional[Callable[[dict[str, Any]], None]] = None,
    ) -> dict[str, Any]:
        """
        Execute Phase 5: embed chunks and upsert to vector store.

        Args:
            chunks: List of CodeChunk objects from Phase 4
            progress_callback: Optional callback for progress events

        Returns:
            Execution result with statistics
        """
        start_time = time.time()
        self._total_chunks = len(chunks)
        self._embedded_chunks = 0
        self._failed_chunks = 0

        logger.info(f"Starting Phase 5: Embeddings for {len(chunks)} chunks")

        if progress_callback:
            progress_callback(
                {
                    "phase": "embeddings",
                    "status": "started",
                    "total_chunks": len(chunks),
                }
            )

        try:
            # Process chunks in batches
            for batch_idx in range(0, len(chunks), self.batch_size):
                batch = chunks[batch_idx : batch_idx + self.batch_size]
                batch_num = batch_idx // self.batch_size + 1
                total_batches = (len(chunks) + self.batch_size - 1) // self.batch_size

                await self._process_batch(
                    batch,
                    batch_num,
                    total_batches,
                    progress_callback,
                )

            elapsed = time.time() - start_time
            self._total_time = elapsed

            result = {
                "phase": "embeddings",
                "status": "completed",
                "total_chunks": self._total_chunks,
                "embedded_chunks": self._embedded_chunks,
                "failed_chunks": self._failed_chunks,
                "duration_seconds": elapsed,
                "average_time_per_chunk": (
                    elapsed / self._embedded_chunks
                    if self._embedded_chunks > 0
                    else 0.0
                ),
            }

            logger.info(
                f"Phase 5 completed: {self._embedded_chunks}/{self._total_chunks} "
                f"chunks embedded in {elapsed:.2f}s"
            )

            if progress_callback:
                progress_callback(result)

            return result

        except Exception as e:
            logger.error(f"Phase 5 failed: {e}", exc_info=True)
            raise

    async def _process_batch(
        self,
        batch: list[CodeChunk],
        batch_num: int,
        total_batches: int,
        progress_callback: Optional[Callable[[dict[str, Any]], None]],
    ) -> None:
        """
        Process a batch of chunks: embed and upsert.

        Args:
            batch: List of CodeChunk objects
            batch_num: Current batch number
            total_batches: Total number of batches
            progress_callback: Optional progress callback
        """
        batch_start_time = time.time()

        # Extract content for embedding
        contents = [chunk.content for chunk in batch]

        try:
            # Generate embeddings
            embeddings = await self.embedding_service.embed_documents(contents)

            # Prepare chunks for upsert
            upsert_chunks = []
            for chunk, embedding in zip(batch, embeddings):
                upsert_chunks.append(
                    {
                        "id": chunk.id,
                        "content": chunk.content,
                        "embedding": embedding,
                        "metadata": {
                            "file_path": chunk.file_path,
                            "start_line": chunk.start_line,
                            "end_line": chunk.end_line,
                            "language": chunk.language,
                            "chunk_type": chunk.chunk_type,
                            "tokens": chunk.tokens,
                            "symbols": chunk.symbols,
                            "imports": chunk.imports,
                            "parent_context": chunk.parent_context or "",
                        },
                    }
                )

            # Upsert to vector store
            upserted = await self.vector_store.upsert_chunks(upsert_chunks)
            self._embedded_chunks += upserted

            elapsed = time.time() - batch_start_time

            logger.info(
                f"Batch {batch_num}/{total_batches}: "
                f"embedded and upserted {upserted} chunks in {elapsed:.2f}s"
            )

            if progress_callback:
                progress = {
                    "phase": "embeddings",
                    "status": "in_progress",
                    "batch_number": batch_num,
                    "total_batches": total_batches,
                    "chunks_processed": self._embedded_chunks,
                    "total_chunks": self._total_chunks,
                    "percentage": (
                        (self._embedded_chunks / self._total_chunks * 100)
                        if self._total_chunks > 0
                        else 0.0
                    ),
                    "batch_time_seconds": elapsed,
                }
                progress_callback(progress)

        except Exception as e:
            logger.error(
                f"Batch {batch_num}/{total_batches} failed: {e}",
                exc_info=True,
            )
            self._failed_chunks += len(batch)

            if progress_callback:
                progress_callback(
                    {
                        "phase": "embeddings",
                        "status": "error",
                        "batch_number": batch_num,
                        "error": str(e),
                    }
                )

            # Continue with next batch instead of failing completely
            logger.warning(
                f"Continuing with next batch despite error in batch {batch_num}"
            )

    def get_statistics(self) -> dict[str, Any]:
        """Get executor statistics."""
        return {
            "phase": "embeddings",
            "total_chunks": self._total_chunks,
            "embedded_chunks": self._embedded_chunks,
            "failed_chunks": self._failed_chunks,
            "total_time_seconds": self._total_time,
            "average_time_per_chunk": (
                self._total_time / self._embedded_chunks
                if self._embedded_chunks > 0
                else 0.0
            ),
        }

    def reset_statistics(self) -> None:
        """Reset statistics counters."""
        self._total_chunks = 0
        self._embedded_chunks = 0
        self._failed_chunks = 0
        self._total_time = 0.0
