from __future__ import annotations

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.retrieve import get_retriever
from app.models.chat import ChatRequest
from app.services import storage, stream_control
from app.services.model_adapter import stream_from_ollama_safe

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/stream")
async def stream_chat(req: ChatRequest, request: Request):
    """
    Chat streaming endpoint with optional request cancellation and history persistence.
    - Retrieves evidence via MultiLevelRetriever
    - Builds a prompt (system + evidence + user prompt)
    - Registers/uses request_id for cancellation
    - Saves user/assistant chunks to SQLite history (session_id)
    - Returns X-Request-Id header
    """
    retriever = await get_retriever()

    # Resolve session and request IDs
    session_id = req.session_id or (request.client and request.client.host) or "default"  # type: ignore[truthy-bool]
    request_id = req.request_id or stream_control.new_request_id()
    stream_control.ensure(request_id)

    # Retrieve evidence
    results = await retriever.retrieve(query=req.prompt, top_k=5)
    evidence_texts: list[str] = [r.get("content", "") for r in results][:5]

    # Build prompt
    system_prefix = (
        "You are LocalPilot. Use the evidence below to answer the user's question.\n\n"
    )
    evidence_block = "\n\n--- Evidence ---\n\n" + (
        "\n\n".join(evidence_texts) if evidence_texts else "<no evidence>"
    )
    full_prompt = f"{system_prefix}{evidence_block}\n\n--- User ---\n\n{req.prompt}"

    # Save user message
    try:
        await storage.save_message(session_id, "user", req.prompt)
    except Exception:
        logger.debug("Failed saving user message", exc_info=True)

    async def streamer():
        try:
            # Normalize model (strip provider prefix like 'ollama:')
            model_name = (req.model or "llama2").strip()
            if model_name.lower().startswith("ollama:"):
                model_name = model_name.split(":", 1)[1]
            try:
                agen = stream_from_ollama_safe(
                    full_prompt, model=model_name, request_id=request_id
                )
            except TypeError as e:
                if "request_id" in str(e):
                    agen = stream_from_ollama_safe(full_prompt, model=model_name)
                else:
                    raise
            async for chunk in agen:
                # Save assistant chunk
                try:
                    await storage.save_message(session_id, "assistant", chunk)
                except Exception:
                    logger.debug("Failed saving assistant chunk", exc_info=True)
                yield chunk
            logger.info("chat stream finished")
        except Exception as e:
            logger.exception("Error in chat stream: %s", e)
            yield "\n\n[Error generating response]\n"
        finally:
            stream_control.cleanup(request_id)

    headers = {"X-Request-Id": request_id}
    return StreamingResponse(streamer(), media_type="text/plain", headers=headers)


@router.post("/abort")
async def abort_chat(payload: dict):
    request_id = payload.get("request_id") if isinstance(payload, dict) else None
    if not request_id:
        return JSONResponse({"error": "missing request_id"}, status_code=400)
    stream_control.cancel_request(request_id)
    return {"ok": True}


@router.get("/history")
async def get_history(session_id: str, limit: int = 200):
    data = await storage.load_history(session_id, limit=limit)
    return {"history": data}
