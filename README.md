# LocalPilot
 
## Quickstart
 
- Prerequisites
  - VS Code ≥ 1.88
  - Node.js 20.x
  - Python 3.11
  - GitHub CLI (gh) and `gh auth login`
 
- Backend (FastAPI)
  - Create venv and install
    - `cd backend`
    - `python -m venv .venv`
    - `.venv\\Scripts\\python -m pip install --upgrade pip`
    - `.venv\\Scripts\\python -m pip install -r requirements.txt`
    - `.venv\\Scripts\\python -m pip install -r requirements-dev.txt`
  - Test: `.venv\\Scripts\\python -m pytest -q`
  - Run: `.venv\\Scripts\\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
  - Health: http://127.0.0.1:8000/health
 
- Extension (VS Code)
  - `cd extension`
  - `npm install`
  - `npm run typecheck`
  - `npm run lint`
  - `npm run compile`
  - Debug: VS Code launch config “Run Extension” (uses `extensionHost`)
 
- VS Code tasks
  - Backend: Run → starts uvicorn
  - Backend: Test → runs pytest
  - Extension: Build → compiles TypeScript
 
## CI
- Workflows live in `.github/workflows/`
  - `ci-extension.yml` (Node 20 on Windows/Linux): typecheck, lint, tests
  - `ci-backend.yml` (Python 3.11 on Windows/Linux): ruff, pytest
- Push to `main` triggers CI. View runs on GitHub → Actions tab.
 
## Seed GitHub Backlog
- Script: `scripts/gh-seed-issues.ps1`
- Examples:
  - Preview: `powershell -File .\\scripts\\gh-seed-issues.ps1 -Repo <owner/name> -DryRun -AssignAgentMilestones`
  - Assign milestones to existing issues only: `powershell -File .\\scripts\\gh-seed-issues.ps1 -Repo <owner/name> -AssignAgentMilestones -AssignOnly`
 
## Key Documents
- Master Plan: `docs/projectdocuments/Master_Implementation_Plan.md`
- Contracts Index: `docs/projectdocuments/contracts/Contracts_Index.md`
- IDs & Constants: `docs/projectdocuments/contracts/IDs_and_Constants.md`
- Agent Prompts: `docs/agents/Agent_Prompts.md`
- ADR: UI Native Views: `docs/adr/0001-UI-Native-Views.md`
 
## License
MIT