from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState
import json

from server.chat.ollama_chat_client import OllamaChatClient

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        payload = await websocket.receive_json()

        model = payload.get("model")
        messages = payload.get("messages")

        client = OllamaChatClient(
            base_url="http://127.0.0.1:11434",
            model=model,
        )

        for token in client.stream_chat(messages):
            await websocket.send_text(json.dumps({
                "type": "token",
                "value": token
            }))

        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(json.dumps({ "type": "done" }))

    except (WebSocketDisconnect, ConnectionResetError):
        # Client disconnected; nothing to do
        pass
    except Exception as e:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(json.dumps({
                "type": "error",
                "source": "backend",
                "message": str(e)
            }))
            await websocket.send_text(json.dumps({ "type": "done" }))
    finally:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()
