from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


class ChatRequest(BaseModel):
    prompt: str
    model: str | None = None


@app.post("/chat/echo")
async def chat_echo(req: ChatRequest):
    async def gen():
        # Stream back the prompt as a demo
        text = f"Echo ({req.model or 'local'}): " + req.prompt
        for ch in text:
            yield ch
            await asyncio.sleep(0.01)

    return StreamingResponse(gen(), media_type="text/plain")
