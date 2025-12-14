# Contributing to LocalPilot

Thank you for your interest in contributing to LocalPilot 🙌

LocalPilot is a privacy-first, local-only AI coding assistant built with a
phase-driven architecture. Please read this document carefully before contributing.

---

## 1. Project Philosophy

- 🔒 Privacy first (no cloud dependencies)
- 🧱 Strong architecture over quick hacks
- 📋 Structured workflow (Chat → Plan → Act)
- 🧠 Clarity over cleverness

---

## 2. Repository Structure

LocalPilot uses a monorepo:

```
extension/   # VS Code extension (TypeScript)
server/      # Python RAG server (FastAPI)
docs/        # Architecture, specs, decisions
```

Each layer has strict responsibility boundaries. Violations will be rejected.

---

## 3. Branching Model

Do not commit directly to `main`.

### Branch Types

| Branch | Purpose |
|----|----|
| main | Stable, reviewed code only |
| phase/* | Phase-level development |
| feat/* | Experimental or risky work |
| fix/* | Targeted bug fixes |

Example:
```bash
git checkout -b phase/1-chat-foundation
git checkout -b feat/ollama-service
```

---

## 4. Commit Message Convention

All commits must follow the official convention:

See docs/ProjectDocuments/commit-convention.md

Commits that do not follow this format may be rejected.

---

## 5. Phase Discipline (Very Important)

Each development phase has a locked scope.

- ❌ Do not implement features from future phases
- ❌ Do not change Core contracts without approval
- ✅ Propose changes via documentation first

If unsure, ask before coding.

---

## 6. Code Style & Quality

### TypeScript
- strict: true is mandatory
- No any unless explicitly justified
- Prefer interfaces over concrete classes

### Python
- Follow PEP8
- Use type hints where possible
- No blocking I/O in async routes

---

## 7. Testing Requirements

- New features should include tests when feasible
- At minimum, existing tests must pass
- Do not reduce coverage intentionally

---

## 8. Documentation First Rule

For non-trivial changes:

1. Update or add documentation
2. Explain why before how
3. Reference relevant ADRs or phases

---

## 9. Security & Privacy Rules

- Never introduce cloud APIs
- Never send user code externally
- Never log source code content

Violations will result in immediate rejection.

---

## 10. Review Process

- Small PRs preferred
- One concern per PR
- Architecture > speed

---

## 11. Questions & Discussions

Open an issue if:

- You are unsure about scope
- You want to propose an architectural change
- You want to add a new language or model

---

Thank you for helping keep LocalPilot clean, safe, and intentional 🚀
