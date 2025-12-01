from __future__ import annotations

import os

from fastapi import APIRouter, Header, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter()

_METRICS_TOKEN = os.environ.get("METRICS_BEARER_TOKEN")


@router.get("/metrics")
async def metrics_endpoint(authorization: str | None = Header(None)):
    if _METRICS_TOKEN:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization required")
        token = authorization.split(" ", 1)[1]
        if token != _METRICS_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")
    try:
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)
    except Exception:
        return Response(content=b"", media_type=CONTENT_TYPE_LATEST)
