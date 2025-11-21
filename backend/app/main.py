import asyncio
import logging

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger('localpilot.backend')
app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


class ChatRequest(BaseModel):
    prompt: str
    model: str | None = None


@app.post("/chat/echo")
async def chat_echo(req: ChatRequest):
    logger.info(f"Chat request: prompt={req.prompt[:50]}..., model={req.model or 'local'}")

    async def gen():
        try:
            # Stream back the prompt as a demo
            text = f"Echo ({req.model or 'local'}): " + req.prompt
            for ch in text:
                yield ch
                await asyncio.sleep(0.01)
            logger.info("Chat stream completed successfully")
        except Exception as e:
            logger.error(f"Chat stream error: {e}")
            raise

    return StreamingResponse(gen(), media_type="text/plain")
