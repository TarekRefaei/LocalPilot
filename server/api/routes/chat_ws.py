from pathlib import Path
from fastapi import APIRouter, WebSocket, Depends

from ...chat.chat_service import ChatService
from ..dependencies import get_embedder, get_index_root

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_ws(
    websocket: WebSocket,
    embedder = Depends(get_embedder),
    index_root: Path = Depends(get_index_root),
):
    await websocket.accept()
    payload = await websocket.receive_json()

    service = ChatService(
        index_root=index_root / payload["project_id"],
        embedder=embedder,
        ollama_base_url="http://localhost:11434",
        chat_model=payload.get("model", "qwen2.5-coder")
    )

    try:
        for token in service.stream_chat(
            project_id=payload["project_id"],
            user_message=payload["message"],
            top_k=payload.get("top_k", 5)
        ):
            await websocket.send_text(token)
    finally:
        await websocket.close()
