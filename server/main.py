from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import requests
import sys
import asyncio

try:
    from pathlib import Path

    _repo_root = Path(__file__).resolve().parents[1]
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))
except Exception:
    pass

try:
    from server.config.runtime import (
        OLLAMA_BASE_URL,
        OLLAMA_VERSION_ENDPOINT,
        OLLAMA_TIMEOUT_LONG,
        CORS_ALLOW_ORIGINS,
    )

    from server.api.routes import query as query_routes
    from server.api.routes import chat_ws
    from server.api.routes import project as project_routes
    from server.api.routes import index as index_routes
    from server.api import plan as plan_api
    from server.api import plan_structure as plan_structure_api
    from server.api import plan_refine as plan_refine_api
    from server.execute_v2.api import router as execute_v2_router
    from server.execute_v2.store import load_all_executions
except ModuleNotFoundError:
    from config.runtime import (
        OLLAMA_BASE_URL,
        OLLAMA_VERSION_ENDPOINT,
        OLLAMA_TIMEOUT_LONG,
        CORS_ALLOW_ORIGINS,
    )

    from api.routes import query as query_routes
    from api.routes import chat_ws
    from api.routes import project as project_routes
    from api.routes import index as index_routes
    from api import plan as plan_api
    from api import plan_structure as plan_structure_api
    from api import plan_refine as plan_refine_api
    from execute_v2.api import router as execute_v2_router
    from execute_v2.store import load_all_executions

# Windows: prefer selector event loop to reduce WinError 10054 during client disconnects
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup check: Ollama
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}{OLLAMA_VERSION_ENDPOINT}", timeout=OLLAMA_TIMEOUT_LONG)
        r.raise_for_status()
        print("Ollama detected")
    except Exception as e:
        print(f"Warning: Could not connect to Ollama: {e}")

    # Load persisted executions
    load_all_executions()
    print("Execution state restored")

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,          # OK for local dev
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
app.include_router(plan_structure_api.router)
app.include_router(plan_refine_api.router)
app.include_router(execute_v2_router)

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

