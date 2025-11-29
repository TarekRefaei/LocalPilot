# Contributing to LocalPilot

Thank you for your interest in contributing! This guide summarizes the workflow, quality gates, and Windows-friendly steps to get productive quickly.

## Getting Started (Windows ≤ 15 min)

- Clone the repo
  - `git clone https://github.com/<owner>/LocalPilot.git`
  - `cd LocalPilot`
- Backend (FastAPI)
  - `cd backend`
  - `python -m venv .venv`
  - `.venv\Scripts\python -m pip install --upgrade pip`
  - `.venv\Scripts\python -m pip install -r requirements.txt`
  - `.venv\Scripts\python -m pip install -r requirements-dev.txt`
  - Run: `.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8765`
  - Health: http://127.0.0.1:8765/health
- Extension (VS Code)
  - `cd ..\extension`
  - `npm ci`
  - `npm run compile`
  - Press F5 in VS Code → "Run Extension"

## Branching & Commits

- Branch naming: `feat/<scope>-<short>`, `fix/<scope>-<short>`, `docs/<short>`, `chore/<short>`
- Conventional commits: `<type>(<scope>): <subject>`
  - Types: feat, fix, docs, style, refactor, test, chore, perf, build
  - Example: `docs(readme): standardize backend port to 8765`

## Quality Gates (pre-PR)

- Extension
  - Typecheck: `npm run typecheck`
  - Lint: `npm run lint`
  - Test: `npm run test:ci`
- Backend
  - Ruff: `.venv\Scripts\python -m ruff check .`
  - Black (check): `.venv\Scripts\python -m black --check .`
  - Tests: `.venv\Scripts\python -m pytest -q --cov=app --cov-report=term-missing`

## Pull Requests

- Use the repo PR template; include:
  - Problem/Context, Approach
  - Tests (red → green), Screenshots/Demos
  - Risks & Rollback
  - Checklist: lint, type, tests, coverage, docs
- Keep PRs focused and small where possible.

## Windows Notes

- Prefer `python -m venv .venv` and use `.venv\Scripts\` prefix for Python commands.
- If firewall prompts appear on first run, allow local network access for Uvicorn.
- Default backend URL: `http://127.0.0.1:8765` (matches extension setting `localpilot.backend.baseUrl`).

## VSIX Packaging

- See `docs/VSIX_Packaging.md` for packaging and installation on Windows.

## Release & Onboarding Docs

- Release checklist: `docs/Release_Checklist.md`
- Windows onboarding: `docs/Onboarding_Windows.md`

## Code Style

- TypeScript: ESLint + Prettier; Python: Ruff + Black
- Follow SOLID, Clean Architecture, and TDD (red → green → refactor)

Thanks for contributing! 🚀
