Perfect timing 👍
Below is a **clean, Phase-aware patch proposal** that adds **GitHub contribution rules + commit conventions** without touching runtime code.

This patch is **pure governance** → safe, reversible, and future-proof.

---

# 📦 PATCH PROPOSAL — Repository Governance & Collaboration

## 🎯 Scope (Intentionally Limited)

This patch adds:

1. **Commit message convention** (phase-aware, solo & team friendly)
2. **CONTRIBUTING.md** (clear rules for future collaborators)
3. **GitHub-aligned workflow guidance**

🚫 No code changes
🚫 No CI changes
🚫 No branching policy enforcement via tooling (yet)

---

## 1️⃣ Commit Message Convention

### 📄 New File

**`docs/ProjectDocuments/commit-convention.md`**

```markdown
# LocalPilot – Commit Message Convention

This document defines the official commit message format for the LocalPilot repository.

The goal is:
- Clear history
- Easy reverts
- Phase-aware development
- Solo-friendly and team-ready

---

## 1. Commit Message Format

```

<type>(<scope>): <short description>

```

### Examples

```

feat(chat): add RAG-enhanced chat service
fix(ollama): handle connection failure gracefully
docs(phase0): finalize foundation documentation
refactor(core): simplify error hierarchy
test(server): add health endpoint test
chore(repo): update contributing guidelines

```

---

## 2. Allowed Types

| Type | Purpose |
|----|----|
| feat | New feature |
| fix | Bug fix |
| refactor | Code restructuring (no behavior change) |
| test | Adding or updating tests |
| docs | Documentation only |
| chore | Tooling, config, repo maintenance |
| perf | Performance improvements |
| revert | Reverting previous commit |

---

## 3. Scope Guidelines

Scopes should be **small and meaningful**.

### Recommended scopes
- `core`
- `ollama`
- `rag`
- `chat`
- `plan`
- `act`
- `ui`
- `server`
- `extension`
- `repo`
- `phase0`, `phase1`, etc.

---

## 4. Phase Awareness

During development phases:

- Phase branches should reference the phase:
```

docs(phase1): add chat workflow overview
feat(phase1-chat): implement context builder

```

- Phase completion commits should be explicit:
```

chore(phase1): lock phase 1 implementation

```

---

## 5. Commit Size Rules

- One logical change per commit
- Avoid mixing refactors and features
- Tests should accompany features when applicable

---

## 6. Reverts

Use `git revert`, not `git reset`, on shared branches.

Example:
```

revert(chat): remove incomplete streaming logic

```

---

## 7. Enforcement

This convention is currently **human-enforced**.

Automated checks may be added later if the project gains contributors.

---
```

---

## 2️⃣ CONTRIBUTING.md

### 📄 New File

**`CONTRIBUTING.md`** (repo root)

```markdown
# Contributing to LocalPilot

Thank you for your interest in contributing to LocalPilot 🙌

LocalPilot is a **privacy-first, local-only AI coding assistant** built with a
phase-driven architecture. Please read this document carefully before contributing.

---

## 1. Project Philosophy

- 🔒 Privacy first (no cloud dependencies)
- 🧱 Strong architecture over quick hacks
- 📋 Structured workflow (Chat → Plan → Act)
- 🧠 Clarity over cleverness

---

## 2. Repository Structure

LocalPilot uses a **monorepo**:

```

extension/   # VS Code extension (TypeScript)
server/      # Python RAG server (FastAPI)
docs/        # Architecture, specs, decisions

````

Each layer has strict responsibility boundaries.
Violations will be rejected.

---

## 3. Branching Model

**Do not commit directly to `main`.**

### Branch Types

| Branch | Purpose |
|----|----|
| `main` | Stable, reviewed code only |
| `phase/*` | Phase-level development |
| `feat/*` | Experimental or risky work |
| `fix/*` | Targeted bug fixes |

Example:
```bash
git checkout -b phase/1-chat-foundation
git checkout -b feat/ollama-service
````

---

## 4. Commit Message Convention

All commits must follow the official convention:

📄 `docs/ProjectDocuments/commit-convention.md`

Commits that do not follow this format may be rejected.

---

## 5. Phase Discipline (Very Important)

Each development phase has a **locked scope**.

* ❌ Do not implement features from future phases
* ❌ Do not change Core contracts without approval
* ✅ Propose changes via documentation first

If unsure, ask before coding.

---

## 6. Code Style & Quality

### TypeScript

* `strict: true` is mandatory
* No `any` unless explicitly justified
* Prefer interfaces over concrete classes

### Python

* Follow PEP8
* Use type hints where possible
* No blocking I/O in async routes

---

## 7. Testing Requirements

* New features should include tests when feasible
* At minimum, existing tests must pass
* Do not reduce coverage intentionally

---

## 8. Documentation First Rule

For non-trivial changes:

1. Update or add documentation
2. Explain *why* before *how*
3. Reference relevant ADRs or phases

---

## 9. Security & Privacy Rules

* Never introduce cloud APIs
* Never send user code externally
* Never log source code content

Violations will result in immediate rejection.

---

## 10. Review Process

* Small PRs preferred
* One concern per PR
* Architecture > speed

---

## 11. Questions & Discussions

Open an issue if:

* You are unsure about scope
* You want to propose an architectural change
* You want to add a new language or model

---

Thank you for helping keep LocalPilot clean, safe, and intentional 🚀

````

---

## 3️⃣ GitHub Enhancement

📄 **Update `.github/pull_request_template.md`**

Add this checklist at the top:

```markdown
### Checklist
- [ ] Commit messages follow convention
- [ ] Changes match current phase scope
- [ ] Core contracts untouched (or justified)
- [ ] Tests pass
- [ ] Documentation updated if needed
````

---

# ✅ Patch Summary

| Item                       | Status     |
| -------------------------- | ---------- |
| Commit convention          | ✅ Added    |
| CONTRIBUTING.md            | ✅ Added    |
| Phase awareness            | ✅ Explicit |
| Revert safety              | ✅ Improved |
| Future collaboration ready | ✅          |

---

# 🟢 Recommendation

Apply this patch **before** starting Phase 1 work on your new branch.

After that, your repo will be:

* Safe to experiment
* Easy to onboard contributors
* Easy to revert
* Architecturally protected

If you want next, I can:

* Generate a **Phase 1 PR template**
* Add **ADR contribution rules**
* Design **release tagging strategy**

Just tell me.
