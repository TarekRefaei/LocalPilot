from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import requests

from server.api.routes import query as query_routes
from server.api.routes import chat_ws
from server.api.routes import project as project_routes
from server.api.routes import index as index_routes
from server.api import plan as plan_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup check: Ollama
    try:
        r = requests.get("http://127.0.0.1:11434/api/version", timeout=3)
        r.raise_for_status()
        print("Ollama detected")
    except Exception as e:
        print(f"Warning: Could not connect to Ollama: {e}")

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # OK for local dev
    allow_credentials=True,
    allow_methods=["*"],          # IMPORTANT: allows OPTIONS
    allow_headers=["*"],
)


# --------------------
# Routers
# --------------------
app.include_router(query_routes.router, prefix="/api")
app.include_router(project_routes.router, prefix="/api")
app.include_router(chat_ws.router)
app.include_router(index_routes.router, prefix="/api")
app.include_router(plan_api.router, prefix="/api")

# --------------------
# Health endpoints
# --------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/ollama")
def ollama_health():
    try:
        r = requests.get("http://127.0.0.1:11434/api/version", timeout=2)
        r.raise_for_status()
        return {"status": "ok", "ollama": r.json()}
    except Exception as e:
        return {"status": "error", "error": str(e)}
