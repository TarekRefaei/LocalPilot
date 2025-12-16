from fastapi import FastAPI

app = FastAPI()

from .api.routes import query as query_routes
from .api.routes import chat_ws

app.include_router(query_routes.router, prefix="/api")
app.include_router(chat_ws.router)

@app.get("/health")
def health():
    return {"status": "ok"}
