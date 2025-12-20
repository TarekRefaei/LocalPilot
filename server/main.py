from contextlib import asynccontextmanager
from fastapi import FastAPI
import requests

try:
    from .api.routes import query as query_routes
    from .api.routes import chat_ws
except ImportError:
    from api.routes import query as query_routes
    from api.routes import chat_ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        r = requests.get("http://localhost:11434/api/version", timeout=3)
        r.raise_for_status()
    except Exception as e:
        print(f"Warning: Could not connect to Ollama: {e}")

    yield

    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(query_routes.router, prefix="/api")
app.include_router(chat_ws.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/ollama")
def ollama_health():
    try:
        r = requests.get("http://localhost:11434/api/version", timeout=2)
        return {"status": "ok", "ollama": r.json()}
    except Exception as e:
        return {"status": "error", "error": str(e)}
