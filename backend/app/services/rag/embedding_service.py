"""
Embedding service using Ollama bge-m3 model.

Provides:
- Query and document embedding with batching
- Caching for repeated queries
- Retry logic for Ollama API calls
- Metrics tracking
"""

import asyncio
import logging
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Embedding service using Ollama bge-m3 model.

    bge-m3 Specifications:
    - Dimensions: 1024
    - Max sequence length: 8192 tokens
    - Multilingual support
    - Optimized for code and technical text
    """

    # bge-m3 model configuration
    MODEL_NAME = "bge-m3"
    EMBEDDING_DIM = 1024
    MAX_SEQUENCE_LENGTH = 8192

    def __init__(
        self,
        ollama_base_url: str = "http://localhost:11434",
        batch_size: int = 32,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        query_cache: Any | None = None,
    ):
        """
        Initialize embedding service.

        Args:
            ollama_base_url: Base URL for Ollama API
            batch_size: Number of documents to embed in one batch
            max_retries: Maximum retry attempts for Ollama API calls
            retry_delay: Initial delay between retries (seconds)
        """
        self.ollama_base_url = ollama_base_url.rstrip("/")
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        # Optional external query cache (duck-typed for get_embedding/set_embedding)
        self.query_cache = query_cache

        # Statistics
        self._embed_count = 0
        self._query_embed_count = 0
        self._cache_hits = 0
        self._total_embed_time = 0.0
        self._ollama_errors = 0

        logger.info(
            f"EmbeddingService initialized: {self.MODEL_NAME} "
            f"(dim={self.EMBEDDING_DIM}, batch_size={batch_size})"
        )

    async def embed_query(self, query: str) -> list[float]:
        """
        Embed a single query.

        Args:
            query: Query text

        Returns:
            1024-dimensional embedding vector

        Raises:
            RuntimeError: If Ollama API fails after retries
        """
        # Check cache first using raw query string (if available)
        if self.query_cache is not None:
            try:
                cached = self.query_cache.get_embedding(query)
                if cached is not None:
                    self._cache_hits += 1
                    logger.debug(
                        f"EmbeddingService cache hit for query: {query[:50]}..."
                    )
                    return cached
            except Exception:
                # Cache errors should not fail embedding
                pass

        # Prepare query with prefix for better retrieval
        prepared_query = f"Represent this query for searching code: {query}"

        start_time = time.time()
        embedding = await self._embed_text(prepared_query)
        elapsed = time.time() - start_time

        self._query_embed_count += 1
        self._total_embed_time += elapsed

        logger.debug(
            f"Embedded query in {elapsed:.3f}s: {query[:50]}... "
            f"(total queries: {self._query_embed_count})"
        )

        # Store in cache after successful embed
        if self.query_cache is not None:
            try:
                self.query_cache.set_embedding(query, embedding)
            except Exception:
                pass

        return embedding

    async def embed_documents(
        self,
        documents: list[str],
        show_progress: bool = False,
    ) -> list[list[float]]:
        """
        Embed multiple documents in batches.

        Args:
            documents: List of document texts
            show_progress: Whether to log progress (for debugging)

        Returns:
            List of 1024-dimensional embedding vectors

        Raises:
            RuntimeError: If Ollama API fails after retries
        """
        if not documents:
            return []

        all_embeddings = []
        total_batches = (len(documents) + self.batch_size - 1) // self.batch_size

        for batch_idx in range(0, len(documents), self.batch_size):
            batch = documents[batch_idx : batch_idx + self.batch_size]
            batch_num = batch_idx // self.batch_size + 1

            # Prepare documents with prefix for better retrieval
            prepared_batch = [
                f"Represent this code for retrieval: {doc}" for doc in batch
            ]

            start_time = time.time()
            batch_embeddings = await self._embed_batch(prepared_batch)
            elapsed = time.time() - start_time

            all_embeddings.extend(batch_embeddings)
            self._embed_count += len(batch)
            self._total_embed_time += elapsed

            if show_progress:
                logger.info(
                    f"Embedded batch {batch_num}/{total_batches} "
                    f"({len(batch)} docs in {elapsed:.3f}s)"
                )

        avg_time = self._total_embed_time / max(self._embed_count, 1)
        logger.info(
            f"Embedded {len(documents)} documents in {total_batches} batches "
            f"(total: {self._embed_count}, avg time: {avg_time:.3f}s)"
        )

        return all_embeddings

    async def embed_chunks(
        self,
        chunks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Embed code chunks with metadata.

        Args:
            chunks: List of chunk dicts with 'content' and 'metadata'

        Returns:
            Chunks with added 'embedding' field

        Raises:
            RuntimeError: If Ollama API fails after retries
        """
        contents = [chunk["content"] for chunk in chunks]
        embeddings = await self.embed_documents(contents)

        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings, strict=True):
            chunk["embedding"] = embedding

        return chunks

    async def _embed_text(self, text: str) -> list[float]:
        """
        Embed a single text using Ollama API.

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            RuntimeError: If Ollama API fails after retries
        """
        # Truncate if necessary
        text = self._truncate_text(text)

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.ollama_base_url}/api/embeddings",
                    json={"model": self.MODEL_NAME, "prompt": text},
                    timeout=30,
                )
                response.raise_for_status()
                data = response.json()

                if "embedding" not in data:
                    raise ValueError("No embedding in response")

                embedding = data["embedding"]

                # Verify dimension
                if len(embedding) != self.EMBEDDING_DIM:
                    logger.warning(
                        f"Unexpected embedding dimension: {len(embedding)} "
                        f"(expected {self.EMBEDDING_DIM})"
                    )

                return embedding

            except requests.exceptions.RequestException as e:
                self._ollama_errors += 1
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2**attempt)
                    logger.warning(
                        f"Ollama API error (attempt {attempt + 1}/{self.max_retries}): {e}. "
                        f"Retrying in {wait_time:.1f}s..."
                    )
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(
                        f"Ollama API failed after {self.max_retries} attempts: {e}"
                    )
                    raise RuntimeError(
                        f"Failed to embed text after {self.max_retries} attempts: {e}"
                    ) from e

    async def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Embed a batch of texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = await self._embed_text(text)
            embeddings.append(embedding)
        return embeddings

    def _truncate_text(self, text: str, max_length: int = 8192) -> str:
        """
        Truncate text to fit within bge-m3's max sequence length.

        Args:
            text: Input text
            max_length: Maximum length in tokens (approximate by chars/4)

        Returns:
            Truncated text
        """
        # Rough approximation: 1 token ≈ 4 characters
        max_chars = max_length * 4

        if len(text) <= max_chars:
            return text

        # Truncate at word boundary
        truncated = text[:max_chars]
        last_space = truncated.rfind(" ")

        if last_space > 0:
            truncated = truncated[:last_space]

        return truncated + "..."

    def get_statistics(self) -> dict[str, Any]:
        """Get embedding service statistics."""
        total_embeds = self._embed_count + self._query_embed_count
        avg_time = self._total_embed_time / total_embeds if total_embeds > 0 else 0.0

        return {
            "model": self.MODEL_NAME,
            "embedding_dimension": self.EMBEDDING_DIM,
            "batch_size": self.batch_size,
            "total_embeddings": total_embeds,
            "document_embeddings": self._embed_count,
            "query_embeddings": self._query_embed_count,
            "total_time_seconds": self._total_embed_time,
            "average_time_per_embedding": avg_time,
            "ollama_errors": self._ollama_errors,
        }

    def reset_statistics(self) -> None:
        """Reset statistics counters."""
        self._embed_count = 0
        self._query_embed_count = 0
        self._cache_hits = 0
        self._total_embed_time = 0.0
        self._ollama_errors = 0
