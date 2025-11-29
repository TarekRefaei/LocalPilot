# Onboarding (Windows ≤ 15 minutes)

A minimal, reproducible path to get LocalPilot running on Windows.

## 0. Prerequisites
- VS Code ≥ 1.88
- Node.js 20.x (LTS)
- Python 3.11
- Git (and GitHub CLI optional)
- Optional: Ollama ≥ 0.1.20 (only needed for embeddings later)

## 1. Clone
```powershell
git clone https://github.com/<owner>/LocalPilot.git
cd LocalPilot
```

## 2. Backend (FastAPI)
```powershell
cd backend
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pip install -r requirements-dev.txt

# Run backend on 127.0.0.1:8765
.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8765
```

Verify:
- Open http://127.0.0.1:8765/health → expect status "healthy"
- Open http://127.0.0.1:8765/docs if debug is enabled

Tip: Windows Firewall may prompt on first run; allow local network access.

## 3. Extension (VS Code)
Open a new terminal (keep backend running):
```powershell
cd extension
npm ci
npm run compile
```

Launch the extension:
- Press F5 in VS Code → "Run Extension"
- In the Extension Development Host, open the LocalPilot view

Default settings:
- `localpilot.backend.baseUrl`: `http://127.0.0.1:8765`
- `localpilot.model`: `local`

Shortcuts:
- LocalPilot: Show Views → ctrl+alt+l
- LocalPilot: Focus Chat Input → ctrl+alt+c

## 4. Quick smoke test
- With backend running, open the Chat view
- Send a short prompt; the extension uses `/chat/echo` to stream text
- Expect streamed echo text back

## 5. Optional: Tests
Backend:
```powershell
cd backend
.venv\Scripts\python -m pytest -q --cov=app --cov-report=term-missing
```
Extension:
```powershell
cd extension
npm run test:ci
```

## Troubleshooting
- Python not found: ensure Python 3.11 is installed and on PATH
- Node version: use Node 20.x LTS
- Port conflicts: if :8765 is in use, change `--port` and update the extension setting `localpilot.backend.baseUrl`
- SSL/Proxy issues: run on `http://127.0.0.1` to avoid name resolution quirks

## Next
- Packaging: see `docs/VSIX_Packaging.md`
- Release: see `docs/Release_Checklist.md`
