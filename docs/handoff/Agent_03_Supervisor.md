# Agent 03 — Supervisor Handoff

This document summarizes the demo flow, test results, and current limitations for the Chat participant deliverable.

## Demo Script
1) Start backend
   - cd backend
   - python -m venv .venv
   - .venv\Scripts\python -m pip install -r requirements.txt -r requirements-dev.txt
   - .venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
2) Run the extension
   - cd extension
   - npm ci
   - npm run compile
   - Launch “Run Extension” in VS Code
3) Use Chat webview (LocalPilot → Chat)
   - Type a prompt and Send (streaming begins)
   - Stop/Regenerate as needed
   - Click model badge to pick a model
   - Recent prompts appear; click to reuse
   - Transfer to Plan → Plans view reveals and shows the draft

## Test Results
- Extension (Windows/Linux CI)
  - Typecheck/Lint/Compile: pass
  - Unit tests: pass
  - Integration tests: pass (webview state roundtrip, commands, plans insertion)
- Backend (Windows/Linux CI)
  - Black/Ruff: pass
  - Pytest: pass (health + streaming /chat/echo)

## Known Limitations
- Markdown rendering is minimal (code fences + line breaks). No full CommonMark.
- Retrieval is not integrated yet; only contract and placeholders are provided.
- Streaming uses /chat/echo; real model/tokenization is deferred.
- No telemetry; logging kept minimal and local.
