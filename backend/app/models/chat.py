from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    model: str | None = None
    session_id: str | None = None
    request_id: str | None = None


class ChatResponseChunk(BaseModel):
    text: str
