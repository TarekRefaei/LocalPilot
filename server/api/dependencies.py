from pathlib import Path
from functools import lru_cache

try:
    from ..indexing.embeddings.ollama import OllamaEmbeddingProvider
except ImportError:
    from indexing.embeddings.ollama import OllamaEmbeddingProvider

from server.config.runtime import OLLAMA_BASE_URL
from server.config.models import DEFAULT_EMBEDDING_MODEL
from server.config.paths import INDEX_ROOT


@lru_cache()
def get_embedder():
    return OllamaEmbeddingProvider(
        base_url=OLLAMA_BASE_URL,
        model=DEFAULT_EMBEDDING_MODEL,
    )

def get_index_root() -> Path:
    return INDEX_ROOT

