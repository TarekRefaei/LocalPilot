import requests
from typing import List

from .base import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []

        for text in texts:
            res = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text
                },
                timeout=60
            )
            res.raise_for_status()
            data = res.json()
            embeddings.append(data["embedding"])

        return embeddings
