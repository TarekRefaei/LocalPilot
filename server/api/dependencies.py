from pathlib import Path
from functools import lru_cache

from ..indexing.embeddings.ollama import OllamaEmbeddingProvider


@lru_cache()
def get_embedder():
    return OllamaEmbeddingProvider(
        base_url="http://localhost:11434",
        model="mxbai-embed-large"
    )


def get_index_root() -> Path:
    return Path.home() / ".localpilot" / "indexes"
