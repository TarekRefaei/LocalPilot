from pathlib import Path
from typing import Iterable

from .prompt_builder import PromptBuilder
from .ollama_chat_client import OllamaChatClient
try:
    from ..indexing.query_service import QueryService
except ImportError:
    from indexing.query_service import QueryService


class ChatService:
    """
    Phase 1.2
    ----------
    Orchestrates:
    - RAG retrieval
    - Prompt building
    - Streaming chat response
    """

    def __init__(
        self,
        index_root: Path,
        embedder,
        ollama_base_url: str,
        chat_model: str
    ):
        self.query_service = QueryService(
            index_root=index_root,
            embedder=embedder
        )
        self.prompt_builder = PromptBuilder()
        self.chat_client = OllamaChatClient(
            base_url=ollama_base_url,
            model=chat_model
        )

    def stream_chat(
        self,
        project_id: str,
        user_message: str,
        top_k: int = 5
    ) -> Iterable[str]:
        chunks = self.query_service.query(
            text=user_message,
            top_k=top_k
        )

        messages = self.prompt_builder.build(
            user_message=user_message,
            chunks=chunks
        )

        return self.chat_client.stream_chat(messages)
