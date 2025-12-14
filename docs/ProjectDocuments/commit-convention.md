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

Scopes should be small and meaningful.

### Recommended scopes
- core
- ollama
- rag
- chat
- plan
- act
- ui
- server
- extension
- repo
- phase0, phase1, etc.

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

This convention is currently human-enforced.

Automated checks may be added later if the project gains contributors.

---
