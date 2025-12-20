from fastapi import APIRouter, WebSocket
import json

from server.chat.ollama_chat_client import OllamaChatClient

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    payload = await websocket.receive_json()

    model = payload.get("model")
    messages = payload.get("messages")

    try:
        client = OllamaChatClient(
            base_url="http://localhost:11434",
            model=model,
        )

        for token in client.stream_chat(messages):
            await websocket.send_text(json.dumps({
                "type": "token",
                "value": token
            }))

        await websocket.send_text(json.dumps({ "type": "done" }))

    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "source": "backend",
            "message": str(e)
        }))
        await websocket.send_text(json.dumps({ "type": "done" }))

    finally:
        await websocket.close()
