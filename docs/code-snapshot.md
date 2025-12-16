# Code Snapshot

**Generated:** 2025-12-14T23:32:57.249Z
**Roots:** .
**Max file size:** 524,288 bytes

## Project Structure

```
. (67 files)
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── issue_template.md
│   ├── workflows/
│   │   └── windows-ci.yml
│   └── pull_request_template.md
├── docs/
│   ├── decisions/
│   │   ├── ADR-001-monorepo-structure.md
│   │   ├── ADR-002-llamaindex-over-langchain.md
│   │   └── ADR-003-chromadb-for-vectors.md
│   ├── plan/
│   │   ├── phase0/
│   │   │   ├── phase0.md
│   │   │   └── phase0patch.md
│   │   ├── phase1/
│   │   │   └── phase1patch.md
│   │   ├── master-execution-roadmap.md
│   │   └── Phase-by-Phase-TODO-List.md
│   └── ProjectDocuments/
│       ├── architecture.md
│       ├── commit-convention.md
│       ├── development-setup.md
│       ├── indexing-spec.md
│       ├── overview.md
│       ├── prompt-engineer.md
│       ├── release-policy.md
│       ├── security-model.md
│       ├── state-model.md
│       ├── structure.md
│       ├── task0-phase.md
│       ├── testing-strategy.md
│       ├── troubleshooting.md
│       └── webview-protocol.md
├── extension/
│   ├── src/
│   │   ├── core/
│   │   │   ├── entities/
│   │   │   │   ├── index.ts
│   │   │   │   ├── message.entity.ts
│   │   │   │   ├── plan.entity.ts
│   │   │   │   ├── project.entity.ts
│   │   │   │   └── task.entity.ts
│   │   │   ├── errors/
│   │   │   │   ├── base.error.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── ollama.error.ts
│   │   │   └── interfaces/
│   │   │       ├── file-system.interface.ts
│   │   │       ├── index.ts
│   │   │       ├── llm-provider.interface.ts
│   │   │       └── rag-provider.interface.ts
│   │   ├── features/
│   │   │   └── ollama/
│   │   │       └── connection-manager.ts
│   │   ├── infrastructure/
│   │   │   └── http/
│   │   │       └── api-client.ts
│   │   ├── panels/
│   │   │   └── main-panel.ts
│   │   └── extension.ts
│   ├── test/
│   │   └── activation.test.ts
│   ├── package-lock.json
│   ├── package.json
│   └── tsconfig.json
├── server/
│   ├── .pytest_cache/
│   │   └── README.md
│   ├── indexing/
│   │   ├── embeddings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── ollama.py
│   │   ├── parsers/
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   ├── __init__.py
│   │   ├── chunk.py
│   │   ├── chunker.py
│   │   ├── hash_tracker.py
│   │   ├── language.py
│   │   ├── progress.py
│   │   ├── scanner.py
│   │   ├── service.py
│   │   ├── state.py
│   │   └── vector_store.py
│   ├── tests/
│   │   └── test_health.py
│   ├── main.py
│   └── requirements.txt
├── tools/
│   └── export-to-md.mjs
├── CONTRIBUTING.md
└── README.md

```

---
## Table of Contents

- [.github/ISSUE_TEMPLATE/issue_template.md](#-github-issue-template-issue-template-md)
- [.github/pull_request_template.md](#-github-pull-request-template-md)
- [.github/workflows/windows-ci.yml](#-github-workflows-windows-ci-yml)
- [CONTRIBUTING.md](#contributing-md)
- [docs/decisions/ADR-001-monorepo-structure.md](#docs-decisions-adr-001-monorepo-structure-md)
- [docs/decisions/ADR-002-llamaindex-over-langchain.md](#docs-decisions-adr-002-llamaindex-over-langchain-md)
- [docs/decisions/ADR-003-chromadb-for-vectors.md](#docs-decisions-adr-003-chromadb-for-vectors-md)
- [docs/plan/master-execution-roadmap.md](#docs-plan-master-execution-roadmap-md)
- [docs/plan/Phase-by-Phase-TODO-List.md](#docs-plan-phase-by-phase-todo-list-md)
- [docs/plan/phase0/phase0.md](#docs-plan-phase0-phase0-md)
- [docs/plan/phase0/phase0patch.md](#docs-plan-phase0-phase0patch-md)
- [docs/plan/phase1/phase1patch.md](#docs-plan-phase1-phase1patch-md)
- [docs/ProjectDocuments/architecture.md](#docs-projectdocuments-architecture-md)
- [docs/ProjectDocuments/commit-convention.md](#docs-projectdocuments-commit-convention-md)
- [docs/ProjectDocuments/development-setup.md](#docs-projectdocuments-development-setup-md)
- [docs/ProjectDocuments/indexing-spec.md](#docs-projectdocuments-indexing-spec-md)
- [docs/ProjectDocuments/overview.md](#docs-projectdocuments-overview-md)
- [docs/ProjectDocuments/prompt-engineer.md](#docs-projectdocuments-prompt-engineer-md)
- [docs/ProjectDocuments/release-policy.md](#docs-projectdocuments-release-policy-md)
- [docs/ProjectDocuments/security-model.md](#docs-projectdocuments-security-model-md)
- [docs/ProjectDocuments/state-model.md](#docs-projectdocuments-state-model-md)
- [docs/ProjectDocuments/structure.md](#docs-projectdocuments-structure-md)
- [docs/ProjectDocuments/task0-phase.md](#docs-projectdocuments-task0-phase-md)
- [docs/ProjectDocuments/testing-strategy.md](#docs-projectdocuments-testing-strategy-md)
- [docs/ProjectDocuments/troubleshooting.md](#docs-projectdocuments-troubleshooting-md)
- [docs/ProjectDocuments/webview-protocol.md](#docs-projectdocuments-webview-protocol-md)
- [extension/package.json](#extension-package-json)
- [extension/src/core/entities/index.ts](#extension-src-core-entities-index-ts)
- [extension/src/core/entities/message.entity.ts](#extension-src-core-entities-message-entity-ts)
- [extension/src/core/entities/plan.entity.ts](#extension-src-core-entities-plan-entity-ts)
- [extension/src/core/entities/project.entity.ts](#extension-src-core-entities-project-entity-ts)
- [extension/src/core/entities/task.entity.ts](#extension-src-core-entities-task-entity-ts)
- [extension/src/core/errors/base.error.ts](#extension-src-core-errors-base-error-ts)
- [extension/src/core/errors/index.ts](#extension-src-core-errors-index-ts)
- [extension/src/core/errors/ollama.error.ts](#extension-src-core-errors-ollama-error-ts)
- [extension/src/core/interfaces/file-system.interface.ts](#extension-src-core-interfaces-file-system-interface-ts)
- [extension/src/core/interfaces/index.ts](#extension-src-core-interfaces-index-ts)
- [extension/src/core/interfaces/llm-provider.interface.ts](#extension-src-core-interfaces-llm-provider-interface-ts)
- [extension/src/core/interfaces/rag-provider.interface.ts](#extension-src-core-interfaces-rag-provider-interface-ts)
- [extension/src/extension.ts](#extension-src-extension-ts)
- [extension/src/features/ollama/connection-manager.ts](#extension-src-features-ollama-connection-manager-ts)
- [extension/src/infrastructure/http/api-client.ts](#extension-src-infrastructure-http-api-client-ts)
- [extension/src/panels/main-panel.ts](#extension-src-panels-main-panel-ts)
- [extension/test/activation.test.ts](#extension-test-activation-test-ts)
- [extension/tsconfig.json](#extension-tsconfig-json)
- [README.md](#readme-md)
- [server/.pytest_cache/README.md](#server--pytest-cache-readme-md)
- [server/indexing/__init__.py](#server-indexing---init---py)
- [server/indexing/chunk.py](#server-indexing-chunk-py)
- [server/indexing/chunker.py](#server-indexing-chunker-py)
- [server/indexing/embeddings/__init__.py](#server-indexing-embeddings---init---py)
- [server/indexing/embeddings/base.py](#server-indexing-embeddings-base-py)
- [server/indexing/embeddings/ollama.py](#server-indexing-embeddings-ollama-py)
- [server/indexing/hash_tracker.py](#server-indexing-hash-tracker-py)
- [server/indexing/language.py](#server-indexing-language-py)
- [server/indexing/parsers/__init__.py](#server-indexing-parsers---init---py)
- [server/indexing/parsers/base.py](#server-indexing-parsers-base-py)
- [server/indexing/progress.py](#server-indexing-progress-py)
- [server/indexing/scanner.py](#server-indexing-scanner-py)
- [server/indexing/service.py](#server-indexing-service-py)
- [server/indexing/state.py](#server-indexing-state-py)
- [server/indexing/vector_store.py](#server-indexing-vector-store-py)
- [server/main.py](#server-main-py)
- [server/requirements.txt](#server-requirements-txt)
- [server/tests/test_health.py](#server-tests-test-health-py)
- [tools/export-to-md.mjs](#tools-export-to-md-mjs)


---

## .github/ISSUE_TEMPLATE/issue_template.md

*Size: 166 bytes | Modified: 2025-12-07T20:49:06.993Z*

<details>
<summary>View code</summary>

```markdown
---
name: Feature request
about: Create a new feature or improvement
title: ''
labels: ''
assignees: ''
---

**Describe the feature**

**Acceptance criteria**

1.
2.

```

</details>


## .github/pull_request_template.md

*Size: 535 bytes | Modified: 2025-12-14T21:47:59.807Z*

<details>
<summary>View code</summary>

```markdown
### Checklist
- [ ] Commit messages follow convention
- [ ] Changes match current phase scope
- [ ] Core contracts untouched (or justified)
- [ ] Tests pass
- [ ] Documentation updated if needed

## Summary
Provide a short description of the change.

## Linked issue
Fixes #<issue number>

## Acceptance Criteria
- [ ] Add tests for new behavior
- [ ] All CI checks pass
- [ ] Documentation updated (if applicable)

## How to test locally
1. Steps to reproduce
2. Commands to run

## Reviewer notes
Any special notes for the reviewer.

```

</details>


## .github/workflows/windows-ci.yml

*Size: 1,163 bytes | Modified: 2025-12-14T22:13:17.080Z*

<details>
<summary>View code</summary>

```yaml
name: Windows CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install server deps and run tests
        shell: pwsh
        run: |
          python -m venv .venv
          .\.venv\Scripts\python -m pip install --upgrade pip
          .\.venv\Scripts\python -m pip install -r server/requirements.txt
          .\.venv\Scripts\python -m pip install pytest
          .\.venv\Scripts\pytest -q server/tests

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install extension deps
        shell: pwsh
        working-directory: extension
        run: |
          npm ci

      - name: Build extension
        shell: pwsh
        working-directory: extension
        run: |
          npm run build

      - name: Run extension tests
        shell: pwsh
        working-directory: extension
        run: |
          npm test -s

```

</details>


## CONTRIBUTING.md

*Size: 2,661 bytes | Modified: 2025-12-14T21:21:30.671Z*

<details>
<summary>View code</summary>

````markdown
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

````

</details>


## docs/decisions/ADR-001-monorepo-structure.md

*Size: 675 bytes | Modified: 2025-12-13T07:27:16.371Z*

<details>
<summary>View code</summary>

```markdown
# ADR-001: Monorepo Structure

## Status
Accepted

## Context
We need to decide how to organize the codebase containing:
- VS Code extension (TypeScript)
- Python RAG server
- Shared documentation

## Decision
Use a monorepo structure with both packages in one repository.

## Consequences
### Positive
- Single source of truth
- Easier to keep extension and server in sync
- Unified versioning
- Simpler for solo developer

### Negative
- Larger repository size
- Need to manage two package managers (pnpm + uv)

## Alternatives Considered
- Multi-repo: Rejected due to coordination overhead
- Workspace package (npm/yarn): Not suitable for Python
```

</details>


## docs/decisions/ADR-002-llamaindex-over-langchain.md

*Size: 581 bytes | Modified: 2025-12-13T07:28:18.874Z*

<details>
<summary>View code</summary>

```markdown
# ADR-002: LlamaIndex over LangChain

## Status
Accepted

## Context
Need a framework for RAG (Retrieval-Augmented Generation) operations.

## Decision
Use LlamaIndex instead of LangChain.

## Consequences
### Positive
- Better designed for indexing/retrieval use cases
- Simpler API for our needs
- Good Ollama integration
- Less abstraction overhead

### Negative
- Smaller community than LangChain
- Fewer tutorials available

## Alternatives Considered
- LangChain: More complex, designed for chains/agents
- Custom implementation: Too much work for MVP
```

</details>


## docs/decisions/ADR-003-chromadb-for-vectors.md

*Size: 640 bytes | Modified: 2025-12-13T07:28:53.819Z*

<details>
<summary>View code</summary>

```markdown
# ADR-003: ChromaDB for Vector Storage

## Status
Accepted

## Context
Need a vector database for storing and querying code embeddings.

## Decision
Use ChromaDB as the vector database.

## Consequences
### Positive
- Simple setup (embedded, no separate server)
- Python native
- Sufficient performance for MVP
- Easy persistence

### Negative
- May need to switch for larger codebases
- Less feature-rich than alternatives

## Alternatives Considered
- Qdrant: Better performance but more complex setup
- FAISS: No metadata filtering, not persistent by default
- Pinecone: Cloud-based, violates privacy requirement
```

</details>


## docs/plan/master-execution-roadmap.md

*Size: 5,400 bytes | Modified: 2025-12-13T18:47:10.856Z*

<details>
<summary>View code</summary>

```markdown
# 🧭 LocalPilot – Master Execution Roadmap (Step 1)

This roadmap answers **“what gets built, in what order, and why”** — without slipping into implementation details yet.

It is derived from:

* `PROJECT_OVERVIEW.md` (vision & scope) 
* `ARCHITECTURE.md` (clean architecture & responsibilities) 
* `INDEXING_SPEC.md` (RAG quality contract) 
* `STATE_MODEL.md` (mode gating & transitions) 
* `SECURITY_MODEL.md` (Act mode safety) 
* `TESTING_STRATEGY.md` (test boundaries) 

---

## 🔹 Phase 0 — Foundation & Skeleton (Stability First)

**Goal:**
A running VS Code extension + Python server that can talk to each other, but **does nothing intelligent yet**.

**Why this phase exists:**
If Phase 0 is weak, everything else becomes fragile. This phase is about *plumbing, not AI*.

### Capabilities by end of Phase 0

* Extension activates correctly
* Sidebar WebView loads
* Python server starts & responds
* Ollama availability can be detected
* Health checks work
* Clean architecture boundaries enforced
* Tests run (even if minimal)

### Explicitly NOT in Phase 0

* ❌ Indexing logic
* ❌ RAG
* ❌ Chat intelligence
* ❌ File modification

📌 This phase corresponds to (and slightly hardens) `task0-phase.md` 

---

## 🔹 Phase 1 — Indexing Engine (The Backbone)

**Goal:**
Build a **trustworthy, deterministic, persistent indexing system**.
Nothing else matters if this is wrong.

### Core Principle

> **No index → no modes → no AI**

This phase enforces your decision:

* indexing failure = **hard block**

### Capabilities by end of Phase 1

* Workspace scan (respecting `.gitignore`)
* AST-aware parsing (Tree-sitter)
* Semantic chunking (per `INDEXING_SPEC.md`)
* Embedding via Ollama
* Vector storage in ChromaDB
* Persistent storage in `~/.localpilot/indexes/{projectId}`
* Hash-based state tracking
* Progress reporting to UI
* Indexing summary generation
* Workspace summary written to
  `.localpilot/PROJECT_SUMMARY.md`

### UX State After Phase 1

* Onboarding screen
* Index button
* Progress indicator
* Final “Index complete” state
* **No Chat / Plan / Act yet**

### Explicitly NOT in Phase 1

* ❌ Chat UI
* ❌ Querying
* ❌ Plan generation
* ❌ Act mode

This phase is entirely about **data correctness**.

---

## 🔹 Phase 2 — Chat Mode (Understanding First)

**Goal:**
Allow the user to **talk about the indexed project** — safely and informatively.

### Role of Chat Mode (Locked)

* Explain code
* Answer questions
* Discuss architecture
* Suggest approaches
* Allow **proto-planning**

Chat is **not authoritative**.

### Capabilities by end of Phase 2

* RAG-powered Q&A
* Context assembly (RAG + history)
* Streaming responses
* Display of retrieved chunks
* Automatic project summary display (read-only)
* “Transfer to Plan Mode” trigger

### Hard Boundaries

* Chat **cannot**:

  * create TODOs
  * define file operations
  * modify files
  * execute anything

This keeps Chat safe, exploratory, and educational.

---

## 🔹 Phase 3 — Plan Mode (Intent → Structure)

**Goal:**
Convert **discussion into explicit intent** — with full user control.

### Core Rule

> **Editable markdown is the source of truth**

### Capabilities by end of Phase 3

* LLM-generated initial plan (markdown)
* Fully editable markdown plan
* Robust plan parsing
* Validation (file paths, task clarity)
* Task dependency ordering
* Plan approval flow
* Transfer to Act Mode

### What a Plan Is (Conceptually)

* A contract between user and agent
* Human-readable
* Machine-parseable
* Reviewable before execution

### Explicitly NOT in Phase 3

* ❌ File modification
* ❌ Diff generation
* ❌ Execution

---

## 🔹 Phase 4 — Act Mode (MVP-Safe Execution)

**Goal:**
Execute **approved plans**, one task at a time, with **maximum transparency**.

### MVP Safety Rules (Strict)

* ❌ No terminal execution
* ❌ No command running
* ❌ No dependency installation

### Capabilities by end of Phase 4

* TODO markdown file creation
* Per-task execution
* Per-task approval
* Patch proposal generation:

  * structured patch objects
  * unified diffs
* File create / modify / delete
* Automatic backups
* Rollback support
* Progress tracking
* Error recovery
* Mark index as `sync-required`

### After Execution

* Smart hash-based sync indexing
* Updated summary if needed
* Clean state transition

---

## 🔹 Phase 5 — Hardening & MVP Release

**Goal:**
Make LocalPilot **boring, stable, and trustworthy**.

### Focus Areas

* Error handling polish
* Edge cases (large repos, failures)
* Performance tuning
* UX clarity
* Documentation accuracy
* Test coverage ≥ 70%

---

## 🧭 Forward Compatibility (v1.1 / v1.2 Awareness)

This roadmap intentionally leaves room for:

### v1.1

* Terminal execution (allowlisted)
* Auto file watching
* Conversation persistence
* Settings UI

### v1.2

* Multiple workspaces
* Partial auto-approval
* More languages
* Agent heuristics

No architectural rewrites required.

---

## ✅ Step 1 Complete

You now have:

* a **clean, phase-based execution strategy**
* hard MVP boundaries
* no scope confusion
* future versions accounted for

---
```

</details>


## docs/plan/Phase-by-Phase-TODO-List.md

*Size: 8,112 bytes | Modified: 2025-12-13T18:50:00.385Z*

<details>
<summary>View code</summary>

```markdown
# 📋 LocalPilot – Phase-by-Phase TODO List (AI-Agent Friendly)

> **Global Rules (apply to ALL phases):**
>
> * Do NOT skip tasks
> * Do NOT merge phases
> * Each task must pass its verification checklist before continuing
> * If a task fails → stop and report error
> * Respect Clean Architecture boundaries at all times 

---

## 🔹 PHASE 0 — FOUNDATION & SKELETON

**Objective:**
Create a working monorepo where:

* VS Code extension loads
* Python server runs
* Extension ↔ server communication works
* Ollama availability can be checked

📌 Reference: Phase 0 definition 

---

### 🧩 Task 0.1 — Create Monorepo Folder Structure

**Goal:**
Create the complete folder structure exactly as defined.

**Instructions for AI Agent:**

* Create all directories from `PROJECT_STRUCTURE.md`
* Add placeholder `index.ts` files where required
* Do NOT add logic yet

**Verification Checklist:**

* [ ] Folder tree matches spec
* [ ] No missing directories
* [ ] No TypeScript build errors

---

### 🧩 Task 0.2 — Define Core Entities

**Goal:**
Create immutable domain entities (no logic).

**Create files:**

* `Message`
* `Project`
* `Plan`
* `Task`
* Related enums/types

**Rules:**

* Interfaces only
* JSDoc required
* No imports from Features / UI

**Verification Checklist:**

* [ ] Entities compile
* [ ] Barrel exports work
* [ ] Can be imported from Features layer

---

### 🧩 Task 0.3 — Define Core Interfaces (Ports)

**Goal:**
Define contracts for external systems.

**Interfaces to define:**

* `ILLMProvider`
* `IRAGProvider`
* `IFileSystem`
* `ISettings`

**Rules:**

* No implementation
* No side effects
* No Node / VS Code imports

**Verification Checklist:**

* [ ] Interfaces compile
* [ ] Features depend only on interfaces
* [ ] No circular dependencies

---

### 🧩 Task 0.4 — Define Core Errors

**Goal:**
Create a unified error model.

**Rules:**

* All errors extend `LocalPilotError`
* Errors are serializable
* Include recoverable flag

**Verification Checklist:**

* [ ] Errors thrown correctly
* [ ] Errors can be logged as JSON

---

### 🧩 Task 0.5 — Python Server Skeleton

**Goal:**
Create a FastAPI server that starts and responds.

**Endpoints (stub only):**

* `/health`
* `/index`
* `/query`
* `/chat`

**Rules:**

* No real logic
* Return static responses
* Server must start cleanly

**Verification Checklist:**

* [ ] Server starts
* [ ] `/health` returns OK
* [ ] No runtime errors

---

### 🧩 Task 0.6 — Extension ↔ Server Communication

**Goal:**
Verify HTTP communication.

**Steps:**

* Create API client in extension
* Call `/health`
* Display result in Output Channel

**Verification Checklist:**

* [ ] Extension can reach server
* [ ] Errors handled gracefully

---

### 🧩 Task 0.7 — Ollama Availability Check

**Goal:**
Verify Ollama connection (no generation yet).

**Steps:**

* Call `GET /api/version`
* Display status in UI

**Verification Checklist:**

* [ ] Detect running Ollama
* [ ] Show error if unavailable

---

✅ **Phase 0 Exit Criteria:**

* Extension loads
* Server runs
* Ollama detected
* Tests run

---

## 🔹 PHASE 1 — INDEXING ENGINE (BACKBONE)

**Objective:**
Build a **deterministic, persistent indexing system**.

📌 Reference: Indexing guarantees 

---

### 🧩 Task 1.1 — Workspace Scanner

**Goal:**
Discover indexable files.

**Rules:**

* Respect `.gitignore`
* Skip binaries
* Supported extensions only

**Verification Checklist:**

* [ ] Correct file count
* [ ] Skipped files reported

---

### 🧩 Task 1.2 — Language Detection

**Goal:**
Detect language per file.

**Rules:**

* Based on extension
* Deterministic mapping

---

### 🧩 Task 1.3 — AST Parsing (Tree-sitter)

**Goal:**
Parse files into ASTs.

**Rules:**

* One parser per language
* Errors reported, not swallowed

---

### 🧩 Task 1.4 — Semantic Chunking

**Goal:**
Convert AST → semantic chunks.

**Rules (non-negotiable):**

* No function splitting
* Line-accurate metadata
* Stable chunk IDs

📌 Reference: Chunk rules 

---

### 🧩 Task 1.5 — Embedding Generation

**Goal:**
Generate embeddings via Ollama.

**Rules:**

* Use embedding model only
* Batch requests
* Retry on failure

---

### 🧩 Task 1.6 — Vector Storage (ChromaDB)

**Goal:**
Persist embeddings.

**Rules:**

* One collection per project
* Stored in `~/.localpilot/indexes/`

---

### 🧩 Task 1.7 — Hash Tracking & Persistence

**Goal:**
Enable smart sync.

**Rules:**

* Hash per file
* Stored in state file
* Deterministic

---

### 🧩 Task 1.8 — Index Progress Reporting

**Goal:**
Show progress in UI.

**Phases:**

* scanning
* parsing
* embedding
* storing

---

### 🧩 Task 1.9 — Project Summary Generation

**Goal:**
Generate **informational summary only**.

**Output:**

* `.localpilot/PROJECT_SUMMARY.md`

**Rules:**

* Human readable
* Never authoritative

---

✅ **Phase 1 Exit Criteria:**

* Index survives restart
* Summary generated
* Modes remain locked until success

---

## 🔹 PHASE 2 — CHAT MODE

**Objective:**
Allow **safe discussion** of indexed project.

📌 Reference: Chat responsibilities 

---

### 🧩 Task 2.1 — RAG Query Endpoint

**Goal:**
Retrieve relevant chunks.

---

### 🧩 Task 2.2 — Context Builder

**Goal:**
Assemble prompt from:

* RAG chunks
* History
* Summary (optional)

---

### 🧩 Task 2.3 — Streaming Chat

**Goal:**
Stream responses to UI.

---

### 🧩 Task 2.4 — Chat UI

**Goal:**
Render:

* messages
* code blocks
* retrieved chunks

---

### 🧩 Task 2.5 — Transfer to Plan Trigger

**Goal:**
Enable transition when user approves.

---

✅ **Phase 2 Exit Criteria:**

* User can discuss project
* No file changes possible

---

## 🔹 PHASE 3 — PLAN MODE

**Objective:**
Turn discussion into **explicit intent**.

---

### 🧩 Task 3.1 — Plan Generation Prompt

**Goal:**
Generate markdown plan.

---

### 🧩 Task 3.2 — Editable Plan UI

**Goal:**
Allow full markdown editing.

---

### 🧩 Task 3.3 — Plan Parser

**Goal:**
Convert markdown → `Plan` entity.

**Rules:**

* Tolerant parsing
* Order preserved

---

### 🧩 Task 3.4 — Plan Validation

**Goal:**
Ensure tasks are:

* clear
* atomic
* safe

---

### 🧩 Task 3.5 — Transfer to Act Mode

**Goal:**
Lock plan for execution.

---

✅ **Phase 3 Exit Criteria:**

* Approved plan exists
* Tasks are parseable

---

## 🔹 PHASE 4 — ACT MODE (MVP-SAFE)

**Objective:**
Execute plan **safely, visibly, reversibly**.

📌 Reference: Security rules 

---

### 🧩 Task 4.1 — TODO.md Creation

**Goal:**
Persist execution intent.

---

### 🧩 Task 4.2 — Task Executor

**Goal:**
Execute ONE task at a time.

---

### 🧩 Task 4.3 — Patch Proposal Generation

**Goal:**
Generate:

* structured patch
* unified diff

---

### 🧩 Task 4.4 — Per-Task Approval UI

**Goal:**
Require user approval.

---

### 🧩 Task 4.5 — File Backup & Write

**Goal:**
Modify files safely.

---

### 🧩 Task 4.6 — Error Handling & Rollback

**Goal:**
Recover gracefully.

---

### 🧩 Task 4.7 — Smart Sync Index Trigger

**Goal:**
Mark `sync-required` and sync changed files.

---

✅ **Phase 4 Exit Criteria:**

* Files modified safely
* Index updated
* No commands executed

---

## 🔹 PHASE 5 — HARDENING

**Objective:**
Make LocalPilot **boring and reliable**.

---

### Focus Areas

* Performance
* Error UX
* Tests ≥ 70%
* Docs accuracy

---

## ✅ Step 2 Complete

You now have:

* an **AI-agent-friendly execution plan**
* clear phase boundaries
* no ambiguity
* no scope creep

---
```

</details>


## docs/plan/phase0/phase0.md

*Size: 6,887 bytes | Modified: 2025-12-14T23:05:32.701Z*

<details>
<summary>View code</summary>

````markdown
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

````

</details>


## docs/plan/phase0/phase0patch.md

*Size: 8,499 bytes | Modified: 2025-12-13T18:58:11.395Z*

<details>
<summary>View code</summary>

````markdown
# 🧩 STEP 4 — PHASE 0 PATCH PROPOSALS

> **Global Safety Rules**
>
> * Apply patches **in order**
> * One task at a time
> * Abort on first failure
> * Do NOT infer missing requirements
> * Do NOT introduce intelligence or autonomy

---

## 🧱 TASK 0.1 — Initialize Monorepo & Root Structure

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.1",
  "title": "Initialize monorepo root structure",
  "files": [
    { "path": ".gitignore", "action": "create" },
    { "path": ".editorconfig", "action": "create" },
    { "path": "README.md", "action": "create" },
    { "path": "extension/", "action": "create-directory" },
    { "path": "server/", "action": "create-directory" },
    { "path": "docs/", "action": "create-directory" },
    { "path": "scripts/", "action": "create-directory" }
  ],
  "requiresApproval": true,
  "riskLevel": "low",
  "rollback": "safe-delete"
}
```

---

### 🧾 Unified Diff

```diff
+++ .gitignore
+node_modules/
+dist/
+.venv/
+.env
+.localpilot/
+__pycache__/

+++ .editorconfig
+root = true
+[*]
+indent_style = space
+indent_size = 2
+end_of_line = lf
+charset = utf-8
+trim_trailing_whitespace = true
+insert_final_newline = true

+++ README.md
+# LocalPilot
+
+Privacy-first AI coding agent for VS Code using local LLMs.
```

---

## 🧱 TASK 0.2 — VS Code Extension Skeleton

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.2",
  "title": "Create VS Code extension skeleton",
  "files": [
    { "path": "extension/package.json", "action": "create" },
    { "path": "extension/tsconfig.json", "action": "create" },
    { "path": "extension/src/extension.ts", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low",
  "rollback": "safe-delete"
}
```

---

### 🧾 Unified Diff

```diff
+++ extension/package.json
+{
+  "name": "localpilot",
+  "displayName": "LocalPilot",
+  "description": "Privacy-first AI coding agent using local LLMs",
+  "version": "0.1.0",
+  "engines": { "vscode": "^1.85.0" },
+  "activationEvents": ["*"],
+  "main": "./dist/extension.js",
+  "scripts": {
+    "build": "esbuild src/extension.ts --bundle --outfile=dist/extension.js --platform=node",
+    "test": "vitest"
+  }
+}

+++ extension/tsconfig.json
+{
+  "compilerOptions": {
+    "target": "ES2020",
+    "module": "ESNext",
+    "strict": true,
+    "outDir": "dist",
+    "rootDir": "src"
+  }
+}

+++ extension/src/extension.ts
+import * as vscode from 'vscode';
+
+export function activate(context: vscode.ExtensionContext) {
+  console.log('LocalPilot activated');
+}
+
+export function deactivate() {}
```

---

## 🧱 TASK 0.3 — Python Server Skeleton

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.3",
  "title": "Create FastAPI server skeleton",
  "files": [
    { "path": "server/main.py", "action": "create" },
    { "path": "server/requirements.txt", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low",
  "rollback": "safe-delete"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/requirements.txt
+fastapi
+uvicorn

+++ server/main.py
+from fastapi import FastAPI
+
+app = FastAPI()
+
+@app.get("/health")
+def health():
+    return {"status": "ok"}
```

---

## 🧱 TASK 0.4 — Core Domain Entities

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.4",
  "title": "Add core domain entities",
  "files": [
    { "path": "extension/src/core/entities/message.entity.ts", "action": "create" },
    { "path": "extension/src/core/entities/project.entity.ts", "action": "create" },
    { "path": "extension/src/core/entities/plan.entity.ts", "action": "create" },
    { "path": "extension/src/core/entities/task.entity.ts", "action": "create" },
    { "path": "extension/src/core/entities/index.ts", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low",
  "rollback": "safe-delete"
}
```

---

### 🧾 Unified Diff (example: Message entity)

```diff
+++ extension/src/core/entities/message.entity.ts
+/**
+ * Represents a single chat message.
+ */
+export interface Message {
+  id: string;
+  role: 'user' | 'assistant' | 'system';
+  content: string;
+  timestamp: Date;
+}
```

(Other entities follow **exactly** the spec you already approved — no deviation.)

---

## 🧱 TASK 0.5 — Core Interfaces (Ports)

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.5",
  "title": "Define core interfaces (ports)",
  "files": [
+   { "path": "extension/src/core/interfaces/llm-provider.interface.ts", "action": "create" },
+   { "path": "extension/src/core/interfaces/rag-provider.interface.ts", "action": "create" },
+   { "path": "extension/src/core/interfaces/file-system.interface.ts", "action": "create" },
+   { "path": "extension/src/core/interfaces/index.ts", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff (example)

```diff
+++ extension/src/core/interfaces/llm-provider.interface.ts
+export interface ILLMProvider {
+  isAvailable(): Promise<boolean>;
+}
```

---

## 🧱 TASK 0.6 — Error Model

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.6",
  "title": "Create unified error model",
  "files": [
    { "path": "extension/src/core/errors/base.error.ts", "action": "create" },
    { "path": "extension/src/core/errors/index.ts", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff

```diff
+++ extension/src/core/errors/base.error.ts
+export abstract class LocalPilotError extends Error {
+  abstract readonly code: string;
+  abstract readonly recoverable: boolean;
+
+  constructor(message: string) {
+    super(message);
+  }
+}
```

---

## 🧱 TASK 0.7 — Extension ↔ Server Health Check

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.7",
  "title": "Add server health API client",
  "files": [
    { "path": "extension/src/infrastructure/http/api-client.ts", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff

```diff
+++ extension/src/infrastructure/http/api-client.ts
+export async function checkServerHealth(): Promise<boolean> {
+  const res = await fetch('http://localhost:52741/health');
+  return res.ok;
+}
```

---

## 🧱 TASK 0.8 — Ollama Availability Check

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.8",
  "title": "Detect Ollama availability",
  "files": [
    { "path": "extension/src/features/ollama/connection-manager.ts", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff

```diff
+++ extension/src/features/ollama/connection-manager.ts
+export async function isOllamaAvailable(): Promise<boolean> {
+  try {
+    const res = await fetch('http://localhost:11434/api/version');
+    return res.ok;
+  } catch {
+    return false;
+  }
+}
```

---

## 🧱 TASK 0.9 — Minimal WebView Panel

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "0.9",
  "title": "Add minimal sidebar WebView",
  "files": [
    { "path": "extension/src/panels/main-panel.ts", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff

```diff
+++ extension/src/panels/main-panel.ts
+import * as vscode from 'vscode';
+
+export class MainPanel {
+  static register(context: vscode.ExtensionContext) {
+    context.subscriptions.push(
+      vscode.window.registerWebviewViewProvider(
+        'localpilot.sidebar',
+        {
+          resolveWebviewView(view) {
+            view.webview.html = `<h1>LocalPilot</h1>`;
+          }
+        }
+      )
+    );
+  }
+}
```

---

## 🧱 TASK 0.10–0.12 (Tests & Validation)

These are **verification-only patches**:

* Add basic tests
* Confirm build + server start
* No logic changes

---

## ✅ STEP 4 COMPLETE — PHASE 0 IS NOW PATCH-READY

You now have:

* ✔ deterministic patch format
* ✔ machine + human representations
* ✔ MVP-safe changes
* ✔ rollback-safe operations
* ✔ AI-agent-executable instructions

---
````

</details>


## docs/plan/phase1/phase1patch.md

*Size: 20,703 bytes | Modified: 2025-12-14T23:14:58.948Z*

<details>
<summary>View code</summary>

````markdown
Excellent.
We now move into **Phase 1: Indexing Engine patch proposals** — the **backbone of LocalPilot**.

Below is **Phase 1, Tasks 1.1 → 1.4** as **patch proposals**, following **exactly** the agent constitution you approved:

* patch-driven
* deterministic
* no shortcuts
* no AI generation logic yet (only plumbing + deterministic algorithms)
* future-proof for v1.1 / v1.2

> ⚠️ **Important scope note**
> I am intentionally splitting Phase 1 into **controlled batches**.
> This message covers **Index Discovery → Parsing → Chunking (no embeddings yet)**.
> This keeps risk low and patches reviewable.

---

# 🧩 PHASE 1 — PATCH PROPOSALS (PART 1)

## Indexing Engine: Scan → Parse → Chunk

---

## 🧱 TASK 1.1 — Workspace Scanner

### 🎯 Objective

Deterministically discover indexable files while respecting user intent.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.1",
  "title": "Implement workspace file scanner",
  "files": [
    { "path": "server/indexing/scanner.py", "action": "create" },
    { "path": "server/indexing/__init__.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium",
  "rollback": "safe-delete"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/scanner.py
+from pathlib import Path
+from typing import List
+
+EXCLUDED_DIRS = {
+    ".git",
+    "node_modules",
+    "dist",
+    "build",
+    ".venv",
+    "__pycache__",
+    ".localpilot"
+}
+
+SUPPORTED_EXTENSIONS = {
+    ".ts", ".js", ".py", ".json", ".md", ".dart"
+}
+
+
+class WorkspaceScanner:
+    def scan(self, root: Path) -> List[Path]:
+        files: List[Path] = []
+
+        for path in root.rglob("*"):
+            if not path.is_file():
+                continue
+
+            if any(part in EXCLUDED_DIRS for part in path.parts):
+                continue
+
+            if path.suffix not in SUPPORTED_EXTENSIONS:
+                continue
+
+            files.append(path)
+
+        return sorted(files)
```

---

### ✅ Verification Checklist

* [ ] Skips excluded directories
* [ ] Deterministic ordering
* [ ] No file reads yet
* [ ] No gitignore parsing yet (v1.1)

---

## 🧱 TASK 1.2 — Language Detection

### 🎯 Objective

Determine programming language **deterministically** from file extension.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.2",
  "title": "Add language detection utility",
  "files": [
    { "path": "server/indexing/language.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/language.py
+from pathlib import Path
+
+
+EXTENSION_LANGUAGE_MAP = {
+    ".ts": "typescript",
+    ".js": "javascript",
+    ".py": "python",
+    ".dart": "dart",
+    ".json": "json",
+    ".md": "markdown"
+}
+
+
+def detect_language(path: Path) -> str | None:
+    return EXTENSION_LANGUAGE_MAP.get(path.suffix)
```

---

### ✅ Verification Checklist

* [ ] Deterministic mapping
* [ ] Returns None for unsupported files
* [ ] No heuristics

---

## 🧱 TASK 1.3 — AST Parsing Abstraction (Tree-sitter Ready)

### 🎯 Objective

Create a **parser abstraction**, without binding to Tree-sitter yet.

This keeps Phase 1 safe and testable.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.3",
  "title": "Introduce parser abstraction and base parser",
  "files": [
    { "path": "server/indexing/parsers/base.py", "action": "create" },
    { "path": "server/indexing/parsers/__init__.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/parsers/base.py
+from pathlib import Path
+from typing import Any
+
+
+class ParseResult:
+    def __init__(self, ast: Any, source: str):
+        self.ast = ast
+        self.source = source
+
+
+class BaseParser:
+    language: str
+
+    def parse(self, path: Path) -> ParseResult:
+        raise NotImplementedError("Parser must implement parse()")
```

---

### ✅ Verification Checklist

* [ ] No Tree-sitter dependency yet
* [ ] Abstract contract only
* [ ] Safe to extend later

---

## 🧱 TASK 1.4 — Semantic Chunk Model

### 🎯 Objective

Define **what a chunk is** — before generating embeddings.

This is critical for RAG quality.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.4",
  "title": "Define semantic chunk data model",
  "files": [
    { "path": "server/indexing/chunk.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

````diff
+++ server/indexing/chunk.py
+from dataclasses import dataclass
+
+
+@dataclass(frozen=True)
+class CodeChunk:
+    id: str
+    file_path: str
+    language: str
+    start_line: int
+    end_line: int
+    content: str
+    symbol_type: str  # function, class, module, block
+```

---

### ✅ Verification Checklist
- [ ] Immutable chunk
- [ ] Line-accurate metadata
- [ ] No embeddings yet
- [ ] No vector DB coupling

---

## 🔒 Phase 1 (Part 1) Status

At this point, you have:

✅ Deterministic workspace scanning  
✅ Explicit language detection  
✅ Parser abstraction (no premature complexity)  
✅ Canonical chunk model  

🚫 Still intentionally missing:
- embeddings
- ChromaDB
- Ollama calls
- RAG queries

This is **exactly correct**.

---

## 🔜 Next Step (Phase 1 – Part 2)

Next batch will cover:

- **Task 1.5** — Semantic chunking logic (AST → chunks)
- **Task 1.6** — Hash tracking (sync foundation)
- **Task 1.7** — Index state persistence
- **Task 1.8** — Progress reporting

Say when ready:

👉 **“Continue Phase 1 patch proposals (Part 2)”**

You’re building this the *right* way.
````

Perfect.
This is **Phase 1 – Part 2**, completing the **Indexing Engine core (still no embeddings yet)**.

Scope of this message:

* Semantic chunking logic (AST → chunks)
* Hash tracking (for smart sync)
* Index state persistence
* Progress reporting (server-side)

Still **NO Ollama**, **NO ChromaDB**, **NO RAG queries**.
We are finishing the *deterministic backbone* first.

---

# 🧩 PHASE 1 — PATCH PROPOSALS (PART 2)

## Chunking → Sync → Persistence → Progress

---

## 🧱 TASK 1.5 — Semantic Chunker (AST → CodeChunks)

### 🎯 Objective

Convert parsed source into **stable, semantically meaningful chunks**.

> ⚠️ Important:
> This implementation is **language-agnostic fallback chunking**.
> Tree-sitter–aware chunking will *extend* this in v1.1, not replace it.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.5",
  "title": "Implement semantic chunker",
  "files": [
    { "path": "server/indexing/chunker.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium",
  "rollback": "safe-delete"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/chunker.py
+import hashlib
+from typing import List
+
+from .chunk import CodeChunk
+
+
+class SemanticChunker:
+    def chunk_file(
+        self,
+        file_path: str,
+        language: str,
+        source: str
+    ) -> List[CodeChunk]:
+        """
+        Fallback semantic chunking:
+        - Entire file = single chunk
+        - Used until AST-aware chunkers are plugged in
+        """
+
+        lines = source.splitlines()
+        content = source.strip()
+
+        chunk_id = self._stable_id(file_path, content)
+
+        return [
+            CodeChunk(
+                id=chunk_id,
+                file_path=file_path,
+                language=language,
+                start_line=1,
+                end_line=len(lines),
+                content=content,
+                symbol_type="file"
+            )
+        ]
+
+    def _stable_id(self, file_path: str, content: str) -> str:
+        h = hashlib.sha256()
+        h.update(file_path.encode("utf-8"))
+        h.update(content.encode("utf-8"))
+        return h.hexdigest()
```

---

### ✅ Verification Checklist

* [ ] One chunk per file (for now)
* [ ] Stable chunk IDs
* [ ] Line numbers correct
* [ ] No AST dependency yet

---

## 🧱 TASK 1.6 — File Hash Tracker (Smart Sync Foundation)

### 🎯 Objective

Track file changes deterministically for **smart re-indexing**.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.6",
  "title": "Add file hash tracker",
  "files": [
    { "path": "server/indexing/hash_tracker.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/hash_tracker.py
+import hashlib
+from pathlib import Path
+
+
+def hash_file(path: Path) -> str:
+    h = hashlib.sha256()
+    with open(path, "rb") as f:
+        for chunk in iter(lambda: f.read(8192), b""):
+            h.update(chunk)
+    return h.hexdigest()
```

---

### ✅ Verification Checklist

* [ ] Deterministic hash
* [ ] Handles large files
* [ ] No global state

---

## 🧱 TASK 1.7 — Index State Persistence

### 🎯 Objective

Persist index metadata to disk so indexing survives restarts.

📍 Location (locked earlier):

```
~/.localpilot/indexes/{projectId}/state.json
```

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.7",
  "title": "Persist index state to disk",
  "files": [
    { "path": "server/indexing/state.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/state.py
+import json
+from pathlib import Path
+from typing import Dict
+
+
+class IndexState:
+    def __init__(self, root: Path):
+        self.path = root / "state.json"
+        self.file_hashes: Dict[str, str] = {}
+
+    def load(self) -> None:
+        if not self.path.exists():
+            return
+        with open(self.path, "r", encoding="utf-8") as f:
+            data = json.load(f)
+            self.file_hashes = data.get("file_hashes", {})
+
+    def save(self) -> None:
+        self.path.parent.mkdir(parents=True, exist_ok=True)
+        with open(self.path, "w", encoding="utf-8") as f:
+            json.dump(
+                {"file_hashes": self.file_hashes},
+                f,
+                indent=2
+            )
```

---

### ✅ Verification Checklist

* [ ] Creates directory if missing
* [ ] JSON readable
* [ ] Safe when state absent

---

## 🧱 TASK 1.8 — Indexing Progress Reporter

### 🎯 Objective

Expose **structured progress events** to the extension UI.

> No WebSockets yet — this is an internal abstraction.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.8",
  "title": "Add indexing progress tracker",
  "files": [
    { "path": "server/indexing/progress.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/progress.py
+from typing import Callable, Literal
+
+Phase = Literal["scan", "parse", "chunk", "hash", "complete"]
+
+
+class ProgressTracker:
+    def __init__(self, callback: Callable[[Phase, int, int], None]):
+        self.callback = callback
+
+    def report(self, phase: Phase, current: int, total: int) -> None:
+        self.callback(phase, current, total)
```

---

### ✅ Verification Checklist

* [ ] No side effects
* [ ] Phase-limited enum
* [ ] UI-agnostic

---

## 🔒 Phase 1 (Parts 1 + 2) — CURRENT STATE

You now have:

✅ Workspace scanning
✅ Language detection
✅ Parser abstraction
✅ Canonical chunk model
✅ Deterministic chunking
✅ Hash-based sync foundation
✅ Persistent index state
✅ Progress reporting abstraction

🚫 Still NOT present (by design):

* embeddings
* Ollama calls
* vector database
* RAG querying
* summary generation

This is **exactly where you want to be** before introducing ML.

---

Excellent.
This is **Phase 1 – Part 3**, where we **carefully introduce embeddings and vector storage**, while still keeping everything **deterministic, auditable, and MVP-safe**.

Scope of this message:

* Embedding abstraction (port)
* Ollama embedding implementation
* ChromaDB vector storage
* Index orchestration service (the glue)

This **completes Phase 1**.

---

# 🧩 PHASE 1 — PATCH PROPOSALS (PART 3)

## Embeddings → Vector Store → Index Orchestration

---

## 🧱 TASK 1.9 — Embedding Provider Abstraction

### 🎯 Objective

Define a **clean embedding contract** so the rest of the system does not depend on Ollama directly.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.9",
  "title": "Define embedding provider interface",
  "files": [
    { "path": "server/indexing/embeddings/base.py", "action": "create" },
    { "path": "server/indexing/embeddings/__init__.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/embeddings/base.py
+from abc import ABC, abstractmethod
+from typing import List
+
+
+class EmbeddingProvider(ABC):
+    @abstractmethod
+    def embed(self, texts: List[str]) -> List[List[float]]:
+        """
+        Generate embeddings for a list of texts.
+        Must be deterministic for identical inputs.
+        """
+        raise NotImplementedError
```

---

### ✅ Verification Checklist

* [ ] No Ollama import
* [ ] Batch-based API
* [ ] Deterministic contract

---

## 🧱 TASK 1.10 — Ollama Embedding Implementation

### 🎯 Objective

Implement embeddings using **Ollama**, without leaking Ollama details upward.

📌 Model choice stays configurable later (v1.1).

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.10",
  "title": "Implement Ollama embedding provider",
  "files": [
    { "path": "server/indexing/embeddings/ollama.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "high"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/embeddings/ollama.py
+import requests
+from typing import List
+
+from .base import EmbeddingProvider
+
+
+class OllamaEmbeddingProvider(EmbeddingProvider):
+    def __init__(self, base_url: str, model: str):
+        self.base_url = base_url.rstrip("/")
+        self.model = model
+
+    def embed(self, texts: List[str]) -> List[List[float]]:
+        embeddings: List[List[float]] = []
+
+        for text in texts:
+            res = requests.post(
+                f"{self.base_url}/api/embeddings",
+                json={
+                    "model": self.model,
+                    "prompt": text
+                },
+                timeout=60
+            )
+            res.raise_for_status()
+            data = res.json()
+            embeddings.append(data["embedding"])
+
+        return embeddings
```

---

### ✅ Verification Checklist

* [ ] Uses `/api/embeddings`
* [ ] No streaming
* [ ] One embedding per chunk
* [ ] Raises on failure (no silent errors)

---

## 🧱 TASK 1.11 — Vector Store (ChromaDB)

### 🎯 Objective

Persist embeddings + metadata in a **queryable vector database**.

📌 Storage location:

```
~/.localpilot/indexes/{projectId}/chroma/
```

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.11",
  "title": "Add ChromaDB vector store",
  "files": [
    { "path": "server/indexing/vector_store.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "high"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/vector_store.py
+from typing import List
+
+import chromadb
+
+from .chunk import CodeChunk
+
+
+class VectorStore:
+    def __init__(self, persist_dir: str, collection_name: str):
+        self.client = chromadb.Client(
+            settings=chromadb.Settings(
+                persist_directory=persist_dir,
+                anonymized_telemetry=False
+            )
+        )
+        self.collection = self.client.get_or_create_collection(
+            name=collection_name
+        )
+
+    def add(
+        self,
+        chunks: List[CodeChunk],
+        embeddings: List[List[float]]
+    ) -> None:
+        self.collection.add(
+            ids=[c.id for c in chunks],
+            documents=[c.content for c in chunks],
+            metadatas=[
+                {
+                    "file_path": c.file_path,
+                    "language": c.language,
+                    "start_line": c.start_line,
+                    "end_line": c.end_line,
+                    "symbol_type": c.symbol_type
+                }
+                for c in chunks
+            ],
+            embeddings=embeddings
+        )
+        self.client.persist()
```

---

### ✅ Verification Checklist

* [ ] One collection per project
* [ ] Metadata stored correctly
* [ ] Persist called
* [ ] No querying yet

---

## 🧱 TASK 1.12 — Index Orchestration Service

### 🎯 Objective

Create the **single entry point** that runs the full indexing pipeline.

This is the heart of Phase 1.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.12",
  "title": "Implement indexing orchestration service",
  "files": [
    { "path": "server/indexing/service.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "high"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/service.py
+from pathlib import Path
+
+from .scanner import WorkspaceScanner
+from .language import detect_language
+from .chunker import SemanticChunker
+from .hash_tracker import hash_file
+from .state import IndexState
+from .vector_store import VectorStore
+
+
+class IndexingService:
+    def __init__(
+        self,
+        workspace: Path,
+        index_root: Path,
+        embedder,
+        progress=None
+    ):
+        self.workspace = workspace
+        self.index_root = index_root
+        self.embedder = embedder
+        self.progress = progress
+
+        self.scanner = WorkspaceScanner()
+        self.chunker = SemanticChunker()
+
+    def run(self) -> None:
+        state = IndexState(self.index_root)
+        state.load()
+
+        files = self.scanner.scan(self.workspace)
+
+        all_chunks = []
+        texts = []
+
+        for idx, path in enumerate(files, start=1):
+            if self.progress:
+                self.progress.report("scan", idx, len(files))
+
+            current_hash = hash_file(path)
+            stored_hash = state.file_hashes.get(str(path))
+
+            if stored_hash == current_hash:
+                continue
+
+            language = detect_language(path)
+            if not language:
+                continue
+
+            source = path.read_text(encoding="utf-8", errors="ignore")
+
+            chunks = self.chunker.chunk_file(
+                file_path=str(path),
+                language=language,
+                source=source
+            )
+
+            all_chunks.extend(chunks)
+            texts.extend([c.content for c in chunks])
+
+            state.file_hashes[str(path)] = current_hash
+
+        if not all_chunks:
+            return
+
+        embeddings = self.embedder.embed(texts)
+
+        store = VectorStore(
+            persist_dir=str(self.index_root / "chroma"),
+            collection_name="code_chunks"
+        )
+        store.add(all_chunks, embeddings)
+
+        state.save()
```

---

### ✅ Verification Checklist

* [ ] End-to-end pipeline runs
* [ ] Hash-based skipping works
* [ ] Index persists across restarts
* [ ] No querying
* [ ] No UI logic

---

## 🎉 PHASE 1 — COMPLETE

You now have:

✅ Deterministic indexing pipeline
✅ Semantic chunking (safe fallback)
✅ Hash-based smart sync
✅ Persistent index state
✅ Ollama embeddings
✅ ChromaDB vector storage

All aligned with:

* privacy-first design
* MVP security constraints
* future v1.1 / v1.2 expansion

---

````

</details>


## docs/ProjectDocuments/architecture.md

*Size: 305,197 bytes | Modified: 2025-12-13T07:37:43.540Z*

<details>
<summary>View code</summary>

````markdown
# 📄 ARCHITECTURE.md

# LocalPilot - System Architecture

> Comprehensive architecture documentation for the LocalPilot VS Code extension

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Architecture Specification |
| **Related To** | PROJECT_OVERVIEW.md, PROJECT_STRUCTURE.md |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents
1. [Architecture Overview](#1-architecture-overview)
2. [System Context](#2-system-context)
3. [High-Level Architecture](#3-high-level-architecture)
4. [Layer Architecture](#4-layer-architecture)
5. [Component Details](#5-component-details)
6. [Data Flow Diagrams](#6-data-flow-diagrams)
7. [Sequence Diagrams](#7-sequence-diagrams)
8. [Interface Definitions](#8-interface-definitions)
9. [State Management](#9-state-management)
10. [Error Handling Strategy](#10-error-handling-strategy)
11. [Security Considerations](#11-security-considerations)

---

## 1. Architecture Overview

### 1.1 Architecture Style

LocalPilot follows a **Practical Clean Architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE STYLE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PATTERN: Practical Clean Architecture                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  KEY PRINCIPLES:                                                 │
│                                                                  │
│  1. DEPENDENCY RULE                                              │
│     Dependencies point INWARD only.                             │
│     Inner layers know nothing about outer layers.               │
│                                                                  │
│           UI ──────────────────────►                             │
│                                     │                            │
│           Features ─────────────────┼───►                        │
│                                     │    │                       │
│           Infrastructure ───────────┼────┼───►                   │
│                                     │    │    │                  │
│                                     ▼    ▼    ▼                  │
│                                 ┌──────────────┐                 │
│                                 │     CORE     │                 │
│                                 │  (Entities,  │                 │
│                                 │  Interfaces) │                 │
│                                 └──────────────┘                 │
│                                                                  │
│  2. INTERFACE SEGREGATION                                        │
│     Core defines interfaces (WHAT).                             │
│     Infrastructure implements (HOW).                            │
│                                                                  │
│  3. FEATURE-BASED ORGANIZATION                                   │
│     Related code lives together.                                │
│     Easy to find, easy to understand.                           │
│                                                                  │
│  4. TESTABILITY                                                  │
│     Core and Features can be tested without external deps.      │
│     Mock Infrastructure for unit tests.                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Monorepo vs Multi-repo** | Monorepo | Single source of truth, easier for solo dev |
| **Extension-Server Split** | Hybrid (TS + Python) | Best of both ecosystems |
| **Communication** | HTTP + WebSocket | REST for operations, WS for streaming |
| **State Management** | Zustand | Lightweight, simple, React-friendly |
| **RAG Framework** | LlamaIndex | Better for code indexing use case |
| **Vector Database** | ChromaDB | Simple setup, Python native |
| **LLM Provider** | Ollama | Local-first, privacy-focused |

---

## 2. System Context

### 2.1 System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM CONTEXT DIAGRAM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                        ┌─────────────┐                          │
│                        │             │                          │
│                        │  Developer  │                          │
│                        │   (User)    │                          │
│                        │             │                          │
│                        └──────┬──────┘                          │
│                               │                                  │
│                               │ Uses                             │
│                               ▼                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │                     VS CODE IDE                             │ │
│  │                                                             │ │
│  │  ┌───────────────────────────────────────────────────────┐ │ │
│  │  │                                                        │ │ │
│  │  │                 LOCALPILOT EXTENSION                   │ │ │
│  │  │                                                        │ │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │ │
│  │  │  │    Chat     │  │    Plan     │  │     Act     │   │ │ │
│  │  │  │    Mode     │  │    Mode     │  │    Mode     │   │ │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘   │ │ │
│  │  │                                                        │ │ │
│  │  └───────────────────────────┬───────────────────────────┘ │ │
│  │                              │                              │ │
│  └──────────────────────────────┼──────────────────────────────┘ │
│                                 │                                │
│                                 │ HTTP/WebSocket                 │
│                                 │ (localhost:52741)              │
│                                 ▼                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                             │ │
│  │                    PYTHON RAG SERVER                        │ │
│  │                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │  Indexing   │  │    RAG      │  │    Chat     │        │ │
│  │  │   Engine    │  │   Query     │  │   Handler   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │                                                             │ │
│  └──────────────────────────┬──────────────────────────────────┘ │
│                             │                                    │
│              ┌──────────────┼──────────────┐                    │
│              │              │              │                    │
│              ▼              ▼              ▼                    │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │               │  │               │  │               │       │
│  │    OLLAMA     │  │   CHROMADB    │  │  FILE SYSTEM  │       │
│  │   (LLM API)   │  │ (Vector Store)│  │  (Workspace)  │       │
│  │               │  │               │  │               │       │
│  │ localhost:    │  │  Embedded     │  │  Project      │       │
│  │    11434      │  │  Database     │  │  Files        │       │
│  │               │  │               │  │               │       │
│  └───────────────┘  └───────────────┘  └───────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 External Systems

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL DEPENDENCIES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SYSTEM: Ollama                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Purpose:    Local LLM inference engine                         │
│  Interface:  REST API on http://localhost:11434                 │
│  Required:   Yes (core dependency)                              │
│  Managed:    By user (must be installed separately)             │
│                                                                  │
│  Endpoints Used:                                                 │
│  ├── GET  /api/tags          - List available models           │
│  ├── POST /api/generate      - Text generation (streaming)     │
│  ├── POST /api/chat          - Chat completion (streaming)     │
│  ├── POST /api/embeddings    - Generate embeddings             │
│  └── GET  /api/version       - Check Ollama version            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SYSTEM: VS Code                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Purpose:    Host IDE for the extension                         │
│  Interface:  VS Code Extension API                              │
│  Required:   Yes (runtime environment)                          │
│  Version:    1.85.0 or higher                                   │
│                                                                  │
│  APIs Used:                                                      │
│  ├── vscode.window         - UI interactions                    │
│  ├── vscode.workspace      - File system access                 │
│  ├── vscode.commands       - Command registration               │
│  ├── vscode.WebviewView    - Custom UI panels                   │
│  └── vscode.OutputChannel  - Logging                            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SYSTEM: File System                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Purpose:    Workspace files and index storage                  │
│  Interface:  VS Code FileSystem API + Node.js fs                │
│  Required:   Yes                                                 │
│                                                                  │
│  Locations:                                                      │
│  ├── Workspace folder      - User's project files               │
│  ├── ~/.localpilot/        - Index storage, settings            │
│  └── Extension storage     - VS Code managed storage            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. High-Level Architecture

### 3.1 Container Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTAINER DIAGRAM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    VS CODE PROCESS                        │   │
│  │                                                           │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │           LOCALPILOT EXTENSION HOST                  │ │   │
│  │  │                 (TypeScript)                         │ │   │
│  │  │                                                      │ │   │
│  │  │  ┌───────────────┐    ┌───────────────────────────┐ │ │   │
│  │  │  │               │    │                           │ │ │   │
│  │  │  │   Extension   │◄──►│      WebView Panel        │ │ │   │
│  │  │  │    Backend    │    │       (React App)         │ │ │   │
│  │  │  │               │    │                           │ │ │   │
│  │  │  │  • Commands   │    │  • Chat UI                │ │ │   │
│  │  │  │  • Services   │    │  • Plan UI                │ │ │   │
│  │  │  │  • VS Code    │    │  • Act UI                 │ │ │   │
│  │  │  │    APIs       │    │  • State Management       │ │ │   │
│  │  │  │               │    │                           │ │ │   │
│  │  │  └───────┬───────┘    └───────────────────────────┘ │ │   │
│  │  │          │                                           │ │   │
│  │  └──────────┼───────────────────────────────────────────┘ │   │
│  │             │                                              │   │
│  └─────────────┼──────────────────────────────────────────────┘   │
│                │                                                  │
│                │ HTTP REST + WebSocket                            │
│                │ (localhost:52741)                                │
│                │                                                  │
│  ┌─────────────┼──────────────────────────────────────────────┐   │
│  │             ▼                                               │   │
│  │  ┌──────────────────────────────────────────────────────┐  │   │
│  │  │              PYTHON RAG SERVER                        │  │   │
│  │  │                  (FastAPI)                            │  │   │
│  │  │                                                       │  │   │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │  │   │
│  │  │  │   API       │ │  Services   │ │ Infrastructure  │ │  │   │
│  │  │  │   Routes    │ │             │ │                 │ │  │   │
│  │  │  │             │ │ • Indexing  │ │ • Ollama Client │ │  │   │
│  │  │  │ • /index    │ │ • RAG Query │ │ • ChromaDB      │ │  │   │
│  │  │  │ • /query    │ │ • Chat      │ │ • Tree-sitter   │ │  │   │
│  │  │  │ • /chat     │ │ • Sync      │ │ • LlamaIndex    │ │  │   │
│  │  │  │ • /health   │ │             │ │                 │ │  │   │
│  │  │  └─────────────┘ └─────────────┘ └─────────────────┘ │  │   │
│  │  │                                                       │  │   │
│  │  └──────────────────────────────────────────────────────┘  │   │
│  │                      PYTHON PROCESS                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│                │               │               │                    │
│                ▼               ▼               ▼                    │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐       │
│  │     OLLAMA      │ │    CHROMADB     │ │   WORKSPACE     │       │
│  │    PROCESS      │ │   (Embedded)    │ │     FILES       │       │
│  │                 │ │                 │ │                 │       │
│  │  LLM Models:    │ │  Collections:   │ │  User's code:   │       │
│  │  • qwen2.5-coder│ │  • code_chunks  │ │  • .ts, .js     │       │
│  │  • mxbai-embed  │ │  • metadata     │ │  • .py, .dart   │       │
│  │                 │ │                 │ │  • etc.         │       │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Responsibilities

```
┌─────────────────────────────────────────────────────────────────┐
│                 COMPONENT RESPONSIBILITIES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  EXTENSION HOST (TypeScript)                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Responsibilities:                                               │
│  ├── Extension lifecycle management                             │
│  ├── VS Code API integration                                     │
│  ├── WebView panel hosting and communication                    │
│  ├── Command registration and handling                          │
│  ├── File system operations (create/modify/delete)              │
│  ├── HTTP/WebSocket client for Python server                    │
│  ├── Settings management                                         │
│  └── Status bar and notifications                               │
│                                                                  │
│  Does NOT:                                                       │
│  ├── Run LLM inference                                           │
│  ├── Manage vector database                                      │
│  ├── Parse code with Tree-sitter                                │
│  └── Generate embeddings                                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  WEBVIEW PANEL (React)                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Responsibilities:                                               │
│  ├── Render Chat/Plan/Act UI                                    │
│  ├── Manage UI state (Zustand)                                  │
│  ├── Handle user input                                           │
│  ├── Display streaming responses                                │
│  ├── Show diffs and code previews                               │
│  ├── Progress indicators                                         │
│  └── Send messages to Extension Host                            │
│                                                                  │
│  Does NOT:                                                       │
│  ├── Access file system directly                                │
│  ├── Make HTTP calls to Python server                           │
│  └── Access VS Code APIs directly                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PYTHON RAG SERVER (FastAPI)                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Responsibilities:                                               │
│  ├── Workspace file scanning and parsing                        │
│  ├── AST-aware code chunking                                    │
│  ├── Embedding generation (via Ollama)                          │
│  ├── Vector storage and retrieval (ChromaDB)                    │
│  ├── RAG query processing                                        │
│  ├── LLM chat orchestration                                      │
│  ├── Streaming response handling                                │
│  ├── File hash tracking for sync                                │
│  └── Index persistence                                           │
│                                                                  │
│  Does NOT:                                                       │
│  ├── Modify workspace files (extension does this)               │
│  ├── Access VS Code APIs                                         │
│  └── Manage UI state                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Layer Architecture

### 4.1 Extension Layer Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                EXTENSION LAYER ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     UI LAYER                                 ││
│  │              (Presentation & Interaction)                    ││
│  │                                                              ││
│  │  ┌──────────────────────────────────────────────────────┐   ││
│  │  │                 WebView (React)                       │   ││
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────────┐    │   ││
│  │  │  │ Components │ │   Hooks    │ │  Store (Zustand)│    │   ││
│  │  │  └────────────┘ └────────────┘ └────────────────┘    │   ││
│  │  └──────────────────────────────────────────────────────┘   ││
│  │                                                              ││
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐     ││
│  │  │  Commands  │  │   Panels   │  │  Status Bar        │     ││
│  │  └────────────┘  └────────────┘  └────────────────────┘     ││
│  │                                                              ││
│  └───────────────────────────┬─────────────────────────────────┘│
│                              │ Uses                              │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   FEATURES LAYER                             ││
│  │               (Business Logic & Use Cases)                   ││
│  │                                                              ││
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ ││
│  │  │  Indexing  │ │    Chat    │ │    Plan    │ │   Act    │ ││
│  │  │  Feature   │ │  Feature   │ │  Feature   │ │ Feature  │ ││
│  │  │            │ │            │ │            │ │          │ ││
│  │  │ •Service   │ │ •Service   │ │ •Service   │ │ •Service │ ││
│  │  │ •SyncSvc   │ │ •Context   │ │ •Parser    │ │ •Executor│ ││
│  │  │ •Progress  │ │  Builder   │ │ •TaskExtr  │ │ •CodeGen │ ││
│  │  └────────────┘ └────────────┘ └────────────┘ └──────────┘ ││
│  │                                                              ││
│  │  ┌────────────┐ ┌────────────────────────────────────────┐  ││
│  │  │   Ollama   │ │              Settings                   │  ││
│  │  │  Feature   │ │              Feature                    │  ││
│  │  └────────────┘ └────────────────────────────────────────┘  ││
│  │                                                              ││
│  └───────────────────────────┬─────────────────────────────────┘│
│                              │ Uses                              │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     CORE LAYER                               ││
│  │            (Entities, Interfaces, Types)                     ││
│  │                                                              ││
│  │  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐   ││
│  │  │    Entities    │  │   Interfaces   │  │    Errors    │   ││
│  │  │                │  │                │  │              │   ││
│  │  │ • Project      │  │ • ILLMProvider │  │ • BaseError  │   ││
│  │  │ • Message      │  │ • IRAGProvider │  │ • OllamaErr  │   ││
│  │  │ • Plan         │  │ • IFileSystem  │  │ • IndexErr   │   ││
│  │  │ • Task         │  │ • IIndexer     │  │              │   ││
│  │  │ • IndexedDoc   │  │ • ISettings    │  │              │   ││
│  │  └────────────────┘  └────────────────┘  └──────────────┘   ││
│  │                                                              ││
│  │  ┌──────────────────────────────────────────────────────┐   ││
│  │  │                     Types                             │   ││
│  │  │  • ModeType  • OllamaTypes  • EventTypes             │   ││
│  │  └──────────────────────────────────────────────────────┘   ││
│  │                                                              ││
│  └───────────────────────────▲─────────────────────────────────┘│
│                              │ Implements                        │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                INFRASTRUCTURE LAYER                          ││
│  │              (External Implementations)                      ││
│  │                                                              ││
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐     ││
│  │  │   VS Code  │  │    HTTP    │  │     WebSocket      │     ││
│  │  │  Adapters  │  │   Client   │  │      Client        │     ││
│  │  │            │  │            │  │                    │     ││
│  │  │ •FileSys   │  │ •ApiClient │  │ •WSClient          │     ││
│  │  │ •Settings  │  │ •Endpoints │  │ •StreamProcessor   │     ││
│  │  │ •Output    │  │            │  │                    │     ││
│  │  └────────────┘  └────────────┘  └────────────────────┘     ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Server Layer Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                  SERVER LAYER ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      API LAYER                               ││
│  │               (Routes, Schemas, WebSocket)                   ││
│  │                                                              ││
│  │  ┌─────────────────────────────────────────────────────┐    ││
│  │  │                  FastAPI Routes                      │    ││
│  │  │                                                      │    ││
│  │  │  /health    /index    /query    /chat    /models    │    ││
│  │  └─────────────────────────────────────────────────────┘    ││
│  │                                                              ││
│  │  ┌────────────────────┐  ┌────────────────────────────┐     ││
│  │  │   Pydantic Schemas │  │    WebSocket Handlers      │     ││
│  │  │   (Request/Response)│  │    (Streaming)             │     ││
│  │  └────────────────────┘  └────────────────────────────┘     ││
│  │                                                              ││
│  └───────────────────────────┬─────────────────────────────────┘│
│                              │ Uses                              │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    SERVICES LAYER                            ││
│  │               (Business Logic Orchestration)                 ││
│  │                                                              ││
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ ││
│  │  │  Indexing  │ │    RAG     │ │    Chat    │ │   Sync   │ ││
│  │  │  Service   │ │  Service   │ │  Service   │ │ Service  │ ││
│  │  └────────────┘ └────────────┘ └────────────┘ └──────────┘ ││
│  │                                                              ││
│  │  ┌──────────────────────────────────────────────────────┐   ││
│  │  │                  Summary Service                      │   ││
│  │  └──────────────────────────────────────────────────────┘   ││
│  │                                                              ││
│  └───────────────────────────┬─────────────────────────────────┘│
│                              │ Uses                              │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   INDEXING SUBSYSTEM                         ││
│  │            (Parsing, Chunking, Embedding)                    ││
│  │                                                              ││
│  │  ┌────────────────────────────────────────────────────┐     ││
│  │  │                   Parsers                           │     ││
│  │  │  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌────────┐  │     ││
│  │  │  │TypeScript│ │JavaScript│ │ Python │ │  Dart  │  │     ││
│  │  │  │  Parser  │ │  Parser  │ │ Parser │ │ Parser │  │     ││
│  │  │  └──────────┘ └──────────┘ └────────┘ └────────┘  │     ││
│  │  └────────────────────────────────────────────────────┘     ││
│  │                                                              ││
│  │  ┌────────────┐ ┌────────────┐ ┌────────────────────┐       ││
│  │  │  Chunker   │ │  Scanner   │ │   Hash Tracker     │       ││
│  │  └────────────┘ └────────────┘ └────────────────────┘       ││
│  │                                                              ││
│  └───────────────────────────┬─────────────────────────────────┘│
│                              │ Uses                              │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     CORE LAYER                               ││
│  │            (Entities, Interfaces, Errors)                    ││
│  │                                                              ││
│  │  ┌────────────┐  ┌──────────────┐  ┌────────────────┐       ││
│  │  │  Entities  │  │  Interfaces  │  │     Errors     │       ││
│  │  │            │  │              │  │                │       ││
│  │  │ •Document  │  │ •IEmbedder   │  │ •IndexingError │       ││
│  │  │ •Chunk     │  │ •IVectorStore│  │ •OllamaError   │       ││
│  │  │ •Embedding │  │ •ILLM        │  │ •ParseError    │       ││
│  │  │ •QueryRes  │  │ •IParser     │  │                │       ││
│  │  └────────────┘  └──────────────┘  └────────────────┘       ││
│  │                                                              ││
│  └───────────────────────────▲─────────────────────────────────┘│
│                              │ Implements                        │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                INFRASTRUCTURE LAYER                          ││
│  │              (External Implementations)                      ││
│  │                                                              ││
│  │  ┌──────────────┐ ┌──────────────┐ ┌────────────────────┐   ││
│  │  │    Ollama    │ │   ChromaDB   │ │    Tree-sitter     │   ││
│  │  │              │ │              │ │                    │   ││
│  │  │ •Client      │ │ •Client      │ │ •Parser wrapper    │   ││
│  │  │ •Embedder    │ │ •VectorStore │ │ •Query files       │   ││
│  │  │ •LLM         │ │              │ │                    │   ││
│  │  └──────────────┘ └──────────────┘ └────────────────────┘   ││
│  │                                                              ││
│  │  ┌──────────────────────────────────────────────────────┐   ││
│  │  │                    LlamaIndex                         │   ││
│  │  │         (Index Builder, Query Engine)                 │   ││
│  │  └──────────────────────────────────────────────────────┘   ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Layer Communication Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                  LAYER COMMUNICATION RULES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ALLOWED DEPENDENCIES (→ means "can depend on")                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│                                                                  │
│  UI Layer ────────────────────────────────────────►             │
│       │                                                          │
│       ├──► Features Layer (use services)                        │
│       ├──► Core Layer (use entities, types)                     │
│       └──► Infrastructure Layer (ONLY through Features)         │
│                                                                  │
│                                                                  │
│  Features Layer ──────────────────────────────────►             │
│       │                                                          │
│       ├──► Core Layer (use entities, interfaces, types)        │
│       └──► Other Features (with caution, prefer events)        │
│                                                                  │
│                                                                  │
│  Infrastructure Layer ────────────────────────────►             │
│       │                                                          │
│       └──► Core Layer (implement interfaces)                    │
│                                                                  │
│                                                                  │
│  Core Layer ──────────────────────────────────────►             │
│       │                                                          │
│       └──► NOTHING (innermost layer)                            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FORBIDDEN DEPENDENCIES (✗)                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ✗ Core → Features                                              │
│  ✗ Core → Infrastructure                                        │
│  ✗ Core → UI                                                    │
│  ✗ Features → Infrastructure (use interfaces instead!)         │
│  ✗ Features → UI                                                │
│  ✗ Infrastructure → Features                                    │
│  ✗ Infrastructure → UI                                          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  EXAMPLE: How Chat Feature Uses Ollama                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────┐                                            │
│  │   ChatService   │  (Features Layer)                          │
│  │                 │                                            │
│  │  constructor(   │                                            │
│  │    llm: ILLMProvider  ◄──── Interface from Core             │
│  │  )              │                                            │
│  └────────┬────────┘                                            │
│           │                                                      │
│           │ At runtime, receives:                               │
│           │                                                      │
│  ┌────────▼────────┐                                            │
│  │  OllamaService  │  (Infrastructure Layer)                    │
│  │                 │                                            │
│  │  implements     │                                            │
│  │  ILLMProvider   │                                            │
│  └─────────────────┘                                            │
│                                                                  │
│  WHY? ChatService doesn't know about Ollama directly.          │
│  It only knows about ILLMProvider interface.                    │
│  This means we could swap Ollama for another LLM provider       │
│  without changing ChatService!                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4 Dependency Injection

```
┌─────────────────────────────────────────────────────────────────┐
│                  DEPENDENCY INJECTION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  EXTENSION (TypeScript)                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  We use a simple "Composition Root" pattern:                    │
│                                                                  │
│  // extension.ts (entry point)                                   │
│                                                                  │
│  export async function activate(context: ExtensionContext) {    │
│                                                                  │
│    // 1. Create Infrastructure (implementations)                │
│    const fileSystem = new VSCodeFileSystemAdapter();            │
│    const httpClient = new ApiClient('http://localhost:52741');  │
│    const wsClient = new WebSocketClient();                      │
│                                                                  │
│    // 2. Create Features (inject dependencies)                  │
│    const ollamaFeature = new OllamaService(httpClient);         │
│    const indexingFeature = new IndexingService(httpClient);     │
│    const chatFeature = new ChatService(httpClient, wsClient);   │
│    const planFeature = new PlanService(chatFeature);            │
│    const actFeature = new ActService(fileSystem, chatFeature);  │
│                                                                  │
│    // 3. Create UI (inject features)                            │
│    const panel = new MainPanel(context, {                       │
│      ollama: ollamaFeature,                                      │
│      indexing: indexingFeature,                                  │
│      chat: chatFeature,                                          │
│      plan: planFeature,                                          │
│      act: actFeature,                                            │
│    });                                                           │
│                                                                  │
│    // 4. Register commands                                       │
│    registerCommands(context, { indexing, chat, plan, act });    │
│  }                                                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SERVER (Python)                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  We use FastAPI's dependency injection:                         │
│                                                                  │
│  # dependencies.py                                               │
│                                                                  │
│  from functools import lru_cache                                │
│                                                                  │
│  @lru_cache()                                                   │
│  def get_ollama_client() -> OllamaClient:                       │
│      return OllamaClient(base_url="http://localhost:11434")     │
│                                                                  │
│  @lru_cache()                                                   │
│  def get_vector_store() -> ChromaDBStore:                       │
│      return ChromaDBStore(persist_dir="~/.localpilot/indexes")  │
│                                                                  │
│  @lru_cache()                                                   │
│  def get_embedder(                                               │
│      client: OllamaClient = Depends(get_ollama_client)          │
│  ) -> OllamaEmbedder:                                            │
│      return OllamaEmbedder(client, model="mxbai-embed-large")   │
│                                                                  │
│  def get_indexing_service(                                       │
│      embedder: OllamaEmbedder = Depends(get_embedder),          │
│      store: ChromaDBStore = Depends(get_vector_store)           │
│  ) -> IndexingService:                                           │
│      return IndexingService(embedder, store)                    │
│                                                                  │
│  # routes/index.py                                               │
│                                                                  │
│  @router.post("/start")                                          │
│  async def start_indexing(                                       │
│      request: IndexRequest,                                      │
│      service: IndexingService = Depends(get_indexing_service)   │
│  ):                                                              │
│      return await service.index_workspace(request.path)         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Component Details

### 5.1 Extension Components Deep Dive

#### 5.1.1 Chat Feature

```
┌─────────────────────────────────────────────────────────────────┐
│                      CHAT FEATURE COMPONENT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PURPOSE:                                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Enable natural language conversation about the codebase with   │
│  RAG-enhanced context retrieval.                                │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  INTERNAL STRUCTURE:                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ChatService                           │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Orchestrate chat conversation flow                   │   │
│  │  • Manage conversation history (session)                │   │
│  │  • Coordinate with Python server for RAG queries        │   │
│  │  • Handle streaming responses                           │   │
│  │  • Detect when plan should be created                   │   │
│  │                                                          │   │
│  │  Public Methods:                                         │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async sendMessage(message: string): Promise<void>  │ │   │
│  │  │   • Sends user message                             │ │   │
│  │  │   • Triggers RAG query                             │ │   │
│  │  │   • Receives streaming response                    │ │   │
│  │  │   • Emits events for UI updates                    │ │   │
│  │  │                                                    │ │   │
│  │  │ async generateSummary(): Promise<string>           │ │   │
│  │  │   • Called after indexing completes                │ │   │
│  │  │   • Requests project summary from server           │ │   │
│  │  │   • Returns formatted summary                      │ │   │
│  │  │                                                    │ │   │
│  │  │ async transferToPlan(): Promise<Plan>              │ │   │
│  │  │   • Analyzes conversation context                  │ │   │
│  │  │   • Requests plan generation from LLM              │ │   │
│  │  │   • Returns structured Plan entity                 │ │   │
│  │  │                                                    │ │   │
│  │  │ clearHistory(): void                               │ │   │
│  │  │   • Clears current conversation                    │ │   │
│  │  │   • Resets context window                          │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │                                                          │   │
│  │  Dependencies:                                           │   │
│  │  • ApiClient (HTTP communication)                       │   │
│  │  • WebSocketClient (streaming)                          │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  ContextBuilder                          │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Build LLM prompt with RAG context                    │   │
│  │  • Manage context window budget                         │   │
│  │  • Format retrieved code chunks                         │   │
│  │                                                          │   │
│  │  Key Method:                                             │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ buildPrompt(                                       │ │   │
│  │  │   userMessage: string,                             │ │   │
│  │  │   ragChunks: Chunk[],                              │ │   │
│  │  │   history: Message[]                               │ │   │
│  │  │ ): string                                          │ │   │
│  │  │                                                    │ │   │
│  │  │ Algorithm:                                         │ │   │
│  │  │ 1. Allocate token budget (8K model example):      │ │   │
│  │  │    - System prompt: 500 tokens                    │ │   │
│  │  │    - RAG context: 2000 tokens                     │ │   │
│  │  │    - History: 3500 tokens                         │ │   │
│  │  │    - Current + buffer: 2000 tokens                │ │   │
│  │  │                                                    │ │   │
│  │  │ 2. Format RAG chunks:                              │ │   │
│  │  │    For each chunk:                                 │ │   │
│  │  │      Add file path, line numbers                  │ │   │
│  │  │      Add code with syntax highlighting markers    │ │   │
│  │  │      Trim if exceeds budget                       │ │   │
│  │  │                                                    │ │   │
│  │  │ 3. Trim history to fit budget:                     │ │   │
│  │  │    Keep most recent messages                      │ │   │
│  │  │    Remove oldest if needed                        │ │   │
│  │  │                                                    │ │   │
│  │  │ 4. Assemble final prompt:                          │ │   │
│  │  │    System + RAG Context + History + Current       │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   MessageHandler                         │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Process incoming streaming tokens                    │   │
│  │  • Detect special markers (code blocks, etc.)          │   │
│  │  • Emit UI update events                                │   │
│  │                                                          │   │
│  │  Handles:                                                │   │
│  │  • Markdown code blocks                                  │   │
│  │  • File references                                       │   │
│  │  • Error messages                                        │   │
│  │  • Completion signals                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  DATA FLOW:                                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  User Input                                                      │
│      │                                                           │
│      ▼                                                           │
│  ChatService.sendMessage()                                       │
│      │                                                           │
│      ├──► 1. Query RAG (HTTP POST /api/query)                   │
│      │       └──► Returns: Chunk[]                              │
│      │                                                           │
│      ├──► 2. ContextBuilder.buildPrompt()                       │
│      │       └──► Returns: formatted prompt                     │
│      │                                                           │
│      ├──► 3. Open WebSocket (/ws/chat)                          │
│      │       └──► Send: { prompt, model, ... }                  │
│      │                                                           │
│      └──► 4. MessageHandler processes stream                    │
│            └──► Emits: token events → UI updates                │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  EVENTS EMITTED:                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  • 'message:start'    - New assistant message beginning         │
│  • 'message:token'    - New token received                      │
│  • 'message:complete' - Message fully received                  │
│  • 'message:error'    - Error occurred                          │
│  • 'rag:retrieved'    - RAG chunks retrieved                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.1.2 Plan Feature

```
┌─────────────────────────────────────────────────────────────────┐
│                      PLAN FEATURE COMPONENT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PURPOSE:                                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Convert chat discussion into structured, actionable TODO list  │
│  with file paths and clear steps.                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  INTERNAL STRUCTURE:                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    PlanService                           │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Generate plan from conversation context              │   │
│  │  • Parse LLM output into Plan entity                    │   │
│  │  • Validate plan structure                               │   │
│  │  • Handle plan editing and regeneration                 │   │
│  │                                                          │   │
│  │  Public Methods:                                         │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async generatePlan(                                │ │   │
│  │  │   context: ConversationContext                     │ │   │
│  │  │ ): Promise<Plan>                                   │ │   │
│  │  │                                                    │ │   │
│  │  │   Steps:                                           │ │   │
│  │  │   1. Build planning prompt from context           │ │   │
│  │  │   2. Query RAG for relevant code structure        │ │   │
│  │  │   3. Send to LLM with planning system prompt      │ │   │
│  │  │   4. Parse LLM response                            │ │   │
│  │  │   5. Validate plan structure                       │ │   │
│  │  │   6. Return Plan entity                            │ │   │
│  │  │                                                    │ │   │
│  │  │ async regeneratePlan(                              │ │   │
│  │  │   currentPlan: Plan,                               │ │   │
│  │  │   feedback: string                                 │ │   │
│  │  │ ): Promise<Plan>                                   │ │   │
│  │  │                                                    │ │   │
│  │  │   • Incorporates user feedback                     │ │   │
│  │  │   • Keeps what worked from current plan           │ │   │
│  │  │   • Modifies based on feedback                     │ │   │
│  │  │                                                    │ │   │
│  │  │ validatePlan(plan: Plan): ValidationResult        │ │   │
│  │  │                                                    │ │   │
│  │  │   Checks:                                          │ │   │
│  │  │   • All tasks have file paths                      │ │   │
│  │  │   • File paths exist or are valid new paths       │ │   │
│  │  │   • Tasks are atomic and clear                    │ │   │
│  │  │   • Dependencies are logical                       │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    PlanParser                            │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Parse LLM markdown output into structured Plan      │   │
│  │  • Extract tasks with metadata                         │   │
│  │  • Handle various markdown formats gracefully          │   │
│  │                                                          │   │
│  │  Key Method:                                             │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ parse(markdown: string): Plan                      │ │   │
│  │  │                                                    │ │   │
│  │  │ Expected Input Format:                             │ │   │
│  │  │                                                    │ │   │
│  │  │ ## Plan: {Title}                                   │ │   │
│  │  │                                                    │ │   │
│  │  │ ### Overview                                       │ │   │
│  │  │ {Description}                                      │ │   │
│  │  │                                                    │ │   │
│  │  │ ### Implementation Steps                           │ │   │
│  │  │                                                    │ │   │
│  │  │ - [ ] 1. {Task Title}                              │ │   │
│  │  │   📁 {file/path}                                   │ │   │
│  │  │   ├─ {Detail}                                      │ │   │
│  │  │   └─ {Detail}                                      │ │   │
│  │  │                                                    │ │   │
│  │  │ - [ ] 2. {Task Title}                              │ │   │
│  │  │   ...                                              │ │   │
│  │  │                                                    │ │   │
│  │  │ Parsing Algorithm:                                 │ │   │
│  │  │ 1. Extract title from ## Plan: line               │ │   │
│  │  │ 2. Extract overview text                           │ │   │
│  │  │ 3. Find "### Implementation Steps" section        │ │   │
│  │  │ 4. For each "- [ ]" checkbox:                      │ │   │
│  │  │    a. Extract task number and title               │ │   │
│  │  │    b. Look for 📁 or file path pattern            │ │   │
│  │  │    c. Extract indented details                     │ │   │
│  │  │    d. Determine action type (create/modify/delete) │ │   │
│  │  │    e. Create Task entity                           │ │   │
│  │  │ 5. Build dependency graph from task order         │ │   │
│  │  │ 6. Return complete Plan entity                     │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   TaskExtractor                          │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Extract individual tasks from plan text             │   │
│  │  • Determine task type (create/modify/delete)          │   │
│  │  • Infer file paths if not explicitly stated           │   │
│  │                                                          │   │
│  │  Task Types:                                             │   │
│  │  • CREATE    - New file                                  │   │
│  │  • MODIFY    - Edit existing file                        │   │
│  │  • DELETE    - Remove file                               │   │
│  │  • COMMAND   - Run command (future, v1.1)               │   │
│  │                                                          │   │
│  │  Inference Rules:                                        │   │
│  │  • "Create {file}" → CREATE                             │   │
│  │  • "Update {file}" → MODIFY                             │   │
│  │  • "Add to {file}" → MODIFY                             │   │
│  │  • "Remove {file}" → DELETE                             │   │
│  │  • "Install" → COMMAND (skip in MVP)                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  DATA STRUCTURES:                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Plan Entity:                                                    │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ interface Plan {                                       │     │
│  │   id: string;                                          │     │
│  │   title: string;                                       │     │
│  │   overview: string;                                    │     │
│  │   tasks: Task[];                                       │     │
│  │   createdAt: Date;                                     │     │
│  │   updatedAt: Date;                                     │     │
│  │   status: 'draft' | 'approved' | 'executing';         │     │
│  │ }                                                      │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Task Entity:                                                    │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ interface Task {                                       │     │
│  │   id: string;                                          │     │
│  │   orderIndex: number;                                  │     │
│  │   title: string;                                       │     │
│  │   description: string;                                 │     │
│  │   filePath: string;                                    │     │
│  │   actionType: 'create' | 'modify' | 'delete';         │     │
│  │   details: string[];                                   │     │
│  │   dependencies: string[]; // task IDs                  │     │
│  │   status: 'pending' | 'running' | 'done' | 'error';   │     │
│  │   estimatedComplexity?: 'simple' | 'medium' | 'complex';│    │
│  │ }                                                      │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.1.3 Act Feature

```
┌─────────────────────────────────────────────────────────────────┐
│                       ACT FEATURE COMPONENT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PURPOSE:                                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Execute plan tasks step-by-step, generating code and modifying │
│  files with user approval at each step.                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  INTERNAL STRUCTURE:                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     ActService                           │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Orchestrate task execution                           │   │
│  │  • Manage execution state and progress                  │   │
│  │  • Handle pause/resume/stop                             │   │
│  │  • Create TODO markdown file                            │   │
│  │  • Emit progress events                                 │   │
│  │                                                          │   │
│  │  Public Methods:                                         │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async executePlan(plan: Plan): Promise<void>       │ │   │
│  │  │                                                    │ │   │
│  │  │   Flow:                                            │ │   │
│  │  │   1. Create TODO.md file in workspace              │ │   │
│  │  │   2. Initialize execution state                    │ │   │
│  │  │   3. For each task in plan.tasks:                  │ │   │
│  │  │      a. Set task status = 'running'                │ │   │
│  │  │      b. Execute task (via TaskExecutor)            │ │   │
│  │  │      c. If user approval needed, wait              │ │   │
│  │  │      d. Apply changes if approved                  │ │   │
│  │  │      e. Set task status = 'done' | 'error'         │ │   │
│  │  │      f. Update TODO.md                             │ │   │
│  │  │   4. Emit completion event                         │ │   │
│  │  │                                                    │ │   │
│  │  │ pause(): void                                      │ │   │
│  │  │   • Pauses after current task completes            │ │   │
│  │  │                                                    │ │   │
│  │  │ resume(): void                                     │ │   │
│  │  │   • Continues from next pending task               │ │   │
│  │  │                                                    │ │   │
│  │  │ stop(): void                                       │ │   │
│  │  │   • Cancels execution immediately                  │ │   │
│  │  │   • Marks remaining tasks as 'pending'             │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │                                                          │   │
│  │  State Machine:                                          │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │                                                    │ │   │
│  │  │    IDLE ──► RUNNING ──► PAUSED ──► RUNNING        │ │   │
│  │  │              │  ▲         │                        │ │   │
│  │  │              │  │         │                        │ │   │
│  │  │              ▼  │         ▼                        │ │   │
│  │  │           STOPPED ◄── COMPLETED                    │ │   │
│  │  │                                                    │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   TaskExecutor                           │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Execute a single task                                │   │
│  │  • Generate code for the task                          │   │
│  │  • Create file diff if modifying                       │   │
│  │  • Return execution result                             │   │
│  │                                                          │   │
│  │  Key Method:                                             │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async executeTask(                                 │ │   │
│  │  │   task: Task,                                      │ │   │
│  │  │   context: ExecutionContext                        │ │   │
│  │  │ ): Promise<TaskResult>                             │ │   │
│  │  │                                                    │ │   │
│  │  │ Algorithm by Action Type:                          │ │   │
│  │  │                                                    │ │   │
│  │  │ CREATE:                                            │ │   │
│  │  │   1. Generate code via CodeGenerator               │ │   │
│  │  │   2. Preview code to user                          │ │   │
│  │  │   3. Wait for approval                             │ │   │
│  │  │   4. Write file via FileWriter                     │ │   │
│  │  │   5. Return success/failure                        │ │   │
│  │  │                                                    │ │   │
│  │  │ MODIFY:                                            │ │   │
│  │  │   1. Read existing file                            │ │   │
│  │  │   2. Generate new version via CodeGenerator        │ │   │
│  │  │   3. Create diff via DiffGenerator                 │ │   │
│  │  │   4. Show diff to user                             │ │   │
│  │  │   5. Wait for approval                             │ │   │
│  │  │   6. Apply changes via FileWriter                  │ │   │
│  │  │   7. Return success/failure                        │ │   │
│  │  │                                                    │ │   │
│  │  │ DELETE:                                            │ │   │
│  │  │   1. Confirm file exists                           │ │   │
│  │  │   2. Show file contents to user                    │ │   │
│  │  │   3. Wait for deletion approval                    │ │   │
│  │  │   4. Delete file via FileWriter                    │ │   │
│  │  │   5. Return success/failure                        │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   CodeGenerator                          │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Generate code for a specific task                    │   │
│  │  • Use RAG to understand project patterns              │   │
│  │  • Ensure code follows project conventions             │   │
│  │                                                          │   │
│  │  Key Method:                                             │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async generateCode(                                │ │   │
│  │  │   task: Task,                                      │ │   │
│  │  │   context: CodeContext                             │ │   │
│  │  │ ): Promise<string>                                 │ │   │
│  │  │                                                    │ │   │
│  │  │ Process:                                           │ │   │
│  │  │ 1. Query RAG for similar code patterns            │ │   │
│  │  │    └─ "Find examples of {task.type} in {lang}"    │ │   │
│  │  │                                                    │ │   │
│  │  │ 2. If MODIFY, get existing file content           │ │   │
│  │  │                                                    │ │   │
│  │  │ 3. Build generation prompt:                        │ │   │
│  │  │    • Task description                              │ │   │
│  │  │    • Similar code examples from RAG               │ │   │
│  │  │    • Existing file content (if MODIFY)            │ │   │
│  │  │    • Project conventions                           │ │   │
│  │  │    • Language-specific guidelines                  │ │   │
│  │  │                                                    │ │   │
│  │  │ 4. Send to LLM (via Python server)                │ │   │
│  │  │                                                    │ │   │
│  │  │ 5. Extract code from LLM response                 │ │   │
│  │  │    └─ Remove markdown markers                      │ │   │
│  │  │    └─ Validate syntax (basic)                      │ │   │
│  │  │                                                    │ │   │
│  │  │ 6. Return generated code                           │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   DiffGenerator                          │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Generate unified diff between old and new code      │   │
│  │  • Format diff for display                             │   │
│  │                                                          │   │
│  │  Uses library: 'diff' (npm package)                     │   │
│  │                                                          │   │
│  │  Output Format:                                          │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ --- a/src/auth/auth.service.ts                     │ │   │
│  │  │ +++ b/src/auth/auth.service.ts                     │ │   │
│  │  │ @@ -1,5 +1,8 @@                                    │ │   │
│  │  │  import { Injectable } from '@nestjs/common';      │ │   │
│  │  │ +import { JwtService } from '@nestjs/jwt';         │ │   │
│  │  │                                                    │ │   │
│  │  │  export class AuthService {                        │ │   │
│  │  │ -  // TODO: implement                              │ │   │
│  │  │ +  constructor(private jwt: JwtService) {}         │ │   │
│  │  │ +                                                   │ │   │
│  │  │ +  async login(user: User) {                       │ │   │
│  │  │ +    return this.jwt.sign({ sub: user.id });       │ │   │
│  │  │ +  }                                                │ │   │
│  │  │  }                                                  │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    FileWriter                            │   │
│  │                                                          │   │
│  │  Responsibilities:                                       │   │
│  │  • Write files to workspace safely                     │   │
│  │  • Create backup before modifying                      │   │
│  │  • Handle file system errors                           │   │
│  │  • Trigger re-indexing for modified files              │   │
│  │                                                          │   │
│  │  Key Methods:                                            │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async createFile(                                  │ │   │
│  │  │   path: string,                                    │ │   │
│  │  │   content: string                                  │ │   │
│  │  │ ): Promise<void>                                   │ │   │
│  │  │                                                    │ │   │
│  │  │ async modifyFile(                                  │ │   │
│  │  │   path: string,                                    │ │   │
│  │  │   newContent: string                               │ │   │
│  │  │ ): Promise<void>                                   │ │   │
│  │  │                                                    │ │   │
│  │  │ Safety Features:                                   │ │   │
│  │  │ • Creates .localpilot/backups/{timestamp}/         │ │   │
│  │  │ • Backs up before modify                           │ │   │
│  │  │ • Validates paths (no outside workspace)           │ │   │
│  │  │ • Handles permissions errors                       │ │   │
│  │  │ • Triggers index update after write                │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  EVENTS EMITTED:                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  • 'execution:started'     - Plan execution began               │
│  • 'task:started'          - Task execution started             │
│  • 'task:code-generated'   - Code generated, awaiting approval  │
│  • 'task:completed'        - Task successfully completed        │
│  • 'task:error'            - Task failed                        │
│  • 'task:skipped'          - User skipped task                  │
│  • 'execution:paused'      - Execution paused                   │
│  • 'execution:completed'   - All tasks completed                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Server Components Deep Dive

#### 5.2.1 Indexing Service

```
┌─────────────────────────────────────────────────────────────────┐
│                   INDEXING SERVICE COMPONENT                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PURPOSE:                                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Orchestrate the entire indexing pipeline from file scanning    │
│  to vector storage.                                             │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CLASS DIAGRAM:                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  IndexingService                         │   │
│  │                                                          │   │
│  │  Dependencies:                                           │   │
│  │  • scanner: FileScanner                                  │   │
│  │  • parser_factory: ParserFactory                        │   │
│  │  • chunker: Chunker                                      │   │
│  │  • embedder: IEmbedder                                   │   │
│  │  • vector_store: IVectorStore                           │   │
│  │  • hash_tracker: HashTracker                            │   │
│  │  • progress_tracker: ProgressTracker                    │   │
│  │                                                          │   │
│  │  Public Methods:                                         │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async def index_workspace(                         │ │   │
│  │  │     self,                                          │ │   │
│  │  │     workspace_path: str,                           │ │   │
│  │  │     project_id: str                                │ │   │
│  │  │ ) -> IndexResult                                   │ │   │
│  │  │                                                    │ │   │
│  │  │ Pipeline:                                          │ │   │
│  │  │                                                    │ │   │
│  │  │ 1. SCAN PHASE                                      │ │   │
│  │  │    files = scanner.scan(workspace_path)            │ │   │
│  │  │    • Recursively find all files                    │ │   │
│  │  │    • Filter by extensions                          │ │   │
│  │  │    • Respect .gitignore                            │ │   │
│  │  │    • Skip node_modules, .git, etc.                 │ │   │
│  │  │                                                    │ │   │
│  │  │ 2. PARSE & CHUNK PHASE                             │ │   │
│  │  │    For each file:                                  │ │   │
│  │  │      a. Detect language from extension            │ │   │
│  │  │      b. Get appropriate parser                     │ │   │
│  │  │      c. Parse file → AST                           │ │   │
│  │  │      d. Extract code units (functions, classes)   │ │   │
│  │  │      e. Create chunks with metadata                │ │   │
│  │  │      f. Report progress                            │ │   │
│  │  │                                                    │ │   │
│  │  │ 3. EMBEDDING PHASE                                 │ │   │
│  │  │    For each chunk:                                 │ │   │
│  │  │      a. Generate embedding via Ollama              │ │   │
│  │  │      b. Attach metadata (file, line, type)         │ │   │
│  │  │      c. Report progress                            │ │   │
│  │  │                                                    │ │   │
│  │  │ 4. STORAGE PHASE                                   │ │   │
│  │  │    Batch insert embeddings to ChromaDB             │ │   │
│  │  │    • Collection: project_{project_id}              │ │   │
│  │  │    • Persist to disk                               │ │   │
│  │  │                                                    │ │   │
│  │  │ 5. HASH TRACKING                                   │ │   │
│  │  │    For each file:                                  │ │   │
│  │  │      Save hash to tracker for sync                 │ │   │
│  │  │                                                    │ │   │
│  │  │ 6. RETURN RESULT                                   │ │   │
│  │  │    return IndexResult(                             │ │   │
│  │  │      files_indexed=count,                          │ │   │
│  │  │      chunks_created=count,                         │ │   │
│  │  │      embeddings_generated=count,                   │ │   │
│  │  │      duration=elapsed_time                         │ │   │
│  │  │    )                                               │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async def sync_index(                              │ │   │
│  │  │     self,                                          │ │   │
│  │  │     workspace_path: str,                           │ │   │
│  │  │     project_id: str                                │ │   │
│  │  │ ) -> SyncResult                                    │ │   │
│  │  │                                                    │ │   │
│  │  │ Smart Sync Algorithm:                              │ │   │
│  │  │                                                    │ │   │
│  │  │ 1. Scan workspace files                            │ │   │
│  │  │                                                    │ │   │
│  │  │ 2. For each file:                                  │ │   │
│  │  │    current_hash = hash_file(file)                  │ │   │
│  │  │    stored_hash = hash_tracker.get(file)            │ │   │
│  │  │                                                    │ │   │
│  │  │    if current_hash != stored_hash:                 │ │   │
│  │  │      changed_files.add(file)                       │ │   │
│  │  │                                                    │ │   │
│  │  │ 3. Find deleted files                              │ │   │
│  │  │    for file in hash_tracker:                       │ │   │
│  │  │      if not exists(file):                          │ │   │
│  │  │        deleted_files.add(file)                     │ │   │
│  │  │                                                    │ │   │
│  │  │ 4. Re-index changed files only                     │ │   │
│  │  │    For each changed_file:                          │ │   │
│  │  │      a. Remove old embeddings from vector store    │ │   │
│  │  │      b. Re-parse, chunk, embed                     │ │   │
│  │  │      c. Insert new embeddings                      │ │   │
│  │  │      d. Update hash tracker                        │ │   │
│  │  │                                                    │ │   │
│  │  │ 5. Clean up deleted files                          │ │   │
│  │  │    For each deleted_file:                          │ │   │
│  │  │      a. Remove embeddings from vector store        │ │   │
│  │  │      b. Remove from hash tracker                   │ │   │
│  │  │                                                    │ │   │
│  │  │ 6. Return sync statistics                          │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.2.2 RAG Service

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAG SERVICE COMPONENT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PURPOSE:                                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Handle retrieval-augmented generation queries to find relevant │
│  code context for LLM prompts.                                  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CLASS DIAGRAM:                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     RAGService                           │   │
│  │                                                          │   │
│  │  Dependencies:                                           │   │
│  │  • embedder: IEmbedder                                   │   │
│  │  • vector_store: IVectorStore                           │   │
│  │  • llama_index: LlamaIndexAdapter                       │   │
│  │                                                          │   │
│  │  Key Method:                                             │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ async def query(                                   │ │   │
│  │  │     self,                                          │ │   │
│  │  │     query_text: str,                               │ │   │
│  │  │     project_id: str,                               │ │   │
│  │  │     top_k: int = 5,                                │ │   │
│  │  │     filters: Optional[Dict] = None                 │ │   │
│  │  │ ) -> List[Chunk]                                   │ │   │
│  │  │                                                    │ │   │
│  │  │ Algorithm:                                         │ │   │
│  │  │                                                    │ │   │
│  │  │ 1. EMBED QUERY                                     │ │   │
│  │  │    query_embedding = await embedder.embed(         │ │   │
│  │  │        query_text                                  │ │   │
│  │  │    )                                               │ │   │
│  │  │    # Returns: List[float] of 1024 dimensions       │ │   │
│  │  │                                                    │ │   │
│  │  │ 2. SIMILARITY SEARCH                               │ │   │
│  │  │    results = vector_store.search(                  │ │   │
│  │  │        collection=f"project_{project_id}",         │ │   │
│  │  │        query_embedding=query_embedding,            │ │   │
│  │  │        top_k=top_k,                                │ │   │
│  │  │        filters=filters  # e.g., {"file_type": "ts"}│ │   │
│  │  │    )                                               │ │   │
│  │  │    # ChromaDB returns closest vectors by cosine    │ │   │
│  │  │                                                    │ │   │
│  │  │ 3. RERANK (optional, simple scoring)               │ │   │
│  │  │    For each result:                                │ │   │
│  │  │      # Boost recent files                          │ │   │
│  │  │      if result.modified_recently:                  │ │   │
│  │  │        result.score *= 1.1                         │ │   │
│  │  │                                                    │ │   │
│  │  │      # Boost exact file name matches               │ │   │
│  │  │      if query_text in result.file_path:            │ │   │
│  │  │        result.score *= 1.2                         │ │   │
│  │  │                                                    │ │   │
│  │  │    Sort by adjusted score                          │ │   │
│  │  │                                                    │ │   │
│  │  │ 4. HYDRATE CHUNKS                                  │ │   │
│  │  │    For each result:                                │ │   │
│  │  │      Create Chunk object with:                     │ │   │
│  │  │      • content (code text)                         │ │   │
│  │  │      • file_path                                   │ │   │
│  │  │      • line_start, line_end                        │ │   │
│  │  │      • chunk_type (function, class, etc.)          │ │   │
│  │  │      • language                                    │ │   │
│  │  │      • similarity_score                            │ │   │
│  │  │                                                    │ │   │
│  │  │ 5. RETURN                                          │ │   │
│  │  │    return chunks[:top_k]                           │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ Specialized Query Methods:                         │ │   │
│  │  │                                                    │ │   │
│  │  │ query_by_file(file_path: str) -> List[Chunk]      │ │   │
│  │  │   • Returns all chunks from specific file          │ │   │
│  │  │                                                    │ │   │
│  │  │ query_by_symbol(symbol_name: str) -> List[Chunk]  │ │   │
│  │  │   • Finds function/class by name                   │ │   │
│  │  │                                                    │ │   │
│  │  │ get_project_summary(project_id: str) -> Summary   │ │   │
│  │  │   • Analyzes all chunks                            │ │   │
│  │  │   • Returns project statistics                     │ │   │
│  │  │   • Lists main files, languages, structure         │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 5.2.3 Chunk ID Generation

Chunk IDs are deterministic hashes to enable:
- Sync detection (compare IDs across sessions)
- Deduplication
- Reproducible indexing

**Algorithm:**
```python
def generate_chunk_id(file_path: str, content: str, chunk_type: str, line_start: int) -> str:
    data = f"{file_path}|{content}|{chunk_type}|{line_start}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]
```

---

## 6. Data Flow Diagrams

### 6.1 Complete Indexing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    INDEXING DATA FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  USER CLICKS "INDEX PROJECT"                                     │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Extension: IndexingFeature.startIndexing()              │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           │ HTTP POST /api/index/start          │
│                           │ Body: { workspace_path, project_id }│
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Server: IndexingService.index_workspace()               │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                  │
│         │                 │                 │                  │
│         ▼                 ▼                 ▼                  │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐             │
│  │   SCAN     │   │   PARSE    │   │   EMBED    │             │
│  │   FILES    │──►│   & CHUNK  │──►│  & STORE   │             │
│  └────────────┘   └────────────┘   └────────────┘             │
│                                                                  │
│  DETAILED BREAKDOWN:                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  STEP 1: SCAN FILES                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  FileScanner.scan("/path/to/workspace")                 │   │
│  │                                                          │   │
│  │  Input:  workspace_path                                 │   │
│  │  Output: List[FileInfo]                                 │   │
│  │                                                          │   │
│  │  FileInfo:                                               │   │
│  │    {                                                     │   │
│  │      path: "/workspace/src/auth/login.ts",              │   │
│  │      extension: ".ts",                                  │   │
│  │      size: 2048,                                        │   │
│  │      language: "typescript"                             │   │
│  │    }                                                     │   │
│  │                                                          │   │
│  │  Filters:                                                │   │
│  │  • Include: .ts, .js, .py, .dart                        │   │
│  │  • Exclude: node_modules/, .git/, dist/, build/         │   │
│  │  • Respects: .gitignore                                 │   │
│  │                                                          │   │
│  │  Progress Event (WebSocket):                            │   │
│  │    { type: "scan", progress: 0.2, current: "src/..." }  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  STEP 2: PARSE & CHUNK                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  For each FileInfo:                                      │   │
│  │                                                          │   │
│  │  1. Get Parser                                           │   │
│  │     parser = ParserFactory.get(file.language)            │   │
│  │     # Returns: TypeScriptParser | PythonParser | etc.    │   │
│  │                                                          │   │
│  │  2. Parse File                                           │   │
│  │     file_content = read_file(file.path)                  │   │
│  │     ast = parser.parse(file_content)                     │   │
│  │                                                          │   │
│  │  3. Extract Code Units                                   │   │
│  │     units = parser.extract_units(ast)                    │   │
│  │                                                          │   │
│  │     Example Unit (function):                             │   │
│  │     {                                                    │   │
│  │       type: "function",                                  │   │
│  │       name: "authenticateUser",                          │   │
│  │       content: "async function authenticateUser...",     │   │
│  │       docstring: "Authenticates a user...",              │   │
│  │       start_line: 15,                                    │   │
│  │       end_line: 42,                                      │   │
│  │       dependencies: ["validateCredentials", "createToken"]│  │
│  │     }                                                    │   │
│  │                                                          │   │
│  │  4. Create Chunks                                        │   │
│  │     For each unit:                                       │   │
│  │       chunk = Chunk(                                     │   │
│  │         id=generate_id(),                                │   │
│  │         content=unit.content,                            │   │
│  │         file_path=file.path,                             │   │
│  │         chunk_type=unit.type,                            │   │
│  │         symbol_name=unit.name,                           │   │
│  │         line_start=unit.start_line,                      │   │
│  │         line_end=unit.end_line,                          │   │
│  │         language=file.language,                          │   │
│  │         metadata={                                       │   │
│  │           "docstring": unit.docstring,                   │   │
│  │           "dependencies": unit.dependencies              │   │
│  │         }                                                │   │
│  │       )                                                  │   │
│  │                                                          │   │
│  │  Progress Event:                                         │   │
│  │    { type: "parse", progress: 0.5, current: file.path } │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  STEP 3: EMBED & STORE                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  For each Chunk:                                         │   │
│  │                                                          │   │
│  │  1. Generate Embedding                                   │   │
│  │     embedding = await OllamaEmbedder.embed(              │   │
│  │       text=chunk.content,                                │   │
│  │       model="mxbai-embed-large"                          │   │
│  │     )                                                    │   │
│  │                                                          │   │
│  │     HTTP POST http://localhost:11434/api/embeddings      │   │
│  │     Request:                                             │   │
│  │       {                                                  │   │
│  │         "model": "mxbai-embed-large",                    │   │
│  │         "prompt": "async function authenticateUser..."   │   │
│  │       }                                                  │   │
│  │                                                          │   │
│  │     Response:                                            │   │
│  │       {                                                  │   │
│  │         "embedding": [0.123, -0.456, 0.789, ... ]       │   │
│  │         # 1024 dimensions for mxbai-embed-large          │   │
│  │       }                                                  │   │
│  │                                                          │   │
│  │  2. Store in ChromaDB                                    │   │
│  │     ChromaDBStore.add(                                   │   │
│  │       collection="project_{project_id}",                 │   │
│  │       id=chunk.id,                                       │   │
│  │       embedding=embedding,                               │   │
│  │       document=chunk.content,                            │   │
│  │       metadata={                                         │   │
│  │         "file_path": chunk.file_path,                    │   │
│  │         "chunk_type": chunk.chunk_type,                  │   │
│  │         "symbol_name": chunk.symbol_name,                │   │
│  │         "line_start": chunk.line_start,                  │   │
│  │         "line_end": chunk.line_end,                      │   │
│  │         "language": chunk.language                       │   │
│  │       }                                                  │   │
│  │     )                                                    │   │
│  │                                                          │   │
│  │  3. Track Hash                                           │   │
│  │     file_hash = compute_hash(file.content)               │   │
│  │     HashTracker.save(file.path, file_hash)               │   │
│  │     # Stored in: ~/.localpilot/indexes/{project}/hashes.json│
│  │                                                          │   │
│  │  Progress Event:                                         │   │
│  │    { type: "embed", progress: 0.85, completed: 200/234 }│   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  STEP 4: FINALIZE                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  1. Persist ChromaDB to disk                             │   │
│  │     ~/.localpilot/indexes/{project_id}/chroma.sqlite3    │   │
│  │                                                          │   │
│  │  2. Save index metadata                                  │   │
│  │     metadata.json:                                       │   │
│  │     {                                                    │   │
│  │       "project_id": "abc123",                            │   │
│  │       "workspace_path": "/path/to/workspace",            │   │
│  │       "indexed_at": "2024-01-15T10:30:00Z",             │   │
│  │       "files_count": 234,                                │   │
│  │       "chunks_count": 1523,                              │   │
│  │       "languages": ["typescript", "python", "dart"]      │   │
│  │     }                                                    │   │
│  │                                                          │   │
│  │  3. Return result to extension                           │   │
│  │     HTTP 200 OK                                          │   │
│  │     {                                                    │   │
│  │       "success": true,                                   │   │
│  │       "files_indexed": 234,                              │   │
│  │       "chunks_created": 1523,                            │   │
│  │       "duration_seconds": 125                            │   │
│  │     }                                                    │   │
│  │                                                          │   │
│  │  4. Trigger summary generation                           │   │
│  │     Extension receives result → calls generateSummary()  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Chat Query Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      CHAT QUERY DATA FLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  USER SENDS MESSAGE: "How does authentication work?"            │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ UI: ChatInput component                                  │   │
│  │   → Calls: chatStore.sendMessage(text)                  │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Extension: ChatService.sendMessage()                     │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│            ┌──────────────┼──────────────┐                      │
│            │              │              │                      │
│            ▼              ▼              ▼                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Query RAG    │ │ Build Context│ │ Stream Chat  │            │
│  │ for Context  │→│   Prompt     │→│   Response   │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                  │
│  DETAILED BREAKDOWN:                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  STEP 1: QUERY RAG                                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Extension sends:                                        │   │
│  │                                                          │   │
│  │  HTTP POST /api/query                                    │   │
│  │  {                                                       │   │
│  │    "project_id": "abc123",                               │   │
│  │    "query_text": "How does authentication work?",       │   │
│  │    "top_k": 5                                            │   │
│  │  }                                                       │   │
│  │                                                          │   │
│  │  Server (RAGService):                                    │   │
│  │  1. Embed query → [0.234, -0.567, ...]                  │   │
│  │  2. Search ChromaDB for similar chunks                   │   │
│  │  3. Return top 5 most relevant                           │   │
│  │                                                          │   │
│  │  Response:                                               │   │
│  │  {                                                       │   │
│  │    "chunks": [                                           │   │
│  │      {                                                   │   │
│  │        "content": "async function authenticateUser...",  │   │
│  │        "file_path": "src/auth/auth.service.ts",         │   │
│  │        "line_start": 15,                                 │   │
│  │        "line_end": 42,                                   │   │
│  │        "chunk_type": "function",                         │   │
│  │        "symbol_name": "authenticateUser",                │   │
│  │        "similarity_score": 0.87                          │   │
│  │      },                                                  │   │
│  │      { ... 4 more chunks ... }                           │   │
│  │    ]                                                     │   │
│  │  }                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  STEP 2: BUILD CONTEXT PROMPT                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ContextBuilder.buildPrompt(                             │   │
│  │    userMessage: "How does authentication work?",         │   │
│  │    ragChunks: [...],                                     │   │
│  │    history: [previous messages]                          │   │
│  │  )                                                       │   │
│  │                                                          │   │
│  │  Assembled Prompt:                                       │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │ [SYSTEM PROMPT]                                    │ │   │
│  │  │ You are LocalPilot, an AI assistant for this      │ │   │
│  │  │ codebase. Answer questions based on the code      │ │   │
│  │  │ context provided.                                  │ │   │
│  │  │                                                    │ │   │
│  │  │ [RAG CONTEXT]                                      │ │   │
│  │  │ Relevant code from the project:                    │ │   │
│  │  │                                                    │ │   │
│  │  │ File: src/auth/auth.service.ts (lines 15-42)      │ │   │
│  │  │ ```typescript                                      │ │   │
│  │  │ async function authenticateUser(credentials) {     │ │   │
│  │  │   // Validates user credentials                    │ │   │
│  │  │   const user = await validateCredentials(...);     │ │   │
│  │  │   if (user) {                                      │ │   │
│  │  │     return createToken(user);                      │ │   │
│  │  │   }                                                │ │   │
│  │  │   throw new UnauthorizedError();                   │ │   │
│  │  │ }                                                  │ │   │
│  │  │ ```                                                │ │   │
│  │  │                                                    │ │   │
│  │  │ File: src/auth/token.ts (lines 8-23)              │ │   │
│  │  │ ```typescript                                      │ │   │
│  │  │ function createToken(user: User): string {         │ │   │
│  │  │   return jwt.sign({ sub: user.id }, SECRET);      │ │   │
│  │  │ }                                                  │ │   │
│  │  │ ```                                                │ │   │
│  │  │                                                    │ │   │
│  │  │ ... (3 more chunks) ...                            │ │   │
│  │  │                                                    │ │   │
│  │  │ [CONVERSATION HISTORY]                             │ │   │
│  │  │ User: What frameworks does this project use?       │ │   │
│  │  │ Assistant: This project uses React with Redux...   │ │   │
│  │  │                                                    │ │   │
│  │  │ [CURRENT QUERY]                                    │ │   │
│  │  │ User: How does authentication work?                │ │   │
│  │  │                                                    │ │   │
│  │  │ [INSTRUCTIONS]                                     │ │   │
│  │  │ Based on the code context above, explain how       │ │   │
│  │  │ authentication works. Reference specific files     │ │   │
│  │  │ and functions in your answer.                      │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  STEP 3: STREAM CHAT RESPONSE                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Extension opens WebSocket:                              │   │
│  │  WS ws://localhost:52741/ws/chat                         │   │
│  │                                                          │   │
│  │  Extension sends:                                        │   │
│  │  {                                                       │   │
│  │    "type": "chat",                                       │   │
│  │    "project_id": "abc123",                               │   │
│  │    "prompt": "[full prompt from step 2]",               │   │
│  │    "model": "qwen2.5-coder:7b",                         │   │
│  │    "stream": true                                        │   │
│  │  }                                                       │   │
│  │                                                          │   │
│  │  Server forwards to Ollama:                              │   │
│  │  HTTP POST http://localhost:11434/api/chat (streaming)   │   │
│  │                                                          │   │
│  │  Server receives tokens from Ollama:                     │   │
│  │  { "message": { "content": "Based" } }                   │   │
│  │  { "message": { "content": " on" } }                     │   │
│  │  { "message": { "content": " the" } }                    │   │
│  │  { "message": { "content": " code" } }                   │   │
│  │  ...                                                     │   │
│  │                                                          │   │
│  │  Server forwards to Extension via WebSocket:             │   │
│  │  { "type": "token", "content": "Based" }                 │   │
│  │  { "type": "token", "content": " on" }                   │   │
│  │  { "type": "token", "content": " the" }                  │   │
│  │  { "type": "token", "content": " code" }                 │   │
│  │  ...                                                     │   │
│  │  { "type": "done" }                                      │   │
│  │                                                          │   │
│  │  Extension (MessageHandler):                             │   │
│  │  • Accumulates tokens                                    │   │
│  │  • Emits events: 'message:token'                        │   │
│  │  • UI updates in real-time                               │   │
│  │                                                          │   │
│  │  Final message displayed to user:                        │   │
│  │  "Based on the code context, authentication works       │   │
│  │   through the `authenticateUser` function in            │   │
│  │   `src/auth/auth.service.ts`. Here's the flow:          │   │
│  │                                                          │   │
│  │   1. User credentials are validated...                  │   │
│  │   2. If valid, a JWT token is created...                │   │
│  │   3. The token is returned to the client...             │   │
│  │                                                          │   │
│  │   The main files involved are:                          │   │
│  │   • `auth.service.ts` - Main authentication logic       │   │
│  │   • `token.ts` - JWT token creation                     │   │
│  │   • `validators.ts` - Credential validation"            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

```

## 7. Sequence Diagrams

### 7.1 Plan Generation Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│              PLAN GENERATION SEQUENCE DIAGRAM                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Actors:                                                         │
│  • User                                                          │
│  • WebView (React UI)                                           │
│  • Extension Host                                                │
│  • Python Server                                                 │
│  • Ollama                                                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  User        WebView      Extension     Server       Ollama      │
│   │            │             │            │            │         │
│   │  Click     │             │            │            │         │
│   │ "Transfer  │             │            │            │         │
│   │  to Plan"  │             │            │            │         │
│   │───────────►│             │            │            │         │
│   │            │             │            │            │         │
│   │            │  postMessage│            │            │         │
│   │            │ (transfer-  │            │            │         │
│   │            │  to-plan)   │            │            │         │
│   │            │────────────►│            │            │         │
│   │            │             │            │            │         │
│   │            │             │ Get current│            │         │
│   │            │             │ conversation            │         │
│   │            │             │ context    │            │         │
│   │            │             │───────────►│            │         │
│   │            │             │            │            │         │
│   │            │             │ POST       │            │         │
│   │            │             │ /api/query │            │         │
│   │            │             │ (get project            │         │
│   │            │             │  structure) │            │         │
│   │            │             │───────────►│            │         │
│   │            │             │            │            │         │
│   │            │             │            │ Query      │         │
│   │            │             │            │ ChromaDB   │         │
│   │            │             │            │────┐       │         │
│   │            │             │            │    │       │         │
│   │            │             │            │◄───┘       │         │
│   │            │             │            │            │         │
│   │            │             │◄───────────│            │         │
│   │            │             │ Chunks[]   │            │         │
│   │            │             │            │            │         │
│   │            │             │ Build      │            │         │
│   │            │             │ planning   │            │         │
│   │            │             │ prompt     │            │         │
│   │            │             │────┐       │            │         │
│   │            │             │    │       │            │         │
│   │            │             │◄───┘       │            │         │
│   │            │             │            │            │         │
│   │            │             │ WS /ws/chat│            │         │
│   │            │             │ (stream    │            │         │
│   │            │             │  plan)     │            │         │
│   │            │             │═══════════►│            │         │
│   │            │             │            │            │         │
│   │            │             │            │ POST       │         │
│   │            │             │            │ /api/chat  │         │
│   │            │             │            │ (stream)   │         │
│   │            │             │            │───────────►│         │
│   │            │             │            │            │         │
│   │            │             │            │◄──token────│         │
│   │            │             │◄═══token═══│            │         │
│   │            │◄────token───│            │            │         │
│   │◄──render───│             │            │            │         │
│   │            │             │            │            │         │
│   │            │             │            │◄──token────│         │
│   │            │             │◄═══token═══│            │         │
│   │            │◄────token───│            │            │         │
│   │◄──render───│             │            │            │         │
│   │            │             │            │            │         │
│   │   ... streaming continues ...         │            │         │
│   │            │             │            │            │         │
│   │            │             │            │◄───done────│         │
│   │            │             │◄════done═══│            │         │
│   │            │             │            │            │         │
│   │            │             │ Parse LLM  │            │         │
│   │            │             │ output to  │            │         │
│   │            │             │ Plan entity│            │         │
│   │            │             │────┐       │            │         │
│   │            │             │    │ PlanParser.parse() │         │
│   │            │             │◄───┘       │            │         │
│   │            │             │            │            │         │
│   │            │             │ Validate   │            │         │
│   │            │             │ plan       │            │         │
│   │            │             │────┐       │            │         │
│   │            │             │    │       │            │         │
│   │            │             │◄───┘       │            │         │
│   │            │             │            │            │         │
│   │            │ postMessage │            │            │         │
│   │            │ (plan-ready,│            │            │         │
│   │            │  Plan obj)  │            │            │         │
│   │            │◄────────────│            │            │         │
│   │            │             │            │            │         │
│   │            │ Update      │            │            │         │
│   │            │ planStore   │            │            │         │
│   │            │────┐        │            │            │         │
│   │            │    │        │            │            │         │
│   │            │◄───┘        │            │            │         │
│   │            │             │            │            │         │
│   │            │ Switch to   │            │            │         │
│   │            │ Plan tab    │            │            │         │
│   │            │────┐        │            │            │         │
│   │            │    │        │            │            │         │
│   │            │◄───┘        │            │            │         │
│   │            │             │            │            │         │
│   │◄─ Display ─│             │            │            │         │
│   │  Plan UI   │             │            │            │         │
│   │            │             │            │            │         │
│   │════════════════════════════════════════════════════│         │
│   │                    PLAN READY                      │         │
│   │════════════════════════════════════════════════════│         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Plan Generation Prompt Template

```
┌─────────────────────────────────────────────────────────────────┐
│                   PLANNING PROMPT TEMPLATE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SYSTEM PROMPT:                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ You are LocalPilot in Planning Mode. Your task is to create││
│  │ a detailed, actionable implementation plan.                 ││
│  │                                                              ││
│  │ Based on the conversation and project context, create a     ││
│  │ step-by-step TODO list that can be executed to implement    ││
│  │ the discussed feature.                                      ││
│  │                                                              ││
│  │ RULES:                                                       ││
│  │ 1. Each task must have a specific file path                 ││
│  │ 2. Tasks should be atomic (one action per task)             ││
│  │ 3. Use existing project patterns and conventions            ││
│  │ 4. Order tasks logically (dependencies first)               ││
│  │ 5. Include testing tasks when appropriate                   ││
│  │                                                              ││
│  │ OUTPUT FORMAT:                                               ││
│  │ Use exactly this markdown structure:                        ││
│  │                                                              ││
│  │ ## Plan: [Title]                                             ││
│  │                                                              ││
│  │ ### Overview                                                 ││
│  │ [Brief description of what we're building]                  ││
│  │                                                              ││
│  │ ### Implementation Steps                                     ││
│  │                                                              ││
│  │ - [ ] 1. **[Task Title]**                                   ││
│  │   📁 `path/to/file.ts`                                      ││
│  │   ├─ [Detail 1]                                              ││
│  │   └─ [Detail 2]                                              ││
│  │                                                              ││
│  │ - [ ] 2. **[Task Title]**                                   ││
│  │   📁 `path/to/another/file.ts`                              ││
│  │   └─ [Detail]                                                ││
│  │                                                              ││
│  │ ### Testing                                                  ││
│  │ - [ ] [How to verify the implementation works]              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  CONTEXT SECTION:                                                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ## Project Context                                          ││
│  │                                                              ││
│  │ ### Project Structure                                        ││
│  │ {Retrieved from RAG - folder structure}                     ││
│  │                                                              ││
│  │ ### Relevant Code                                            ││
│  │ {Retrieved from RAG - similar implementations}              ││
│  │                                                              ││
│  │ ### Conversation Summary                                     ││
│  │ {Summary of chat discussion}                                 ││
│  │                                                              ││
│  │ User wants to: {extracted goal from conversation}           ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Act Execution Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│                ACT EXECUTION SEQUENCE DIAGRAM                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Actors:                                                         │
│  • User                                                          │
│  • WebView (React UI)                                           │
│  • Extension Host                                                │
│  • Python Server                                                 │
│  • VS Code FileSystem                                           │
│  • Ollama                                                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  User     WebView    Extension   Server    FileSystem  Ollama    │
│   │         │           │          │           │          │      │
│   │ Click   │           │          │           │          │      │
│   │"Approve │           │          │           │          │      │
│   │& Execute"           │          │           │          │      │
│   │────────►│           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │         │ postMessage          │           │          │      │
│   │         │(execute-plan,        │           │          │      │
│   │         │ Plan obj)  │          │           │          │      │
│   │         │──────────►│          │           │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ Create TODO.md       │          │      │
│   │         │           │──────────────────────►          │      │
│   │         │           │          │           │          │      │
│   │         │           │◄─────────────────────│          │      │
│   │         │           │ (file created)       │          │      │
│   │         │           │          │           │          │      │
│   │         │◄──────────│          │           │          │      │
│   │         │ (execution-started)  │           │          │      │
│   │◄────────│           │          │           │          │      │
│   │(show    │           │          │           │          │      │
│   │progress)│           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │═══════════════ FOR EACH TASK ══════════════════════════     │
│   │         │           │          │           │          │      │
│   │         │◄──────────│          │           │          │      │
│   │         │ (task-started,       │           │          │      │
│   │         │  task[i])  │          │           │          │      │
│   │◄────────│           │          │           │          │      │
│   │(update  │           │          │           │          │      │
│   │ UI)     │           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ Query RAG for        │          │      │
│   │         │           │ similar code         │          │      │
│   │         │           │──────────►│          │          │      │
│   │         │           │           │          │          │      │
│   │         │           │◄──────────│          │          │      │
│   │         │           │ Chunks[]  │          │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ IF MODIFY: Read      │          │      │
│   │         │           │ existing file        │          │      │
│   │         │           │──────────────────────►          │      │
│   │         │           │           │          │          │      │
│   │         │           │◄─────────────────────│          │      │
│   │         │           │ fileContent          │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ Build code│          │          │      │
│   │         │           │ generation│          │          │      │
│   │         │           │ prompt    │          │          │      │
│   │         │           │────┐      │          │          │      │
│   │         │           │    │      │          │          │      │
│   │         │           │◄───┘      │          │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ WS /ws/chat          │          │      │
│   │         │           │ (generate code)      │          │      │
│   │         │           │══════════►│          │          │      │
│   │         │           │          │           │          │      │
│   │         │           │          │ POST      │          │      │
│   │         │           │          │ /api/chat │          │      │
│   │         │           │          │──────────────────────►      │
│   │         │           │          │           │          │      │
│   │         │           │          │◄─────────────────────│      │
│   │         │           │◄═════════│ (code response)     │      │
│   │         │           │          │           │          │      │
│   │         │           │ Extract  │           │          │      │
│   │         │           │ code from│           │          │      │
│   │         │           │ response │           │          │      │
│   │         │           │────┐     │           │          │      │
│   │         │           │    │     │           │          │      │
│   │         │           │◄───┘     │           │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ IF MODIFY:           │          │      │
│   │         │           │ Generate diff        │          │      │
│   │         │           │────┐     │           │          │      │
│   │         │           │    │ DiffGenerator   │          │      │
│   │         │           │◄───┘     │           │          │      │
│   │         │           │          │           │          │      │
│   │         │◄──────────│          │           │          │      │
│   │         │ (code-generated,     │           │          │      │
│   │         │  code/diff)│          │           │          │      │
│   │◄────────│           │          │           │          │      │
│   │(show    │           │          │           │          │      │
│   │ preview)│           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │ User    │           │          │           │          │      │
│   │ reviews │           │          │           │          │      │
│   │ code    │           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │─────────────────── IF APPROVED ─────────────────────────    │
│   │         │           │          │           │          │      │
│   │ Click   │           │          │           │          │      │
│   │"Apply"  │           │          │           │          │      │
│   │────────►│           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │         │ postMessage          │           │          │      │
│   │         │(apply-task,│          │           │          │      │
│   │         │ taskId)    │          │           │          │      │
│   │         │──────────►│          │           │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ Backup   │           │          │      │
│   │         │           │ existing │           │          │      │
│   │         │           │ file     │           │          │      │
│   │         │           │──────────────────────►          │      │
│   │         │           │           │          │          │      │
│   │         │           │◄─────────────────────│          │      │
│   │         │           │          │           │          │      │
│   │         │           │ Write    │           │          │      │
│   │         │           │ new      │           │          │      │
│   │         │           │ content  │           │          │      │
│   │         │           │──────────────────────►          │      │
│   │         │           │          │           │          │      │
│   │         │           │◄─────────────────────│          │      │
│   │         │           │ (success)│           │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ Request  │           │          │      │
│   │         │           │ re-index │           │          │      │
│   │         │           │ file     │           │          │      │
│   │         │           │──────────►│          │          │      │
│   │         │           │          │           │          │      │
│   │         │           │◄─────────│           │          │      │
│   │         │           │          │           │          │      │
│   │         │           │ Update   │           │          │      │
│   │         │           │ TODO.md  │           │          │      │
│   │         │           │ (mark    │           │          │      │
│   │         │           │  done)   │           │          │      │
│   │         │           │──────────────────────►          │      │
│   │         │           │          │           │          │      │
│   │         │◄──────────│          │           │          │      │
│   │         │ (task-completed,     │           │          │      │
│   │         │  taskId)   │          │           │          │      │
│   │◄────────│           │          │           │          │      │
│   │(update  │           │          │           │          │      │
│   │progress)│           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │───────────────── IF SKIPPED ────────────────────────────    │
│   │         │           │          │           │          │      │
│   │ Click   │           │          │           │          │      │
│   │"Skip"   │           │          │           │          │      │
│   │────────►│           │          │           │          │      │
│   │         │ postMessage          │           │          │      │
│   │         │(skip-task) │          │           │          │      │
│   │         │──────────►│          │           │          │      │
│   │         │           │ Mark task│           │          │      │
│   │         │           │ skipped  │           │          │      │
│   │         │◄──────────│          │           │          │      │
│   │         │ (task-skipped)       │           │          │      │
│   │◄────────│           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │═══════════════ END FOR EACH ═══════════════════════════     │
│   │         │           │          │           │          │      │
│   │         │◄──────────│          │           │          │      │
│   │         │ (execution-completed,│           │          │      │
│   │         │  summary)  │          │           │          │      │
│   │◄────────│           │          │           │          │      │
│   │(show    │           │          │           │          │      │
│   │complete)│           │          │           │          │      │
│   │         │           │          │           │          │      │
│   │════════════════════════════════════════════════════════     │
│   │                 EXECUTION COMPLETE                     │     │
│   │════════════════════════════════════════════════════════     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.4 Code Generation Prompt Template

```
┌─────────────────────────────────────────────────────────────────┐
│                CODE GENERATION PROMPT TEMPLATE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FOR CREATE ACTION:                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ You are LocalPilot in Act Mode. Generate code for a new file││
│  │                                                              ││
│  │ ## Task                                                      ││
│  │ Create file: `{file_path}`                                   ││
│  │                                                              ││
│  │ ## Description                                               ││
│  │ {task.title}                                                 ││
│  │ {task.description}                                           ││
│  │                                                              ││
│  │ ## Requirements                                              ││
│  │ {task.details as bullet points}                             ││
│  │                                                              ││
│  │ ## Project Context                                           ││
│  │ ### Similar Files (for reference)                           ││
│  │ {RAG chunks of similar files}                               ││
│  │                                                              ││
│  │ ### Project Patterns                                         ││
│  │ - Uses {framework} with {conventions}                       ││
│  │ - Follows {naming patterns}                                 ││
│  │                                                              ││
│  │ ## Output Instructions                                       ││
│  │ 1. Generate ONLY the file content                           ││
│  │ 2. Include necessary imports                                ││
│  │ 3. Add JSDoc/docstring comments                             ││
│  │ 4. Follow project conventions from examples                 ││
│  │ 5. Output code inside ```{language} blocks                  ││
│  │                                                              ││
│  │ Generate the complete file:                                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FOR MODIFY ACTION:                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ You are LocalPilot in Act Mode. Modify an existing file.    ││
│  │                                                              ││
│  │ ## Task                                                      ││
│  │ Modify file: `{file_path}`                                   ││
│  │                                                              ││
│  │ ## Description                                               ││
│  │ {task.title}                                                 ││
│  │ {task.description}                                           ││
│  │                                                              ││
│  │ ## Current File Content                                      ││
│  │ ```{language}                                                ││
│  │ {existing file content}                                      ││
│  │ ```                                                          ││
│  │                                                              ││
│  │ ## Required Changes                                          ││
│  │ {task.details as bullet points}                             ││
│  │                                                              ││
│  │ ## Related Code (from RAG)                                   ││
│  │ {RAG chunks showing patterns}                               ││
│  │                                                              ││
│  │ ## Output Instructions                                       ││
│  │ 1. Output the COMPLETE modified file                        ││
│  │ 2. Keep existing code that shouldn't change                 ││
│  │ 3. Apply only the requested modifications                   ││
│  │ 4. Maintain existing style and conventions                  ││
│  │ 5. Output inside ```{language} blocks                       ││
│  │                                                              ││
│  │ Generate the complete modified file:                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.5 Smart Sync Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│                  SMART SYNC SEQUENCE DIAGRAM                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User clicks "Sync Index" after making file changes             │
│                                                                  │
│  User      WebView     Extension    Server      ChromaDB         │
│   │          │            │           │            │             │
│   │ Click    │            │           │            │             │
│   │ "Sync"   │            │           │            │             │
│   │─────────►│            │           │            │             │
│   │          │            │           │            │             │
│   │          │ postMessage│           │            │             │
│   │          │(sync-index)│           │            │             │
│   │          │───────────►│           │            │             │
│   │          │            │           │            │             │
│   │          │◄───────────│           │            │             │
│   │          │(sync-started)          │            │             │
│   │◄─────────│            │           │            │             │
│   │(show     │            │           │            │             │
│   │progress) │            │           │            │             │
│   │          │            │           │            │             │
│   │          │            │ POST      │            │             │
│   │          │            │/api/index/│            │             │
│   │          │            │sync       │            │             │
│   │          │            │──────────►│            │             │
│   │          │            │           │            │             │
│   │          │            │           │ Load stored│             │
│   │          │            │           │ hashes     │             │
│   │          │            │           │────┐       │             │
│   │          │            │           │    │       │             │
│   │          │            │           │◄───┘       │             │
│   │          │            │           │            │             │
│   │          │            │           │ Scan       │             │
│   │          │            │           │ workspace  │             │
│   │          │            │           │────┐       │             │
│   │          │            │           │    │       │             │
│   │          │            │           │◄───┘       │             │
│   │          │            │           │            │             │
│   │          │            │           │ Compare    │             │
│   │          │            │           │ hashes:    │             │
│   │          │            │           │            │             │
│   │          │            │           │ changed=[] │             │
│   │          │            │           │ deleted=[] │             │
│   │          │            │           │ for file   │             │
│   │          │            │           │ in scanned:│             │
│   │          │            │           │   if hash  │             │
│   │          │            │           │   differs: │             │
│   │          │            │           │     add to │             │
│   │          │            │           │     changed│             │
│   │          │            │           │            │             │
│   │          │◄═══════════│           │            │             │
│   │          │(WS: found 5│           │            │             │
│   │          │changed,    │           │            │             │
│   │          │2 deleted)  │           │            │             │
│   │◄─────────│            │           │            │             │
│   │(update   │            │           │            │             │
│   │ status)  │            │           │            │             │
│   │          │            │           │            │             │
│   │══════════ FOR EACH CHANGED FILE ═════════════════════════   │
│   │          │            │           │            │             │
│   │          │            │           │ Delete old │             │
│   │          │            │           │ embeddings │             │
│   │          │            │           │────────────────────────► │
│   │          │            │           │            │             │
│   │          │            │           │ Re-parse   │             │
│   │          │            │           │ & chunk    │             │
│   │          │            │           │────┐       │             │
│   │          │            │           │    │       │             │
│   │          │            │           │◄───┘       │             │
│   │          │            │           │            │             │
│   │          │            │           │ Embed new  │             │
│   │          │            │           │ chunks     │             │
│   │          │            │           │───► Ollama │             │
│   │          │            │           │◄───────────│             │
│   │          │            │           │            │             │
│   │          │            │           │ Store new  │             │
│   │          │            │           │ embeddings │             │
│   │          │            │           │────────────────────────► │
│   │          │            │           │            │             │
│   │          │            │           │ Update hash│             │
│   │          │            │           │────┐       │             │
│   │          │            │           │    │       │             │
│   │          │            │           │◄───┘       │             │
│   │          │            │           │            │             │
│   │          │◄═══════════│           │            │             │
│   │          │(WS: progress            │            │             │
│   │          │ 3/5 files) │           │            │             │
│   │◄─────────│            │           │            │             │
│   │          │            │           │            │             │
│   │══════════════════════════════════════════════════════════   │
│   │          │            │           │            │             │
│   │══════════ FOR EACH DELETED FILE ═════════════════════════   │
│   │          │            │           │            │             │
│   │          │            │           │ Delete     │             │
│   │          │            │           │ embeddings │             │
│   │          │            │           │────────────────────────► │
│   │          │            │           │            │             │
│   │          │            │           │ Remove from│             │
│   │          │            │           │ hash tracker             │
│   │          │            │           │────┐       │             │
│   │          │            │           │    │       │             │
│   │          │            │           │◄───┘       │             │
│   │          │            │           │            │             │
│   │══════════════════════════════════════════════════════════   │
│   │          │            │           │            │             │
│   │          │            │◄──────────│            │             │
│   │          │            │ SyncResult            │             │
│   │          │            │ {changed:5,            │             │
│   │          │            │  deleted:2,            │             │
│   │          │            │  duration:12s}         │             │
│   │          │            │           │            │             │
│   │          │◄───────────│           │            │             │
│   │          │(sync-complete)         │            │             │
│   │◄─────────│            │           │            │             │
│   │(show     │            │           │            │             │
│   │result)   │            │           │            │             │
│   │          │            │           │            │             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Interface Definitions

### 8.1 TypeScript Interfaces (Extension)

#### 8.1.1 Core Entities

```typescript
┌─────────────────────────────────────────────────────────────────┐
│                    CORE ENTITY INTERFACES                        │
├─────────────────────────────────────────────────────────────────┤

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/entities/project.entity.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Represents an indexed project/workspace
 */
export interface Project {
  /** Unique identifier (hash of workspace path) */
  id: string;
  
  /** Display name (folder name) */
  name: string;
  
  /** Absolute path to workspace */
  workspacePath: string;
  
  /** Index status */
  indexStatus: IndexStatus;
  
  /** When indexing was last completed */
  lastIndexedAt: Date | null;
  
  /** Statistics about indexed content */
  stats: ProjectStats;
  
  /** Languages detected in project */
  languages: string[];
}

export type IndexStatus = 
  | 'not-indexed'
  | 'indexing'
  | 'indexed'
  | 'sync-required'
  | 'error';

export interface ProjectStats {
  filesCount: number;
  chunksCount: number;
  totalLines: number;
  byLanguage: Record<string, number>;
}

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/entities/message.entity.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Represents a chat message
 */
export interface Message {
  /** Unique message ID */
  id: string;
  
  /** Who sent the message */
  role: 'user' | 'assistant' | 'system';
  
  /** Message content (may include markdown) */
  content: string;
  
  /** When the message was created */
  timestamp: Date;
  
  /** If this message used RAG context */
  ragContext?: RAGContext;
  
  /** Status for assistant messages (streaming) */
  status?: 'streaming' | 'complete' | 'error';
  
  /** Error details if status is 'error' */
  error?: string;
}

export interface RAGContext {
  /** Chunks used to generate response */
  chunks: RetrievedChunk[];
  
  /** Query that was sent to RAG */
  query: string;
}

export interface RetrievedChunk {
  /** Chunk ID in vector store */
  id: string;
  
  /** Code content */
  content: string;
  
  /** File path relative to workspace */
  filePath: string;
  
  /** Starting line number */
  lineStart: number;
  
  /** Ending line number */
  lineEnd: number;
  
  /** Type of code unit */
  chunkType: ChunkType;
  
  /** Symbol name (function/class name) */
  symbolName?: string;
  
  /** Programming language */
  language: string;
  
  /** Similarity score (0-1) */
  score: number;
}

export type ChunkType = 
  | 'function'
  | 'class'
  | 'method'
  | 'interface'
  | 'type'
  | 'variable'
  | 'import'
  | 'module'
  | 'file';  // When entire file is one chunk

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/entities/plan.entity.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Represents an implementation plan
 */
export interface Plan {
  /** Unique plan ID */
  id: string;
  
  /** Plan title */
  title: string;
  
  /** Brief description/overview */
  overview: string;
  
  /** List of tasks to execute */
  tasks: Task[];
  
  /** When the plan was created */
  createdAt: Date;
  
  /** When the plan was last modified */
  updatedAt: Date;
  
  /** Current plan status */
  status: PlanStatus;
  
  /** Original conversation that led to this plan */
  sourceConversationId?: string;
}

export type PlanStatus = 
  | 'draft'       // Just generated, not approved
  | 'approved'    // User approved, ready to execute
  | 'executing'   // Currently being executed
  | 'paused'      // Execution paused
  | 'completed'   // All tasks done
  | 'cancelled';  // User cancelled

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/entities/task.entity.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Represents a single task in a plan
 */
export interface Task {
  /** Unique task ID */
  id: string;
  
  /** Order in the plan (0-based) */
  orderIndex: number;
  
  /** Short task title */
  title: string;
  
  /** Detailed description */
  description: string;
  
  /** File to create/modify/delete */
  filePath: string;
  
  /** What action to take */
  actionType: TaskActionType;
  
  /** Additional details/requirements */
  details: string[];
  
  /** IDs of tasks this depends on */
  dependencies: string[];
  
  /** Current task status */
  status: TaskStatus;
  
  /** Generated code (after code generation) */
  generatedCode?: string;
  
  /** Diff for modify actions */
  diff?: string;
  
  /** Error message if failed */
  error?: string;
  
  /** Execution timestamps */
  startedAt?: Date;
  completedAt?: Date;
}

export type TaskActionType = 
  | 'create'   // Create new file
  | 'modify'   // Modify existing file
  | 'delete';  // Delete file

export type TaskStatus = 
  | 'pending'     // Not started
  | 'running'     // Currently executing
  | 'awaiting-approval'  // Code generated, waiting for user
  | 'done'        // Successfully completed
  | 'skipped'     // User skipped
  | 'error';      // Failed

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/entities/file-change.entity.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Represents a file change to be applied
 */
export interface FileChange {
  /** File path relative to workspace */
  filePath: string;
  
  /** Type of change */
  changeType: 'create' | 'modify' | 'delete';
  
  /** New content (for create/modify) */
  newContent?: string;
  
  /** Original content (for modify, used in diff) */
  originalContent?: string;
  
  /** Unified diff (for modify) */
  diff?: string;
  
  /** Whether backup was created */
  backedUp: boolean;
  
  /** Path to backup file */
  backupPath?: string;
}

└─────────────────────────────────────────────────────────────────┘
```

#### 8.1.2 Core Interfaces (Ports)

```typescript
┌─────────────────────────────────────────────────────────────────┐
│                    CORE INTERFACE DEFINITIONS                    │
├─────────────────────────────────────────────────────────────────┤

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/interfaces/llm-provider.interface.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Interface for LLM operations
 * 
 * WHY: Abstracts LLM provider (Ollama) so features don't depend
 * on specific implementation. Allows swapping providers.
 */
export interface ILLMProvider {
  /**
   * Check if the LLM provider is available
   */
  isAvailable(): Promise<boolean>;
  
  /**
   * Get list of available models
   */
  listModels(): Promise<ModelInfo[]>;
  
  /**
   * Generate chat completion (non-streaming)
   */
  chat(request: ChatRequest): Promise<ChatResponse>;
  
  /**
   * Generate chat completion with streaming
   */
  chatStream(request: ChatRequest): AsyncGenerator<string, void, unknown>;
  
  /**
   * Generate embeddings for text
   */
  embed(text: string, model?: string): Promise<number[]>;
}

export interface ModelInfo {
  name: string;
  size: number;
  modifiedAt: Date;
  family: string;
  parameterSize: string;
  quantizationLevel: string;
}

export interface ChatRequest {
  model: string;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  options?: {
    temperature?: number;
    topP?: number;
    maxTokens?: number;
  };
}

export interface ChatResponse {
  content: string;
  model: string;
  totalDuration: number;
  promptEvalCount: number;
  evalCount: number;
}

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/interfaces/rag-provider.interface.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Interface for RAG operations
 * 
 * WHY: Abstracts RAG system (Python server + ChromaDB) so
 * features don't depend on specific implementation.
 */
export interface IRAGProvider {
  /**
   * Start indexing a workspace
   */
  startIndexing(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: IndexProgress) => void
  ): Promise<IndexResult>;
  
  /**
   * Sync index (re-index only changed files)
   */
  syncIndex(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: SyncProgress) => void
  ): Promise<SyncResult>;
  
  /**
   * Query for relevant code chunks
   */
  query(
    projectId: string,
    queryText: string,
    topK?: number,
    filters?: QueryFilters
  ): Promise<RetrievedChunk[]>;
  
  /**
   * Get project summary after indexing
   */
  getProjectSummary(projectId: string): Promise<ProjectSummary>;
  
  /**
   * Check if project is indexed
   */
  isIndexed(projectId: string): Promise<boolean>;
  
  /**
   * Clear project index
   */
  clearIndex(projectId: string): Promise<void>;
}

export interface IndexProgress {
  phase: 'scanning' | 'parsing' | 'embedding' | 'storing';
  current: number;
  total: number;
  currentFile?: string;
  message?: string;
}

export interface IndexResult {
  success: boolean;
  filesIndexed: number;
  chunksCreated: number;
  durationSeconds: number;
  languages: string[];
  error?: string;
}

export interface SyncProgress {
  phase: 'scanning' | 'comparing' | 'updating';
  changedFiles: number;
  deletedFiles: number;
  processed: number;
  total: number;
}

export interface SyncResult {
  success: boolean;
  filesUpdated: number;
  filesDeleted: number;
  chunksUpdated: number;
  durationSeconds: number;
}

export interface QueryFilters {
  fileTypes?: string[];
  chunkTypes?: ChunkType[];
  filePaths?: string[];
}

export interface ProjectSummary {
  projectName: string;
  description: string;
  mainLanguages: string[];
  keyFiles: string[];
  architecture: string;
  frameworks: string[];
  stats: ProjectStats;
}

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/interfaces/file-system.interface.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Interface for file system operations
 * 
 * WHY: Abstracts VS Code file system API for testability
 * and potential future cross-platform support.
 */
export interface IFileSystem {
  /**
   * Read file content
   */
  readFile(filePath: string): Promise<string>;
  
  /**
   * Write content to file (creates if not exists)
   */
  writeFile(filePath: string, content: string): Promise<void>;
  
  /**
   * Delete a file
   */
  deleteFile(filePath: string): Promise<void>;
  
  /**
   * Check if file exists
   */
  exists(filePath: string): Promise<boolean>;
  
  /**
   * Create directory (recursive)
   */
  createDirectory(dirPath: string): Promise<void>;
  
  /**
   * List files in directory
   */
  listFiles(dirPath: string, recursive?: boolean): Promise<string[]>;
  
  /**
   * Get file stats
   */
  stat(filePath: string): Promise<FileStat>;
  
  /**
   * Create backup of a file
   */
  backup(filePath: string): Promise<string>; // Returns backup path
  
  /**
   * Restore file from backup
   */
  restore(backupPath: string, targetPath: string): Promise<void>;
  
  /**
   * Get workspace root path
   */
  getWorkspaceRoot(): string | undefined;
}

export interface FileStat {
  isFile: boolean;
  isDirectory: boolean;
  size: number;
  modifiedAt: Date;
  createdAt: Date;
}

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/interfaces/indexer.interface.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Interface for indexing operations (extension-side)
 * 
 * WHY: Provides high-level indexing control for features.
 */
export interface IIndexer {
  /**
   * Start full indexing of workspace
   */
  startIndexing(): Promise<IndexResult>;
  
  /**
   * Sync index with current workspace state
   */
  syncIndex(): Promise<SyncResult>;
  
  /**
   * Get current indexing status
   */
  getStatus(): IndexStatus;
  
  /**
   * Cancel ongoing indexing
   */
  cancelIndexing(): void;
  
  /**
   * Re-index a single file
   */
  reindexFile(filePath: string): Promise<void>;
  
  /**
   * Subscribe to indexing events
   */
  onProgress(callback: (progress: IndexProgress) => void): Disposable;
  onComplete(callback: (result: IndexResult) => void): Disposable;
  onError(callback: (error: Error) => void): Disposable;
}

export interface Disposable {
  dispose(): void;
}

// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/core/interfaces/settings.interface.ts
// ═══════════════════════════════════════════════════════════════

/**
 * Interface for settings management
 */
export interface ISettings {
  /**
   * Get all settings
   */
  getAll(): LocalPilotSettings;
  
  /**
   * Get a specific setting
   */
  get<K extends keyof LocalPilotSettings>(key: K): LocalPilotSettings[K];
  
  /**
   * Update a setting
   */
  set<K extends keyof LocalPilotSettings>(
    key: K, 
    value: LocalPilotSettings[K]
  ): Promise<void>;
  
  /**
   * Reset to defaults
   */
  reset(): Promise<void>;
  
  /**
   * Subscribe to setting changes
   */
  onChange(callback: (settings: LocalPilotSettings) => void): Disposable;
}

export interface LocalPilotSettings {
  // Ollama settings
  ollamaUrl: string;
  chatModel: string;
  embeddingModel: string;
  
  // Indexing settings
  indexingExcludePatterns: string[];
  indexingIncludeExtensions: string[];
  maxFileSizeKb: number;
  
  // Chat settings
  maxContextTokens: number;
  ragTopK: number;
  temperature: number;
  
  // Act mode settings
  autoApproveSimpleTasks: boolean;
  createBackups: boolean;
  
  // UI settings
  theme: 'auto' | 'light' | 'dark';
  showLineNumbers: boolean;
}

└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Python Interfaces (Server)

```python
┌─────────────────────────────────────────────────────────────────┐
│                   PYTHON INTERFACE DEFINITIONS                   │
├─────────────────────────────────────────────────────────────────┤

# ═══════════════════════════════════════════════════════════════
# FILE: server/src/core/interfaces/embedder.py
# ═══════════════════════════════════════════════════════════════

from abc import ABC, abstractmethod
from typing import List

class IEmbedder(ABC):
    """
    Interface for embedding generation.
    
    WHY: Abstracts embedding provider (Ollama) so we could
    swap to different embedding models or providers.
    """
    
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats (embedding vector)
        """
        pass
    
    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        pass
    
    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Return the embedding dimensions."""
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model name."""
        pass


# ═══════════════════════════════════════════════════════════════
# FILE: server/src/core/interfaces/vector_store.py
# ═══════════════════════════════════════════════════════════════

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..entities.chunk import Chunk

class IVectorStore(ABC):
    """
    Interface for vector storage and retrieval.
    
    WHY: Abstracts vector database (ChromaDB) so we could
    swap to Qdrant or other providers in the future.
    """
    
    @abstractmethod
    async def create_collection(self, name: str) -> None:
        """Create a new collection."""
        pass
    
    @abstractmethod
    async def delete_collection(self, name: str) -> None:
        """Delete a collection and all its data."""
        pass
    
    @abstractmethod
    async def add(
        self,
        collection: str,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]]
    ) -> None:
        """
        Add documents with embeddings to collection.
        
        Args:
            collection: Collection name
            ids: Document IDs
            embeddings: Embedding vectors
            documents: Original text content
            metadatas: Metadata for each document
        """
        pass
    
    @abstractmethod
    async def search(
        self,
        collection: str,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            collection: Collection name
            query_embedding: Query vector
            top_k: Number of results
            filters: Metadata filters
            
        Returns:
            List of results with id, document, metadata, score
        """
        pass
    
    @abstractmethod
    async def delete(
        self,
        collection: str,
        ids: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> None:
        """Delete documents by ID or filter."""
        pass
    
    @abstractmethod
    async def get_collection_stats(self, collection: str) -> Dict[str, Any]:
        """Get statistics about a collection."""
        pass


# ═══════════════════════════════════════════════════════════════
# FILE: server/src/core/interfaces/llm.py
# ═══════════════════════════════════════════════════════════════

from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator

class ILLM(ABC):
    """
    Interface for LLM chat operations.
    
    WHY: Abstracts LLM provider for potential multi-provider support.
    """
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate chat completion (non-streaming).
        
        Args:
            messages: List of {role, content} messages
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        Generate chat completion with streaming.
        
        Yields:
            Token strings as they're generated
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if LLM is available."""
        pass
    
    @abstractmethod
    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models."""
        pass


# ═══════════════════════════════════════════════════════════════
# FILE: server/src/core/interfaces/parser.py
# ═══════════════════════════════════════════════════════════════

from abc import ABC, abstractmethod
from typing import List
from ..entities.chunk import CodeUnit

class IParser(ABC):
    """
    Interface for language-specific code parsing.
    
    WHY: Each language has different syntax. Parser interface
    allows adding new language support easily.
    """
    
    @property
    @abstractmethod
    def language(self) -> str:
        """Return the language this parser handles."""
        pass
    
    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """Return file extensions this parser handles."""
        pass
    
    @abstractmethod
    def parse(self, content: str, file_path: str) -> List[CodeUnit]:
        """
        Parse source code into code units.
        
        Args:
            content: Source code content
            file_path: Path to the file (for context)
            
        Returns:
            List of extracted code units (functions, classes, etc.)
        """
        pass
    
    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the file."""
        pass


# Code unit entity referenced by parser
# FILE: server/src/core/entities/chunk.py

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class CodeUnit:
    """Represents a parsed code unit (function, class, etc.)"""
    
    unit_type: str  # 'function', 'class', 'method', etc.
    name: str
    content: str
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    dependencies: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.metadata is None:
            self.metadata = {}


@dataclass 
class Chunk:
    """Represents an indexed chunk with embedding metadata"""
    
    id: str
    content: str
    file_path: str
    chunk_type: str
    symbol_name: Optional[str]
    line_start: int
    line_end: int
    language: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = None

└─────────────────────────────────────────────────────────────────┘
```

### 8.3 API Contracts (HTTP/WebSocket)

```
┌─────────────────────────────────────────────────────────────────┐
│                      API CONTRACT DEFINITIONS                    │
├─────────────────────────────────────────────────────────────────┤

BASE URL: http://localhost:52741/api

═══════════════════════════════════════════════════════════════════
HEALTH & STATUS ENDPOINTS
═══════════════════════════════════════════════════════════════════

GET /health
─────────────────────────────────────────
Response 200:
{
  "status": "healthy",
  "ollama_connected": true,
  "ollama_url": "http://localhost:11434",
  "version": "0.1.0"
}

Response 503:
{
  "status": "unhealthy",
  "ollama_connected": false,
  "error": "Cannot connect to Ollama"
}


GET /models
─────────────────────────────────────────
Response 200:
{
  "models": [
    {
      "name": "qwen2.5-coder:7b-instruct-q4_K_M",
      "size": 4500000000,
      "family": "qwen2",
      "parameter_size": "7B",
      "quantization": "Q4_K_M"
    },
    {
      "name": "mxbai-embed-large:latest",
      "size": 670000000,
      "family": "mxbai",
      "parameter_size": "335M",
      "quantization": "F16"
    }
  ]
}


═══════════════════════════════════════════════════════════════════
INDEXING ENDPOINTS  
═══════════════════════════════════════════════════════════════════

POST /index/start
─────────────────────────────────────────
Request:
{
  "workspace_path": "/path/to/workspace",
  "project_id": "abc123"
}

Response 202 (Accepted):
{
  "status": "started",
  "project_id": "abc123",
  "message": "Indexing started. Connect to WebSocket for progress."
}

Response 400:
{
  "error": "workspace_path is required"
}

Response 409:
{
  "error": "Indexing already in progress for this project"
}


POST /index/sync
─────────────────────────────────────────
Request:
{
  "workspace_path": "/path/to/workspace",
  "project_id": "abc123"
}

Response 202:
{
  "status": "started",
  "project_id": "abc123"
}


GET /index/status/{project_id}
─────────────────────────────────────────
Response 200 (indexed):
{
  "project_id": "abc123",
  "status": "indexed",
  "last_indexed_at": "2024-01-15T10:30:00Z",
  "stats": {
    "files_count": 234,
    "chunks_count": 1523,
    "languages": ["typescript", "python"]
  }
}

Response 200 (not indexed):
{
  "project_id": "abc123",
  "status": "not-indexed"
}


DELETE /index/{project_id}
─────────────────────────────────────────
Response 200:
{
  "status": "deleted",
  "project_id": "abc123"
}


═══════════════════════════════════════════════════════════════════
RAG QUERY ENDPOINTS
═══════════════════════════════════════════════════════════════════

POST /query
─────────────────────────────────────────
Request:
{
  "project_id": "abc123",
  "query_text": "How does authentication work?",
  "top_k": 5,
  "filters": {
    "file_types": ["typescript"],
    "chunk_types": ["function", "class"]
  }
}

Response 200:
{
  "chunks": [
    {
      "id": "chunk_001",
      "content": "async function authenticateUser(credentials)...",
      "file_path": "src/auth/auth.service.ts",
      "line_start": 15,
      "line_end": 42,
      "chunk_type": "function",
      "symbol_name": "authenticateUser",
      "language": "typescript",
      "score": 0.87
    },
    // ... more chunks
  ],
  "query_time_ms": 45
}


GET /summary/{project_id}
─────────────────────────────────────────
Response 200:
{
  "project_name": "my-app",
  "description": "A React application with Express backend...",
  "main_languages": ["typescript", "javascript"],
  "key_files": [
    "src/App.tsx",
    "src/server/index.ts",
    "src/api/routes.ts"
  ],
  "architecture": "React frontend with Express API backend",
  "frameworks": ["React", "Express", "Redux"],
  "stats": {
    "files_count": 234,
    "chunks_count": 1523,
    "total_lines": 45000
  }
}


═══════════════════════════════════════════════════════════════════
CHAT ENDPOINTS
═══════════════════════════════════════════════════════════════════

POST /chat (non-streaming)
─────────────────────────────────────────
Request:
{
  "project_id": "abc123",
  "messages": [
    {"role": "system", "content": "You are LocalPilot..."},
    {"role": "user", "content": "How does auth work?"}
  ],
  "model": "qwen2.5-coder:7b-instruct-q4_K_M",
  "include_rag": true,
  "rag_top_k": 5
}

Response 200:
{
  "response": "Based on the code, authentication works by...",
  "model": "qwen2.5-coder:7b-instruct-q4_K_M",
  "rag_chunks_used": 5,
  "total_tokens": 1250,
  "duration_ms": 3400
}


═══════════════════════════════════════════════════════════════════
WEBSOCKET ENDPOINTS
═══════════════════════════════════════════════════════════════════

WS /ws/chat
─────────────────────────────────────────
Connect: ws://localhost:52741/ws/chat

Client sends:
{
  "type": "chat",
  "project_id": "abc123",
  "messages": [...],
  "model": "qwen2.5-coder:7b-instruct-q4_K_M",
  "include_rag": true
}

Server sends (streaming):
{"type": "rag_start"}
{"type": "rag_chunk", "chunk": {...}}
{"type": "rag_chunk", "chunk": {...}}
{"type": "rag_complete", "count": 5}
{"type": "token", "content": "Based"}
{"type": "token", "content": " on"}
{"type": "token", "content": " the"}
// ... more tokens
{"type": "done", "total_tokens": 450}

Error:
{"type": "error", "message": "Model not found"}


WS /ws/progress
─────────────────────────────────────────
Connect: ws://localhost:52741/ws/progress?project_id=abc123

Server sends (during indexing):
{"type": "started", "project_id": "abc123"}
{"type": "progress", "phase": "scanning", "current": 50, "total": 234}
{"type": "progress", "phase": "parsing", "current": 100, "total": 234, "file": "src/auth.ts"}
{"type": "progress", "phase": "embedding", "current": 150, "total": 234}
{"type": "progress", "phase": "storing", "current": 200, "total": 234}
{"type": "completed", "result": {"files_indexed": 234, "chunks_created": 1523}}

Or:
{"type": "error", "message": "Failed to parse file: src/bad.ts"}

└─────────────────────────────────────────────────────────────────┘
```

## 9. State Management

### 9.1 Zustand Store Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    STATE MANAGEMENT OVERVIEW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WHY ZUSTAND?                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Lightweight (~1KB)                                            │
│  • Simple API, minimal boilerplate                              │
│  • No providers needed                                           │
│  • Built-in TypeScript support                                  │
│  • Works great with React                                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  STORE STRUCTURE:                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      ROOT STATE                          │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │  appStore   │  │  chatStore  │  │  planStore  │      │   │
│  │  │             │  │             │  │             │      │   │
│  │  │ • mode      │  │ • messages  │  │ • plan      │      │   │
│  │  │ • project   │  │ • isLoading │  │ • isLoading │      │   │
│  │  │ • ollama    │  │ • error     │  │ • error     │      │   │
│  │  │   Status    │  │             │  │             │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────────────────────────┐   │   │
│  │  │  actStore   │  │         settingsStore           │   │   │
│  │  │             │  │                                  │   │   │
│  │  │ • plan      │  │ • ollamaUrl    • chatModel      │   │   │
│  │  │ • current   │  │ • embedModel   • temperature    │   │   │
│  │  │   Task      │  │ • ragTopK      • autoApprove    │   │   │
│  │  │ • status    │  │                                  │   │   │
│  │  └─────────────┘  └─────────────────────────────────┘   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Store Implementations

```typescript
// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/ui/webview/store/app.store.ts
// ═══════════════════════════════════════════════════════════════

import { create } from 'zustand';

type AppMode = 'onboarding' | 'chat' | 'plan' | 'act';
type OllamaStatus = 'checking' | 'connected' | 'disconnected' | 'error';
type IndexStatus = 'not-indexed' | 'indexing' | 'indexed' | 'sync-required';

interface AppState {
  // Current mode
  mode: AppMode;
  
  // Project info
  projectId: string | null;
  projectName: string | null;
  workspacePath: string | null;
  
  // Ollama connection
  ollamaStatus: OllamaStatus;
  ollamaError: string | null;
  availableModels: string[];
  
  // Indexing
  indexStatus: IndexStatus;
  indexProgress: number;
  indexMessage: string | null;
  
  // Actions
  setMode: (mode: AppMode) => void;
  setProject: (id: string, name: string, path: string) => void;
  setOllamaStatus: (status: OllamaStatus, error?: string) => void;
  setModels: (models: string[]) => void;
  setIndexStatus: (status: IndexStatus) => void;
  setIndexProgress: (progress: number, message?: string) => void;
  reset: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  mode: 'onboarding',
  projectId: null,
  projectName: null,
  workspacePath: null,
  ollamaStatus: 'checking',
  ollamaError: null,
  availableModels: [],
  indexStatus: 'not-indexed',
  indexProgress: 0,
  indexMessage: null,
  
  // Actions
  setMode: (mode) => set({ mode }),
  
  setProject: (id, name, path) => set({
    projectId: id,
    projectName: name,
    workspacePath: path
  }),
  
  setOllamaStatus: (status, error) => set({
    ollamaStatus: status,
    ollamaError: error || null
  }),
  
  setModels: (models) => set({ availableModels: models }),
  
  setIndexStatus: (status) => set({ indexStatus: status }),
  
  setIndexProgress: (progress, message) => set({
    indexProgress: progress,
    indexMessage: message || null
  }),
  
  reset: () => set({
    mode: 'onboarding',
    indexStatus: 'not-indexed',
    indexProgress: 0
  })
}));


// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/ui/webview/store/chat.store.ts
// ═══════════════════════════════════════════════════════════════

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  isStreaming: boolean;
  error: string | null;
  ragChunks: RetrievedChunk[];
  
  // Actions
  addMessage: (message: Message) => void;
  updateLastMessage: (content: string) => void;
  appendToLastMessage: (token: string) => void;
  setLoading: (loading: boolean) => void;
  setStreaming: (streaming: boolean) => void;
  setError: (error: string | null) => void;
  setRagChunks: (chunks: RetrievedChunk[]) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,
  isStreaming: false,
  error: null,
  ragChunks: [],
  
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message]
  })),
  
  updateLastMessage: (content) => set((state) => {
    const messages = [...state.messages];
    if (messages.length > 0) {
      messages[messages.length - 1].content = content;
    }
    return { messages };
  }),
  
  appendToLastMessage: (token) => set((state) => {
    const messages = [...state.messages];
    if (messages.length > 0) {
      messages[messages.length - 1].content += token;
    }
    return { messages };
  }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  setStreaming: (streaming) => set({ isStreaming: streaming }),
  setError: (error) => set({ error }),
  setRagChunks: (chunks) => set({ ragChunks: chunks }),
  clearMessages: () => set({ messages: [], ragChunks: [] })
}));


// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/ui/webview/store/plan.store.ts
// ═══════════════════════════════════════════════════════════════

interface PlanState {
  plan: Plan | null;
  isGenerating: boolean;
  error: string | null;
  
  // Actions
  setPlan: (plan: Plan) => void;
  updateTask: (taskId: string, updates: Partial<Task>) => void;
  setGenerating: (generating: boolean) => void;
  setError: (error: string | null) => void;
  clearPlan: () => void;
}

export const usePlanStore = create<PlanState>((set) => ({
  plan: null,
  isGenerating: false,
  error: null,
  
  setPlan: (plan) => set({ plan, error: null }),
  
  updateTask: (taskId, updates) => set((state) => {
    if (!state.plan) return state;
    
    const tasks = state.plan.tasks.map((task) =>
      task.id === taskId ? { ...task, ...updates } : task
    );
    
    return { plan: { ...state.plan, tasks } };
  }),
  
  setGenerating: (generating) => set({ isGenerating: generating }),
  setError: (error) => set({ error }),
  clearPlan: () => set({ plan: null, error: null })
}));


// ═══════════════════════════════════════════════════════════════
// FILE: extension/src/ui/webview/store/act.store.ts
// ═══════════════════════════════════════════════════════════════

type ExecutionStatus = 'idle' | 'running' | 'paused' | 'completed' | 'error';

interface ActState {
  plan: Plan | null;
  status: ExecutionStatus;
  currentTaskIndex: number;
  currentTaskCode: string | null;
  currentTaskDiff: string | null;
  error: string | null;
  
  // Actions
  startExecution: (plan: Plan) => void;
  setCurrentTask: (index: number) => void;
  setTaskCode: (code: string, diff?: string) => void;
  updateTaskStatus: (taskId: string, status: TaskStatus) => void;
  setStatus: (status: ExecutionStatus) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export const useActStore = create<ActState>((set) => ({
  plan: null,
  status: 'idle',
  currentTaskIndex: -1,
  currentTaskCode: null,
  currentTaskDiff: null,
  error: null,
  
  startExecution: (plan) => set({
    plan,
    status: 'running',
    currentTaskIndex: 0,
    error: null
  }),
  
  setCurrentTask: (index) => set({
    currentTaskIndex: index,
    currentTaskCode: null,
    currentTaskDiff: null
  }),
  
  setTaskCode: (code, diff) => set({
    currentTaskCode: code,
    currentTaskDiff: diff || null
  }),
  
  updateTaskStatus: (taskId, status) => set((state) => {
    if (!state.plan) return state;
    
    const tasks = state.plan.tasks.map((task) =>
      task.id === taskId ? { ...task, status } : task
    );
    
    return { plan: { ...state.plan, tasks } };
  }),
  
  setStatus: (status) => set({ status }),
  setError: (error) => set({ error, status: 'error' }),
  reset: () => set({
    plan: null,
    status: 'idle',
    currentTaskIndex: -1,
    currentTaskCode: null,
    currentTaskDiff: null,
    error: null
  })
}));
```

### 9.3 State Flow Between Modes

```
┌─────────────────────────────────────────────────────────────────┐
│                  STATE FLOW BETWEEN MODES                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ONBOARDING → CHAT                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Trigger: Indexing completes successfully                       │
│                                                                  │
│  State Changes:                                                  │
│  • appStore.mode = 'chat'                                       │
│  • appStore.indexStatus = 'indexed'                             │
│  • chatStore.addMessage(projectSummary)                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CHAT → PLAN                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Trigger: User clicks "Transfer to Plan"                        │
│                                                                  │
│  State Changes:                                                  │
│  • planStore.setGenerating(true)                                │
│  • [Generate plan from conversation]                            │
│  • planStore.setPlan(generatedPlan)                             │
│  • planStore.setGenerating(false)                               │
│  • appStore.mode = 'plan'                                       │
│                                                                  │
│  Data Transferred:                                               │
│  • chatStore.messages → Used for context                        │
│  • chatStore.ragChunks → Used for project understanding         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PLAN → ACT                                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Trigger: User clicks "Approve & Execute"                       │
│                                                                  │
│  State Changes:                                                  │
│  • planStore.plan.status = 'approved'                           │
│  • actStore.startExecution(planStore.plan)                      │
│  • appStore.mode = 'act'                                        │
│                                                                  │
│  Data Transferred:                                               │
│  • planStore.plan → actStore.plan (deep copy)                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ACT → CHAT (after completion)                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Trigger: Execution completes or user returns                   │
│                                                                  │
│  State Changes:                                                  │
│  • chatStore.addMessage(executionSummary)                       │
│  • actStore.reset()                                              │
│  • planStore.clearPlan()                                        │
│  • appStore.mode = 'chat'                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Error Handling Strategy

### 10.1 Error Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                     ERROR CATEGORIES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CATEGORY 1: CONNECTION ERRORS                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Source: Ollama or Python server unreachable                    │
│  Severity: Critical                                              │
│  Recovery: Retry with backoff, show reconnect option            │
│                                                                  │
│  Examples:                                                       │
│  • OllamaConnectionError - Ollama not running                   │
│  • ServerConnectionError - Python server not running            │
│  • TimeoutError - Request timed out                             │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CATEGORY 2: INDEXING ERRORS                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Source: File parsing, embedding, or storage failures           │
│  Severity: Medium (can skip problematic files)                  │
│  Recovery: Skip file, continue indexing, report at end          │
│                                                                  │
│  Examples:                                                       │
│  • ParseError - Tree-sitter failed to parse file               │
│  • EmbeddingError - Ollama failed to embed text                │
│  • StorageError - ChromaDB write failed                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CATEGORY 3: LLM ERRORS                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Source: Model not found, context overflow, generation fail     │
│  Severity: Medium                                                │
│  Recovery: Retry, suggest different model, truncate context     │
│                                                                  │
│  Examples:                                                       │
│  • ModelNotFoundError - Requested model not in Ollama          │
│  • ContextOverflowError - Input too long for model             │
│  • GenerationError - Model failed to generate response         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CATEGORY 4: FILE OPERATION ERRORS                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Source: File read/write failures                               │
│  Severity: High (can corrupt user files)                        │
│  Recovery: Restore from backup, abort task                      │
│                                                                  │
│  Examples:                                                       │
│  • FileNotFoundError - File doesn't exist                       │
│  • PermissionError - No write access                            │
│  • DirectoryNotEmptyError - Cannot delete                       │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CATEGORY 5: VALIDATION ERRORS                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Source: Invalid input, malformed data                          │
│  Severity: Low                                                   │
│  Recovery: Show validation message, request correction          │
│                                                                  │
│  Examples:                                                       │
│  • InvalidPathError - Path outside workspace                    │
│  • PlanParseError - Cannot parse LLM output to plan            │
│  • InvalidSettingError - Setting value out of range            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 Error Class Hierarchy

```typescript
// FILE: extension/src/core/errors/base.error.ts

export abstract class LocalPilotError extends Error {
  abstract readonly code: string;
  abstract readonly category: ErrorCategory;
  abstract readonly recoverable: boolean;
  
  constructor(
    message: string,
    public readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
  }
  
  toJSON() {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      category: this.category,
      recoverable: this.recoverable,
      details: this.details
    };
  }
}

export type ErrorCategory = 
  | 'connection'
  | 'indexing'
  | 'llm'
  | 'file'
  | 'validation';


// FILE: extension/src/core/errors/ollama.error.ts

export class OllamaConnectionError extends LocalPilotError {
  readonly code = 'OLLAMA_CONNECTION_FAILED';
  readonly category = 'connection' as const;
  readonly recoverable = true;
  
  constructor(url: string, cause?: Error) {
    super(`Cannot connect to Ollama at ${url}`, { url, cause: cause?.message });
  }
}

export class OllamaModelNotFoundError extends LocalPilotError {
  readonly code = 'OLLAMA_MODEL_NOT_FOUND';
  readonly category = 'llm' as const;
  readonly recoverable = true;
  
  constructor(model: string) {
    super(`Model "${model}" not found in Ollama`, { model });
  }
}


// FILE: extension/src/core/errors/indexing.error.ts

export class IndexingError extends LocalPilotError {
  readonly code = 'INDEXING_FAILED';
  readonly category = 'indexing' as const;
  readonly recoverable = true;
  
  constructor(message: string, public readonly failedFiles: string[]) {
    super(message, { failedFiles });
  }
}

export class ParseError extends LocalPilotError {
  readonly code = 'PARSE_FAILED';
  readonly category = 'indexing' as const;
  readonly recoverable = true;
  
  constructor(filePath: string, reason: string) {
    super(`Failed to parse ${filePath}: ${reason}`, { filePath, reason });
  }
}


// FILE: extension/src/core/errors/file-operation.error.ts

export class FileOperationError extends LocalPilotError {
  readonly code = 'FILE_OPERATION_FAILED';
  readonly category = 'file' as const;
  readonly recoverable = false;
  
  constructor(
    operation: 'read' | 'write' | 'delete',
    filePath: string,
    reason: string
  ) {
    super(`Failed to ${operation} file ${filePath}: ${reason}`, {
      operation,
      filePath,
      reason
    });
  }
}
```

### 10.3 Error Handling Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                   ERROR HANDLING PATTERNS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PATTERN 1: Retry with Exponential Backoff                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Used for: Connection errors, transient failures               │
│                                                                  │
│  async function withRetry<T>(                                    │
│    fn: () => Promise<T>,                                         │
│    maxAttempts = 3,                                              │
│    baseDelay = 1000                                              │
│  ): Promise<T> {                                                 │
│    for (let attempt = 1; attempt <= maxAttempts; attempt++) {   │
│      try {                                                       │
│        return await fn();                                        │
│      } catch (error) {                                           │
│        if (attempt === maxAttempts) throw error;                │
│        const delay = baseDelay * Math.pow(2, attempt - 1);      │
│        await sleep(delay);                                       │
│      }                                                           │
│    }                                                             │
│  }                                                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PATTERN 2: Graceful Degradation                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Used for: Indexing (skip bad files, continue)                  │
│                                                                  │
│  async function indexWithGracefulDegradation(files: string[]) { │
│    const results = { success: [], failed: [] };                 │
│                                                                  │
│    for (const file of files) {                                   │
│      try {                                                       │
│        await indexFile(file);                                    │
│        results.success.push(file);                               │
│      } catch (error) {                                           │
│        logger.warn(`Skipping ${file}: ${error.message}`);       │
│        results.failed.push({ file, error: error.message });     │
│      }                                                           │
│    }                                                             │
│                                                                  │
│    if (results.failed.length > 0) {                             │
│      showWarning(`${results.failed.length} files skipped`);     │
│    }                                                             │
│                                                                  │
│    return results;                                               │
│  }                                                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PATTERN 3: User-Facing Error Messages                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Used for: All errors shown to user                             │
│                                                                  │
│  function getUserMessage(error: LocalPilotError): string {      │
│    const messages: Record<string, string> = {                   │
│      OLLAMA_CONNECTION_FAILED:                                   │
│        'Cannot connect to Ollama. Make sure Ollama is running.',│
│      OLLAMA_MODEL_NOT_FOUND:                                     │
│        'Model not found. Run "ollama pull <model>" to install.',│
│      FILE_OPERATION_FAILED:                                      │
│        'File operation failed. Check file permissions.',        │
│    };                                                            │
│                                                                  │
│    return messages[error.code] || error.message;                │
│  }                                                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PATTERN 4: Backup Before Modify                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Used for: Act mode file modifications                          │
│                                                                  │
│  async function safeModifyFile(                                  │
│    filePath: string,                                             │
│    newContent: string                                            │
│  ): Promise<void> {                                              │
│    // 1. Create backup                                           │
│    const backupPath = await fileSystem.backup(filePath);        │
│                                                                  │
│    try {                                                         │
│      // 2. Write new content                                     │
│      await fileSystem.writeFile(filePath, newContent);          │
│    } catch (error) {                                             │
│      // 3. Restore from backup on failure                       │
│      await fileSystem.restore(backupPath, filePath);            │
│      throw new FileOperationError('write', filePath, error.msg);│
│    }                                                             │
│  }                                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. Security Considerations

```
┌─────────────────────────────────────────────────────────────────┐
│                  SECURITY CONSIDERATIONS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRINCIPLE 1: LOCALHOST ONLY                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  All network communication stays on localhost:                  │
│  • Python server: 127.0.0.1:52741                               │
│  • Ollama: 127.0.0.1:11434                                      │
│  • No external network calls                                     │
│  • No telemetry or analytics                                     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PRINCIPLE 2: WORKSPACE SANDBOXING                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  File operations are restricted to workspace:                   │
│                                                                  │
│  function validatePath(filePath: string): boolean {             │
│    const workspaceRoot = getWorkspaceRoot();                    │
│    const absolutePath = path.resolve(workspaceRoot, filePath);  │
│                                                                  │
│    // Ensure path is within workspace                           │
│    if (!absolutePath.startsWith(workspaceRoot)) {               │
│      throw new SecurityError('Path outside workspace');          │
│    }                                                             │
│                                                                  │
│    // Block sensitive files                                      │
│    const blocked = ['.env', '.git/config', 'secrets'];          │
│    for (const pattern of blocked) {                             │
│      if (absolutePath.includes(pattern)) {                      │
│        throw new SecurityError('Access to sensitive file');      │
│      }                                                           │
│    }                                                             │
│                                                                  │
│    return true;                                                  │
│  }                                                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PRINCIPLE 3: USER APPROVAL FOR ACTIONS                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Act mode requires explicit approval:                           │
│  • Every file change shown before applying                      │
│  • User must click "Apply" for each task                        │
│  • "Skip" option always available                                │
│  • No silent file modifications                                  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PRINCIPLE 4: BACKUP BEFORE MODIFY                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  All file modifications are reversible:                         │
│  • Backup created in .localpilot/backups/                       │
│  • Timestamped backup folders                                    │
│  • Backup includes original content                              │
│  • Restore mechanism available                                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PRINCIPLE 5: NO CODE EXECUTION (MVP)                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  MVP does not execute arbitrary code:                           │
│  • No terminal command execution                                 │
│  • No script running                                             │
│  • Only file create/modify/delete operations                    │
│  • Terminal support added in v1.1 with additional safeguards    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PRINCIPLE 6: DATA STAYS LOCAL                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  User data never leaves the machine:                            │
│  • Index stored in ~/.localpilot/                               │
│  • No cloud sync                                                 │
│  • No external API calls                                         │
│  • All processing via local Ollama                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   DEPLOYMENT ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  COMPONENT LIFECYCLE:                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  1. USER STARTS VS CODE                                          │
│     │                                                            │
│     ▼                                                            │
│  2. EXTENSION ACTIVATES                                          │
│     • Checks for Python server                                   │
│     • Starts Python server if not running                       │
│     • Checks Ollama connection                                   │
│     │                                                            │
│     ▼                                                            │
│  3. PYTHON SERVER STARTS                                         │
│     • Binds to localhost:52741                                   │
│     • Initializes ChromaDB                                       │
│     • Connects to Ollama                                         │
│     │                                                            │
│     ▼                                                            │
│  4. READY FOR USE                                                │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PYTHON SERVER MANAGEMENT:                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Option A: Bundled Python (Recommended for MVP)                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  extension/                                              │   │
│  │  └── bundled/                                            │   │
│  │      └── server/           ← Python server included      │   │
│  │          ├── src/                                        │   │
│  │          ├── requirements.txt                            │   │
│  │          └── run.py                                       │   │
│  │                                                          │   │
│  │  Extension starts server:                                │   │
│  │  spawn('python', ['run.py'], { cwd: bundledPath })       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Option B: System Python (Alternative)                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  • User installs server separately via pip              │   │
│  │  • pip install localpilot-server                         │   │
│  │  • Extension connects to running server                  │   │
│  │  • More flexible but more setup                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FILE LOCATIONS:                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Windows:                                                        │
│  • Extension: %USERPROFILE%\.vscode\extensions\localpilot\      │
│  • User data: %USERPROFILE%\.localpilot\                        │
│  • Indexes: %USERPROFILE%\.localpilot\indexes\                  │
│  • Logs: %USERPROFILE%\.localpilot\logs\                        │
│                                                                  │
│  macOS/Linux (Future):                                           │
│  • Extension: ~/.vscode/extensions/localpilot/                  │
│  • User data: ~/.localpilot/                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 13. WebView Communication Protocol

```md
Reference WEBVIEW_PROTOCOL.md
```

---

## 14. Architecture Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                   ARCHITECTURE SUMMARY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  KEY DECISIONS:                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ✓ Practical Clean Architecture                                 │
│    └── Testable, maintainable, junior-friendly                  │
│                                                                  │
│  ✓ Hybrid TypeScript + Python                                   │
│    └── Best tools for each job                                  │
│                                                                  │
│  ✓ HTTP + WebSocket communication                               │
│    └── REST for operations, WS for streaming                    │
│                                                                  │
│  ✓ Zustand for state management                                 │
│    └── Simple, lightweight, React-friendly                      │
│                                                                  │
│  ✓ LlamaIndex for RAG                                           │
│    └── Built for code indexing, simpler than LangChain          │
│                                                                  │
│  ✓ ChromaDB for vectors                                         │
│    └── Easy setup, Python native, good for MVP                  │
│                                                                  │
│  ✓ AST-aware indexing with Tree-sitter                          │
│    └── Quality over simplicity (your requirement)               │
│                                                                  │
│  ✓ Privacy-first with localhost-only communication              │
│    └── Core value proposition                                    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Document Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | TarekRefaei | | |

---

*Document Version: 1.0.0*
*Created: Planning Phase*
*Last Updated: [Current Date]*
````

</details>


## docs/ProjectDocuments/commit-convention.md

*Size: 1,868 bytes | Modified: 2025-12-14T22:02:31.951Z*

<details>
<summary>View code</summary>

````markdown
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

````

</details>


## docs/ProjectDocuments/development-setup.md

*Size: 33,296 bytes | Modified: 2025-12-13T07:44:14.580Z*

<details>
<summary>View code</summary>

````markdown
# 📄 DEVELOPMENT_SETUP.md

# LocalPilot - Development Environment Setup

> Step-by-step guide to set up your LocalPilot development environment

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Development Setup Guide |
| **Platform** | Windows (MVP) |
| **Last Updated** | [Current Date] |

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install Required Software](#2-install-required-software)
3. [Repository Setup](#3-repository-setup)
4. [Extension Setup (TypeScript)](#4-extension-setup-typescript)
5. [Server Setup (Python)](#5-server-setup-python)
6. [Ollama Configuration](#6-ollama-configuration)
7. [VS Code Development Setup](#7-vs-code-development-setup)
8. [Running the Project](#8-running-the-project)
9. [Verification Checklist](#9-verification-checklist)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Software Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    REQUIRED SOFTWARE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Software          Version        Purpose                        │
│  ─────────────────────────────────────────────────────────────  │
│  Node.js           18.x or 20.x   Extension runtime             │
│  pnpm              8.x+           Package manager               │
│  Python            3.11+          RAG server                    │
│  uv                Latest         Python package manager         │
│  Git               Latest         Version control               │
│  VS Code           1.85+          IDE & extension host          │
│  Ollama            Latest         Local LLM provider            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Your System

Based on your specs:
- **OS:** Windows 11
- **RAM:** 16GB ✓ (sufficient)
- **GPU:** RTX 4060 ✓ (excellent for Ollama)
- **CPU:** AMD Ryzen 7 8845HS ✓

---

## 2. Install Required Software

### 2.1 Install Node.js

```powershell
# Option A: Download installer from nodejs.org
# https://nodejs.org/en/download/ (LTS version 20.x)

# Option B: Using winget
winget install OpenJS.NodeJS.LTS

# Verify installation
node --version   # Should show v20.x.x
npm --version    # Should show 10.x.x
```

### 2.2 Install pnpm

```powershell
# Install pnpm globally
npm install -g pnpm

# Verify installation
pnpm --version   # Should show 8.x.x or 9.x.x
```

### 2.3 Install Python 3.11+

```powershell
# Option A: Download from python.org
# https://www.python.org/downloads/ (3.11 or 3.12)
# ⚠️ CHECK "Add Python to PATH" during installation!

# Option B: Using winget
winget install Python.Python.3.11

# Verify installation
python --version   # Should show Python 3.11.x or 3.12.x
pip --version      # Should show pip 23.x or 24.x
```

### 2.4 Install uv (Python Package Manager)

```powershell
# Install uv
pip install uv

# Verify installation
uv --version   # Should show uv 0.x.x
```

### 2.5 Install Git

```powershell
# Using winget
winget install Git.Git

# Verify installation
git --version   # Should show git version 2.x.x

# Configure Git (if not already done)
git config --global user.name "TarekRefaei"
git config --global user.email "your-email@example.com"
```

### 2.6 Install VS Code

```powershell
# Using winget
winget install Microsoft.VisualStudioCode

# Or download from: https://code.visualstudio.com/
```

### 2.7 Install Ollama

```powershell
# Download from: https://ollama.com/download/windows

# After installation, Ollama runs as a service
# Verify it's running:
curl http://localhost:11434/api/version

# Or in browser: http://localhost:11434
```

---

## 3. Repository Setup

### 3.1 Create Repository

```powershell
# Navigate to your projects directory
cd C:\Projects  # or your preferred location

# Create project directory
mkdir LocalPilot
cd LocalPilot

# Initialize Git repository
git init

# Create initial structure
mkdir extension
mkdir server
mkdir docs
mkdir scripts
mkdir .vscode
```

### 3.2 Create Root Configuration Files

#### .gitignore

```powershell
# Create .gitignore
New-Item -Path ".gitignore" -ItemType File
```

Add this content to `.gitignore`:

```gitignore
# Node
node_modules/
*.vsix
dist/
out/

# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
*.egg-info/

# IDE
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
server/data/
.localpilot/
*.log

# Environment
.env
.env.local

# Build
*.tsbuildinfo
```

#### .editorconfig

```editorconfig
# .editorconfig
root = true

[*]
indent_style = space
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{ts,tsx,js,jsx,json}]
indent_size = 2

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
```

### 3.3 Initial Commit

```powershell
git add .
git commit -m "chore: initial project structure"
```

---

## 4. Extension Setup (TypeScript)

### 4.1 Initialize Extension Package

```powershell
cd extension

# Initialize package.json
pnpm init
```

### 4.2 Create package.json

Replace the generated `package.json` with:

```json
{
  "name": "localpilot",
  "displayName": "LocalPilot",
  "description": "Privacy-First AI Pair Programming",
  "version": "0.1.0",
  "publisher": "TarekRefaei",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Other"],
  "activationEvents": [],
  "main": "./dist/extension.js",
  "contributes": {
    "viewsContainers": {
      "activitybar": [
        {
          "id": "localpilot",
          "title": "LocalPilot",
          "icon": "resources/icons/icon.svg"
        }
      ]
    },
    "views": {
      "localpilot": [
        {
          "type": "webview",
          "id": "localpilot.mainView",
          "name": "LocalPilot"
        }
      ]
    },
    "commands": [
      {
        "command": "localpilot.startIndexing",
        "title": "LocalPilot: Start Indexing"
      },
      {
        "command": "localpilot.syncIndex",
        "title": "LocalPilot: Sync Index"
      }
    ],
    "configuration": {
      "title": "LocalPilot",
      "properties": {
        "localpilot.ollamaUrl": {
          "type": "string",
          "default": "http://localhost:11434",
          "description": "Ollama server URL"
        },
        "localpilot.chatModel": {
          "type": "string",
          "default": "qwen2.5-coder:7b-instruct-q4_K_M",
          "description": "Model for chat"
        },
        "localpilot.embeddingModel": {
          "type": "string",
          "default": "mxbai-embed-large:latest",
          "description": "Model for embeddings"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "pnpm run build",
    "build": "node esbuild.js --production",
    "watch": "node esbuild.js --watch",
    "lint": "eslint src --ext ts,tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@types/vscode": "^1.85.0",
    "@typescript-eslint/eslint-plugin": "^6.13.0",
    "@typescript-eslint/parser": "^6.13.0",
    "esbuild": "^0.19.8",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0",
    "typescript": "^5.3.2",
    "vitest": "^1.0.0"
  },
  "dependencies": {
    "ws": "^8.14.2"
  }
}
```

### 4.3 Install Extension Dependencies

```powershell
# Install all dependencies
pnpm install

# Install React and related packages
pnpm add react react-dom zustand
pnpm add -D @types/react @types/react-dom

# Install Tailwind CSS
pnpm add -D tailwindcss postcss autoprefixer
```

### 4.4 Create TypeScript Configuration

Create `extension/tsconfig.json`:

```json
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2022",
    "lib": ["ES2022", "DOM"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "baseUrl": "./src",
    "paths": {
      "@core/*": ["core/*"],
      "@features/*": ["features/*"],
      "@infrastructure/*": ["infrastructure/*"],
      "@ui/*": ["ui/*"],
      "@utils/*": ["utils/*"]
    },
    "jsx": "react-jsx"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 4.5 Create esbuild Configuration

Create `extension/esbuild.js`:

```javascript
const esbuild = require('esbuild');

const production = process.argv.includes('--production');
const watch = process.argv.includes('--watch');

async function main() {
  const ctx = await esbuild.context({
    entryPoints: ['src/extension.ts'],
    bundle: true,
    format: 'cjs',
    minify: production,
    sourcemap: !production,
    sourcesContent: false,
    platform: 'node',
    outfile: 'dist/extension.js',
    external: ['vscode'],
    logLevel: 'info',
  });

  if (watch) {
    await ctx.watch();
    console.log('Watching for changes...');
  } else {
    await ctx.rebuild();
    await ctx.dispose();
  }
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
```

### 4.6 Create Entry Point

Create `extension/src/extension.ts`:

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot is now active!');

  // Register a simple command to verify extension works
  const disposable = vscode.commands.registerCommand(
    'localpilot.helloWorld',
    () => {
      vscode.window.showInformationMessage('Hello from LocalPilot!');
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {
  console.log('LocalPilot deactivated');
}
```

### 4.7 Verify Extension Setup

```powershell
# Build the extension
pnpm run build

# Should create dist/extension.js without errors
```

---

## 5. Server Setup (Python)

### 5.1 Navigate to Server Directory

```powershell
cd ../server  # From extension directory
# Or: cd C:\Projects\LocalPilot\server
```

### 5.2 Create Virtual Environment

```powershell
# Create virtual environment using uv
uv venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Your prompt should now show (.venv)
```

### 5.3 Create pyproject.toml

Create `server/pyproject.toml`:

```toml
[project]
name = "localpilot-server"
version = "0.1.0"
description = "LocalPilot RAG Server"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "websockets>=12.0",
    "chromadb>=0.4.18",
    "llama-index>=0.9.0",
    "tree-sitter>=0.20.4",
    "httpx>=0.25.2",
    "pydantic>=2.5.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "ruff>=0.1.6",
    "mypy>=1.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### 5.4 Install Python Dependencies

```powershell
# Install dependencies using uv
uv pip install -e ".[dev]"

# This installs:
# - FastAPI (web framework)
# - ChromaDB (vector database)
# - LlamaIndex (RAG framework)
# - Tree-sitter (code parsing)
# - And dev tools (pytest, ruff, mypy)
```

### 5.5 Install Tree-sitter Language Parsers

```powershell
# Install language parsers
uv pip install tree-sitter-python tree-sitter-javascript tree-sitter-typescript
```

**Note:** Dart parser may need to be built from source. For MVP, we'll add it later.

### 5.6 Create Server Entry Point

Create `server/src/__init__.py`:

```python
"""LocalPilot RAG Server"""
```

Create `server/src/main.py`:

```python
"""
LocalPilot RAG Server - Main Entry Point

This is the FastAPI application that handles:
- Workspace indexing
- RAG queries
- Chat with streaming
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="LocalPilot RAG Server",
    description="Local RAG server for LocalPilot VS Code extension",
    version="0.1.0"
)

# Allow connections from VS Code extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # VS Code extension
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }


@app.get("/api/models")
async def list_models():
    """List available Ollama models (placeholder)"""
    return {
        "models": []
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=52741,
        reload=True
    )
```

### 5.7 Verify Server Setup

```powershell
# Make sure virtual environment is activated
# (.venv) should show in prompt

# Run the server
cd src
python main.py

# Should show:
# INFO:     Uvicorn running on http://127.0.0.1:52741
# INFO:     Started reloader process

# Test in another terminal:
curl http://localhost:52741/health

# Should return: {"status":"healthy","version":"0.1.0"}

# Press Ctrl+C to stop server
```

---

## 6. Ollama Configuration

### 6.1 Verify Ollama is Running

```powershell
# Check Ollama status
curl http://localhost:11434/api/version

# Should return something like:
# {"version":"0.1.x"}
```

### 6.2 Pull Required Models

```powershell
# Pull embedding model (required for RAG)
ollama pull mxbai-embed-large

# Pull chat model (for conversations)
# You already have these based on your earlier message:
# - qwen2.5-coder:7b-instruct-q4_K_M
# - qwen2.5-coder:14b-instruct-q4_K_M

# If not, pull them:
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
```

### 6.3 Verify Models

```powershell
# List installed models
ollama list

# Expected output (your models):
# NAME                                    SIZE
# qwen2.5-coder:7b-instruct-q4_K_M       4.7 GB
# qwen2.5-coder:14b-instruct-q4_K_M      9.0 GB
# mxbai-embed-large:latest               670 MB
# bge-m3:latest                          1.2 GB
# jina/jina-embeddings-v2-base-en        547 MB
```

### 6.4 Test Ollama

```powershell
# Test chat completion
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:7b-instruct-q4_K_M",
  "prompt": "Write hello world in Python",
  "stream": false
}'

# Test embedding
curl http://localhost:11434/api/embeddings -d '{
  "model": "mxbai-embed-large",
  "prompt": "Hello world"
}'
```

---

## 7. VS Code Development Setup

### 7.1 Install Recommended Extensions

Create `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "eamodio.gitlens"
  ]
}
```

### 7.2 Create VS Code Settings

Create `.vscode/settings.json`:

```json
{
  // Editor settings
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },

  // TypeScript
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },

  // Python
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "python.defaultInterpreterPath": "${workspaceFolder}/server/.venv/Scripts/python.exe",

  // Files
  "files.exclude": {
    "**/__pycache__": true,
    "**/node_modules": true,
    "**/.git": true
  },

  // Search
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.venv": true
  }
}
```

### 7.3 Create Launch Configurations

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}/extension"
      ],
      "outFiles": [
        "${workspaceFolder}/extension/dist/**/*.js"
      ],
      "preLaunchTask": "npm: watch"
    },
    {
      "name": "Run Python Server",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/server/src/main.py",
      "cwd": "${workspaceFolder}/server/src",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/server/src"
      }
    }
  ],
  "compounds": [
    {
      "name": "Full Stack",
      "configurations": ["Run Python Server", "Run Extension"]
    }
  ]
}
```

### 7.4 Create Tasks

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "npm",
      "script": "watch",
      "path": "extension",
      "problemMatcher": "$esbuild-watch",
      "isBackground": true,
      "presentation": {
        "reveal": "silent"
      },
      "label": "npm: watch"
    },
    {
      "type": "npm",
      "script": "build",
      "path": "extension",
      "group": "build",
      "label": "npm: build extension"
    },
    {
      "label": "Start Python Server",
      "type": "shell",
      "command": "${workspaceFolder}/server/.venv/Scripts/python.exe",
      "args": ["${workspaceFolder}/server/src/main.py"],
      "isBackground": true,
      "problemMatcher": []
    }
  ]
}
```

---

## 8. Running the Project

### 8.1 Development Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT WORKFLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TERMINAL 1: Python Server                                       │
│  ─────────────────────────────────────────────────────────────  │
│  cd server                                                       │
│  .venv\Scripts\activate                                          │
│  cd src                                                          │
│  python main.py                                                  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  TERMINAL 2: Extension Watch Mode                                │
│  ─────────────────────────────────────────────────────────────  │
│  cd extension                                                    │
│  pnpm run watch                                                  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  VS CODE: Debug Extension                                        │
│  ─────────────────────────────────────────────────────────────  │
│  Press F5 (with "Run Extension" selected)                       │
│  A new VS Code window opens with extension loaded                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Quick Start Commands

```powershell
# From project root (C:\Projects\LocalPilot)

# Terminal 1: Start Python server
cd server
.venv\Scripts\activate
cd src
python main.py

# Terminal 2: Watch extension (new terminal)
cd extension
pnpm run watch

# Terminal 3: Test extension (or press F5 in VS Code)
# Opens new VS Code window with extension
```
---

### 8.3 Starting the Python Server

Use the provided script to start the server:

```powershell
# From project root
.\scripts\start-server.ps1

# Or with auto-reload for development
.\scripts\start-server.ps1 -Dev
```

The script will:
1. Check virtual environment exists
2. Verify port 52741 is available
3. Check Ollama connection (warning if not running)
4. Start the FastAPI server

**Manual Start (Alternative):**
```powershell
cd server
.venv\Scripts\activate
cd src
python -m uvicorn api.main:app --host 127.0.0.1 --port 52741 --reload
```

---

## 9. Verification Checklist

Run through this checklist to ensure everything is set up correctly:

```
┌─────────────────────────────────────────────────────────────────┐
│                   VERIFICATION CHECKLIST                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SOFTWARE VERSIONS                                               │
│  ─────────────────────────────────────────────────────────────  │
│  □ node --version          → v20.x.x                            │
│  □ pnpm --version          → 8.x.x or 9.x.x                     │
│  □ python --version        → 3.11.x or 3.12.x                   │
│  □ uv --version            → 0.x.x                              │
│  □ git --version           → 2.x.x                              │
│  □ code --version          → 1.85.x+                            │
│                                                                  │
│  OLLAMA                                                          │
│  ─────────────────────────────────────────────────────────────  │
│  □ Ollama running          → http://localhost:11434 responds    │
│  □ Embedding model         → mxbai-embed-large installed        │
│  □ Chat model              → qwen2.5-coder:7b installed         │
│                                                                  │
│  EXTENSION                                                       │
│  ─────────────────────────────────────────────────────────────  │
│  □ Dependencies installed  → pnpm install succeeds              │
│  □ Build works             → pnpm run build creates dist/       │
│  □ No TypeScript errors    → No red squiggles in VS Code        │
│                                                                  │
│  SERVER                                                          │
│  ─────────────────────────────────────────────────────────────  │
│  □ Virtual env created     → .venv folder exists                │
│  □ Dependencies installed  → uv pip install succeeds            │
│  □ Server starts           → python main.py runs                │
│  □ Health check works      → /health returns healthy            │
│                                                                  │
│  DEVELOPMENT                                                     │
│  ─────────────────────────────────────────────────────────────  │
│  □ VS Code opens project   → No errors in terminal              │
│  □ Extensions installed    → ESLint, Prettier, Python working   │
│  □ F5 launches extension   → New VS Code window opens           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Troubleshooting

### Common Issues

```
┌─────────────────────────────────────────────────────────────────┐
│                    TROUBLESHOOTING                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ISSUE: "pnpm not found"                                         │
│  ─────────────────────────────────────────────────────────────  │
│  Solution: Restart terminal after npm install -g pnpm           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: "python not found" after installation                   │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Ensure "Add to PATH" was checked during install             │
│  2. Restart terminal/VS Code                                     │
│  3. Or manually add to PATH:                                     │
│     C:\Users\{you}\AppData\Local\Programs\Python\Python311\     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: Ollama connection refused                                │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Check Ollama is running (system tray icon)                  │
│  2. Restart Ollama from Start Menu                              │
│  3. Check port 11434 is not blocked                             │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: Extension not loading in debug                           │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Run pnpm run build first                                     │
│  2. Check dist/extension.js exists                               │
│  3. Check Output panel for errors                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: Python import errors                                     │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Ensure virtual environment is activated                     │
│  2. Check (.venv) appears in terminal prompt                    │
│  3. Re-run: uv pip install -e ".[dev]"                          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: Tree-sitter build errors                                 │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Install Visual Studio Build Tools                           │
│  2. Or use pre-built wheels:                                     │
│     pip install tree-sitter-python --only-binary :all:          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

After completing this setup:

1. **Verify everything works** using the checklist above

---

*Document Version: 1.0.0*
*Created: Planning Phase*
````

</details>


## docs/ProjectDocuments/indexing-spec.md

*Size: 29,168 bytes | Modified: 2025-12-13T07:47:07.576Z*

<details>
<summary>View code</summary>

````markdown
# 📄 INDEXING_SPEC.md

# LocalPilot - Indexing Specification

> Quality contract and technical specification for the indexing system

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Technical Specification |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [Indexing Goals](#1-indexing-goals)
2. [Indexing Guarantees](#2-indexing-guarantees)
3. [Indexing Non-Goals](#3-indexing-non-goals)
4. [Chunking Strategy](#4-chunking-strategy)
5. [Quality Metrics](#5-quality-metrics)
6. [Language Support](#6-language-support)
7. [Performance Targets](#7-performance-targets)
8. [Testing & Validation](#8-testing--validation)

---

## 1. Indexing Goals

```
┌─────────────────────────────────────────────────────────────────┐
│                     INDEXING GOALS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRIMARY GOAL:                                                   │
│  Enable the LLM to retrieve relevant code context for any      │
│  user query about the codebase.                                 │
│                                                                  │
│  SUCCESS DEFINITION:                                             │
│  When user asks "How does X work?", the RAG system retrieves   │
│  the actual code that implements X, not unrelated code.         │
│                                                                  │
│  CORE REQUIREMENTS:                                              │
│  1. Every function/class is retrievable by its purpose         │
│  2. Retrieved code includes enough context to understand        │
│  3. Retrieval is fast enough for interactive use (<2s)         │
│  4. Index survives VS Code restart                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Indexing Guarantees

### What We WILL Do

```
┌─────────────────────────────────────────────────────────────────┐
│                   INDEXING GUARANTEES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GUARANTEE 1: AST-Aware Chunking                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  We chunk code by semantic units, NOT by character count.       │
│                                                                  │
│  ✓ Functions are never split in half                            │
│  ✓ Classes stay together (unless very large)                    │
│  ✓ Methods are individual chunks                                │
│  ✓ Imports are preserved with their file                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GUARANTEE 2: Line-Accurate Metadata                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Every chunk includes:                                           │
│                                                                  │
│  ✓ Exact file path (relative to workspace)                     │
│  ✓ Start line number                                             │
│  ✓ End line number                                               │
│  ✓ Chunk type (function/class/method/etc.)                      │
│  ✓ Symbol name (function name, class name)                      │
│  ✓ Language identifier                                           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GUARANTEE 3: Complete Coverage                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Every supported file is indexed. No silent skipping.           │
│                                                                  │
│  ✓ All .ts, .js, .py, .dart files indexed                      │
│  ✓ Failed files reported (not silently skipped)                │
│  ✓ Index statistics show coverage                              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GUARANTEE 4: Persistence                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Index survives:                                                 │
│                                                                  │
│  ✓ VS Code restart                                               │
│  ✓ Computer restart                                              │
│  ✓ Extension update (same project ID)                           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GUARANTEE 5: Determinism                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Same code → Same chunks → Same embeddings                      │
│                                                                  │
│  ✓ Parsing is deterministic                                      │
│  ✓ Chunk IDs are hash-based (reproducible)                      │
│  ✓ Re-indexing same file produces same result                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Indexing Non-Goals

### What We Will NOT Do (v0.1)

```
┌─────────────────────────────────────────────────────────────────┐
│                   INDEXING NON-GOALS (MVP)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✗ Runtime Execution Analysis                                   │
│    We don't run code to understand it.                          │
│    Static analysis only.                                         │
│                                                                  │
│  ✗ Dynamic Type Inference                                        │
│    We don't infer types beyond what's in source.               │
│    No runtime type tracking.                                     │
│                                                                  │
│  ✗ Cross-Package Dependency Graph                               │
│    We index files, not npm/pip dependency trees.                │
│    (May add in v1.2+)                                           │
│                                                                  │
│  ✗ Semantic Understanding                                        │
│    We don't "understand" what code does.                        │
│    We chunk and embed, LLM does understanding.                  │
│                                                                  │
│  ✗ Binary/Compiled File Indexing                                │
│    No .pyc, .class, .dll, .exe files.                          │
│    Source code only.                                             │
│                                                                  │
│  ✗ Media File Indexing                                           │
│    No images, videos, audio.                                     │
│    Text/code files only.                                         │
│                                                                  │
│  ✗ Minified Code Handling                                        │
│    We don't de-minify JavaScript.                               │
│    Minified files indexed as-is (poor quality).                 │
│                                                                  │
│  ✗ Git History Analysis                                          │
│    Current state only.                                           │
│    No blame, no history, no diffs.                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Chunking Strategy

### 4.1 Chunk Types

| Type | Description | Example |
|------|-------------|---------|
| `function` | Standalone function | `function add(a, b)` |
| `class` | Class definition (without methods) | `class User { }` |
| `method` | Method inside a class | `User.save()` |
| `interface` | TypeScript interface | `interface Props` |
| `type` | Type alias | `type ID = string` |
| `variable` | Top-level const/let/var | `const API_URL = ...` |
| `import` | Import block (grouped) | All imports in file |
| `module` | Module-level code | File-level statements |
| `file` | Entire file (fallback) | When AST parsing fails |

### 4.2 Chunking Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                     CHUNKING RULES                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  RULE 1: Maximum Chunk Size                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Max tokens per chunk: 500 tokens (~2000 chars)                 │
│                                                                  │
│  If a function exceeds this:                                     │
│  • Keep first 400 tokens                                         │
│  • Add "[...truncated...]"                                       │
│  • Store full content in metadata for retrieval                 │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  RULE 2: Minimum Chunk Size                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Min tokens per chunk: 20 tokens                                 │
│                                                                  │
│  Tiny functions/variables: Group with neighbors                 │
│  • Group consecutive small items                                 │
│  • Label as "module" chunk type                                 │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  RULE 3: Context Inclusion                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Each chunk includes:                                            │
│  • Docstring/JSDoc (if present)                                 │
│  • Decorators (Python) / Annotations (TS)                       │
│  • Type annotations                                              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  RULE 4: Class Handling                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Classes with < 5 methods: One chunk (whole class)              │
│  Classes with ≥ 5 methods: Split into method chunks            │
│  Each method chunk includes: Class name + method                │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  RULE 5: Import Handling                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  All imports in a file: One chunk (type: "import")              │
│  Helps LLM understand file dependencies                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Chunk Metadata Schema

```typescript
interface ChunkMetadata {
  // Identity
  chunk_id: string;        // Hash of file_path + content
  file_path: string;       // Relative to workspace
  
  // Location
  line_start: number;
  line_end: number;
  
  // Classification
  chunk_type: ChunkType;
  symbol_name: string | null;
  language: string;
  
  // Context
  docstring: string | null;
  parent_class: string | null;  // For methods
  
  // Quality
  token_count: number;
  is_truncated: boolean;
}
```

---

## 5. Quality Metrics

### 5.1 Retrieval Quality Targets

```
┌─────────────────────────────────────────────────────────────────┐
│                   QUALITY METRICS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  METRIC 1: Precision@5                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Target: ≥ 60%                                                  │
│                                                                  │
│  Definition: Of top 5 retrieved chunks, how many are           │
│  actually relevant to the query?                                │
│                                                                  │
│  Test: 10 sample queries, manually evaluate results             │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  METRIC 2: Recall@10                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Target: ≥ 80%                                                  │
│                                                                  │
│  Definition: When searching for a known function,              │
│  is it in the top 10 results?                                   │
│                                                                  │
│  Test: Search for 20 known functions by description            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  METRIC 3: Coverage                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Target: 100% of supported files indexed                        │
│                                                                  │
│  Definition: All .ts, .js, .py, .dart files have chunks        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  METRIC 4: Chunk Completeness                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Target: ≤ 5% truncated chunks                                  │
│                                                                  │
│  Definition: How many chunks had to be truncated?              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 How to Measure

```python
# Quality test script (manual for MVP)
def test_retrieval_quality():
    queries = [
        ("How does user authentication work?", ["auth.service.ts"]),
        ("Where is the login function?", ["login.ts"]),
        # ... more test queries
    ]
    
    precision_scores = []
    for query, expected_files in queries:
        results = rag_query(query, top_k=5)
        relevant = sum(1 for r in results if r.file_path in expected_files)
        precision_scores.append(relevant / 5)
    
    avg_precision = sum(precision_scores) / len(precision_scores)
    print(f"Precision@5: {avg_precision:.2%}")
    assert avg_precision >= 0.60, "Quality below threshold!"
```

---

## 6. Language Support

### 6.1 MVP Languages

| Language | Parser | Chunk Types Extracted |
|----------|--------|----------------------|
| **TypeScript** | Tree-sitter | function, class, method, interface, type, variable |
| **JavaScript** | Tree-sitter | function, class, method, variable |
| **Python** | Tree-sitter | function, class, method, variable |
| **Dart** | Tree-sitter | function, class, method, variable |

### 6.2 File Extensions

```python
SUPPORTED_EXTENSIONS = {
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.py': 'python',
    '.dart': 'dart',
}

EXCLUDED_PATTERNS = [
    '**/node_modules/**',
    '**/.git/**',
    '**/dist/**',
    '**/build/**',
    '**/__pycache__/**',
    '**/.venv/**',
    '**/venv/**',
    '**/*.min.js',
    '**/*.bundle.js',
]
```

---

## 7. Performance Targets

```
┌─────────────────────────────────────────────────────────────────┐
│                  PERFORMANCE TARGETS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INDEXING SPEED:                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Small project (<100 files): < 2 minutes                      │
│  • Medium project (100-500 files): < 10 minutes                 │
│  • Target: ~100ms per file average                              │
│                                                                  │
│  QUERY SPEED:                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • RAG query (top-5): < 500ms                                   │
│  • Embedding generation: < 200ms                                │
│  • Vector search: < 100ms                                        │
│                                                                  │
│  MEMORY USAGE:                                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Indexing: < 500MB RAM                                        │
│  • Query: < 200MB RAM                                            │
│  • Idle: < 50MB RAM                                              │
│                                                                  │
│  STORAGE:                                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • ~10KB per file indexed (chunks + embeddings)                 │
│  • 100 files ≈ 1MB storage                                      │
│  • 1000 files ≈ 10MB storage                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Testing & Validation

### 8.1 Unit Tests Required

```
□ Parser correctly extracts functions from TypeScript
□ Parser correctly extracts classes from Python
□ Parser correctly extracts methods from Dart
□ Chunker respects max token limit
□ Chunker groups small items correctly
□ Metadata includes accurate line numbers
□ Hash-based IDs are deterministic
□ Excluded patterns are respected
```

### 8.2 Integration Tests Required

```
□ Full index of sample project completes
□ Index persists to disk and reloads
□ Sync correctly detects changed files
□ Query returns relevant results
□ Performance meets targets
```

### 8.3 Sample Test Project

```
test-project/
├── src/
│   ├── auth/
│   │   ├── auth.service.ts    (5 functions)
│   │   └── auth.types.ts      (3 interfaces)
│   ├── users/
│   │   ├── user.model.ts      (1 class, 4 methods)
│   │   └── user.service.ts    (6 functions)
│   └── utils/
│       └── helpers.ts         (10 small functions)
├── lib/
│   └── api.py                 (3 classes)
└── app/
    └── main.dart              (2 classes, 8 methods)

Total: ~50 files, ~200 code units
Expected index time: < 1 minute
Expected chunks: ~150-200
```

---

## 9. Chunk ID Specification

### 9.1 ID Generation

Chunk IDs must be deterministic to enable sync detection.

**Algorithm:**
```python
import hashlib

def generate_chunk_id(
    file_path: str,      # Relative to workspace
    content: str,        # Full chunk content
    chunk_type: str,     # function, class, method, etc.
    line_start: int      # Starting line number
) -> str:
    """
    Generate deterministic 16-character chunk ID.
    
    Same inputs always produce same output.
    """
    data = f"{file_path}|{content}|{chunk_type}|{line_start}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]
```

### 9.2 ID Properties

- **Deterministic:** Same code = same ID
- **Unique:** Collision probability < 1 in 2^64
- **Compact:** 16 hex characters
- **Stable:** Only changes if content, type, or location changes


---

*Document Version: 1.0.0*
````

</details>


## docs/ProjectDocuments/overview.md

*Size: 96,626 bytes | Modified: 2025-12-13T04:44:47.859Z*

<details>
<summary>View code</summary>

````markdown
# 📄 PROJECT_OVERVIEW.md

# LocalPilot - Project Overview

> **Privacy-First AI Pair Programming**

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Version** | 0.1.0-planning |
| **Author** | TarekRefaei |
| **Repository** | github.com/TarekRefaei/LocalPilot |
| **Document Type** | Master Project Overview |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Vision](#2-project-vision)
3. [Problem Statement](#3-problem-statement)
4. [Solution Overview](#4-solution-overview)
5. [Target Users](#5-target-users)
6. [Core Features](#6-core-features)
7. [System Architecture](#7-system-architecture)
8. [Technology Stack](#8-technology-stack)
9. [Project Scope](#9-project-scope)
10. [Success Criteria](#10-success-criteria)
11. [Constraints & Assumptions](#11-constraints--assumptions)
12. [Glossary](#12-glossary)
13. [Document References](#13-document-references)

---

## 1. Executive Summary

### What is LocalPilot?

LocalPilot is a Visual Studio Code extension that brings AI-powered coding assistance 
to developers who want to keep their code **private and offline**. Unlike cloud-based 
AI coding assistants (GitHub Copilot, Cursor, Augment), LocalPilot runs entirely on 
your local machine using Ollama as the LLM provider.

### Key Differentiator

LocalPilot introduces a **structured three-mode workflow**:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│    💬 CHAT          📋 PLAN           ⚡ ACT                   │
│    ─────────────    ─────────────    ─────────────              │
│    Discuss &        Create           Execute &                  │
│    Understand       TODO List        Implement                  │
│    Project          with Steps       Changes                    │
│                                                                 │
│         │                │                 │                    │
│         └───────────────►└────────────────►│                    │
│                                                                 │
│    "I want to add     "Here's the        "Creating              │
│     authentication"    step-by-step       auth.service.ts..."   │
│                        plan..."                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

This workflow ensures that AI assistance is **deliberate and controlled**, not just 
autocomplete-style suggestions. Users understand what will happen before any code 
is written.

### One-Line Description

> A VS Code extension that provides privacy-first AI coding assistance using local 
> LLMs (Ollama) with a structured Chat → Plan → Act workflow powered by advanced 
> RAG indexing.

---

## 2. Project Vision

### Vision Statement

To empower developers with intelligent AI coding assistance that:
- **Never sends code to the cloud**
- **Understands project context deeply** through advanced RAG indexing
- **Produces deliberate, planned changes** rather than unpredictable autocomplete
- **Works offline** in any environment

### Mission

Make local LLM-powered coding assistance accessible, effective, and structured, 
enabling developers to maintain complete control over their code and data while 
benefiting from AI productivity gains.

### Core Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                      CORE PRINCIPLES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔒 PRIVACY FIRST                                                │
│     All processing happens locally. No code ever leaves         │
│     your machine. Period.                                        │
│                                                                  │
│  🧠 CONTEXT-AWARE                                                │
│     The LLM understands your entire project through             │
│     intelligent RAG indexing, not just the current file.        │
│                                                                  │
│  📋 STRUCTURED WORKFLOW                                          │
│     Chat → Plan → Act ensures you understand and approve        │
│     every change before it happens.                             │
│                                                                  │
│  👁️ TRANSPARENT                                                  │
│     Every action is visible. Every change is reviewable.        │
│     No magic, no surprises.                                      │
│                                                                  │
│  🎯 PRACTICAL                                                    │
│     Built for real-world use with real-world hardware.          │
│     Works on 16GB RAM with consumer GPUs.                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Problem Statement

### The Current Landscape

AI coding assistants have transformed software development. However, current 
solutions present significant challenges:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROBLEMS WITH CURRENT SOLUTIONS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ PROBLEM 1: Privacy & Security Concerns                       │
│  ─────────────────────────────────────────────────────────────  │
│  • Code is sent to cloud servers                                │
│  • Enterprise policies may prohibit cloud AI tools              │
│  • Sensitive/proprietary code at risk                           │
│  • GDPR, HIPAA, and compliance issues                           │
│  • No control over how code is used for training                │
│                                                                  │
│  ❌ PROBLEM 2: Subscription Fatigue & Cost                       │
│  ─────────────────────────────────────────────────────────────  │
│  • GitHub Copilot: $19/month                                    │
│  • Cursor Pro: $20/month                                        │
│  • Augment: Enterprise pricing                                  │
│  • Costs add up for independent developers                      │
│                                                                  │
│  ❌ PROBLEM 3: Internet Dependency                               │
│  ─────────────────────────────────────────────────────────────  │
│  • No offline capability                                         │
│  • Unusable in restricted networks                              │
│  • Latency issues with cloud round-trips                        │
│  • Service outages affect productivity                          │
│                                                                  │
│  ❌ PROBLEM 4: Limited Project Understanding                     │
│  ─────────────────────────────────────────────────────────────  │
│  • Most tools only see current file or limited context          │
│  • Suggestions often ignore project conventions                 │
│  • No understanding of architecture or patterns                 │
│  • Repetitive explanations needed                               │
│                                                                  │
│  ❌ PROBLEM 5: Unstructured Assistance                           │
│  ─────────────────────────────────────────────────────────────  │
│  • Autocomplete is reactive, not deliberate                     │
│  • No planning phase before implementation                      │
│  • Hard to implement complex, multi-file features               │
│  • Changes can be unpredictable                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Who Feels These Problems?

1. **Enterprise Developers** - Cannot use cloud AI due to policies
2. **Security-Conscious Developers** - Don't trust code in the cloud
3. **Offline Workers** - Air-gapped environments, travel, poor connectivity
4. **Independent Developers** - Subscription costs are prohibitive
5. **Open Source Contributors** - Privacy concerns with commercial tools

---

## 4. Solution Overview

### How LocalPilot Solves These Problems

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOCALPILOT SOLUTION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ SOLUTION 1: Complete Privacy                                 │
│  ─────────────────────────────────────────────────────────────  │
│  • All LLM inference runs locally via Ollama                    │
│  • RAG index stored on your machine                             │
│  • Zero network calls for AI features                           │
│  • Your code never leaves your computer                         │
│                                                                  │
│  ✅ SOLUTION 2: Free After Hardware                              │
│  ─────────────────────────────────────────────────────────────  │
│  • Ollama is free and open source                               │
│  • LocalPilot extension is free                                  │
│  • One-time hardware investment, unlimited use                  │
│                                                                  │
│  ✅ SOLUTION 3: Works Offline                                    │
│  ─────────────────────────────────────────────────────────────  │
│  • No internet required after initial setup                     │
│  • Works in air-gapped environments                             │
│  • No latency from network round-trips                          │
│  • No service dependency                                        │
│                                                                  │
│  ✅ SOLUTION 4: Deep Project Understanding via RAG               │
│  ─────────────────────────────────────────────────────────────  │
│  • Indexes entire codebase semantically                         │
│  • Understands code structure (functions, classes, modules)     │
│  • Retrieves relevant context for every query                   │
│  • Learns your project's patterns and conventions               │
│                                                                  │
│  ✅ SOLUTION 5: Structured Chat → Plan → Act Workflow            │
│  ─────────────────────────────────────────────────────────────  │
│  • Discuss before deciding (Chat Mode)                          │
│  • Plan before implementing (Plan Mode)                         │
│  • Review before applying (Act Mode)                            │
│  • Full control at every step                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The LocalPilot Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE LOCALPILOT WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STEP 0: INDEXING (One-time setup per project)                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  📁 Your Project                                             ││
│  │       │                                                      ││
│  │       ▼                                                      ││
│  │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐  ││
│  │  │   Scanner   │ ───► │   Chunker   │ ───► │  Embedder   │  ││
│  │  │             │      │  (AST-aware)│      │  (Ollama)   │  ││
│  │  └─────────────┘      └─────────────┘      └─────────────┘  ││
│  │                                                   │          ││
│  │                                                   ▼          ││
│  │                                          ┌─────────────┐     ││
│  │                                          │ Vector DB   │     ││
│  │                                          │ (ChromaDB)  │     ││
│  │                                          └─────────────┘     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  STEP 1: CHAT MODE                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  User: "I want to add user authentication to my app"           │
│                                                                  │
│  LocalPilot:                                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Based on your project structure, I can see you're using     ││
│  │ Express.js with a modular architecture. Here's how I'd      ││
│  │ approach authentication:                                     ││
│  │                                                              ││
│  │ 1. Create an auth module in src/modules/auth/               ││
│  │ 2. Add JWT token handling                                   ││
│  │ 3. Create middleware for protected routes                   ││
│  │ 4. Add login/register endpoints                             ││
│  │                                                              ││
│  │ [📋 Transfer to Plan Mode]                                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  STEP 2: PLAN MODE                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ## Plan: User Authentication Implementation                  ││
│  │                                                              ││
│  │ ### Prerequisites                                            ││
│  │ - [ ] Install jsonwebtoken and bcrypt packages              ││
│  │                                                              ││
│  │ ### Tasks                                                    ││
│  │ 1. [ ] Create src/modules/auth/auth.service.ts              ││
│  │    └── JWT sign/verify, password hashing                    ││
│  │                                                              ││
│  │ 2. [ ] Create src/modules/auth/auth.controller.ts           ││
│  │    └── Login, register, refresh endpoints                   ││
│  │                                                              ││
│  │ 3. [ ] Create src/middleware/auth.middleware.ts             ││
│  │    └── Token verification middleware                        ││
│  │                                                              ││
│  │ 4. [ ] Update src/routes/index.ts                           ││
│  │    └── Add auth routes                                       ││
│  │                                                              ││
│  │ 5. [ ] Create src/modules/auth/auth.test.ts                 ││
│  │    └── Unit tests for auth service                          ││
│  │                                                              ││
│  │ [✏️ Edit] [🔄 Regenerate] [✅ Approve & Execute]             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  STEP 3: ACT MODE                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 📋 Progress: ████░░░░░░ 40% (2/5 tasks)                      ││
│  │                                                              ││
│  │ ✅ Task 1: Create auth.service.ts         DONE              ││
│  │ ✅ Task 2: Create auth.controller.ts      DONE              ││
│  │ 🔄 Task 3: Create auth.middleware.ts      IN PROGRESS       ││
│  │ ⏳ Task 4: Update routes                  PENDING           ││
│  │ ⏳ Task 5: Create tests                   PENDING           ││
│  │                                                              ││
│  │ ─────────────────────────────────────────────────────────── ││
│  │ Currently creating: src/middleware/auth.middleware.ts       ││
│  │                                                              ││
│  │ ```typescript                                                ││
│  │ import { Request, Response, NextFunction } from 'express';  ││
│  │ import { AuthService } from '../modules/auth/auth.service'; ││
│  │                                                              ││
│  │ export const authMiddleware = async (                       ││
│  │   req: Request,                                              ││
│  │   res: Response,                                             ││
│  │   next: NextFunction                                         ││
│  │ ) => {                                                       ││
│  │   // ... implementation                                      ││
│  │ };                                                           ││
│  │ ```                                                          ││
│  │                                                              ││
│  │ [👁️ View Full] [✅ Apply] [❌ Skip] [✏️ Edit]                ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Target Users

### Primary User Personas

```
┌─────────────────────────────────────────────────────────────────┐
│                      TARGET USER PERSONAS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  👤 PERSONA 1: The Privacy-Conscious Developer                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: Alex                                                      │
│  Role: Senior Developer at a security-focused startup            │
│  Pain: "I can't use Copilot because our security policy          │
│         prohibits sending code to external servers"              │
│  Need: AI coding help that stays completely local               │
│  Tech: Works with TypeScript, Python, handles sensitive data    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  👤 PERSONA 2: The Independent Developer                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: Sam                                                       │
│  Role: Freelancer working on multiple projects                   │
│  Pain: "Subscription costs for all these AI tools add up        │
│         quickly when you're independent"                        │
│  Need: Free/one-time-cost AI assistance                         │
│  Tech: Full-stack, works with React, Node, Python               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  👤 PERSONA 3: The Mobile Developer                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: Jordan                                                    │
│  Role: Flutter/React Native developer                           │
│  Pain: "Most AI tools don't understand Dart well, and I         │
│         often work offline during commutes"                     │
│  Need: Offline-capable AI that understands mobile patterns      │
│  Tech: Dart/Flutter, TypeScript, occasionally Kotlin            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  👤 PERSONA 4: The Learning Developer                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: Taylor                                                    │
│  Role: Junior developer, 1 year experience                      │
│  Pain: "I want to understand what AI suggests, not just         │
│         accept code blindly"                                    │
│  Need: Structured workflow that explains before doing           │
│  Tech: Learning TypeScript and Python                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### User Requirements Summary

| Requirement | Priority | Addressed By |
|-------------|----------|--------------|
| Code stays local | MUST | Ollama + local RAG |
| Works offline | MUST | No cloud dependencies |
| Free to use | SHOULD | Open source + Ollama |
| Understands whole project | MUST | RAG indexing system |
| Explains before changing | MUST | Chat → Plan → Act workflow |
| Supports multiple languages | SHOULD | Extensible parser system |
| Fast responses | SHOULD | Optimized local inference |
| Easy to set up | MUST | Guided onboarding |

---

## 6. Core Features

### Feature Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      CORE FEATURES                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔧 FEATURE 1: Intelligent Project Indexing                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Scans all project files                                       │
│  • Parses code structure (functions, classes, imports)          │
│  • Creates semantic embeddings using local LLM                  │
│  • Stores in local vector database                              │
│  • Enables intelligent code retrieval                           │
│                                                                  │
│  User sees:                                                      │
│  • One-click "Index Project" button                             │
│  • Progress indicator during indexing                           │
│  • Summary of indexed content                                    │
│                                                                  │
│  Technical details:                                              │
│  • Uses Tree-sitter for AST parsing                             │
│  • mxbai-embed-large for embeddings                             │
│  • ChromaDB for vector storage                                   │
│  • Incremental updates via file watching                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  💬 FEATURE 2: Chat Mode                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Natural conversation about your codebase                     │
│  • Retrieves relevant code context automatically                │
│  • Explains code, answers questions                             │
│  • Suggests approaches for new features                         │
│  • Provides project summary after indexing                      │
│                                                                  │
│  User sees:                                                      │
│  • Chat interface in sidebar                                     │
│  • Messages with code highlighting                              │
│  • "Transfer to Plan" button when ready                         │
│                                                                  │
│  Technical details:                                              │
│  • RAG-enhanced prompts                                          │
│  • Streaming responses via WebSocket                            │
│  • Context window management                                     │
│  • Conversation history (session-based)                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  📋 FEATURE 3: Plan Mode                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Converts chat discussion into structured plan                │
│  • Creates detailed TODO list with file paths                   │
│  • Specifies what will be created/modified                      │
│  • Allows editing before execution                              │
│                                                                  │
│  User sees:                                                      │
│  • Formatted plan with checkboxes                               │
│  • File paths for each change                                    │
│  • Edit/Regenerate/Approve buttons                              │
│                                                                  │
│  Technical details:                                              │
│  • Specialized planning prompt                                   │
│  • Structured output parsing                                     │
│  • Plan state management                                         │
│  • Transfer mechanism to Act Mode                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ⚡ FEATURE 4: Act Mode                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Executes plan step by step                                   │
│  • Creates and modifies files                                    │
│  • Shows diffs before applying                                   │
│  • Tracks progress visually                                      │
│  • Allows pause/resume/skip                                      │
│                                                                  │
│  User sees:                                                      │
│  • Progress tracker with task status                            │
│  • Current task details with code preview                       │
│  • Apply/Skip/Edit controls per task                            │
│  • Terminal output (when running commands)                       │
│                                                                  │
│  Technical details:                                              │
│  • VS Code file system API integration                          │
│  • Diff generation and display                                   │
│  • Task queue management                                         │
│  • Rollback capability                                           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  🔗 FEATURE 5: Ollama Integration                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Detects running Ollama instance                              │
│  • Lists available models                                        │
│  • Handles chat completions                                      │
│  • Handles embedding generation                                  │
│  • Manages connection health                                     │
│                                                                  │
│  User sees:                                                      │
│  • Ollama status indicator                                       │
│  • Model selection dropdown                                      │
│  • Connection error messages                                     │
│                                                                  │
│  Technical details:                                              │
│  • REST API communication (port 11434)                          │
│  • Streaming response handling                                   │
│  • Automatic reconnection                                        │
│  • Model capability detection                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Feature Matrix by Release

| Feature | MVP (v0.1) | v1.1 | v1.2+ |
|---------|------------|------|-------|
| Ollama connection | ✅ | ✅ | ✅ |
| AST-aware indexing | ✅ | ✅ | ✅ |
| Smart Sync indexing | ✅ | ✅ | ✅ |
| Auto file watching | ❌ | ✅ | ✅ |
| Chat mode | ✅ | ✅ | ✅ |
| Plan mode | ✅ | ✅ | ✅ |
| Act mode (basic) | ✅ | ✅ | ✅ |
| Act mode (terminal) | ❌ | ✅ | ✅ |
| Conversation persistence | ❌ | ✅ | ✅ |
| TypeScript/JavaScript | ✅ | ✅ | ✅ |
| Python | ✅ | ✅ | ✅ |
| Dart/Flutter | ✅ | ✅ | ✅ |
| Kotlin | ❌ | ✅ | ✅ |
| Swift | ❌ | ❌ | ✅ |
| Settings UI | ❌ | ✅ | ✅ |
| Multiple workspaces | ❌ | ❌ | ✅ |
---

## 7. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 LOCALPILOT SYSTEM ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                        ┌─────────────────┐                      │
│                        │    VS Code      │                      │
│                        │    (Host)       │                      │
│                        └────────┬────────┘                      │
│                                 │                                │
│  ┌──────────────────────────────┼──────────────────────────────┐│
│  │                              │                               ││
│  │           LOCALPILOT EXTENSION (TypeScript)                  ││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                    PRESENTATION LAYER                    │││
│  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐              │││
│  │  │  │ Onboarding│ │  Chat UI  │ │  Plan UI  │              │││
│  │  │  │   View    │ │           │ │           │              │││
│  │  │  └───────────┘ └───────────┘ └───────────┘              │││
│  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐              │││
│  │  │  │  Act UI   │ │ Settings  │ │  Status   │              │││
│  │  │  │           │ │    UI     │ │   Bar     │              │││
│  │  │  └───────────┘ └───────────┘ └───────────┘              │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                    FEATURE LAYER                         │││
│  │  │                                                          │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │   Indexing   │ │     Chat     │ │     Plan     │     │││
│  │  │  │   Feature    │ │   Feature    │ │   Feature    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  │  ┌──────────────┐ ┌──────────────┐                      │││
│  │  │  │     Act      │ │   Settings   │                      │││
│  │  │  │   Feature    │ │   Feature    │                      │││
│  │  │  └──────────────┘ └──────────────┘                      │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                      CORE LAYER                          │││
│  │  │                                                          │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │   Entities   │ │  Interfaces  │ │    Errors    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                 INFRASTRUCTURE LAYER                     │││
│  │  │                                                          │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │    VS Code   │ │     HTTP     │ │  WebSocket   │     │││
│  │  │  │    Adapter   │ │    Client    │ │    Client    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  └──────────────────────────────┼──────────────────────────────┘│
│                                 │                                │
│                    HTTP / WebSocket                              │
│                                 │                                │
│  ┌──────────────────────────────┼──────────────────────────────┐│
│  │                              │                               ││
│  │              PYTHON RAG SERVER (FastAPI)                     ││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                       API LAYER                          │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │  /index      │ │  /query      │ │  /chat       │     │││
│  │  │  │  endpoint    │ │  endpoint    │ │  endpoint    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                    SERVICE LAYER                         │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │  Indexing    │ │     RAG      │ │     LLM      │     │││
│  │  │  │   Service    │ │   Service    │ │   Service    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                 INFRASTRUCTURE LAYER                     │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │  LlamaIndex  │ │   ChromaDB   │ │ Tree-sitter  │     │││
│  │  │  │   Adapter    │ │   Adapter    │ │   Parser     │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  └──────────────────────────────┼──────────────────────────────┘│
│                                 │                                │
│                           Ollama API                             │
│                                 │                                │
│                    ┌────────────┴───────────┐                   │
│                    │       OLLAMA           │                   │
│                    │   (Local LLM Server)   │                   │
│                    │                        │                   │
│                    │  ┌──────────────────┐  │                   │
│                    │  │ qwen2.5-coder    │  │                   │
│                    │  │ mxbai-embed      │  │                   │
│                    │  └──────────────────┘  │                   │
│                    └────────────────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA FLOW OVERVIEW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FLOW 1: INDEXING                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │ VS Code│───►│  Scan  │───►│ Parse  │───►│ Chunk  │          │
│  │  Files │    │ Files  │    │  AST   │    │  Code  │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                   │              │
│       ┌────────────────────────────────────────────┘              │
│       │                                                          │
│       ▼                                                          │
│  ┌────────┐    ┌────────┐    ┌────────┐                         │
│  │Ollama  │───►│Generate│───►│ Store  │                         │
│  │Embed   │    │Vectors │    │ChromaDB│                         │
│  └────────┘    └────────┘    └────────┘                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FLOW 2: CHAT QUERY                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │  User  │───►│ Embed  │───►│ Query  │───►│Retrieve│          │
│  │  Query │    │  Query │    │ChromaDB│    │ Chunks │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                   │              │
│       ┌────────────────────────────────────────────┘              │
│       │                                                          │
│       ▼                                                          │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │ Build  │───►│ Send   │───►│ Stream │───►│Display │          │
│  │ Prompt │    │ Ollama │    │Response│    │  Chat  │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FLOW 3: PLAN TO ACT                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │  Plan  │───►│ Parse  │───►│Generate│───►│ Write  │          │
│  │  JSON  │    │ Tasks  │    │  Code  │    │  File  │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                   │              │
│       ┌────────────────────────────────────────────┘              │
│       │                                                          │
│       ▼                                                          │
│  ┌────────┐    ┌────────┐    ┌────────┐                         │
│  │ Update │───►│ Re-    │───►│  Next  │                         │
│  │ Index  │    │ Index  │    │  Task  │                         │
│  └────────┘    └────────┘    └────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Communication

```
┌─────────────────────────────────────────────────────────────────┐
│                  COMMUNICATION PROTOCOLS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VS Code Extension ◄──────► Python RAG Server                    │
│                                                                  │
│  Protocol: HTTP REST + WebSocket                                │
│  Port: 52741 (configurable)                                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  REST Endpoints:                                             ││
│  │                                                              ││
│  │  POST   /api/index/start    - Start indexing                 ││
│  │  GET    /api/index/status   - Get indexing progress          ││
│  │  DELETE /api/index          - Clear index                    ││
│  │  POST   /api/query          - Query RAG                      ││
│  │  GET    /api/health         - Health check                   ││
│  │  GET    /api/models         - List Ollama models            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  WebSocket:                                                  ││
│  │                                                              ││
│  │  WS /ws/chat     - Streaming chat responses                  ││
│  │  WS /ws/progress - Real-time indexing progress               ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Python RAG Server ◄──────► Ollama                               │
│                                                                  │
│  Protocol: HTTP REST                                             │
│  Port: 11434 (Ollama default)                                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Ollama Endpoints Used:                                      ││
│  │                                                              ││
│  │  POST   /api/generate    - Text generation (chat)           ││
│  │  POST   /api/embeddings  - Generate embeddings               ││
│  │  GET    /api/tags        - List available models             ││
│  │  POST   /api/show        - Model information                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Technology Stack

### Complete Stack Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VS CODE EXTENSION (TypeScript)                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Core:                                                           │
│  ├── Language:        TypeScript 5.x                            │
│  ├── Runtime:         Node.js 18+                               │
│  ├── VS Code API:     1.85+                                     │
│  └── Module System:   ES Modules                                │
│                                                                  │
│  UI:                                                             │
│  ├── Framework:       React 18                                  │
│  ├── Styling:         Tailwind CSS                              │
│  ├── State:           Zustand                                   │
│  ├── Rendering:       VS Code WebView                           │
│  └── Icons:           Lucide React                              │
│                                                                  │
│  Build & Dev:                                                    │
│  ├── Bundler:         esbuild                                   │
│  ├── Package Manager: pnpm                                      │
│  ├── Linting:         ESLint + Prettier                         │
│  └── Testing:         Vitest + Testing Library                  │
│                                                                  │
│  Communication:                                                  │
│  ├── HTTP Client:     fetch (native)                            │
│  └── WebSocket:       ws                                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PYTHON RAG SERVER                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Core:                                                           │
│  ├── Language:        Python 3.11+                              │
│  ├── Framework:       FastAPI                                   │
│  ├── Server:          Uvicorn                                   │
│  └── Async:           asyncio                                   │
│                                                                  │
│  RAG:                                                            │
│  ├── Framework:       LlamaIndex                                │
│  ├── Vector DB:       ChromaDB                                  │
│  ├── Embeddings:      Ollama (mxbai-embed-large)                │
│  └── LLM:             Ollama (qwen2.5-coder)                    │
│                                                                  │
│  Code Parsing:                                                   │
│  ├── AST Parser:      Tree-sitter                               │
│  └── Languages:       TS, JS, Python, Dart (MVP)                │
│                                                                  │
│  Build & Dev:                                                    │
│  ├── Package Manager: uv (or poetry)                            │
│  ├── Linting:         Ruff                                      │
│  ├── Type Checking:   mypy                                      │
│  └── Testing:         pytest + pytest-asyncio                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  LLM PROVIDER                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Platform:            Ollama                                     │
│  Default Chat Model:  qwen2.5-coder:7b-instruct-q4_K_M         │
│  Default Embed Model: mxbai-embed-large:latest                  │
│  Backup Chat Model:   qwen2.5-coder:14b-instruct-q4_K_M        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  DEVELOPMENT TOOLS                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Version Control:     Git + GitHub                              │
│  CI/CD:               GitHub Actions                            │
│  Documentation:       Markdown + TypeDoc + Sphinx               │
│  Pre-commit:          Husky + lint-staged                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why These Technologies?

| Technology | Chosen Over | Reason |
|------------|-------------|--------|
| **TypeScript** | JavaScript | Type safety, better tooling, required for complex extension |
| **React** | Vue, Svelte, Vanilla | Most familiar to developer, largest ecosystem |
| **Zustand** | Redux, MobX | Lightweight, simple API, less boilerplate |
| **esbuild** | Webpack, Vite | Fastest bundler, simple config |
| **FastAPI** | Flask, Django | Modern async Python, great for APIs |
| **LlamaIndex** | LangChain | Better for indexing/RAG, simpler API |
| **ChromaDB** | Qdrant, FAISS | Easiest setup, Python native, sufficient for MVP |
| **Tree-sitter** | Regex, Custom | Industry standard, supports all needed languages |
| **pnpm** | npm, yarn | Faster, disk efficient |
| **uv** | pip, poetry | Faster, simpler than poetry |

---

## 9. Project Scope

### In Scope (MVP)

```
┌─────────────────────────────────────────────────────────────────┐
│                     MVP SCOPE (v0.1.0)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ INCLUDED IN MVP                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Extension Core:                                                 │
│  ☑ VS Code extension activation and lifecycle                   │
│  ☑ Sidebar panel with three-tab interface                       │
│  ☑ Onboarding screen with indexing button                       │
│  ☑ Basic settings (model selection)                             │
│  ☑ Status bar indicator                                          │
│                                                                  │
│  Ollama Integration:                                             │
│  ☑ Detect Ollama running status                                  │
│  ☑ List available models                                         │
│  ☑ Chat completions with streaming                              │
│  ☑ Embedding generation                                          │
│  ☑ Error handling for connection issues                         │
│                                                                  │
│  Indexing (ENHANCED):                                            │
│  ☑ Scan workspace files                                          │
│  ☑ AST-aware code chunking (functions, classes, methods)        │
│  ☑ Tree-sitter parsing for TS, JS, Python, Dart                 │
│  ☑ Generate embeddings via Ollama                               │
│  ☑ Store in ChromaDB with metadata                              │
│  ☑ Progress indicator                                            │
│  ☑ Index persistence                                             │
│  ☑ Smart "Sync Index" with hash-based change detection          │
│                                                                  │
│  Chat Mode:                                                       │
│  ☑ Chat interface with message display                          │
│  ☑ RAG-enhanced responses                                        │
│  ☑ Project summary after indexing                               │
│  ☑ Transfer to Plan button                                       │
│  ☑ Streaming response display                                    │
│                                                                  │
│  Plan Mode:                                                       │
│  ☑ Display structured plan                                       │
│  ☑ TODO list with checkboxes                                    │
│  ☑ File paths for each task                                     │
│  ☑ Edit/Regenerate capabilities                                 │
│  ☑ Approve and transfer to Act                                  │
│                                                                  │
│  Act Mode (Basic):                                                │
│  ☑ Display task list with progress                              │
│  ☑ Create new files                                              │
│  ☑ Modify existing files with diff preview                      │
│  ☑ Delete files (with confirmation)                             │
│  ☑ Create folders                                                │
│  ☑ Apply/Skip/Edit controls                                     │
│  ☑ Generate TODO markdown file                                  │
│  ☐ Terminal command execution (v1.1)                            │
│                                                                  │
│  Languages (Full AST Support):                                   │
│  ☑ TypeScript                                                    │
│  ☑ JavaScript                                                    │
│  ☑ Python                                                        │
│  ☑ Dart (Flutter)                                                │
│                                                                  │
│  Platform:                                                        │
│  ☑ Windows 10/11                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```


### Out of Scope (MVP)

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOT IN MVP (Future)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ EXCLUDED FROM MVP                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Features:                                                       │
│  ☐ Incremental indexing / file watching (v1.1)                  │
│  ☐ Terminal command execution (v1.1)                            │
│  ☐ Conversation history persistence (v1.1)                      │
│  ☐ Multiple workspace support (v1.2)                            │
│  ☐ Git integration (v1.2)                                        │
│  ☐ Voice input (Future)                                          │
│  ☐ Custom system prompts (v1.2)                                 │
│                                                                  │
│  Languages (Future):                                              │
│  ☐ Kotlin                                                        │
│  ☐ Swift                                                         │
│  ☐ Java                                                          │
│  ☐ C/C++                                                         │
│  ☐ Rust                                                          │
│  ☐ Go                                                            │
│                                                                  │
│  Platforms (Future):                                              │
│  ☐ macOS                                                         │
│  ☐ Linux                                                         │
│                                                                  │
│  Advanced:                                                        │
│  ☐ Cloud LLM providers (OpenAI, Anthropic)                      │
│  ☐ Team collaboration features                                  │
│  ☐ Model fine-tuning                                             │
│  ☐ Multi-model routing                                          │
│  ☐ LangChain alternative provider                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Success Criteria

### Definition of Done (MVP)

```
┌─────────────────────────────────────────────────────────────────┐
│                      MVP SUCCESS CRITERIA                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  The MVP is successful when a user can:                         │
│                                                                  │
│  ✅ CRITERION 1: Installation & Setup                            │
│  ─────────────────────────────────────────────────────────────  │
│  • Install the extension from .vsix file                        │
│  • See Ollama connection status                                  │
│  • Select from available Ollama models                          │
│  • Complete without reading documentation                       │
│  Time: < 5 minutes                                               │
│                                                                  │
│  ✅ CRITERION 2: Project Indexing                                │
│  ─────────────────────────────────────────────────────────────  │
│  • Click "Index Project" button                                  │
│  • See progress indicator                                        │
│  • Complete indexing for 100-file project                       │
│  • Receive project summary                                       │
│  Time: < 5 minutes for 100 files                                 │
│                                                                  │
│  ✅ CRITERION 3: Chat Understanding                              │
│  ─────────────────────────────────────────────────────────────  │
│  • Ask "What does this project do?"                             │
│  • Receive accurate, context-aware answer                       │
│  • Ask about specific file/function                             │
│  • Get relevant code in response                                 │
│  Accuracy: 80%+ relevant responses                               │
│                                                                  │
│  ✅ CRITERION 4: Plan Generation                                 │
│  ─────────────────────────────────────────────────────────────  │
│  • Request a new feature in chat                                 │
│  • Transfer to Plan mode                                         │
│  • See structured TODO list                                      │
│  • Tasks include file paths                                      │
│  Quality: Actionable, specific tasks                             │
│                                                                  │
│  ✅ CRITERION 5: Code Execution                                  │
│  ─────────────────────────────────────────────────────────────  │
│  • Approve plan and enter Act mode                              │
│  • See task progress                                             │
│  • Preview code before applying                                  │
│  • Files are created/modified correctly                         │
│  Quality: Code compiles/runs without errors                      │
│                                                                  │
│  ✅ CRITERION 6: Reliability                                     │
│  ─────────────────────────────────────────────────────────────  │
│  • No crashes during normal use                                  │
│  • Graceful error handling                                       │
│  • Clear error messages                                          │
│  Stability: 95%+ uptime during sessions                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Performance Indicators (KPIs)

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Indexing Speed** | <100ms per file | Stopwatch during indexing |
| **Query Response** | <3s for first token | Time from send to display |
| **Memory Usage** | <500MB extension | VS Code memory monitor |
| **Chat Accuracy** | 80%+ relevant | Manual review of 10 queries |
| **Code Quality** | Compiles 90%+ | Manual testing of generated code |
| **Crash Rate** | <1 per session | Crash logs |

---

## 11. Constraints & Assumptions

### Constraints

```
┌─────────────────────────────────────────────────────────────────┐
│                        CONSTRAINTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TECHNICAL CONSTRAINTS                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Hardware Requirements:                                          │
│  • Minimum 16GB RAM                                              │
│  • GPU optional but recommended                                  │
│  • ~10GB disk space (Ollama models)                             │
│                                                                  │
│  Software Requirements:                                          │
│  • VS Code 1.85 or higher                                       │
│  • Ollama installed and running                                 │
│  • At least one chat model in Ollama                           │
│  • At least one embedding model in Ollama                       │
│                                                                  │
│  Platform:                                                       │
│  • Windows only for MVP                                          │
│                                                                  │
│  LLM Limitations:                                                │
│  • Context window limits (8K-32K tokens)                        │
│  • Local inference speed depends on hardware                    │
│  • Model quality varies                                          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PROJECT CONSTRAINTS                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Team:                                                           │
│  • Solo developer                                                │
│  • Part-time availability                                        │
│  • Learning TypeScript and VS Code extensions                   │
│                                                                  │
│  Timeline:                                                       │
│  • Flexible but aiming for usable MVP                           │
│                                                                  │
│  Budget:                                                         │
│  • No paid services                                              │
│  • Open source tools only                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Assumptions

```
┌─────────────────────────────────────────────────────────────────┐
│                       ASSUMPTIONS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  USER ASSUMPTIONS                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  • User has Ollama installed before using LocalPilot            │
│  • User has downloaded at least one compatible model            │
│  • User is comfortable with VS Code                             │
│  • User understands basic LLM concepts                          │
│  • User has a project they want to work on                      │
│                                                                  │
│  TECHNICAL ASSUMPTIONS                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  • Ollama API remains stable (v0.1.x)                           │
│  • VS Code WebView API remains stable                           │
│  • ChromaDB can handle <10,000 document workspaces              │
│  • LlamaIndex Ollama integration works reliably                 │
│  • Tree-sitter parsers are accurate for target languages        │
│                                                                  │
│  QUALITY ASSUMPTIONS                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  • qwen2.5-coder can generate usable code                       │
│  • mxbai-embed-large provides good code embeddings              │
│  • RAG retrieval will find relevant context                     │
│  • Semantic chunking is sufficient for MVP                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **AST** | Abstract Syntax Tree - A tree representation of code structure |
| **Chunking** | Splitting documents into smaller pieces for embedding |
| **Embedding** | A numerical vector representation of text |
| **LLM** | Large Language Model - AI model for text generation |
| **Ollama** | Local LLM runtime that runs models on your machine |
| **RAG** | Retrieval-Augmented Generation - Enhancing LLM with retrieved context |
| **Vector Database** | Database optimized for similarity search on embeddings |
| **WebView** | VS Code's way of displaying custom HTML/React UI |
| **Context Window** | Maximum tokens an LLM can process at once |
| **Tree-sitter** | Fast, incremental parsing library for code |
| **ChromaDB** | Open-source embedding database |
| **LlamaIndex** | Framework for building RAG applications |
| **FastAPI** | Modern Python web framework for APIs |
| **Token** | Basic unit of text for LLMs (roughly 4 characters) |

---


## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | TarekRefaei | | |

---

*Document Version: 1.0.0*
*Created: Planning Phase*
*Last Updated: [Current Date]*
````

</details>


## docs/ProjectDocuments/prompt-engineer.md

*Size: 26,277 bytes | Modified: 2025-12-13T03:10:53.627Z*

<details>
<summary>View code</summary>

````markdown
# 📄 PROMPT_ENGINEERING.md

# LocalPilot - Prompt Engineering Guide

> Prompt versioning, testing, and best practices

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Prompt Engineering Specification |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [Prompt Philosophy](#1-prompt-philosophy)
2. [Prompt Structure](#2-prompt-structure)
3. [Prompt Registry](#3-prompt-registry)
4. [Versioning Strategy](#4-versioning-strategy)
5. [Testing Prompts](#5-testing-prompts)
6. [Prompt Templates](#6-prompt-templates)
7. [Best Practices](#7-best-practices)

---

## 1. Prompt Philosophy

### 1.1 Core Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                   PROMPT PHILOSOPHY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRINCIPLE 1: Prompts Are Code                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Prompts live in version control                              │
│  • Prompts have tests                                            │
│  • Prompts have documentation                                    │
│  • Changes are reviewed                                          │
│                                                                  │
│  PRINCIPLE 2: Determinism Where Possible                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Low temperature for structured output                        │
│  • Clear format instructions                                     │
│  • Consistent context structure                                  │
│                                                                  │
│  PRINCIPLE 3: Fail Gracefully                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Define what to do if output is unparseable                   │
│  • Have fallback prompts                                         │
│  • Log failures for debugging                                    │
│                                                                  │
│  PRINCIPLE 4: Context Efficiency                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Don't waste tokens on unnecessary context                   │
│  • Prioritize most relevant information                         │
│  • Truncate gracefully                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Prompt Types in LocalPilot

| Type | Purpose | Output Format | Temperature |
|------|---------|---------------|-------------|
| **System** | Set assistant behavior | N/A | N/A |
| **Chat** | Conversational response | Markdown | 0.7 |
| **Summary** | Project summary | Markdown | 0.3 |
| **Plan** | Generate TODO plan | Structured MD | 0.2 |
| **Code** | Generate code | Code blocks | 0.2 |

---

## 2. Prompt Structure

### 2.1 Standard Prompt Template

```typescript
interface PromptDefinition {
  // Identity
  id: string;           // Unique identifier
  version: string;      // Semantic version
  name: string;         // Human-readable name
  
  // Classification
  type: 'system' | 'chat' | 'summary' | 'plan' | 'code';
  
  // Configuration
  config: {
    temperature: number;
    maxTokens?: number;
    stopSequences?: string[];
  };
  
  // Content
  template: string;     // Prompt template with {{variables}}
  
  // Validation
  expectedOutput: {
    format: 'markdown' | 'json' | 'code' | 'text';
    schema?: object;    // JSON schema if applicable
  };
  
  // Fallback
  onParseFailure: 'retry' | 'fallback' | 'error';
  fallbackPromptId?: string;
  
  // Metadata
  description: string;
  examples?: PromptExample[];
  changelog: ChangelogEntry[];
}
```

### 2.2 File Structure

```
extension/src/prompts/
├── index.ts              # Prompt registry
├── types.ts              # TypeScript types
├── system/
│   ├── chat.system.ts    # Chat mode system prompt
│   ├── plan.system.ts    # Plan mode system prompt
│   └── act.system.ts     # Act mode system prompt
├── templates/
│   ├── summary.prompt.ts    # Project summary
│   ├── plan-generate.prompt.ts
│   ├── code-create.prompt.ts
│   └── code-modify.prompt.ts
└── __tests__/
    ├── prompts.test.ts
    └── fixtures/
        └── sample-outputs.ts
```

---

## 3. Prompt Registry

### 3.1 Registry Implementation

```typescript
// extension/src/prompts/index.ts

import { PromptDefinition } from './types';
import { CHAT_SYSTEM_PROMPT } from './system/chat.system';
import { PLAN_SYSTEM_PROMPT } from './system/plan.system';
import { SUMMARY_PROMPT } from './templates/summary.prompt';
import { PLAN_GENERATE_PROMPT } from './templates/plan-generate.prompt';
import { CODE_CREATE_PROMPT } from './templates/code-create.prompt';
import { CODE_MODIFY_PROMPT } from './templates/code-modify.prompt';

/**
 * Central registry of all prompts.
 * Enables versioning, testing, and runtime selection.
 */
export const PROMPT_REGISTRY: Record<string, PromptDefinition> = {
  'system.chat.v1': CHAT_SYSTEM_PROMPT,
  'system.plan.v1': PLAN_SYSTEM_PROMPT,
  'template.summary.v1': SUMMARY_PROMPT,
  'template.plan-generate.v1': PLAN_GENERATE_PROMPT,
  'template.code-create.v1': CODE_CREATE_PROMPT,
  'template.code-modify.v1': CODE_MODIFY_PROMPT,
};

/**
 * Get a prompt by ID with variable substitution.
 */
export function getPrompt(
  promptId: string,
  variables: Record<string, string> = {}
): string {
  const definition = PROMPT_REGISTRY[promptId];
  
  if (!definition) {
    throw new Error(`Prompt not found: ${promptId}`);
  }
  
  let prompt = definition.template;
  
  // Substitute variables
  for (const [key, value] of Object.entries(variables)) {
    prompt = prompt.replace(new RegExp(`{{${key}}}`, 'g'), value);
  }
  
  // Warn about unused variables
  const unusedVars = prompt.match(/{{[^}]+}}/g);
  if (unusedVars) {
    console.warn(`Unused variables in prompt ${promptId}:`, unusedVars);
  }
  
  return prompt;
}

/**
 * Get prompt configuration.
 */
export function getPromptConfig(promptId: string) {
  return PROMPT_REGISTRY[promptId]?.config;
}
```

---

## 4. Versioning Strategy

### 4.1 Version Format

```
prompt-id.vMAJOR.MINOR

Examples:
- system.chat.v1      (first version)
- system.chat.v1.1    (minor improvement)
- system.chat.v2      (breaking change)
```

### 4.2 Version Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                   VERSIONING RULES                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MAJOR VERSION (v1 → v2):                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Output format changes                                         │
│  • Required variables change                                     │
│  • Fundamental behavior change                                   │
│  • Requires code changes to handle                              │
│                                                                  │
│  MINOR VERSION (v1.0 → v1.1):                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Improved wording                                              │
│  • Better examples                                               │
│  • Clearer instructions                                          │
│  • Same output format                                            │
│  • Backward compatible                                           │
│                                                                  │
│  KEEP BOTH VERSIONS WHEN:                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • A/B testing quality                                           │
│  • Gradual rollout                                               │
│  • Fallback needed                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Changelog Format

```typescript
interface ChangelogEntry {
  version: string;
  date: string;
  changes: string[];
  author: string;
}

// Example
const changelog: ChangelogEntry[] = [
  {
    version: "1.1",
    date: "2024-01-20",
    changes: [
      "Added explicit JSON format instructions",
      "Improved handling of empty code blocks"
    ],
    author: "TarekRefaei"
  },
  {
    version: "1.0",
    date: "2024-01-15",
    changes: ["Initial version"],
    author: "TarekRefaei"
  }
];
```

---

## 5. Testing Prompts

### 5.1 Test Categories

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROMPT TEST TYPES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TYPE 1: Format Tests                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Does output match expected format?                           │
│  • Can it be parsed without errors?                             │
│  • Are all required fields present?                             │
│                                                                  │
│  TYPE 2: Quality Tests                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Is the output relevant?                                       │
│  • Does it follow instructions?                                 │
│  • Is code syntactically valid?                                 │
│                                                                  │
│  TYPE 3: Regression Tests                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Given same input, is output similar?                         │
│  • Did prompt change break anything?                            │
│                                                                  │
│  TYPE 4: Edge Case Tests                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Empty context                                                 │
│  • Very long context                                             │
│  • Unusual queries                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Test Implementation

```typescript
// extension/src/prompts/__tests__/prompts.test.ts

import { describe, it, expect } from 'vitest';
import { getPrompt, PROMPT_REGISTRY } from '../index';
import { parsePlanOutput } from '../parsers/plan-parser';

describe('Plan Generation Prompt', () => {
  const promptId = 'template.plan-generate.v1';
  
  it('should have all required fields', () => {
    const definition = PROMPT_REGISTRY[promptId];
    
    expect(definition).toBeDefined();
    expect(definition.id).toBe(promptId);
    expect(definition.template).toBeDefined();
    expect(definition.config.temperature).toBeLessThan(0.5);
  });
  
  it('should substitute variables correctly', () => {
    const prompt = getPrompt(promptId, {
      goal: 'Add authentication',
      context: 'React app with Express backend'
    });
    
    expect(prompt).toContain('Add authentication');
    expect(prompt).toContain('React app with Express backend');
    expect(prompt).not.toContain('{{goal}}');
  });
  
  it('should generate parseable output', async () => {
    // This test requires actual LLM - mark as integration test
    // In practice, use recorded responses for unit tests
    const sampleOutput = `
## Plan: Add Authentication

### Overview
Add user authentication to the app.

### Implementation Steps
- [ ] 1. **Create auth service**
  📁 src/auth/auth.service.ts
  └─ Handle JWT tokens
    `;
    
    const parsed = parsePlanOutput(sampleOutput);
    
    expect(parsed.title).toBe('Add Authentication');
    expect(parsed.tasks).toHaveLength(1);
    expect(parsed.tasks[0].filePath).toBe('src/auth/auth.service.ts');
  });
});
```

### 5.3 Golden Output Tests

```typescript
// Store known-good outputs for regression testing
const GOLDEN_OUTPUTS = {
  'plan-generate': {
    input: {
      goal: 'Add login page',
      context: 'React app'
    },
    expectedContains: [
      '## Plan:',
      '### Implementation Steps',
      '- [ ]',
      '📁'
    ],
    expectedFormat: 'markdown'
  }
};

describe('Golden Output Tests', () => {
  for (const [name, golden] of Object.entries(GOLDEN_OUTPUTS)) {
    it(`${name} should match expected format`, async () => {
      const output = await generateWithPrompt(name, golden.input);
      
      for (const expected of golden.expectedContains) {
        expect(output).toContain(expected);
      }
    });
  }
});
```

---

## 6. Prompt Templates

### 6.1 Chat System Prompt

```typescript
// extension/src/prompts/system/chat.system.ts

export const CHAT_SYSTEM_PROMPT: PromptDefinition = {
  id: 'system.chat.v1',
  version: '1.0',
  name: 'Chat Mode System Prompt',
  type: 'system',
  
  config: {
    temperature: 0.7,
  },
  
  template: `You are LocalPilot, an AI coding assistant analyzing a local codebase.

## Your Role
- Answer questions about the codebase
- Explain how code works
- Suggest improvements
- Help plan new features

## Your Context
You have access to indexed code from the project through RAG retrieval.
When code is provided in the context, reference it specifically.

## Guidelines
1. Be concise but thorough
2. Reference specific files and line numbers when relevant
3. Use code blocks with language tags
4. If unsure, say so rather than guessing
5. When suggesting implementation, offer to create a plan

## Format
- Use markdown formatting
- Use \`code\` for inline code
- Use code blocks for multi-line code
- Use bullet points for lists

When the user describes a feature they want to implement, suggest:
"Would you like me to create a detailed plan for this? Click 'Transfer to Plan Mode' to proceed."`,
  
  expectedOutput: {
    format: 'markdown',
  },
  
  onParseFailure: 'error',
  
  description: 'System prompt for chat mode conversations',
  changelog: [
    { version: '1.0', date: '2024-01-15', changes: ['Initial version'], author: 'TarekRefaei' }
  ]
};
```

### 6.2 Plan Generation Prompt

```typescript
// extension/src/prompts/templates/plan-generate.prompt.ts

export const PLAN_GENERATE_PROMPT: PromptDefinition = {
  id: 'template.plan-generate.v1',
  version: '1.0',
  name: 'Plan Generation Template',
  type: 'plan',
  
  config: {
    temperature: 0.2,  // Low for consistency
    maxTokens: 2000,
  },
  
  template: `Create a detailed implementation plan for the following goal.

## Goal
{{goal}}

## Project Context
{{context}}

## Relevant Code
{{rag_chunks}}

## Instructions
Create a step-by-step TODO list with the following EXACT format:

## Plan: [Descriptive Title]

### Overview
[2-3 sentences describing what we're building]

### Implementation Steps

- [ ] 1. **[Task Title]**
  📁 \`[exact/file/path.ext]\`
  ├─ [Specific detail 1]
  └─ [Specific detail 2]

- [ ] 2. **[Task Title]**
  📁 \`[exact/file/path.ext]\`
  └─ [Specific detail]

[Continue for all tasks...]

### Testing
- [ ] [How to verify the implementation]

## Rules
1. Each task MUST have a 📁 file path
2. Tasks should be atomic (one file per task)
3. Use existing project patterns from the context
4. Order tasks by dependency (create before use)
5. Include 3-10 tasks typically

Generate the plan now:`,
  
  expectedOutput: {
    format: 'markdown',
    schema: {
      required: ['## Plan:', '### Implementation Steps', '- [ ]', '📁']
    }
  },
  
  onParseFailure: 'retry',
  
  description: 'Generates structured implementation plan from goal',
  changelog: [
    { version: '1.0', date: '2024-01-15', changes: ['Initial version'], author: 'TarekRefaei' }
  ]
};
```

### 6.3 Code Generation Prompt

```typescript
// extension/src/prompts/templates/code-create.prompt.ts

export const CODE_CREATE_PROMPT: PromptDefinition = {
  id: 'template.code-create.v1',
  version: '1.0',
  name: 'Code Creation Template',
  type: 'code',
  
  config: {
    temperature: 0.2,
    maxTokens: 3000,
  },
  
  template: `Generate code for a new file.

## Task
Create file: \`{{file_path}}\`

## Description
{{task_description}}

## Requirements
{{task_details}}

## Project Patterns
The following code shows patterns used in this project:
{{rag_chunks}}

## Instructions
1. Generate ONLY the file content
2. Include all necessary imports
3. Add JSDoc/docstring comments
4. Follow patterns from the project examples
5. Wrap code in \`\`\`{{language}} code block

Generate the complete file:`,
  
  expectedOutput: {
    format: 'code',
  },
  
  onParseFailure: 'retry',
  
  description: 'Generates code for new file creation',
  changelog: [
    { version: '1.0', date: '2024-01-15', changes: ['Initial version'], author: 'TarekRefaei' }
  ]
};
```

---

## 7. Best Practices

### 7.1 Prompt Writing Guidelines

```
┌─────────────────────────────────────────────────────────────────┐
│                  PROMPT WRITING GUIDELINES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DO:                                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  ✓ Use clear section headers (##, ###)                         │
│  ✓ Provide explicit format examples                             │
│  ✓ List requirements as numbered points                        │
│  ✓ Include negative examples ("Don't do X")                    │
│  ✓ Use consistent variable naming ({{snake_case}})             │
│  ✓ Keep system prompts under 500 tokens                        │
│  ✓ Test with multiple models if possible                       │
│                                                                  │
│  DON'T:                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  ✗ Use ambiguous instructions                                  │
│  ✗ Assume LLM remembers previous context                       │
│  ✗ Include unnecessary context (wastes tokens)                 │
│  ✗ Use complex nested formats                                   │
│  ✗ Forget to specify output format                             │
│  ✗ Skip testing after changes                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Context Window Management

```typescript
/**
 * Assembles prompt with context, respecting token limits.
 */
function assemblePrompt(
  systemPrompt: string,
  userQuery: string,
  ragChunks: Chunk[],
  history: Message[],
  maxTokens: number = 8000
): string {
  // Reserve tokens for each section
  const systemTokens = 500;
  const responseBuffer = 2000;
  const queryTokens = estimateTokens(userQuery);
  
  const availableForContext = maxTokens - systemTokens - responseBuffer - queryTokens;
  
  // Allocate: 60% RAG, 40% history
  const ragBudget = Math.floor(availableForContext * 0.6);
  const historyBudget = Math.floor(availableForContext * 0.4);
  
  // Truncate RAG chunks
  const ragContext = truncateToTokens(
    formatChunks(ragChunks),
    ragBudget
  );
  
  // Truncate history (keep most recent)
  const historyContext = truncateToTokens(
    formatHistory(history.slice(-10)),
    historyBudget
  );
  
  return `${systemPrompt}

## Retrieved Code Context
${ragContext}

## Conversation History
${historyContext}

## Current Query
${userQuery}`;
}
```

### 7.3 Error Recovery

```typescript
/**
 * Handle prompt failures with retry and fallback.
 */
async function executePromptWithRecovery(
  promptId: string,
  variables: Record<string, string>,
  llm: ILLMProvider
): Promise<string> {
  const definition = PROMPT_REGISTRY[promptId];
  const prompt = getPrompt(promptId, variables);
  
  let attempts = 0;
  const maxAttempts = 3;
  
  while (attempts < maxAttempts) {
    attempts++;
    
    try {
      const response = await llm.chat({
        model: 'qwen2.5-coder:7b',
        messages: [{ role: 'user', content: prompt }],
        options: { temperature: definition.config.temperature }
      });
      
      // Validate output format
      validateOutput(response.content, definition.expectedOutput);
      
      return response.content;
      
    } catch (error) {
      console.warn(`Prompt attempt ${attempts} failed:`, error);
      
      if (attempts >= maxAttempts) {
        if (definition.onParseFailure === 'fallback' && definition.fallbackPromptId) {
          return executePromptWithRecovery(
            definition.fallbackPromptId,
            variables,
            llm
          );
        }
        throw error;
      }
      
      // Add clarification for retry
      variables['_retry_hint'] = 'Please follow the format exactly.';
    }
  }
  
  throw new Error('Prompt execution failed');
}
```

---

*Document Version: 1.0.0*

---
````

</details>


## docs/ProjectDocuments/release-policy.md

*Size: 970 bytes | Modified: 2025-12-14T22:05:51.856Z*

<details>
<summary>View code</summary>

````markdown
# LocalPilot – Release and Tagging Policy

## Goals
- Clear restore points per phase
- Verifiable milestones
- Safe reverts

## Tagging
- Use annotated tags for milestones and phases.
- Format: `v<major>.<minor>.<patch>-<label>`
  - Examples:
    - `v0.1.0-phase0` (Phase 0 complete)
    - `v0.2.0-phase1` (Phase 1 complete)
- Use signed tags if you maintain a GPG key: `git tag -s ...`

## Creating a tag
```
# Annotated tag
git tag -a v0.1.1 -m "Short description"

# Signed tag (optional)
git tag -s v0.1.1 -m "Short description"

# Push
git push origin --tags
```

## Phase boundaries
- At the end of each Phase:
  - Commit: `chore(phase<N>): lock Phase <N> implementation`
  - Tag: `v0.<N>.0-phase<N>`

## Reverting
- Use `git revert <sha>` on shared branches.
- To restore a prior state locally:
  - `git reset --hard v0.1.0-phase0`

## Releases (optional)
- GitHub releases can be created for phase tags.
- Include changelog summary and verification checklist.

````

</details>


## docs/ProjectDocuments/security-model.md

*Size: 23,905 bytes | Modified: 2025-12-13T07:48:28.665Z*

<details>
<summary>View code</summary>

````markdown
# 📄 SECURITY_MODEL.md

# LocalPilot - Security Model

> Workspace safety rules and security boundaries for LocalPilot

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Security Specification |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [Security Principles](#1-security-principles)
2. [Threat Model](#2-threat-model)
3. [Workspace Boundaries](#3-workspace-boundaries)
4. [Act Mode Security](#4-act-mode-security)
5. [File Operation Rules](#5-file-operation-rules)
6. [Validation Functions](#6-validation-functions)
7. [Audit & Logging](#7-audit--logging)
8. [Security Checklist](#8-security-checklist)

---

## 1. Security Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                   CORE SECURITY PRINCIPLES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRINCIPLE 1: LEAST PRIVILEGE                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  LocalPilot only accesses what it absolutely needs.            │
│  • Only workspace files (no system files)                       │
│  • Only explicit user-approved operations                       │
│  • No background file modifications                             │
│                                                                  │
│  PRINCIPLE 2: EXPLICIT CONSENT                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Every file modification requires explicit user approval.       │
│  • Show diff before applying                                    │
│  • User clicks "Apply" for each change                          │
│  • Never auto-apply without confirmation                        │
│                                                                  │
│  PRINCIPLE 3: DEFENSE IN DEPTH                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Multiple layers of protection:                                 │
│  • Path validation at input                                      │
│  • Path validation at execution                                  │
│  • Backup before modification                                    │
│  • Audit log of all operations                                   │
│                                                                  │
│  PRINCIPLE 4: FAIL SECURE                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  When in doubt, deny the operation.                             │
│  • Invalid path? Reject.                                         │
│  • Suspicious pattern? Reject.                                   │
│  • Outside workspace? Reject.                                    │
│                                                                  │
│  PRINCIPLE 5: TRANSPARENCY                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  User sees everything LocalPilot does.                          │
│  • All operations logged                                         │
│  • No hidden file changes                                        │
│  • Clear error messages                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Threat Model

### 2.1 Identified Threats

| Threat | Severity | Mitigation |
|--------|----------|------------|
| **Path Traversal** | CRITICAL | Path validation, workspace boundary |
| **Arbitrary File Write** | CRITICAL | Allowlist paths, user approval |
| **Sensitive File Access** | HIGH | Block sensitive file patterns |
| **LLM Injection** | MEDIUM | Sanitize LLM output before use |
| **Denial of Service** | LOW | Rate limiting, timeouts |
| **Data Exfiltration** | LOW | Localhost-only communication |

### 2.2 Trust Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                     TRUST BOUNDARIES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TRUSTED:                                                        │
│  ├── User input (explicit commands)                             │
│  ├── VS Code APIs                                                │
│  └── Local file system (within workspace)                       │
│                                                                  │
│  PARTIALLY TRUSTED:                                              │
│  ├── Ollama responses (sanitize before file ops)                │
│  ├── Python server responses                                     │
│  └── LLM-generated code (require user approval)                 │
│                                                                  │
│  UNTRUSTED:                                                      │
│  ├── LLM-suggested file paths (validate strictly)               │
│  ├── LLM-suggested commands (block in MVP)                      │
│  └── Any path containing traversal patterns                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Workspace Boundaries

### 3.1 Workspace Root Definition

```typescript
// The workspace root is the ONLY allowed base directory
const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;

// All file operations MUST be within this boundary
// Exception: ~/.localpilot/ for index storage (read/write by server only)
```

### 3.2 Allowed Paths

```
┌─────────────────────────────────────────────────────────────────┐
│                      ALLOWED PATHS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ ALLOWED (Read & Write):                                     │
│  ├── {workspace}/**/*                                           │
│  ├── {workspace}/src/**/*                                       │
│  ├── {workspace}/lib/**/*                                       │
│  └── {workspace}/[any subfolder]/**/*                          │
│                                                                  │
│  ✅ ALLOWED (Read Only):                                        │
│  ├── {workspace}/node_modules/** (for indexing)                │
│  ├── {workspace}/.git/** (for future git integration)          │
│  └── {workspace}/package.json, etc.                            │
│                                                                  │
│  ❌ BLOCKED (Never Access):                                     │
│  ├── Anything outside {workspace}/                              │
│  ├── C:\Windows\**                                               │
│  ├── /etc/**                                                     │
│  ├── /usr/**                                                     │
│  ├── ~/** (except ~/.localpilot/ for server)                   │
│  └── Any absolute path not under workspace                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Blocked Patterns

```typescript
// BLOCKED_PATTERNS: Never allow these in any path
const BLOCKED_PATTERNS = [
  // Traversal attempts
  '..',
  '..\\',
  '../',
  
  // Sensitive files
  '.env',
  '.env.local',
  '.env.production',
  'secrets',
  'credentials',
  'private_key',
  'id_rsa',
  '.ssh',
  '.aws',
  '.azure',
  
  // System paths (Windows)
  'C:\\Windows',
  'C:\\Program Files',
  'System32',
  
  // System paths (Unix - for future)
  '/etc/',
  '/usr/',
  '/bin/',
  '/sbin/',
  '/var/',
  '/root/',
  
  // Git internals
  '.git/config',
  '.git/hooks',
  
  // Package manager internals
  'node_modules/.bin',
];
```

---

## 4. Act Mode Security

### 4.1 Act Mode Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACT MODE SECURITY RULES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  RULE 1: No Auto-Execution                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Every task requires explicit "Apply" click.                    │
│  Default: Show preview, wait for approval.                      │
│  Future setting: "Auto-approve" only for create (not modify).   │
│                                                                  │
│  RULE 2: Backup Before Modify                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Before ANY file modification:                                  │
│  1. Create backup in .localpilot/backups/{timestamp}/          │
│  2. Store original content                                       │
│  3. Then apply changes                                           │
│  4. If error, restore from backup                               │
│                                                                  │
│  RULE 3: Path Validation at Every Step                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Validate path:                                                  │
│  • When LLM generates it (Plan mode)                            │
│  • When user approves task                                       │
│  • Immediately before file operation                            │
│                                                                  │
│  RULE 4: No Command Execution (MVP)                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  MVP does NOT execute terminal commands.                        │
│  • No npm install                                                │
│  • No shell commands                                             │
│  • No script execution                                           │
│  Future: Allowlisted commands only with explicit approval.      │
│                                                                  │
│  RULE 5: Size Limits                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Max file size to create: 1MB                                 │
│  • Max files per task: 1                                        │
│  • Max tasks per plan: 50                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Dangerous Operations (Blocked)

```typescript
// BLOCKED_OPERATIONS: Never allow in MVP
const BLOCKED_OPERATIONS = [
  // Shell execution
  'exec',
  'spawn',
  'execSync',
  'spawnSync',
  'system',
  'shell',
  
  // Dangerous commands (for future terminal feature)
  'rm -rf',
  'del /f',
  'format',
  'mkfs',
  'dd',
  ':(){:|:&};:',  // Fork bomb
  
  // Network operations
  'curl',
  'wget',
  'fetch' // (external URLs)
];
```

---

## 5. File Operation Rules

### 5.1 CREATE Operation

```typescript
async function safeCreateFile(
  filePath: string,
  content: string
): Promise<void> {
  // STEP 1: Validate path
  validatePath(filePath);  // Throws if invalid
  
  // STEP 2: Check file doesn't exist
  if (await fileExists(filePath)) {
    throw new Error('File already exists. Use MODIFY instead.');
  }
  
  // STEP 3: Check content size
  if (content.length > MAX_FILE_SIZE) {
    throw new Error(`Content exceeds ${MAX_FILE_SIZE} bytes`);
  }
  
  // STEP 4: Ensure directory exists
  await ensureDirectory(path.dirname(filePath));
  
  // STEP 5: Write file
  await writeFile(filePath, content);
  
  // STEP 6: Log operation
  auditLog('CREATE', filePath, 'success');
}
```

### 5.2 MODIFY Operation

```typescript
async function safeModifyFile(
  filePath: string,
  newContent: string
): Promise<void> {
  // STEP 1: Validate path
  validatePath(filePath);
  
  // STEP 2: Check file exists
  if (!(await fileExists(filePath))) {
    throw new Error('File does not exist. Use CREATE instead.');
  }
  
  // STEP 3: Create backup
  const backupPath = await createBackup(filePath);
  
  try {
    // STEP 4: Write new content
    await writeFile(filePath, newContent);
    
    // STEP 5: Log success
    auditLog('MODIFY', filePath, 'success', { backupPath });
  } catch (error) {
    // STEP 6: Restore on failure
    await restoreFromBackup(backupPath, filePath);
    auditLog('MODIFY', filePath, 'failed_restored', { error });
    throw error;
  }
}
```

### 5.3 DELETE Operation

```typescript
async function safeDeleteFile(filePath: string): Promise<void> {
  // STEP 1: Validate path
  validatePath(filePath);
  
  // STEP 2: Check file exists
  if (!(await fileExists(filePath))) {
    throw new Error('File does not exist');
  }
  
  // STEP 3: Create backup (delete is reversible!)
  const backupPath = await createBackup(filePath);
  
  // STEP 4: Delete file
  await deleteFile(filePath);
  
  // STEP 5: Log operation
  auditLog('DELETE', filePath, 'success', { backupPath });
}
```
---

### 5.4 Backup Cleanup

Backups are automatically cleaned to prevent disk space issues:

```typescript
// Cleanup policy (checked on extension activation)
const BACKUP_POLICY = {
  maxAgeDays: 7,          // Delete backups older than 7 days
  maxTotalSizeMB: 100,    // Delete oldest when total exceeds 100MB
  cleanupOnStartup: true  // Run cleanup on every activation
};
```

Cleanup order:
1. Delete all backups older than maxAgeDays
2. If still over size limit, delete oldest until under limit
3. Never delete backups less than 1 hour old

---

## 6. Validation Functions

### 6.1 Path Validation

```typescript
/**
 * Validates that a path is safe to access.
 * Throws SecurityError if path is invalid or dangerous.
 */
function validatePath(filePath: string): void {
  const workspaceRoot = getWorkspaceRoot();
  
  if (!workspaceRoot) {
    throw new SecurityError('No workspace open');
  }
  
  // Normalize path to absolute
  const absolutePath = path.resolve(workspaceRoot, filePath);
  const normalizedPath = path.normalize(absolutePath);
  
  // CHECK 1: Must be within workspace
  if (!normalizedPath.startsWith(workspaceRoot)) {
    throw new SecurityError(
      `Path "${filePath}" is outside workspace boundary`,
      { filePath, workspaceRoot }
    );
  }
  
  // CHECK 2: No blocked patterns
  for (const pattern of BLOCKED_PATTERNS) {
    if (normalizedPath.toLowerCase().includes(pattern.toLowerCase())) {
      throw new SecurityError(
        `Path contains blocked pattern: ${pattern}`,
        { filePath, pattern }
      );
    }
  }
  
  // CHECK 3: No null bytes (injection prevention)
  if (filePath.includes('\0')) {
    throw new SecurityError('Path contains null byte');
  }
  
  // CHECK 4: Reasonable length
  if (filePath.length > 500) {
    throw new SecurityError('Path too long');
  }
}
```

### 6.2 Content Validation

```typescript
/**
 * Validates content before writing to file.
 */
function validateContent(content: string, filePath: string): void {
  // CHECK 1: Size limit
  const MAX_SIZE = 1024 * 1024; // 1MB
  if (content.length > MAX_SIZE) {
    throw new SecurityError(`Content exceeds ${MAX_SIZE} bytes`);
  }
  
  // CHECK 2: No suspicious patterns in executable files
  const executableExtensions = ['.sh', '.bat', '.cmd', '.ps1'];
  const ext = path.extname(filePath).toLowerCase();
  
  if (executableExtensions.includes(ext)) {
    // Extra scrutiny for scripts
    const dangerousPatterns = ['rm -rf', 'format', ':(){', 'del /f'];
    for (const pattern of dangerousPatterns) {
      if (content.includes(pattern)) {
        throw new SecurityError(
          `Script contains dangerous pattern: ${pattern}`
        );
      }
    }
  }
}
```

---

## 7. Audit & Logging

### 7.1 Audit Log Structure

```typescript
interface AuditEntry {
  timestamp: Date;
  operation: 'CREATE' | 'MODIFY' | 'DELETE' | 'READ';
  filePath: string;
  result: 'success' | 'failed' | 'blocked';
  details?: {
    backupPath?: string;
    error?: string;
    userId?: string;
  };
}

// Log location: {workspace}/.localpilot/audit.log
```

### 7.2 Audit Log Implementation

```typescript
function auditLog(
  operation: string,
  filePath: string,
  result: string,
  details?: Record<string, unknown>
): void {
  const entry = {
    timestamp: new Date().toISOString(),
    operation,
    filePath,
    result,
    details
  };
  
  // Log to output channel
  outputChannel.appendLine(JSON.stringify(entry));
  
  // Log to file (async, don't block)
  appendToAuditFile(entry).catch(console.error);
}
```

---

## 8. Security Checklist

### For Every File Operation

```
┌─────────────────────────────────────────────────────────────────┐
│                  PRE-OPERATION CHECKLIST                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  □ Path validated against workspace root                        │
│  □ Path checked for blocked patterns                            │
│  □ Path normalized (no ../ remaining)                           │
│  □ User has approved this operation                             │
│  □ Backup created (for MODIFY/DELETE)                           │
│  □ Content validated (size, patterns)                           │
│  □ Operation logged to audit                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### For Code Review

```
┌─────────────────────────────────────────────────────────────────┐
│                  SECURITY CODE REVIEW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  □ No direct file system access (use IFileSystem interface)    │
│  □ All paths go through validatePath()                          │
│  □ No shell execution                                            │
│  □ No external network calls                                     │
│  □ User approval required before changes                        │
│  □ Errors don't leak sensitive paths                            │
│  □ Audit logging present                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Document Version: 1.0.0*
````

</details>


## docs/ProjectDocuments/state-model.md

*Size: 35,743 bytes | Modified: 2025-12-13T07:39:52.380Z*

<details>
<summary>View code</summary>

````markdown
# 📄 STATE_MODEL.md

# LocalPilot - State Model

> Persistence strategy and state scope definitions

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | State Management Specification |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [State Overview](#1-state-overview)
2. [State Scopes](#2-state-scopes)
3. [State Categories](#3-state-categories)
4. [Storage Locations](#4-storage-locations)
5. [Lifecycle Management](#5-lifecycle-management)
6. [Recovery Strategies](#6-recovery-strategies)
7. [State Schema](#7-state-schema)

---

## 1. State Overview

### 1.1 What is State?

```
┌─────────────────────────────────────────────────────────────────┐
│                     STATE IN LOCALPILOT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  State = Any data that needs to survive beyond immediate use    │
│                                                                  │
│  EXAMPLES:                                                       │
│  • Project index (embeddings, metadata)                         │
│  • Current chat messages                                         │
│  • Plan being edited                                             │
│  • Act mode progress                                             │
│  • User settings                                                 │
│  • Connection status                                             │
│                                                                  │
│  KEY QUESTION FOR EACH STATE:                                    │
│  "What happens to this data when X occurs?"                     │
│                                                                  │
│  X = VS Code reload, extension restart, computer restart,       │
│      crash, user switches project                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 State Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                    STATE PRINCIPLES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRINCIPLE 1: Explicit Scope                                     │
│  Every piece of state has a clearly defined scope.              │
│  No ambiguity about when data persists or clears.              │
│                                                                  │
│  PRINCIPLE 2: Graceful Degradation                              │
│  If state is lost, system remains functional.                   │
│  User can re-index, restart conversation, etc.                  │
│                                                                  │
│  PRINCIPLE 3: User Expectations                                  │
│  State behavior matches what users expect.                      │
│  Index persists. Chat clears on restart (MVP).                  │
│                                                                  │
│  PRINCIPLE 4: Minimal Persistence                               │
│  Don't persist what doesn't need persisting.                   │
│  Reduces complexity and storage.                                │
│                                                                  │
│  PRINCIPLE 5: Recovery Path                                      │
│  Every critical state has a recovery mechanism.                 │
│  User is never permanently stuck.                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. State Scopes

### 2.1 Scope Definitions

| Scope | Survives Reload | Survives Restart | Survives Reboot | Survives Reinstall |
|-------|-----------------|------------------|-----------------|-------------------|
| **Memory** | ❌ | ❌ | ❌ | ❌ |
| **Session** | ✅ | ❌ | ❌ | ❌ |
| **Workspace** | ✅ | ✅ | ✅ | ❌ |
| **Global** | ✅ | ✅ | ✅ | ✅* |

*Global survives reinstall if user data folder preserved

### 2.2 Scope Descriptions

```
┌─────────────────────────────────────────────────────────────────┐
│                      STATE SCOPES                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MEMORY SCOPE                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Lives in: JavaScript/Python runtime memory                    │
│  Cleared when: Any restart, reload, or crash                   │
│  Use for: Temporary UI state, streaming buffers                │
│                                                                  │
│  Examples:                                                       │
│  • Current streaming response                                    │
│  • WebSocket connection object                                   │
│  • Temporary diff calculations                                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SESSION SCOPE                                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Lives in: VS Code extension storage (session)                  │
│  Cleared when: VS Code closes                                    │
│  Survives: Window reload (Ctrl+Shift+P > Reload)               │
│  Use for: Current conversation, unsaved work                   │
│                                                                  │
│  Examples:                                                       │
│  • Chat message history (MVP)                                   │
│  • Current plan draft                                            │
│  • Act mode progress                                             │
│  • Undo/redo stacks                                              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  WORKSPACE SCOPE                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Lives in: {workspace}/.localpilot/ or                         │
│            ~/.localpilot/indexes/{project_id}/                  │
│  Cleared when: User explicitly clears or deletes folder        │
│  Survives: Everything except uninstall/delete                  │
│  Use for: Index, project metadata, backups                     │
│                                                                  │
│  Examples:                                                       │
│  • ChromaDB index                                                │
│  • File hash tracking                                            │
│  • Project summary cache                                         │
│  • File backups                                                  │
│  • Audit logs                                                    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GLOBAL SCOPE                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Lives in: VS Code global storage or ~/.localpilot/settings    │
│  Cleared when: Never (user must manually delete)               │
│  Use for: User preferences, cross-project settings             │
│                                                                  │
│  Examples:                                                       │
│  • Ollama URL setting                                            │
│  • Default model selections                                      │
│  • UI preferences                                                │
│  • Onboarding completion flag                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. State Categories

### 3.1 Complete State Map

```
┌─────────────────────────────────────────────────────────────────┐
│                     STATE CATEGORY MAP                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STATE                        │ SCOPE      │ STORAGE             │
│  ════════════════════════════════════════════════════════════   │
│                                                                  │
│  CONNECTION STATE                                                │
│  ─────────────────────────────────────────────────────────────  │
│  Ollama connection status     │ Memory     │ Runtime             │
│  Server connection status     │ Memory     │ Runtime             │
│  Available models list        │ Memory     │ Runtime (cache)     │
│                                                                  │
│  UI STATE                                                        │
│  ─────────────────────────────────────────────────────────────  │
│  Current mode (chat/plan/act) │ Session    │ Extension storage   │
│  Panel visibility             │ Session    │ VS Code handles     │
│  Scroll positions             │ Memory     │ Runtime             │
│                                                                  │
│  CHAT STATE                                                      │
│  ─────────────────────────────────────────────────────────────  │
│  Message history              │ Session    │ Extension storage   │
│  Current streaming message    │ Memory     │ Runtime             │
│  RAG context for session      │ Memory     │ Runtime             │
│                                                                  │
│  PLAN STATE                                                      │
│  ─────────────────────────────────────────────────────────────  │
│  Current plan draft           │ Session    │ Extension storage   │
│  Plan edit history            │ Memory     │ Runtime             │
│                                                                  │
│  ACT STATE                                                       │
│  ─────────────────────────────────────────────────────────────  │
│  Execution progress           │ Session    │ Extension storage   │
│  Current task index           │ Session    │ Extension storage   │
│  Generated code (pending)     │ Memory     │ Runtime             │
│  TODO.md file                 │ Workspace  │ Workspace file      │
│                                                                  │
│  INDEX STATE                                                     │
│  ─────────────────────────────────────────────────────────────  │
│  Vector embeddings            │ Workspace  │ ChromaDB            │
│  Chunk metadata               │ Workspace  │ ChromaDB            │
│  File hashes                  │ Workspace  │ JSON file           │
│  Index metadata               │ Workspace  │ JSON file           │
│  Indexing progress            │ Memory     │ Runtime             │
│                                                                  │
│  SETTINGS STATE                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  User preferences             │ Global     │ VS Code settings    │
│  Ollama URL                   │ Global     │ VS Code settings    │
│  Model selections             │ Global     │ VS Code settings    │
│                                                                  │
│  BACKUP STATE                                                    │
│  ─────────────────────────────────────────────────────────────  │
│  File backups                 │ Workspace  │ .localpilot/backups │
│  Audit log                    │ Workspace  │ .localpilot/audit   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Storage Locations

### 4.1 File System Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                    STORAGE LOCATIONS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GLOBAL STORAGE (~/.localpilot/)                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ~/.localpilot/                                                  │
│  ├── settings.json           # Global settings (if needed)     │
│  ├── indexes/                # All project indexes              │
│  │   ├── {project-id-1}/                                        │
│  │   │   ├── chroma/         # ChromaDB files                   │
│  │   │   ├── metadata.json   # Index metadata                   │
│  │   │   └── hashes.json     # File hash tracking               │
│  │   └── {project-id-2}/                                        │
│  │       └── ...                                                 │
│  └── logs/                   # Global logs                       │
│      └── server.log                                              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  WORKSPACE STORAGE ({workspace}/.localpilot/)                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  {workspace}/                                                    │
│  ├── .localpilot/            # LocalPilot workspace data        │
│  │   ├── backups/            # File backups from Act mode       │
│  │   │   └── {timestamp}/    # Timestamped backup folder        │
│  │   │       └── {file}      # Backed up file                   │
│  │   └── audit.log           # Audit trail                      │
│  └── TODO.md                 # Generated by Act mode            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  EXTENSION STORAGE (VS Code managed)                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  context.workspaceState      # Session data (per workspace)     │
│  context.globalState         # Global data (all workspaces)     │
│                                                                  │
│  Used for:                                                       │
│  • Chat history (session)                                        │
│  • Current plan (session)                                        │
│  • Act progress (session)                                        │
│  • UI state (session)                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Project ID Generation

```typescript
/**
 * Generate unique project ID from workspace path.
 * Used to isolate indexes between projects.
 */
function generateProjectId(workspacePath: string): string {
  // Hash the absolute path for uniqueness
  const hash = crypto
    .createHash('sha256')
    .update(workspacePath)
    .digest('hex')
    .substring(0, 16);
  
  // Include folder name for readability
  const folderName = path.basename(workspacePath)
    .replace(/[^a-zA-Z0-9]/g, '_')
    .substring(0, 20);
  
  return `${folderName}_${hash}`;
  // Example: "my_project_a1b2c3d4e5f6g7h8"
}
```

---

## 5. Lifecycle Management

### 5.1 Extension Activation

```typescript
/**
 * State initialization on extension activation
 */
async function initializeState(context: vscode.ExtensionContext) {
  // 1. Load global settings
  const settings = loadGlobalSettings(context.globalState);
  
  // 2. Check for existing session state
  const sessionState = context.workspaceState.get('localpilot_session');
  
  // 3. Check for existing index
  const projectId = generateProjectId(getWorkspaceRoot());
  const indexExists = await checkIndexExists(projectId);
  
  // 4. Initialize stores with recovered state
  initializeStores({
    settings,
    sessionState,
    indexExists
  });
  
  // 5. Determine initial mode
  if (!indexExists) {
    setMode('onboarding');
  } else if (sessionState?.mode) {
    setMode(sessionState.mode);
  } else {
    setMode('chat');
  }
}
```

### 5.2 State Save Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    STATE SAVE POINTS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AUTOMATIC SAVES:                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Session state saved when:                                       │
│  • User sends a message (save chat history)                     │
│  • Plan is generated (save plan)                                │
│  • Task completes (save progress)                               │
│  • Mode changes (save current mode)                             │
│  • Every 30 seconds (debounced auto-save)                       │
│                                                                  │
│  Index state saved when:                                         │
│  • Indexing completes (ChromaDB persists)                       │
│  • Sync completes (update hashes)                               │
│  • File modified via Act (trigger re-index)                     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SAVE IMPLEMENTATION:                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  // Debounced save to avoid excessive writes                    │
│  const saveSessionState = debounce(async () => {                │
│    const state = {                                               │
│      mode: appStore.getState().mode,                            │
│      chat: chatStore.getState().messages,                       │
│      plan: planStore.getState().plan,                           │
│      act: actStore.getState().progress,                         │
│      savedAt: new Date().toISOString()                          │
│    };                                                            │
│    await context.workspaceState.update('localpilot_session', state);│
│  }, 1000);                                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Extension Deactivation

```typescript
/**
 * State cleanup on extension deactivation
 */
async function deactivate() {
  // 1. Save final session state
  await saveSessionState.flush(); // Force immediate save
  
  // 2. Close WebSocket connections
  await closeConnections();
  
  // 3. ChromaDB auto-persists, no action needed
  
  // 4. Log deactivation
  console.log('LocalPilot deactivated, state saved');
}
```

---

## 6. Recovery Strategies

### 6.1 Recovery Matrix

| Scenario | State Lost | Recovery Action |
|----------|------------|-----------------|
| Window reload | Memory only | Session restores automatically |
| VS Code restart | Memory + Session | User re-indexes or continues fresh |
| Extension crash | Memory + partial Session | Last auto-save restored |
| Index corruption | Workspace index | User re-indexes (button provided) |
| Settings lost | Global settings | Defaults applied, user reconfigures |

### 6.2 Recovery Implementations

```
┌─────────────────────────────────────────────────────────────────┐
│                   RECOVERY STRATEGIES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SCENARIO 1: Crash During Indexing                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Detection: Index metadata has "status: indexing"              │
│  Recovery:                                                       │
│  1. Show message: "Previous indexing was interrupted"           │
│  2. Offer: "Resume" or "Start Fresh"                            │
│  3. Resume: Continue from last saved hash                       │
│  4. Fresh: Delete partial index, start over                    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SCENARIO 2: Crash During Act Mode                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Detection: Session state has incomplete act progress           │
│  Recovery:                                                       │
│  1. Show message: "Previous execution was interrupted"          │
│  2. Show: Which tasks completed, which pending                  │
│  3. Offer: "Continue from task X" or "Discard"                 │
│  4. Backups are available for any modified files               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SCENARIO 3: Index Corruption                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Detection: ChromaDB fails to load or query                    │
│  Recovery:                                                       │
│  1. Show error: "Index appears corrupted"                       │
│  2. Offer: "Re-index Project" button                           │
│  3. Delete corrupted index folder                               │
│  4. Start fresh indexing                                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SCENARIO 4: Session State Corruption                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Detection: JSON parse fails or schema mismatch                 │
│  Recovery:                                                       │
│  1. Log error for debugging                                     │
│  2. Clear corrupted session state                               │
│  3. Start with fresh session                                    │
│  4. Index is preserved (different storage)                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. State Schema

### 7.1 Session State Schema

```typescript
interface SessionState {
  version: string;  // Schema version for migrations
  savedAt: string;  // ISO timestamp
  
  mode: 'onboarding' | 'chat' | 'plan' | 'act';
  
  chat: {
    messages: Message[];
    lastQuery?: string;
  };
  
  plan: {
    current: Plan | null;
    isDirty: boolean;  // Has unsaved changes
  };
  
  act: {
    plan: Plan | null;
    currentTaskIndex: number;
    status: 'idle' | 'running' | 'paused' | 'completed';
    completedTaskIds: string[];
  };
}

// Example
const sessionState: SessionState = {
  version: "1.0.0",
  savedAt: "2024-01-15T10:30:00Z",
  mode: "chat",
  chat: {
    messages: [
      { id: "1", role: "assistant", content: "Welcome!", timestamp: "..." },
      { id: "2", role: "user", content: "How does auth work?", timestamp: "..." }
    ]
  },
  plan: { current: null, isDirty: false },
  act: { plan: null, currentTaskIndex: -1, status: "idle", completedTaskIds: [] }
};
```

### 7.2 Index Metadata Schema

```typescript
interface IndexMetadata {
  version: string;
  projectId: string;
  workspacePath: string;
  
  status: 'indexing' | 'indexed' | 'error';
  
  createdAt: string;
  updatedAt: string;
  
  stats: {
    filesCount: number;
    chunksCount: number;
    languages: string[];
    totalTokens: number;
  };
  
  lastError?: string;
}

// Stored at: ~/.localpilot/indexes/{projectId}/metadata.json
```

### 7.3 File Hash Schema

```typescript
interface FileHashes {
  version: string;
  updatedAt: string;
  
  files: {
    [relativePath: string]: {
      hash: string;      // SHA256 of content
      indexedAt: string; // When this version was indexed
      chunkIds: string[]; // IDs of chunks from this file
    };
  };
}

// Stored at: ~/.localpilot/indexes/{projectId}/hashes.json
```
---

## 8. Execution Recovery

### 8.1 Checkpoint Strategy

During Act mode execution, checkpoints are saved after each task:

```typescript
interface ExecutionCheckpoint {
  planId: string;
  completedTaskIds: string[];
  currentTaskId: string | null;
  status: 'running' | 'paused' | 'interrupted';
  timestamp: Date;
}
```

### 8.2 Recovery Flow

On extension activation:
1. Check for `execution_checkpoint` in storage
2. If status is `interrupted`:
   - Prompt user: "Resume" or "Discard"
   - Resume continues from next pending task
   - Discard clears checkpoint

### 8.3 Backup Retention Policy

```typescript
interface BackupPolicy {
  maxAgeDays: 7,
  maxTotalSizeMB: 100,
  cleanupOnStartup: true
}
```

Cleanup runs on extension activation, removing backups older than 7 days
or when total size exceeds 100MB (oldest first).

---

*Document Version: 1.0.0*

---
````

</details>


## docs/ProjectDocuments/structure.md

*Size: 78,323 bytes | Modified: 2025-12-13T17:39:27.328Z*

<details>
<summary>View code</summary>

````markdown
# 📄 PROJECT_STRUCTURE.md (Complete Updated Version)

```markdown
# 📄 PROJECT_STRUCTURE.md

# LocalPilot - Project Structure

> Complete folder structure and file organization for the LocalPilot project

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Project Structure Specification |
| **Related To** | PROJECT_OVERVIEW.md, ARCHITECTURE.md |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |
| **Version** | 1.1.0 |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Repository Root Structure](#2-repository-root-structure)
3. [VS Code Extension Structure](#3-vs-code-extension-structure)
4. [Python RAG Server Structure](#4-python-rag-server-structure)
5. [Scripts Folder](#5-scripts-folder)
6. [Storage Locations](#6-storage-locations)
7. [Configuration Files](#7-configuration-files)
8. [File Naming Conventions](#8-file-naming-conventions)
9. [Import Rules](#9-import-rules)
10. [AI Agent Instructions](#10-ai-agent-instructions)

---

## 1. Overview

### Project Type: Monorepo

LocalPilot uses a **monorepo** structure containing two main packages:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONOREPO STRUCTURE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LocalPilot/                                                     │
│  ├── extension/          ← VS Code Extension (TypeScript)       │
│  ├── server/             ← Python RAG Server                    │
│  ├── docs/               ← Documentation                        │
│  ├── scripts/            ← Build & utility scripts              │
│  └── [config files]      ← Root configuration                   │
│                                                                  │
│  WHY MONOREPO?                                                   │
│  • Single repository for all code                               │
│  • Easier to keep extension and server in sync                  │
│  • Shared documentation                                          │
│  • Single git history                                            │
│  • Simpler for solo developer                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Directories Summary

| Directory | Purpose | Language |
|-----------|---------|----------|
| `extension/` | VS Code extension with React WebView | TypeScript |
| `server/` | RAG server with indexing pipeline | Python |
| `docs/` | All project documentation | Markdown |
| `scripts/` | Build, setup, and utility scripts | PowerShell/Bash |
| `.vscode/` | VS Code workspace settings | JSON |
| `.github/` | GitHub Actions and templates | YAML |

---

## 2. Repository Root Structure

```
LocalPilot/
│
├── 📁 extension/                    # VS Code Extension (TypeScript/React)
│   └── [See Section 3 for details]
│
├── 📁 server/                       # Python RAG Server
│   └── [See Section 4 for details]
│
├── 📁 scripts/                      # Build and utility scripts
│   └── [See Section 5 for details]
│
├── 📁 docs/                         # Documentation
│   ├── 📁 ProjectDocuments/         # Main project documentation
│   │   ├── 📄 overview.md           # Master project document
│   │   ├── 📄 architecture.md       # System architecture
│   │   ├── 📄 structure.md          # This document
│   │   ├── 📄 development-setup.md  # Environment setup guide
│   │   ├── 📄 indexing-spec.md      # Indexing quality contract
│   │   ├── 📄 security-model.md     # Security boundaries
│   │   ├── 📄 state-model.md        # State management spec
│   │   ├── 📄 prompt-engineer.md    # Prompt templates
│   │   ├── 📄 task0-phase.md        # Phase 0 tasks
│   │   ├── 📄 webview-protocol.md   # WebView message protocol
│   │   ├── 📄 testing-strategy.md   # Testing approach
│   │   └── 📄 troubleshooting.md    # Common issues & solutions
│   │
│   ├── 📁 decisions/                # Architecture Decision Records
│   │   ├── 📄 000-template.md       # ADR template
│   │   ├── 📄 001-monorepo-structure.md
│   │   ├── 📄 002-llamaindex-over-langchain.md
│   │   └── 📄 003-chromadb-for-vectors.md
│   │
│   └── 📁 images/                   # Documentation images
│       ├── 📷 architecture-diagram.png
│       ├── 📷 workflow-diagram.png
│       └── 📁 ui-mockups/
│
├── 📁 .github/                      # GitHub configuration
│   ├── 📁 workflows/                # GitHub Actions
│   │   ├── 📄 ci.yml                # Continuous Integration
│   │   ├── 📄 extension-build.yml   # Extension build/test
│   │   └── 📄 server-build.yml      # Server build/test
│   ├── 📄 ISSUE_TEMPLATE.md
│   └── 📄 PULL_REQUEST_TEMPLATE.md
│
├── 📁 .vscode/                      # VS Code workspace settings
│   ├── 📄 settings.json             # Editor settings
│   ├── 📄 launch.json               # Debug configurations
│   ├── 📄 tasks.json                # Build tasks
│   └── 📄 extensions.json           # Recommended extensions
│
├── 📄 .gitignore                    # Git ignore rules
├── 📄 .editorconfig                 # Editor configuration
├── 📄 README.md                     # Repository README
├── 📄 LICENSE                       # License file (MIT)
├── 📄 CHANGELOG.md                  # Version changelog
└── 📄 CONTRIBUTING.md               # Contribution guidelines
```

---

## 3. VS Code Extension Structure

### Complete Extension Folder Structure

```
extension/
│
├── 📁 src/                          # Source code
│   │
│   ├── 📁 core/                     # Core domain layer (no external dependencies)
│   │   │
│   │   ├── 📁 entities/             # Business entities
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 project.entity.ts           # Project representation
│   │   │   ├── 📄 message.entity.ts           # Chat message
│   │   │   ├── 📄 plan.entity.ts              # Plan with tasks
│   │   │   ├── 📄 task.entity.ts              # Individual task
│   │   │   ├── 📄 chunk.entity.ts             # Retrieved code chunk
│   │   │   └── 📄 file-change.entity.ts       # File modification
│   │   │
│   │   ├── 📁 interfaces/           # Contracts/Ports (abstract)
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 llm-provider.interface.ts      # LLM operations
│   │   │   ├── 📄 rag-provider.interface.ts      # RAG operations
│   │   │   ├── 📄 file-system.interface.ts       # File operations
│   │   │   ├── 📄 indexer.interface.ts           # Indexing operations
│   │   │   └── 📄 settings.interface.ts          # Settings operations
│   │   │
│   │   ├── 📁 errors/               # Custom error types
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 base.error.ts                 # Base error class
│   │   │   ├── 📄 ollama.error.ts               # Ollama-specific errors
│   │   │   ├── 📄 indexing.error.ts             # Indexing errors
│   │   │   ├── 📄 server.error.ts               # Python server errors
│   │   │   └── 📄 file-operation.error.ts       # File operation errors
│   │   │
│   │   └── 📁 types/                # Shared type definitions
│   │       ├── 📄 index.ts          # Public exports
│   │       ├── 📄 mode.types.ts                 # Chat/Plan/Act modes
│   │       ├── 📄 ollama.types.ts               # Ollama API types
│   │       └── 📄 events.types.ts               # Event types
│   │
│   ├── 📁 features/                 # Feature modules (use cases)
│   │   │
│   │   ├── 📁 indexing/             # Indexing feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 indexing.service.ts           # Main indexing logic
│   │   │   ├── 📄 sync.service.ts               # Smart sync logic
│   │   │   ├── 📄 progress-reporter.ts          # Progress updates
│   │   │   └── 📁 __tests__/        # Feature tests
│   │   │       ├── 📄 indexing.service.test.ts
│   │   │       └── 📄 sync.service.test.ts
│   │   │
│   │   ├── 📁 chat/                 # Chat mode feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 chat.service.ts               # Chat logic
│   │   │   ├── 📄 context-builder.ts            # RAG context assembly
│   │   │   ├── 📄 message-handler.ts            # Message processing
│   │   │   ├── 📄 summary-generator.ts          # Project summary
│   │   │   └── 📁 __tests__/
│   │   │       ├── 📄 chat.service.test.ts
│   │   │       └── 📄 context-builder.test.ts
│   │   │
│   │   ├── 📁 plan/                 # Plan mode feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 plan.service.ts               # Plan generation
│   │   │   ├── 📄 plan-parser.ts                # Parse LLM output to Plan
│   │   │   ├── 📄 task-extractor.ts             # Extract tasks from plan
│   │   │   └── 📁 __tests__/
│   │   │       ├── 📄 plan.service.test.ts
│   │   │       └── 📄 plan-parser.test.ts
│   │   │
│   │   ├── 📁 act/                  # Act mode feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 act.service.ts                # Act orchestration
│   │   │   ├── 📄 task-executor.ts              # Execute single task
│   │   │   ├── 📄 code-generator.ts             # Generate code for task
│   │   │   ├── 📄 diff-generator.ts             # Generate file diffs
│   │   │   ├── 📄 file-writer.ts                # Write files safely
│   │   │   ├── 📄 backup-manager.ts             # Manage file backups
│   │   │   └── 📁 __tests__/
│   │   │       ├── 📄 act.service.test.ts
│   │   │       └── 📄 task-executor.test.ts
│   │   │
│   │   ├── 📁 ollama/               # Ollama integration feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 ollama.service.ts             # Main Ollama service
│   │   │   ├── 📄 connection-manager.ts         # Health checks
│   │   │   ├── 📄 model-manager.ts              # Model listing/selection
│   │   │   ├── 📄 stream-handler.ts             # Handle streaming responses
│   │   │   └── 📁 __tests__/
│   │   │       ├── 📄 ollama.service.test.ts
│   │   │       └── 📄 connection-manager.test.ts
│   │   │
│   │   └── 📁 settings/             # Settings feature
│   │       ├── 📄 README.md
│   │       ├── 📄 index.ts
│   │       ├── 📄 settings.service.ts           # Settings management
│   │       ├── 📄 default-settings.ts           # Default values
│   │       └── 📁 __tests__/
│   │           └── 📄 settings.service.test.ts
│   │
│   ├── 📁 infrastructure/           # External adapters (implementations)
│   │   │
│   │   ├── 📁 vscode/               # VS Code API adapters
│   │   │   ├── 📄 index.ts
│   │   │   ├── 📄 file-system.adapter.ts        # Implements IFileSystem
│   │   │   ├── 📄 settings.adapter.ts           # Implements ISettings
│   │   │   ├── 📄 output-channel.ts             # Logging
│   │   │   └── 📄 status-bar.ts                 # Status bar management
│   │   │
│   │   ├── 📁 http/                 # HTTP client for Python server
│   │   │   ├── 📄 index.ts
│   │   │   ├── 📄 api-client.ts                 # HTTP client wrapper
│   │   │   ├── 📄 endpoints.ts                  # API endpoint definitions
│   │   │   └── 📄 request-builder.ts            # Request construction
│   │   │
│   │   └── 📁 websocket/            # WebSocket for streaming
│   │       ├── 📄 index.ts
│   │       ├── 📄 ws-client.ts                  # WebSocket client
│   │       └── 📄 stream-processor.ts           # Process incoming streams
│   │
│   ├── 📁 ui/                       # Presentation layer
│   │   │
│   │   ├── 📁 webview/              # React WebView application
│   │   │   ├── 📄 index.tsx         # React entry point
│   │   │   ├── 📄 App.tsx           # Main App component
│   │   │   │
│   │   │   ├── 📁 components/       # Reusable UI components
│   │   │   │   ├── 📁 common/       # Shared components
│   │   │   │   │   ├── 📄 Button.tsx
│   │   │   │   │   ├── 📄 Input.tsx
│   │   │   │   │   ├── 📄 Card.tsx
│   │   │   │   │   ├── 📄 Progress.tsx
│   │   │   │   │   ├── 📄 Spinner.tsx
│   │   │   │   │   ├── 📄 Badge.tsx
│   │   │   │   │   ├── 📄 Tabs.tsx
│   │   │   │   │   ├── 📄 CodeBlock.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   ├── 📁 chat/         # Chat-specific components
│   │   │   │   │   ├── 📄 ChatContainer.tsx
│   │   │   │   │   ├── 📄 MessageList.tsx
│   │   │   │   │   ├── 📄 MessageItem.tsx
│   │   │   │   │   ├── 📄 ChatInput.tsx
│   │   │   │   │   ├── 📄 TransferButton.tsx
│   │   │   │   │   ├── 📄 RagContextPanel.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   ├── 📁 plan/         # Plan-specific components
│   │   │   │   │   ├── 📄 PlanContainer.tsx
│   │   │   │   │   ├── 📄 PlanHeader.tsx
│   │   │   │   │   ├── 📄 TaskList.tsx
│   │   │   │   │   ├── 📄 TaskItem.tsx
│   │   │   │   │   ├── 📄 PlanActions.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   ├── 📁 act/          # Act-specific components
│   │   │   │   │   ├── 📄 ActContainer.tsx
│   │   │   │   │   ├── 📄 ProgressTracker.tsx
│   │   │   │   │   ├── 📄 CurrentTask.tsx
│   │   │   │   │   ├── 📄 CodePreview.tsx
│   │   │   │   │   ├── 📄 DiffView.tsx
│   │   │   │   │   ├── 📄 TaskControls.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   ├── 📁 onboarding/   # Onboarding components
│   │   │   │   │   ├── 📄 OnboardingScreen.tsx
│   │   │   │   │   ├── 📄 OllamaStatus.tsx
│   │   │   │   │   ├── 📄 ServerStatus.tsx
│   │   │   │   │   ├── 📄 IndexingProgress.tsx
│   │   │   │   │   ├── 📄 WelcomeMessage.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   └── 📁 layout/       # Layout components
│   │   │   │       ├── 📄 Header.tsx
│   │   │   │       ├── 📄 TabBar.tsx
│   │   │   │       ├── 📄 StatusFooter.tsx
│   │   │   │       └── 📄 index.ts
│   │   │   │
│   │   │   ├── 📁 hooks/            # Custom React hooks
│   │   │   │   ├── 📄 useChat.ts
│   │   │   │   ├── 📄 usePlan.ts
│   │   │   │   ├── 📄 useAct.ts
│   │   │   │   ├── 📄 useIndexing.ts
│   │   │   │   ├── 📄 useOllama.ts
│   │   │   │   ├── 📄 useVSCode.ts              # VS Code API hook
│   │   │   │   └── 📄 index.ts
│   │   │   │
│   │   │   ├── 📁 store/            # Zustand state management
│   │   │   │   ├── 📄 index.ts
│   │   │   │   ├── 📄 app.store.ts              # Main app state
│   │   │   │   ├── 📄 chat.store.ts             # Chat state
│   │   │   │   ├── 📄 plan.store.ts             # Plan state
│   │   │   │   ├── 📄 act.store.ts              # Act state
│   │   │   │   └── 📄 settings.store.ts         # Settings state
│   │   │   │
│   │   │   ├── 📁 styles/           # Styling
│   │   │   │   ├── 📄 globals.css               # Global styles
│   │   │   │   ├── 📄 variables.css             # CSS variables
│   │   │   │   └── 📄 tailwind.css              # Tailwind entry
│   │   │   │
│   │   │   ├── 📁 utils/            # UI utilities
│   │   │   │   ├── 📄 vscode-api.ts             # VS Code WebView API
│   │   │   │   ├── 📄 message-handler.ts        # Handle messages from extension
│   │   │   │   └── 📄 formatters.ts             # Text/code formatters
│   │   │   │
│   │   │   └── 📁 types/            # UI-specific types
│   │   │       ├── 📄 props.types.ts
│   │   │       ├── 📄 messages.types.ts         # WebView message protocol
│   │   │       └── 📄 vscode.d.ts               # VS Code WebView types
│   │   │
│   │   ├── 📁 panels/               # WebView panel management
│   │   │   ├── 📄 index.ts
│   │   │   ├── 📄 main-panel.ts                 # Main sidebar panel
│   │   │   └── 📄 webview-provider.ts           # WebView content provider
│   │   │
│   │   └── 📁 commands/             # VS Code commands
│   │       ├── 📄 index.ts
│   │       ├── 📄 register-commands.ts          # Command registration
│   │       ├── 📄 indexing.commands.ts          # Indexing commands
│   │       ├── 📄 chat.commands.ts              # Chat commands
│   │       └── 📄 settings.commands.ts          # Settings commands
│   │
│   ├── 📁 prompts/                  # LLM prompt templates
│   │   ├── 📄 index.ts              # Prompt registry
│   │   ├── 📄 types.ts              # Prompt types
│   │   ├── 📁 system/               # System prompts
│   │   │   ├── 📄 chat.system.ts
│   │   │   ├── 📄 plan.system.ts
│   │   │   └── 📄 act.system.ts
│   │   └── 📁 templates/            # User prompts
│   │       ├── 📄 summary.prompt.ts
│   │       ├── 📄 plan-generate.prompt.ts
│   │       ├── 📄 code-create.prompt.ts
│   │       └── 📄 code-modify.prompt.ts
│   │
│   ├── 📁 utils/                    # Shared utilities
│   │   ├── 📄 index.ts
│   │   ├── 📄 logger.ts                         # Logging utility
│   │   ├── 📄 debounce.ts                       # Debounce helper
│   │   ├── 📄 retry.ts                          # Retry logic
│   │   ├── 📄 hash.ts                           # Hashing utilities
│   │   └── 📄 validators.ts                     # Input validation
│   │
│   ├── 📄 extension.ts              # Extension entry point
│   └── 📄 constants.ts              # Global constants
│
├── 📁 test/                         # Test configuration and utilities
│   ├── 📄 setup.ts                  # Test setup
│   ├── 📄 mocks.ts                  # Shared mocks
│   └── 📁 fixtures/                 # Test fixtures
│       ├── 📁 sample-ts-project/    # Sample TypeScript project
│       ├── 📁 sample-py-project/    # Sample Python project
│       └── 📄 sample-responses.ts   # Sample LLM responses
│
├── 📁 resources/                    # Static resources
│   ├── 📁 icons/                    # Extension icons
│   │   ├── 📷 icon.png              # Main icon (128x128)
│   │   ├── 📷 icon-dark.svg         # Dark theme icon
│   │   └── 📷 icon-light.svg        # Light theme icon
│   └── 📁 media/                    # WebView media
│       └── 📄 reset.css             # CSS reset for WebView
│
├── 📄 package.json                  # Extension manifest
├── 📄 tsconfig.json                 # TypeScript configuration
├── 📄 tsconfig.webview.json         # WebView TypeScript config
├── 📄 tailwind.config.js            # Tailwind configuration
├── 📄 postcss.config.js             # PostCSS configuration
├── 📄 esbuild.js                    # esbuild configuration
├── 📄 vitest.config.ts              # Vitest configuration
├── 📄 .eslintrc.json                # ESLint configuration
├── 📄 .prettierrc                   # Prettier configuration
└── 📄 README.md                     # Extension README
```

---

## 4. Python RAG Server Structure

### Complete Server Folder Structure

```
server/
│
├── 📁 src/                          # Source code
│   │
│   ├── 📁 api/                      # API layer (FastAPI routes)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py               # FastAPI app entry
│   │   ├── 📄 dependencies.py       # Dependency injection
│   │   │
│   │   ├── 📁 routes/               # API routes
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 health.py         # Health check endpoints
│   │   │   ├── 📄 index.py          # Indexing endpoints
│   │   │   ├── 📄 query.py          # RAG query endpoints
│   │   │   ├── 📄 chat.py           # Chat endpoints
│   │   │   └── 📄 models.py         # Model management endpoints
│   │   │
│   │   ├── 📁 schemas/              # Pydantic models (request/response)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 index.py          # Indexing schemas
│   │   │   ├── 📄 query.py          # Query schemas
│   │   │   ├── 📄 chat.py           # Chat schemas
│   │   │   └── 📄 common.py         # Common schemas
│   │   │
│   │   └── 📁 websocket/            # WebSocket handlers
│   │       ├── 📄 __init__.py
│   │       ├── 📄 chat_ws.py        # Chat streaming
│   │       └── 📄 progress_ws.py    # Indexing progress
│   │
│   ├── 📁 core/                     # Core domain layer
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 entities/             # Domain entities
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 document.py       # Document representation
│   │   │   ├── 📄 chunk.py          # Code chunk
│   │   │   ├── 📄 embedding.py      # Embedding with metadata
│   │   │   └── 📄 query_result.py   # Query result
│   │   │
│   │   ├── 📁 interfaces/           # Abstract interfaces
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 embedder.py       # Embedding interface
│   │   │   ├── 📄 vector_store.py   # Vector store interface
│   │   │   ├── 📄 llm.py            # LLM interface
│   │   │   └── 📄 parser.py         # Code parser interface
│   │   │
│   │   └── 📁 errors/               # Custom exceptions
│   │       ├── 📄 __init__.py
│   │       ├── 📄 base.py           # Base exception
│   │       ├── 📄 indexing.py       # Indexing errors
│   │       └── 📄 ollama.py         # Ollama errors
│   │
│   ├── 📁 services/                 # Business logic services
│   │   ├── 📄 __init__.py
│   │   ├── 📄 indexing_service.py   # Main indexing orchestration
│   │   ├── 📄 rag_service.py        # RAG query service
│   │   ├── 📄 chat_service.py       # Chat with RAG context
│   │   ├── 📄 sync_service.py       # Smart sync service
│   │   └── 📄 summary_service.py    # Project summary generation
│   │
│   ├── 📁 indexing/                 # Indexing subsystem
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 parsers/              # Language-specific parsers
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 base_parser.py    # Base parser class
│   │   │   ├── 📄 typescript_parser.py
│   │   │   ├── 📄 javascript_parser.py
│   │   │   ├── 📄 python_parser.py
│   │   │   ├── 📄 dart_parser.py
│   │   │   └── 📄 parser_factory.py # Parser selection
│   │   │
│   │   ├── 📄 chunker.py            # Code chunking logic
│   │   ├── 📄 file_scanner.py       # File discovery
│   │   ├── 📄 hash_tracker.py       # File hash tracking
│   │   └── 📄 progress_tracker.py   # Progress reporting
│   │
│   ├── 📁 infrastructure/           # External implementations
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 ollama/               # Ollama integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 client.py         # Ollama API client
│   │   │   ├── 📄 embedder.py       # Ollama embedder (implements interface)
│   │   │   └── 📄 llm.py            # Ollama LLM (implements interface)
│   │   │
│   │   ├── 📁 chromadb/             # ChromaDB integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 client.py         # ChromaDB client
│   │   │   └── 📄 vector_store.py   # ChromaDB store (implements interface)
│   │   │
│   │   ├── 📁 llamaindex/           # LlamaIndex integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 index_builder.py  # Build LlamaIndex index
│   │   │   └── 📄 query_engine.py   # Query with LlamaIndex
│   │   │
│   │   └── 📁 treesitter/           # Tree-sitter integration
│   │       ├── 📄 __init__.py
│   │       ├── 📄 parser.py         # Tree-sitter parser wrapper
│   │       └── 📁 queries/          # Tree-sitter query files
│   │           ├── 📄 typescript.scm
│   │           ├── 📄 javascript.scm
│   │           ├── 📄 python.scm
│   │           └── 📄 dart.scm
│   │
│   ├── 📁 utils/                    # Utilities
│   │   ├── 📄 __init__.py
│   │   ├── 📄 logger.py             # Logging setup
│   │   ├── 📄 file_utils.py         # File helpers
│   │   └── 📄 hash_utils.py         # Hashing helpers
│   │
│   └── 📄 config.py                 # Configuration management
│
├── 📁 tests/                        # Test suite
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py               # Pytest fixtures
│   │
│   ├── 📁 unit/                     # Unit tests
│   │   ├── 📄 __init__.py
│   │   ├── 📁 parsers/
│   │   │   ├── 📄 test_typescript_parser.py
│   │   │   ├── 📄 test_python_parser.py
│   │   │   └── 📄 test_dart_parser.py
│   │   ├── 📄 test_chunker.py
│   │   └── 📄 test_hash_tracker.py
│   │
│   ├── 📁 integration/              # Integration tests
│   │   ├── 📄 __init__.py
│   │   ├── 📄 test_ollama_client.py
│   │   ├── 📄 test_chromadb.py
│   │   └── 📄 test_indexing_pipeline.py
│   │
│   └── 📁 fixtures/                 # Test fixtures
│       ├── 📁 sample_code/
│       │   ├── 📄 sample.ts
│       │   ├── 📄 sample.py
│       │   └── 📄 sample.dart
│       └── 📄 expected_chunks.json
│
├── 📄 pyproject.toml                # Project configuration (uv/poetry)
├── 📄 requirements.txt              # Dependencies (fallback)
├── 📄 requirements-dev.txt          # Dev dependencies
├── 📄 pytest.ini                    # Pytest configuration
├── 📄 ruff.toml                     # Ruff linter configuration
├── 📄 mypy.ini                      # MyPy type checking
├── 📄 Dockerfile                    # Container definition (future)
└── 📄 README.md                     # Server README
```

---

## 5. Scripts Folder

### Script Files

```
scripts/
│
├── 📄 start-server.ps1              # Start Python server (Windows)
│   └── Usage: .\scripts\start-server.ps1 [-Dev] [-Port 52741]
│
├── 📄 start-server.sh               # Start Python server (Unix, future)
│   └── Usage: ./scripts/start-server.sh [--dev] [--port 52741]
│
├── 📄 setup.ps1                     # Full environment setup (Windows)
│   └── Installs: Node.js, pnpm, Python, uv, Ollama
│   └── Pulls: Default models
│   └── Creates: Virtual environments
│
├── 📄 build-all.ps1                 # Build both packages
│   └── Runs: Extension build + Server checks
│   └── Output: extension/dist/, type checks
│
├── 📄 package-extension.ps1         # Create .vsix file
│   └── Runs: vsce package
│   └── Output: localpilot-{version}.vsix
│
├── 📄 clean.ps1                     # Clean build artifacts
│   └── Removes: dist/, node_modules/, .venv/, __pycache__/
│
├── 📄 test-all.ps1                  # Run all tests
│   └── Runs: Extension tests + Server tests
│   └── Coverage: Reports combined coverage
│
└── 📄 dev.ps1                       # Start development environment
    └── Starts: Server (background) + Extension watch mode
    └── Opens: VS Code in debug mode
```

### Script Descriptions

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `start-server.ps1` | Start the Python RAG server | Before using extension |
| `setup.ps1` | One-time environment setup | New developer onboarding |
| `build-all.ps1` | Build extension for production | Before packaging |
| `package-extension.ps1` | Create installable .vsix | For distribution |
| `clean.ps1` | Remove all generated files | When things are broken |
| `test-all.ps1` | Run complete test suite | Before commits |
| `dev.ps1` | Quick development startup | Daily development |

---

## 6. Storage Locations

### 6.1 Storage Location Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    STORAGE LOCATIONS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  There are THREE types of storage:                              │
│                                                                  │
│  1. GLOBAL (~/.localpilot/)                                     │
│     Cross-project data that persists across workspaces          │
│                                                                  │
│  2. WORKSPACE ({workspace}/.localpilot/)                        │
│     Project-specific data stored within the workspace           │
│                                                                  │
│  3. EXTENSION (VS Code managed)                                 │
│     Session and workspace state managed by VS Code             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Global Storage (~/.localpilot/)

```
~/.localpilot/                       # User home directory
│
├── 📁 indexes/                      # All project indexes
│   │
│   ├── 📁 {project-id-1}/           # Index for project 1
│   │   ├── 📁 chroma/               # ChromaDB database files
│   │   │   ├── chroma.sqlite3       # SQLite database
│   │   │   └── ...                  # Other ChromaDB files
│   │   ├── 📄 metadata.json         # Index metadata
│   │   │   └── Contains: project_id, workspace_path, 
│   │   │       indexed_at, files_count, chunks_count, languages
│   │   └── 📄 hashes.json           # File hash tracking
│   │       └── Contains: { "path": { hash, indexed_at, chunk_ids } }
│   │
│   └── 📁 {project-id-2}/           # Index for project 2
│       └── ...
│
├── 📁 logs/                         # Application logs
│   ├── 📄 server.log                # Python server logs
│   └── 📄 extension.log             # Extension logs (if file logging enabled)
│
└── 📄 settings.json                 # Global settings (optional override)
    └── Only if not using VS Code settings API
```

**Project ID Generation:**

```typescript
function generateProjectId(workspacePath: string): string {
  // Hash the absolute path for uniqueness
  const hash = crypto
    .createHash('sha256')
    .update(workspacePath)
    .digest('hex')
    .substring(0, 16);
  
  // Include folder name for readability
  const folderName = path.basename(workspacePath)
    .replace(/[^a-zA-Z0-9]/g, '_')
    .substring(0, 20);
  
  return `${folderName}_${hash}`;
  // Example: "my_project_a1b2c3d4e5f6g7h8"
}
```

### 6.3 Workspace Storage ({workspace}/.localpilot/)

```
{workspace}/                         # User's project folder
│
├── 📁 .localpilot/                  # LocalPilot workspace data
│   │
│   ├── 📁 backups/                  # File backups from Act mode
│   │   ├── 📁 2024-01-15T10-30-00/  # Timestamped backup folder
│   │   │   ├── 📄 src_auth_auth.service.ts  # Backed up file
│   │   │   └── 📄 src_utils_helpers.ts      # Another backup
│   │   └── 📁 2024-01-15T14-22-00/  # Another backup session
│   │       └── ...
│   │
│   └── 📄 audit.log                 # Operations audit trail
│       └── JSON lines: { timestamp, operation, file, result }
│
├── 📄 TODO.md                       # Generated by Act mode (in workspace root)
│   └── Contains: Current plan tasks with checkboxes
│
└── ... (other project files)
```

**Important:** Add to your project's `.gitignore`:

```gitignore
# LocalPilot workspace data
.localpilot/
```

### 6.4 Extension Storage (VS Code Managed)

```
┌─────────────────────────────────────────────────────────────────┐
│                  VS CODE EXTENSION STORAGE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  context.workspaceState (per-workspace session data)            │
│  ─────────────────────────────────────────────────────────────  │
│  • Chat message history                                          │
│  • Current plan draft                                            │
│  • Act mode progress                                             │
│  • Current mode (chat/plan/act)                                 │
│  • Execution checkpoint (for recovery)                          │
│                                                                  │
│  Cleared: When VS Code closes (session scope)                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  context.globalState (cross-workspace settings)                 │
│  ─────────────────────────────────────────────────────────────  │
│  • Onboarding completion flag                                    │
│  • User preferences                                              │
│  • Recent projects list                                          │
│                                                                  │
│  Cleared: Never (global scope)                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.5 Storage Decision Matrix

| Data Type | Location | Reason |
|-----------|----------|--------|
| Vector embeddings | `~/.localpilot/indexes/` | Large, reusable across sessions |
| File hashes | `~/.localpilot/indexes/` | Needed for sync even after restart |
| Index metadata | `~/.localpilot/indexes/` | Persists with index |
| File backups | `{workspace}/.localpilot/` | Project-specific, user might want access |
| Audit log | `{workspace}/.localpilot/` | Project-specific history |
| Chat history | VS Code workspaceState | Session-only (MVP) |
| Current plan | VS Code workspaceState | Session-only |
| User settings | VS Code settings API | Standard VS Code pattern |
| Server logs | `~/.localpilot/logs/` | Cross-project, for debugging |

---

## 7. Configuration Files

### 7.1 Root Configuration Files

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROOT CONFIGURATION FILES                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  .gitignore                                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  # Node                                                          │
│  node_modules/                                                   │
│  *.vsix                                                          │
│  dist/                                                           │
│  out/                                                            │
│                                                                  │
│  # Python                                                        │
│  __pycache__/                                                    │
│  *.py[cod]                                                       │
│  *$py.class                                                      │
│  .venv/                                                          │
│  venv/                                                           │
│  *.egg-info/                                                     │
│                                                                  │
│  # IDE                                                           │
│  .idea/                                                          │
│  *.swp                                                           │
│  *.swo                                                           │
│                                                                  │
│  # OS                                                            │
│  .DS_Store                                                       │
│  Thumbs.db                                                       │
│                                                                  │
│  # Project specific                                              │
│  server/data/                                                    │
│  .localpilot/                                                    │
│  *.log                                                           │
│                                                                  │
│  # Environment                                                   │
│  .env                                                            │
│  .env.local                                                      │
│                                                                  │
│  # Build                                                         │
│  *.tsbuildinfo                                                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  .editorconfig                                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  root = true                                                     │
│                                                                  │
│  [*]                                                             │
│  indent_style = space                                            │
│  end_of_line = lf                                                │
│  charset = utf-8                                                 │
│  trim_trailing_whitespace = true                                │
│  insert_final_newline = true                                    │
│                                                                  │
│  [*.{ts,tsx,js,jsx,json}]                                       │
│  indent_size = 2                                                 │
│                                                                  │
│  [*.py]                                                          │
│  indent_size = 4                                                 │
│                                                                  │
│  [*.md]                                                          │
│  trim_trailing_whitespace = false                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Extension Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | Extension manifest + npm dependencies |
| `tsconfig.json` | TypeScript compiler options (extension) |
| `tsconfig.webview.json` | TypeScript options (React WebView) |
| `.eslintrc.json` | ESLint rules |
| `.prettierrc` | Prettier formatting |
| `tailwind.config.js` | Tailwind CSS config |
| `postcss.config.js` | PostCSS plugins |
| `esbuild.js` | Build configuration |
| `vitest.config.ts` | Test configuration |

### 7.3 Server Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project config + Python dependencies |
| `ruff.toml` | Ruff linter configuration |
| `mypy.ini` | Type checking configuration |
| `pytest.ini` | Test configuration |

---

## 8. File Naming Conventions

### 8.1 TypeScript/JavaScript Files

```
┌─────────────────────────────────────────────────────────────────┐
│               TYPESCRIPT FILE NAMING CONVENTIONS                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PATTERN: kebab-case.type.ts                                    │
│                                                                  │
│  FILE TYPES:                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Services (business logic):                                      │
│  ├── chat.service.ts                                             │
│  ├── indexing.service.ts                                         │
│  └── ollama.service.ts                                           │
│                                                                  │
│  Entities (data structures):                                     │
│  ├── message.entity.ts                                           │
│  ├── plan.entity.ts                                              │
│  └── project.entity.ts                                           │
│                                                                  │
│  Interfaces (contracts):                                         │
│  ├── llm-provider.interface.ts                                   │
│  ├── rag-provider.interface.ts                                   │
│  └── file-system.interface.ts                                    │
│                                                                  │
│  Types (type definitions):                                       │
│  ├── mode.types.ts                                               │
│  ├── ollama.types.ts                                             │
│  └── messages.types.ts                                           │
│                                                                  │
│  Errors (custom errors):                                         │
│  ├── base.error.ts                                               │
│  ├── ollama.error.ts                                             │
│  └── indexing.error.ts                                           │
│                                                                  │
│  Adapters (implementations):                                     │
│  ├── file-system.adapter.ts                                      │
│  └── settings.adapter.ts                                         │
│                                                                  │
│  Prompts:                                                        │
│  ├── chat.system.ts                                              │
│  └── plan-generate.prompt.ts                                     │
│                                                                  │
│  Tests:                                                          │
│  ├── chat.service.test.ts                                        │
│  └── plan-parser.test.ts                                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  REACT COMPONENTS: PascalCase.tsx                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ├── ChatContainer.tsx                                           │
│  ├── MessageList.tsx                                             │
│  ├── MessageItem.tsx                                             │
│  ├── Button.tsx                                                  │
│  └── DiffView.tsx                                                │
│                                                                  │
│  HOOKS: useCamelCase.ts                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ├── useChat.ts                                                  │
│  ├── usePlan.ts                                                  │
│  └── useVSCode.ts                                                │
│                                                                  │
│  STORES: camelCase.store.ts                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ├── app.store.ts                                                │
│  ├── chat.store.ts                                               │
│  └── settings.store.ts                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Python Files

```
┌─────────────────────────────────────────────────────────────────┐
│                 PYTHON FILE NAMING CONVENTIONS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PATTERN: snake_case.py                                          │
│                                                                  │
│  FILE TYPES:                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Services:                                                       │
│  ├── indexing_service.py                                         │
│  ├── rag_service.py                                              │
│  └── chat_service.py                                             │
│                                                                  │
│  Entities:                                                       │
│  ├── document.py                                                 │
│  ├── chunk.py                                                    │
│  └── embedding.py                                                │
│                                                                  │
│  Interfaces:                                                     │
│  ├── embedder.py                                                 │
│  ├── vector_store.py                                             │
│  └── parser.py                                                   │
│                                                                  │
│  Parsers:                                                        │
│  ├── base_parser.py                                              │
│  ├── typescript_parser.py                                        │
│  └── python_parser.py                                            │
│                                                                  │
│  Routes:                                                         │
│  ├── health.py                                                   │
│  ├── index.py                                                    │
│  └── query.py                                                    │
│                                                                  │
│  Tests:                                                          │
│  ├── test_indexing_service.py                                    │
│  ├── test_typescript_parser.py                                   │
│  └── test_chromadb.py                                            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CLASS NAMING: PascalCase                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  class IndexingService:                                          │
│  class TypeScriptParser:                                         │
│  class OllamaClient:                                             │
│                                                                  │
│  FUNCTION/METHOD NAMING: snake_case                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  def index_document(self, doc: Document) -> None:               │
│  def get_embeddings(self, text: str) -> List[float]:            │
│  async def query_similar(self, query: str) -> List[Chunk]:      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.3 Tree-sitter Query Files

```
PATTERN: {language}.scm

Files:
├── typescript.scm    # TypeScript queries
├── javascript.scm    # JavaScript queries (often same as TS)
├── python.scm        # Python queries
└── dart.scm          # Dart queries
```

---

## 9. Import Rules

### 9.1 TypeScript Import Order

```typescript
/**
 * Import Order for TypeScript files
 * 
 * 1. Node.js built-in modules
 * 2. External dependencies (npm packages)
 * 3. VS Code API
 * 4. Internal - Core layer (entities, interfaces, errors)
 * 5. Internal - Features
 * 6. Internal - Infrastructure
 * 7. Internal - UI (if applicable)
 * 8. Relative imports (same feature)
 * 
 * Each group separated by a blank line
 */

// 1. Node.js built-in
import * as path from 'path';
import * as fs from 'fs';
import * as crypto from 'crypto';

// 2. External dependencies
import { create } from 'zustand';
import React from 'react';

// 3. VS Code API
import * as vscode from 'vscode';

// 4. Core layer
import { Message, Plan, Task } from '@core/entities';
import { ILLMProvider, IRAGProvider } from '@core/interfaces';
import { OllamaError } from '@core/errors';

// 5. Features
import { ChatService } from '@features/chat';
import { IndexingService } from '@features/indexing';

// 6. Infrastructure
import { OllamaService } from '@infrastructure/ollama';
import { ApiClient } from '@infrastructure/http';

// 7. UI
import { Button, Card } from '@ui/components/common';

// 8. Relative imports
import { MessageHandler } from './message-handler';
import { ContextBuilder } from './context-builder';
```

### 9.2 Python Import Order

```python
"""
Import Order for Python files

1. Standard library imports
2. Third-party imports
3. Local application imports
   - Core layer
   - Services
   - Infrastructure

Each group separated by a blank line
"""

# 1. Standard library
import asyncio
import hashlib
from pathlib import Path
from typing import List, Optional

# 2. Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb

# 3. Local - Core
from src.core.entities import Document, Chunk
from src.core.interfaces import IEmbedder, IVectorStore
from src.core.errors import IndexingError

# 4. Local - Services
from src.services.indexing_service import IndexingService

# 5. Local - Infrastructure
from src.infrastructure.ollama import OllamaClient
from src.infrastructure.chromadb import ChromaDBStore
```

### 9.3 Import Path Aliases (TypeScript)

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@core/*": ["core/*"],
      "@features/*": ["features/*"],
      "@infrastructure/*": ["infrastructure/*"],
      "@ui/*": ["ui/*"],
      "@utils/*": ["utils/*"],
      "@prompts/*": ["prompts/*"]
    }
  }
}
```

### 9.4 Layer Dependency Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                  LAYER DEPENDENCY RULES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ALLOWED DEPENDENCIES (→ means "can import from")               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  UI Layer:                                                       │
│  ├──→ Features Layer (use services)                             │
│  ├──→ Core Layer (use entities, types)                          │
│  └──→ Infrastructure Layer (ONLY via Features)                  │
│                                                                  │
│  Features Layer:                                                 │
│  ├──→ Core Layer (use entities, interfaces, types)             │
│  └──→ Other Features (sparingly, prefer events)                │
│                                                                  │
│  Infrastructure Layer:                                          │
│  └──→ Core Layer (implement interfaces)                        │
│                                                                  │
│  Core Layer:                                                     │
│  └──→ NOTHING (innermost layer)                                 │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FORBIDDEN DEPENDENCIES (✗)                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ✗ Core → Features                                              │
│  ✗ Core → Infrastructure                                        │
│  ✗ Core → UI                                                    │
│  ✗ Features → Infrastructure (use interfaces!)                 │
│  ✗ Features → UI                                                │
│  ✗ Infrastructure → Features                                    │
│  ✗ Infrastructure → UI                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. AI Agent Instructions

### 10.1 For AI Coding Assistants

```
┌─────────────────────────────────────────────────────────────────┐
│              AI AGENT WORKING INSTRUCTIONS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WHEN CREATING FILES:                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  1. Always check PROJECT_STRUCTURE.md for correct location      │
│  2. Use the exact naming conventions specified                  │
│  3. Include the appropriate file header/documentation           │
│  4. Export from the folder's index.ts file                      │
│  5. Create corresponding test file                              │
│                                                                  │
│  Example - Creating a new service:                              │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Task: "Create the BackupManager service"                       │
│                                                                  │
│  Steps:                                                          │
│  1. Create: extension/src/features/act/backup-manager.ts        │
│  2. Update: extension/src/features/act/index.ts (add export)    │
│  3. Create: extension/src/features/act/__tests__/               │
│             backup-manager.test.ts                               │
│  4. If implements interface, reference from @core/interfaces   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 File Header Templates

**TypeScript File Header:**

```typescript
/**
 * @file backup-manager.ts
 * @description Manages file backups for Act mode operations
 *
 * WHY: Before modifying any user file, we create a backup
 * so changes can be reverted if something goes wrong.
 *
 * RESPONSIBILITIES:
 * - Create timestamped backup folders
 * - Copy files before modification
 * - Restore files from backup
 * - Clean up old backups
 *
 * @example
 * const backup = new BackupManager(fileSystem);
 * const backupPath = await backup.createBackup('src/auth.ts');
 * // ... if something goes wrong ...
 * await backup.restore(backupPath, 'src/auth.ts');
 */
```

**Python File Header:**

```python
"""
Indexing Service

Orchestrates the indexing pipeline for code files.

WHY: This is the main entry point for indexing operations.
It coordinates file scanning, parsing, chunking, and
embedding generation.

RESPONSIBILITIES:
- Scan workspace for supported files
- Coordinate parsing with language-specific parsers
- Generate embeddings via Ollama
- Store in ChromaDB vector database
- Track file hashes for incremental sync

Example:
    service = IndexingService(embedder, vector_store)
    result = await service.index_workspace("/path/to/project")
"""
```

### 10.3 Quick Reference: Where to Put Things

```
┌─────────────────────────────────────────────────────────────────┐
│                 QUICK REFERENCE: WHERE TO PUT THINGS             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  "I need to create a..."                  → Put it in...        │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  EXTENSION (TypeScript):                                         │
│                                                                  │
│  New entity/data structure     → extension/src/core/entities/   │
│  New interface/contract        → extension/src/core/interfaces/ │
│  New error type                → extension/src/core/errors/     │
│  New type definition           → extension/src/core/types/      │
│  New feature service           → extension/src/features/{name}/ │
│  VS Code API wrapper           → extension/src/infrastructure/vscode/ │
│  HTTP/API client code          → extension/src/infrastructure/http/ │
│  WebSocket client code         → extension/src/infrastructure/websocket/ │
│  React component               → extension/src/ui/webview/components/ │
│  React hook                    → extension/src/ui/webview/hooks/ │
│  Zustand store                 → extension/src/ui/webview/store/ │
│  VS Code command               → extension/src/ui/commands/     │
│  LLM prompt template           → extension/src/prompts/         │
│  Utility function              → extension/src/utils/           │
│  WebView message types         → extension/src/ui/webview/types/ │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SERVER (Python):                                                │
│                                                                  │
│  New API endpoint              → server/src/api/routes/         │
│  Request/Response schema       → server/src/api/schemas/        │
│  WebSocket handler             → server/src/api/websocket/      │
│  New entity                    → server/src/core/entities/      │
│  New interface                 → server/src/core/interfaces/    │
│  New error type                → server/src/core/errors/        │
│  New service                   → server/src/services/           │
│  Language parser               → server/src/indexing/parsers/   │
│  Tree-sitter query             → server/src/infrastructure/treesitter/queries/ │
│  Ollama integration            → server/src/infrastructure/ollama/ │
│  ChromaDB integration          → server/src/infrastructure/chromadb/ │
│  Utility function              → server/src/utils/              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SCRIPTS:                                                        │
│                                                                  │
│  Build/setup script            → scripts/                       │
│                                                                  │
│  DOCUMENTATION:                                                  │
│                                                                  │
│  Project documentation         → docs/ProjectDocuments/         │
│  Architecture decision         → docs/decisions/                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 10.4 When Modifying Existing Files

```
┌─────────────────────────────────────────────────────────────────┐
│              WHEN MODIFYING EXISTING FILES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Read the entire file first to understand context            │
│  2. Check for existing patterns and match them                  │
│  3. Update related test files                                    │
│  4. Update index.ts exports if adding new exports               │
│  5. Maintain existing documentation style                       │
│  6. Run linter after changes                                     │
│                                                                  │
│  CHECKLIST BEFORE COMMITTING:                                    │
│  □ File is in correct location per structure.md                │
│  □ Naming follows conventions                                    │
│  □ Exports added to index.ts                                    │
│  □ Tests updated or created                                      │
│  □ No circular dependencies introduced                          │
│  □ Layer boundaries respected                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Document Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | TarekRefaei | | |

---

*Document Version: 1.1.0*
*Created: Planning Phase*
*Last Updated: [Current Date]*
```

---

This is the complete, updated `structure.md` document with all the modifications including:

1. ✅ Clarified storage locations (Section 6)
2. ✅ Added scripts folder documentation (Section 5)
3. ✅ Added WebView message types file location
4. ✅ Added Tree-sitter query files location
5. ✅ Added backup-manager.ts to Act feature
6. ✅ Added server status component to onboarding
7. ✅ Added chunk.entity.ts to entities
8. ✅ Added server.error.ts to errors
9. ✅ Updated AI agent instructions
10. ✅ Added layer dependency rules visualization
````

</details>


## docs/ProjectDocuments/task0-phase.md

*Size: 35,996 bytes | Modified: 2025-12-13T07:50:23.786Z*

<details>
<summary>View code</summary>

````markdown
# 📄 PHASE_0_TASKS.md

# LocalPilot - Phase 0: Foundation Setup

> First sprint tasks to establish project foundation

---

## Document Information

| Field | Value |
|-------|-------|
| **Phase** | 0 - Foundation |
| **Goal** | Working project skeleton |
| **Est. Duration** | 1-2 weeks |
| **Prerequisites** | DEVELOPMENT_SETUP.md completed |

---

## Phase 0 Objectives

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 0 GOALS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  By the end of Phase 0, you will have:                          │
│                                                                  │
│  ✓ Complete project structure created                           │
│  ✓ Extension that activates in VS Code                          │
│  ✓ Python server that starts and responds                       │
│  ✓ Extension ↔ Server communication working                     │
│  ✓ Ollama connection verified                                   │
│  ✓ Basic WebView panel showing                                  │
│  ✓ All core entities and interfaces defined                    │
│  ✓ Tests running for both extension and server                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Task Overview

| # | Task | Type | Est. Time | NEW? |
|---|------|------|-----------|------|
| 0.1 | Create folder structure | Setup | 30 min | |
| 0.2 | Create core entities | Code | 1 hour | |
| 0.3 | Create core interfaces | Code | 1 hour | |
| 0.4 | Create core errors | Code | 30 min | |
| 0.5 | Create message protocol types | Code | 30 min | 
| 0.6 | Create Ollama service | Code | 2 hours | |
| 0.7 | Create Python server skeleton | Code | 1 hour | 
| 0.8 | Create Tree-sitter query files | Code | 1 hour |
| 0.9 | Create start-server script | Setup | 30 min | 
| 0.10 | Create API client | Code | 1 hour | |
| 0.11 | Create basic WebView | Code | 2 hours | |
| 0.12 | Wire extension activation | Code | 1 hour | |
| 0.13 | End-to-end verification | Test | 1 hour | |

---

## Task 0.1: Create Folder Structure

### Objective
Create all folders from PROJECT_STRUCTURE.md

### Instructions for Windsurf

```
Create the following folder structure inside the extension/ folder:

extension/src/
├── core/
│   ├── entities/
│   ├── interfaces/
│   ├── errors/
│   └── types/
├── features/
│   ├── indexing/
│   │   └── __tests__/
│   ├── chat/
│   │   └── __tests__/
│   ├── plan/
│   │   └── __tests__/
│   ├── act/
│   │   └── __tests__/
│   ├── ollama/
│   │   └── __tests__/
│   └── settings/
│       └── __tests__/
├── infrastructure/
│   ├── vscode/
│   ├── http/
│   └── websocket/
├── ui/
│   ├── webview/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── chat/
│   │   │   ├── plan/
│   │   │   ├── act/
│   │   │   ├── onboarding/
│   │   │   └── layout/
│   │   ├── hooks/
│   │   ├── store/
│   │   ├── styles/
│   │   ├── utils/
│   │   └── types/
│   ├── panels/
│   └── commands/
├── prompts/
└── utils/

Also create placeholder index.ts files in each folder that exports nothing for now:
// index.ts
export {};
```

### Verification
- [ ] All folders exist
- [ ] Each folder has an index.ts file
- [ ] No TypeScript errors

---

## Task 0.2: Create Core Entities

### Objective
Create all entity types from ARCHITECTURE.md

### Task 0.2.1: Message Entity

**File:** `extension/src/core/entities/message.entity.ts`

```
Create the Message entity file with these interfaces:

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  ragContext?: RAGContext;
  status?: 'streaming' | 'complete' | 'error';
  error?: string;
}

export interface RAGContext {
  chunks: RetrievedChunk[];
  query: string;
}

export interface RetrievedChunk {
  id: string;
  content: string;
  filePath: string;
  lineStart: number;
  lineEnd: number;
  chunkType: ChunkType;
  symbolName?: string;
  language: string;
  score: number;
}

export type ChunkType = 
  | 'function'
  | 'class'
  | 'method'
  | 'interface'
  | 'type'
  | 'variable'
  | 'import'
  | 'module'
  | 'file';

Include JSDoc comments for each interface and type.
```

### Task 0.2.2: Plan Entity

**File:** `extension/src/core/entities/plan.entity.ts`

```
Create the Plan entity file with these interfaces:

export interface Plan {
  id: string;
  title: string;
  overview: string;
  tasks: Task[];
  createdAt: Date;
  updatedAt: Date;
  status: PlanStatus;
  sourceConversationId?: string;
}

export type PlanStatus = 
  | 'draft'
  | 'approved'
  | 'executing'
  | 'paused'
  | 'completed'
  | 'cancelled';

Include JSDoc comments.
```

### Task 0.2.3: Task Entity

**File:** `extension/src/core/entities/task.entity.ts`

```
Create the Task entity file:

export interface Task {
  id: string;
  orderIndex: number;
  title: string;
  description: string;
  filePath: string;
  actionType: TaskActionType;
  details: string[];
  dependencies: string[];
  status: TaskStatus;
  generatedCode?: string;
  diff?: string;
  error?: string;
  startedAt?: Date;
  completedAt?: Date;
}

export type TaskActionType = 'create' | 'modify' | 'delete';

export type TaskStatus = 
  | 'pending'
  | 'running'
  | 'awaiting-approval'
  | 'done'
  | 'skipped'
  | 'error';

Include JSDoc comments.
```

### Task 0.2.4: Project Entity

**File:** `extension/src/core/entities/project.entity.ts`

```
Create the Project entity file:

export interface Project {
  id: string;
  name: string;
  workspacePath: string;
  indexStatus: IndexStatus;
  lastIndexedAt: Date | null;
  stats: ProjectStats;
  languages: string[];
}

export type IndexStatus = 
  | 'not-indexed'
  | 'indexing'
  | 'indexed'
  | 'sync-required'
  | 'error';

export interface ProjectStats {
  filesCount: number;
  chunksCount: number;
  totalLines: number;
  byLanguage: Record<string, number>;
}

Include JSDoc comments.
```

### Task 0.2.5: Entities Index

**File:** `extension/src/core/entities/index.ts`

```
Create the entities barrel export file:

export * from './message.entity';
export * from './plan.entity';
export * from './task.entity';
export * from './project.entity';
```

### Verification
- [ ] All 4 entity files created
- [ ] index.ts exports all entities
- [ ] No TypeScript errors
- [ ] Can import: `import { Message, Plan, Task, Project } from '@core/entities'`

---

## Task 0.3: Create Core Interfaces

### Task 0.3.1: LLM Provider Interface

**File:** `extension/src/core/interfaces/llm-provider.interface.ts`

```
Create the LLM provider interface:

export interface ILLMProvider {
  isAvailable(): Promise<boolean>;
  listModels(): Promise<ModelInfo[]>;
  chat(request: ChatRequest): Promise<ChatResponse>;
  chatStream(request: ChatRequest): AsyncGenerator<string, void, unknown>;
  embed(text: string, model?: string): Promise<number[]>;
}

export interface ModelInfo {
  name: string;
  size: number;
  modifiedAt: Date;
  family: string;
  parameterSize: string;
  quantizationLevel: string;
}

export interface ChatRequest {
  model: string;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  options?: {
    temperature?: number;
    topP?: number;
    maxTokens?: number;
  };
}

export interface ChatResponse {
  content: string;
  model: string;
  totalDuration: number;
  promptEvalCount: number;
  evalCount: number;
}

Include JSDoc comments explaining what each interface is for.
```

### Task 0.3.2: RAG Provider Interface

**File:** `extension/src/core/interfaces/rag-provider.interface.ts`

```
Create the RAG provider interface:

import { RetrievedChunk, ChunkType, ProjectStats } from '../entities';

export interface IRAGProvider {
  startIndexing(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: IndexProgress) => void
  ): Promise<IndexResult>;
  
  syncIndex(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: SyncProgress) => void
  ): Promise<SyncResult>;
  
  query(
    projectId: string,
    queryText: string,
    topK?: number,
    filters?: QueryFilters
  ): Promise<RetrievedChunk[]>;
  
  getProjectSummary(projectId: string): Promise<ProjectSummary>;
  isIndexed(projectId: string): Promise<boolean>;
  clearIndex(projectId: string): Promise<void>;
}

export interface IndexProgress {
  phase: 'scanning' | 'parsing' | 'embedding' | 'storing';
  current: number;
  total: number;
  currentFile?: string;
  message?: string;
}

export interface IndexResult {
  success: boolean;
  filesIndexed: number;
  chunksCreated: number;
  durationSeconds: number;
  languages: string[];
  error?: string;
}

export interface SyncProgress {
  phase: 'scanning' | 'comparing' | 'updating';
  changedFiles: number;
  deletedFiles: number;
  processed: number;
  total: number;
}

export interface SyncResult {
  success: boolean;
  filesUpdated: number;
  filesDeleted: number;
  chunksUpdated: number;
  durationSeconds: number;
}

export interface QueryFilters {
  fileTypes?: string[];
  chunkTypes?: ChunkType[];
  filePaths?: string[];
}

export interface ProjectSummary {
  projectName: string;
  description: string;
  mainLanguages: string[];
  keyFiles: string[];
  architecture: string;
  frameworks: string[];
  stats: ProjectStats;
}

Include JSDoc comments.
```

### Task 0.3.3: File System Interface

**File:** `extension/src/core/interfaces/file-system.interface.ts`

```
Create the file system interface:

export interface IFileSystem {
  readFile(filePath: string): Promise<string>;
  writeFile(filePath: string, content: string): Promise<void>;
  deleteFile(filePath: string): Promise<void>;
  exists(filePath: string): Promise<boolean>;
  createDirectory(dirPath: string): Promise<void>;
  listFiles(dirPath: string, recursive?: boolean): Promise<string[]>;
  stat(filePath: string): Promise<FileStat>;
  backup(filePath: string): Promise<string>;
  restore(backupPath: string, targetPath: string): Promise<void>;
  getWorkspaceRoot(): string | undefined;
}

export interface FileStat {
  isFile: boolean;
  isDirectory: boolean;
  size: number;
  modifiedAt: Date;
  createdAt: Date;
}

Include JSDoc comments.
```

### Task 0.3.4: Interfaces Index

**File:** `extension/src/core/interfaces/index.ts`

```
Create the interfaces barrel export:

export * from './llm-provider.interface';
export * from './rag-provider.interface';
export * from './file-system.interface';
```

### Verification
- [ ] All 3 interface files created
- [ ] index.ts exports all interfaces
- [ ] No TypeScript errors

---

## Task 0.4: Create Core Errors

### Task 0.4.1: Base Error

**File:** `extension/src/core/errors/base.error.ts`

```
Create the base error class:

export type ErrorCategory = 
  | 'connection'
  | 'indexing'
  | 'llm'
  | 'file'
  | 'validation';

export abstract class LocalPilotError extends Error {
  abstract readonly code: string;
  abstract readonly category: ErrorCategory;
  abstract readonly recoverable: boolean;
  
  constructor(
    message: string,
    public readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
    
    // Maintains proper stack trace in V8
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }
  
  toJSON(): Record<string, unknown> {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      category: this.category,
      recoverable: this.recoverable,
      details: this.details
    };
  }
}
```

### Task 0.4.2: Ollama Errors

**File:** `extension/src/core/errors/ollama.error.ts`

```
Create Ollama-specific errors:

import { LocalPilotError } from './base.error';

export class OllamaConnectionError extends LocalPilotError {
  readonly code = 'OLLAMA_CONNECTION_FAILED';
  readonly category = 'connection' as const;
  readonly recoverable = true;
  
  constructor(url: string, cause?: Error) {
    super(
      `Cannot connect to Ollama at ${url}. Make sure Ollama is running.`,
      { url, cause: cause?.message }
    );
  }
}

export class OllamaModelNotFoundError extends LocalPilotError {
  readonly code = 'OLLAMA_MODEL_NOT_FOUND';
  readonly category = 'llm' as const;
  readonly recoverable = true;
  
  constructor(model: string) {
    super(
      `Model "${model}" not found. Run "ollama pull ${model}" to install.`,
      { model }
    );
  }
}

export class OllamaGenerationError extends LocalPilotError {
  readonly code = 'OLLAMA_GENERATION_FAILED';
  readonly category = 'llm' as const;
  readonly recoverable = true;
  
  constructor(message: string, model: string) {
    super(message, { model });
  }
}
```

### Task 0.4.3: Errors Index

**File:** `extension/src/core/errors/index.ts`

```
Create the errors barrel export:

export * from './base.error';
export * from './ollama.error';
```

### Verification
- [ ] Base error and Ollama errors created
- [ ] Exports working
- [ ] No TypeScript errors

---

## Task 0.5: Create Ollama Service

### Objective
Create the service that communicates with Ollama

### Task 0.5.1: Ollama Service Implementation

**File:** `extension/src/features/ollama/ollama.service.ts`

```
Create the Ollama service that implements ILLMProvider:

import { 
  ILLMProvider, 
  ModelInfo, 
  ChatRequest, 
  ChatResponse 
} from '@core/interfaces';
import { 
  OllamaConnectionError, 
  OllamaModelNotFoundError,
  OllamaGenerationError 
} from '@core/errors';

const DEFAULT_OLLAMA_URL = 'http://localhost:11434';

export class OllamaService implements ILLMProvider {
  private baseUrl: string;
  
  constructor(baseUrl: string = DEFAULT_OLLAMA_URL) {
    this.baseUrl = baseUrl;
  }
  
  async isAvailable(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/version`);
      return response.ok;
    } catch {
      return false;
    }
  }
  
  async listModels(): Promise<ModelInfo[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`);
      if (!response.ok) {
        throw new OllamaConnectionError(this.baseUrl);
      }
      
      const data = await response.json();
      return (data.models || []).map((model: any) => ({
        name: model.name,
        size: model.size,
        modifiedAt: new Date(model.modified_at),
        family: model.details?.family || 'unknown',
        parameterSize: model.details?.parameter_size || 'unknown',
        quantizationLevel: model.details?.quantization_level || 'unknown'
      }));
    } catch (error) {
      if (error instanceof OllamaConnectionError) throw error;
      throw new OllamaConnectionError(this.baseUrl, error as Error);
    }
  }
  
  async chat(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: request.model,
          messages: request.messages,
          stream: false,
          options: request.options
        })
      });
      
      if (!response.ok) {
        const error = await response.text();
        if (error.includes('model') && error.includes('not found')) {
          throw new OllamaModelNotFoundError(request.model);
        }
        throw new OllamaGenerationError(error, request.model);
      }
      
      const data = await response.json();
      return {
        content: data.message?.content || '',
        model: data.model,
        totalDuration: data.total_duration || 0,
        promptEvalCount: data.prompt_eval_count || 0,
        evalCount: data.eval_count || 0
      };
    } catch (error) {
      if (error instanceof OllamaConnectionError || 
          error instanceof OllamaModelNotFoundError ||
          error instanceof OllamaGenerationError) {
        throw error;
      }
      throw new OllamaConnectionError(this.baseUrl, error as Error);
    }
  }
  
  async *chatStream(request: ChatRequest): AsyncGenerator<string, void, unknown> {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: request.model,
        messages: request.messages,
        stream: true,
        options: request.options
      })
    });
    
    if (!response.ok || !response.body) {
      throw new OllamaConnectionError(this.baseUrl);
    }
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(line => line.trim());
      
      for (const line of lines) {
        try {
          const json = JSON.parse(line);
          if (json.message?.content) {
            yield json.message.content;
          }
        } catch {
          // Skip invalid JSON lines
        }
      }
    }
  }
  
  async embed(text: string, model: string = 'mxbai-embed-large'): Promise<number[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/embeddings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, prompt: text })
      });
      
      if (!response.ok) {
        throw new OllamaModelNotFoundError(model);
      }
      
      const data = await response.json();
      return data.embedding || [];
    } catch (error) {
      if (error instanceof OllamaModelNotFoundError) throw error;
      throw new OllamaConnectionError(this.baseUrl, error as Error);
    }
  }
}
```

### Task 0.5.2: Ollama Feature Index

**File:** `extension/src/features/ollama/index.ts`

```
Export the Ollama feature:

export { OllamaService } from './ollama.service';
```

### Task 0.5.3: Ollama Service Tests

**File:** `extension/src/features/ollama/__tests__/ollama.service.test.ts`

```
Create basic tests for OllamaService:

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { OllamaService } from '../ollama.service';

describe('OllamaService', () => {
  let service: OllamaService;
  
  beforeEach(() => {
    service = new OllamaService('http://localhost:11434');
  });
  
  describe('isAvailable', () => {
    it('should return true when Ollama is running', async () => {
      // Mock fetch
      global.fetch = vi.fn().mockResolvedValue({
        ok: true
      });
      
      const result = await service.isAvailable();
      expect(result).toBe(true);
    });
    
    it('should return false when Ollama is not running', async () => {
      global.fetch = vi.fn().mockRejectedValue(new Error('Connection refused'));
      
      const result = await service.isAvailable();
      expect(result).toBe(false);
    });
  });
  
  describe('listModels', () => {
    it('should return list of models', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({
          models: [
            { 
              name: 'qwen2.5-coder:7b', 
              size: 4700000000,
              modified_at: '2024-01-01T00:00:00Z',
              details: { family: 'qwen2', parameter_size: '7B' }
            }
          ]
        })
      });
      
      const models = await service.listModels();
      
      expect(models).toHaveLength(1);
      expect(models[0].name).toBe('qwen2.5-coder:7b');
    });
  });
});
```

### Verification
- [ ] OllamaService created and exports correctly
- [ ] Tests pass: `cd extension && pnpm test`
- [ ] No TypeScript errors

---

## Task 0.6: Create Python Server Skeleton

### Task 0.6.1: Server Structure

```
Create the following structure in server/src/:

server/src/
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── models.py
│   └── schemas/
│       ├── __init__.py
│       └── common.py
├── core/
│   ├── __init__.py
│   ├── entities/
│   │   └── __init__.py
│   ├── interfaces/
│   │   └── __init__.py
│   └── errors/
│       └── __init__.py
├── services/
│   └── __init__.py
├── infrastructure/
│   ├── __init__.py
│   └── ollama/
│       ├── __init__.py
│       └── client.py
└── config.py
```

### Task 0.6.2: Main FastAPI App

**File:** `server/src/api/main.py`

```python
"""
LocalPilot RAG Server

Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health, models

app = FastAPI(
    title="LocalPilot RAG Server",
    description="Local RAG server for LocalPilot VS Code extension",
    version="0.1.0"
)

# CORS for VS Code extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(models.router, prefix="/api", tags=["Models"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=52741)
```

### Task 0.6.3: Health Route

**File:** `server/src/api/routes/health.py`

```python
"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }
```

### Task 0.6.4: Models Route

**File:** `server/src/api/routes/models.py`

```python
"""Model-related endpoints."""

from fastapi import APIRouter
from typing import List
import httpx

router = APIRouter()

OLLAMA_URL = "http://localhost:11434"


@router.get("/models")
async def list_models():
    """List available Ollama models."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return {"models": data.get("models", [])}
            return {"models": [], "error": "Failed to fetch models"}
    except Exception as e:
        return {"models": [], "error": str(e)}
```

### Task 0.6.5: Routes Init

**File:** `server/src/api/routes/__init__.py`

```python
"""API routes."""
from . import health, models
```

### Verification
- [ ] Server starts: `cd server/src/api && python main.py`
- [ ] Health check works: `curl http://localhost:52741/health`
- [ ] Models endpoint works: `curl http://localhost:52741/api/models`

---

## Task 0.7: Create API Client

### Objective
Create HTTP client in extension to communicate with Python server

### Task 0.7.1: API Client

**File:** `extension/src/infrastructure/http/api-client.ts`

```
Create the API client:

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  status: number;
}

export class ApiClient {
  private baseUrl: string;
  
  constructor(baseUrl: string = 'http://localhost:52741') {
    this.baseUrl = baseUrl;
  }
  
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`);
      const data = await response.json();
      
      return {
        data: response.ok ? data : null,
        error: response.ok ? null : data.error || 'Request failed',
        status: response.status
      };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 0
      };
    }
  }
  
  async post<T>(endpoint: string, body: unknown): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      
      return {
        data: response.ok ? data : null,
        error: response.ok ? null : data.error || 'Request failed',
        status: response.status
      };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 0
      };
    }
  }
  
  async healthCheck(): Promise<boolean> {
    const response = await this.get<{ status: string }>('/health');
    return response.data?.status === 'healthy';
  }
}
```

### Task 0.7.2: HTTP Infrastructure Index

**File:** `extension/src/infrastructure/http/index.ts`

```
Export HTTP infrastructure:

export { ApiClient } from './api-client';
export type { ApiResponse } from './api-client';
```

### Verification
- [ ] ApiClient compiles without errors
- [ ] Exports correctly

---

## Task 0.8: Create Basic WebView

### Task 0.8.1: WebView Provider

**File:** `extension/src/ui/panels/webview-provider.ts`

```
Create the WebView provider:

import * as vscode from 'vscode';

export class LocalPilotViewProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'localpilot.mainView';
  
  private _view?: vscode.WebviewView;
  
  constructor(private readonly _extensionUri: vscode.Uri) {}
  
  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    _context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ): void {
    this._view = webviewView;
    
    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri]
    };
    
    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
    
    // Handle messages from webview
    webviewView.webview.onDidReceiveMessage(
      message => {
        switch (message.type) {
          case 'ready':
            console.log('WebView is ready');
            break;
        }
      }
    );
  }
  
  private _getHtmlForWebview(webview: vscode.Webview): string {
    return `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LocalPilot</title>
        <style>
          body {
            padding: 20px;
            color: var(--vscode-foreground);
            font-family: var(--vscode-font-family);
          }
          h1 {
            font-size: 1.5em;
            margin-bottom: 10px;
          }
          .status {
            padding: 10px;
            background: var(--vscode-editor-background);
            border-radius: 4px;
            margin-top: 10px;
          }
          .status-item {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
          }
        </style>
      </head>
      <body>
        <h1>🧭 LocalPilot</h1>
        <p>Privacy-First AI Pair Programming</p>
        
        <div class="status">
          <div class="status-item">
            <span>Extension Status:</span>
            <span>✅ Active</span>
          </div>
          <div class="status-item">
            <span>Server Status:</span>
            <span id="server-status">Checking...</span>
          </div>
          <div class="status-item">
            <span>Ollama Status:</span>
            <span id="ollama-status">Checking...</span>
          </div>
        </div>
        
        <script>
          const vscode = acquireVsCodeApi();
          vscode.postMessage({ type: 'ready' });
        </script>
      </body>
      </html>
    `;
  }
  
  public postMessage(message: unknown): void {
    this._view?.webview.postMessage(message);
  }
}
```

### Task 0.8.2: Panels Index

**File:** `extension/src/ui/panels/index.ts`

```
Export panels:

export { LocalPilotViewProvider } from './webview-provider';
```

### Verification
- [ ] WebView provider compiles
- [ ] Exports correctly

---

## Task 0.9: Wire Extension Activation

### Task 0.9.1: Update Extension Entry Point

**File:** `extension/src/extension.ts`

```
Update the main extension file:

import * as vscode from 'vscode';
import { LocalPilotViewProvider } from './ui/panels';
import { OllamaService } from './features/ollama';
import { ApiClient } from './infrastructure/http';

let ollamaService: OllamaService;
let apiClient: ApiClient;

export async function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot is activating...');
  
  // Initialize services
  ollamaService = new OllamaService();
  apiClient = new ApiClient();
  
  // Register WebView provider
  const provider = new LocalPilotViewProvider(context.extensionUri);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      LocalPilotViewProvider.viewType,
      provider
    )
  );
  
  // Check connections
  const ollamaAvailable = await ollamaService.isAvailable();
  const serverAvailable = await apiClient.healthCheck();
  
  console.log(`Ollama available: ${ollamaAvailable}`);
  console.log(`Server available: ${serverAvailable}`);
  
  // Show status
  if (!ollamaAvailable) {
    vscode.window.showWarningMessage(
      'LocalPilot: Ollama is not running. Please start Ollama.'
    );
  }
  
  if (!serverAvailable) {
    vscode.window.showWarningMessage(
      'LocalPilot: Python server is not running.'
    );
  }
  
  // Register commands
  const startIndexing = vscode.commands.registerCommand(
    'localpilot.startIndexing',
    () => {
      vscode.window.showInformationMessage('Indexing will start here!');
    }
  );
  
  context.subscriptions.push(startIndexing);
  
  console.log('LocalPilot activated successfully!');
}

export function deactivate() {
  console.log('LocalPilot deactivated');
}
```

### Verification
- [ ] Build succeeds: `pnpm run build`
- [ ] Extension activates in VS Code (F5)
- [ ] Sidebar panel shows "LocalPilot"
- [ ] Console shows connection status

---

## Task 0.10: End-to-End Verification

### Verification Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│                 PHASE 0 COMPLETION CHECKLIST                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STRUCTURE                                                       │
│  □ All folders exist per PROJECT_STRUCTURE.md                  │
│  □ All index.ts files export correctly                          │
│                                                                  │
│  CORE                                                            │
│  □ All entities compile and export                              │
│  □ All interfaces compile and export                            │
│  □ All errors compile and export                                │
│                                                                  │
│  EXTENSION                                                       │
│  □ pnpm run build succeeds                                      │
│  □ pnpm test passes                                             │
│  □ F5 opens new VS Code window                                  │
│  □ LocalPilot appears in sidebar                                │
│  □ WebView shows status panel                                   │
│                                                                  │
│  SERVER                                                          │
│  □ python main.py starts server                                 │
│  □ /health returns healthy                                      │
│  □ /api/models returns model list                               │
│                                                                  │
│  INTEGRATION                                                     │
│  □ Extension detects Ollama running                             │
│  □ Extension detects Python server running                      │
│  □ No errors in console                                         │
│                                                                  │
│  GIT                                                             │
│  □ All files committed                                          │
│  □ Tag created: v0.1.0-alpha                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Final Commit

```powershell
git add .
git commit -m "feat: complete Phase 0 foundation setup

- Created project structure
- Added core entities, interfaces, errors
- Implemented OllamaService with tests
- Created Python server skeleton
- Added API client for server communication
- Implemented basic WebView panel
- Wired extension activation"

git tag v0.1.0-alpha
```

---

## Next Phase Preview

After completing Phase 0, you're ready for **Phase 1: Ollama Integration**:

- Complete Ollama service with all methods
- Model selection UI
- Connection management
- Settings integration

---

*Document Version: 1.0.0*
```
````

</details>


## docs/ProjectDocuments/testing-strategy.md

*Size: 2,071 bytes | Modified: 2025-12-13T07:22:34.584Z*

<details>
<summary>View code</summary>

````markdown
### Document 2: TESTING_STRATEGY.md

**Location:** `docs/ProjectDocuments/testing-strategy.md`

**Purpose:** Define testing approach for both extension and server

**Content Required:**

# LocalPilot - Testing Strategy

## Overview
- Extension: Vitest + @vscode/test-electron
- Server: pytest + pytest-asyncio
- Coverage Target: 70% minimum

## Test Categories

### Unit Tests
| Component | Framework | Mock Strategy |
|-----------|-----------|---------------|
| Core entities | Vitest | None needed |
| Services | Vitest | Mock interfaces |
| Parsers | pytest | Sample code fixtures |
| Chunker | pytest | Pre-parsed AST fixtures |

### Integration Tests
| Test | Components | Setup |
|------|------------|-------|
| Ollama connection | OllamaService ↔ Ollama | Requires running Ollama |
| Server API | Extension ↔ Python Server | Both running |
| Full indexing | All indexing components | Sample project |

### E2E Tests (Post-MVP)
- Full workflow: Index → Chat → Plan → Act
- Requires test workspace

## Test Fixtures

### Sample TypeScript Project
```
test/fixtures/sample-ts-project/
├── src/
│   ├── index.ts          # Entry point
│   ├── auth/
│   │   ├── auth.service.ts
│   │   └── auth.types.ts
│   └── utils/
│       └── helpers.ts
├── package.json
└── tsconfig.json
```

### Sample Python Project
```
test/fixtures/sample-py-project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── services/
│       └── auth_service.py
└── requirements.txt
```

### Mock Ollama Responses
[Include sample responses for testing without Ollama]

## Running Tests

### Extension
```bash
cd extension
pnpm test           # Run all tests
pnpm test:watch     # Watch mode
pnpm test:coverage  # With coverage
```

### Server
```bash
cd server
pytest                    # Run all tests
pytest --cov=src         # With coverage
pytest -k "test_parser"  # Specific tests
```
````

</details>


## docs/ProjectDocuments/troubleshooting.md

*Size: 2,659 bytes | Modified: 2025-12-13T07:23:56.568Z*

<details>
<summary>View code</summary>

````markdown
### Document 3: TROUBLESHOOTING.md

**Location:** `docs/ProjectDocuments/troubleshooting.md`

**Purpose:** Common issues and solutions for developers and users

**Content Required:**

# LocalPilot - Troubleshooting Guide

## Connection Issues

### "Cannot connect to Ollama"
**Symptoms:** Extension shows Ollama as disconnected
**Solutions:**
1. Verify Ollama is running: `curl http://localhost:11434/api/version`
2. Check system tray for Ollama icon
3. Restart Ollama: Close from tray → Start from Start Menu
4. Check firewall isn't blocking port 11434

### "Python server not responding"
**Symptoms:** Extension shows server as disconnected
**Solutions:**
1. Ensure server is running: `curl http://localhost:52741/health`
2. Check virtual environment is activated
3. Check port 52741 isn't used: `netstat -an | findstr 52741`
4. Review logs: `~/.localpilot/logs/server.log`

## Indexing Issues

### "Indexing is very slow"
**Causes:**
- Large files being processed
- Many files in workspace
- Ollama overloaded

**Solutions:**
1. Check `.gitignore` excludes `node_modules`, `dist`, etc.
2. Add large binary files to exclude patterns
3. Ensure embedding model is loaded: `ollama list`

### "Some files weren't indexed"
**Check:** Look at indexing summary for skipped files
**Common reasons:**
- File too large (>1MB)
- Unsupported extension
- Parse error (syntax issues)

## Chat Issues

### "Responses seem unrelated to my code"
**Solutions:**
1. Sync index if files changed: Click "Sync Index"
2. Check if relevant files are in supported languages
3. Be more specific in queries (mention file names)

### "Chat is very slow"
**Causes:**
- Large context being processed
- Model loading for first request

**Solutions:**
1. First request is slow (model loading) - wait
2. Reduce `ragTopK` setting
3. Try smaller model

## Act Mode Issues

### "Generated code doesn't compile"
**Solutions:**
1. Review code before applying
2. Edit generated code in preview
3. Re-generate with more specific task description

### "Can't recover from failed task"
**Solutions:**
1. Check `.localpilot/backups/` for original files
2. Use VS Code's undo (Ctrl+Z) immediately after
3. Restore from backup folder manually

## Development Issues

### "TypeScript errors after pulling"
```bash
cd extension
pnpm install
pnpm run build
```

### "Python import errors"
```bash
cd server
.venv\Scripts\activate
uv pip install -e ".[dev]"
```

### "Extension not loading in debug"
1. Ensure `pnpm run build` completed
2. Check `dist/extension.js` exists
3. Check Output panel for errors
````

</details>


## docs/ProjectDocuments/webview-protocol.md

*Size: 2,110 bytes | Modified: 2025-12-13T07:00:54.811Z*

<details>
<summary>View code</summary>

```markdown
# LocalPilot - WebView Communication Protocol

**Purpose:** Define all message types between WebView (React) and Extension Host

## Message Types

### WebView → Extension Host

| Message Type | Payload | Trigger |
|--------------|---------|---------|
| `ready` | `{}` | WebView mounted |
| `sendChat` | `{ message: string }` | User sends message |
| `startIndexing` | `{}` | Click "Index Project" |
| `syncIndex` | `{}` | Click "Sync Index" |
| `transferToPlan` | `{}` | Click "Transfer to Plan" |
| `approvePlan` | `{ planId: string }` | Click "Approve & Execute" |
| `applyTask` | `{ taskId: string }` | Click "Apply" on task |
| `skipTask` | `{ taskId: string }` | Click "Skip" on task |
| `editTask` | `{ taskId: string, updates: Partial<Task> }` | Edit task |
| `pauseExecution` | `{}` | Click "Pause" |
| `resumeExecution` | `{}` | Click "Resume" |
| `cancelExecution` | `{}` | Click "Cancel" |
| `updateSetting` | `{ key: string, value: unknown }` | Setting changed |

### Extension Host → WebView

| Message Type | Payload | Trigger |
|--------------|---------|---------|
| `initialize` | `{ state: WebViewState }` | Extension ready |
| `stateUpdate` | `{ partial: Partial<WebViewState> }` | State changed |
| `chatToken` | `{ token: string, messageId: string }` | Streaming token |
| `chatComplete` | `{ messageId: string }` | Message complete |
| `chatError` | `{ error: string }` | Chat failed |
| `ragChunks` | `{ chunks: RetrievedChunk[] }` | RAG results |
| `indexProgress` | `{ phase, current, total, file? }` | Indexing progress |
| `indexComplete` | `{ result: IndexResult }` | Indexing done |
| `indexError` | `{ error: string }` | Indexing failed |
| `planReady` | `{ plan: Plan }` | Plan generated |
| `taskCodeReady` | `{ taskId, code, diff? }` | Code generated |
| `taskComplete` | `{ taskId: string }` | Task applied |
| `taskError` | `{ taskId, error }` | Task failed |

## TypeScript Definitions

[Include full TypeScript interface definitions as shown in Gap 1]

## Message Flow Diagrams

[Include sequence diagrams for key flows]

```

</details>


## extension/package.json

*Size: 843 bytes | Modified: 2025-12-14T22:10:31.906Z*

<details>
<summary>View code</summary>

```json
{
  "name": "localpilot",
  "displayName": "LocalPilot",
  "description": "Privacy-first AI coding agent using local LLMs",
  "version": "0.1.0",
  "engines": {
    "vscode": "^1.85.0"
  },
  "main": "./dist/extension.js",
  "scripts": {
    "build": "esbuild src/extension.ts --bundle --outfile=dist/extension.js --platform=node --external:vscode --format=cjs",
    "test": "vitest run"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/vscode": "^1.85.0",
    "esbuild": "^0.27.1",
    "vitest": "^4.0.15"
  },
  "contributes": {
    "viewsContainers": {
      "activitybar": [
        {
          "id": "localpilot",
          "title": "LocalPilot"
        }
      ]
    },
    "views": {
      "localpilot": [
        {
          "id": "localpilot.sidebar",
          "name": "LocalPilot"
        }
      ]
    }
  }
}

```

</details>


## extension/src/core/entities/index.ts

*Size: 130 bytes | Modified: 2025-12-13T19:55:55.762Z*

<details>
<summary>View code</summary>

```typescript
export * from './message.entity';
export * from './plan.entity';
export * from './task.entity';
export * from './project.entity';

```

</details>


## extension/src/core/entities/message.entity.ts

*Size: 1,341 bytes | Modified: 2025-12-13T19:55:19.325Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Represents a single chat message.
 */
export interface Message {
  /** Unique message ID */
  id: string;
  /** Who sent the message */
  role: 'user' | 'assistant' | 'system';
  /** Message content (may include markdown) */
  content: string;
  /** When the message was created */
  timestamp: Date;
  /** If this message used RAG context */
  ragContext?: RAGContext;
  /** Status for assistant messages (streaming) */
  status?: 'streaming' | 'complete' | 'error';
  /** Error details if status is 'error' */
  error?: string;
}

export interface RAGContext {
  /** Chunks used to generate response */
  chunks: RetrievedChunk[];
  /** Query that was sent to RAG */
  query: string;
}

export interface RetrievedChunk {
  /** Chunk ID in vector store */
  id: string;
  /** Code content */
  content: string;
  /** File path relative to workspace */
  filePath: string;
  /** Starting line number */
  lineStart: number;
  /** Ending line number */
  lineEnd: number;
  /** Type of code unit */
  chunkType: ChunkType;
  /** Symbol name (function/class name) */
  symbolName?: string;
  /** Programming language */
  language: string;
  /** Similarity score (0-1) */
  score: number;
}

export type ChunkType =
  | 'function'
  | 'class'
  | 'method'
  | 'interface'
  | 'type'
  | 'variable'
  | 'import'
  | 'module'
  | 'file';

```

</details>


## extension/src/core/entities/plan.entity.ts

*Size: 662 bytes | Modified: 2025-12-13T19:56:33.211Z*

<details>
<summary>View code</summary>

```typescript
import type { Task } from './task.entity';
/**
 * Represents an implementation plan
 */
export interface Plan {
  /** Unique plan ID */
  id: string;
  /** Plan title */
  title: string;
  /** Brief description/overview */
  overview: string;
  /** List of tasks to execute */
  tasks: Task[];
  /** When the plan was created */
  createdAt: Date;
  /** When the plan was last modified */
  updatedAt: Date;
  /** Current plan status */
  status: PlanStatus;
  /** Original conversation that led to this plan */
  sourceConversationId?: string;
}

export type PlanStatus =
  | 'draft'
  | 'approved'
  | 'executing'
  | 'paused'
  | 'completed'
  | 'cancelled';

```

</details>


## extension/src/core/entities/project.entity.ts

*Size: 755 bytes | Modified: 2025-12-13T19:55:55.126Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Represents an indexed project/workspace
 */
export interface Project {
  /** Unique identifier (hash of workspace path) */
  id: string;
  /** Display name (folder name) */
  name: string;
  /** Absolute path to workspace */
  workspacePath: string;
  /** Index status */
  indexStatus: IndexStatus;
  /** When indexing was last completed */
  lastIndexedAt: Date | null;
  /** Statistics about indexed content */
  stats: ProjectStats;
  /** Languages detected in project */
  languages: string[];
}

export type IndexStatus =
  | 'not-indexed'
  | 'indexing'
  | 'indexed'
  | 'sync-required'
  | 'error';

export interface ProjectStats {
  filesCount: number;
  chunksCount: number;
  totalLines: number;
  byLanguage: Record<string, number>;
}

```

</details>


## extension/src/core/entities/task.entity.ts

*Size: 984 bytes | Modified: 2025-12-13T19:55:54.016Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Represents a single task in a plan
 */
export interface Task {
  /** Unique task ID */
  id: string;
  /** Order in the plan (0-based) */
  orderIndex: number;
  /** Short task title */
  title: string;
  /** Detailed description */
  description: string;
  /** File to create/modify/delete */
  filePath: string;
  /** What action to take */
  actionType: TaskActionType;
  /** Additional details/requirements */
  details: string[];
  /** IDs of tasks this depends on */
  dependencies: string[];
  /** Current task status */
  status: TaskStatus;
  /** Generated code (after code generation) */
  generatedCode?: string;
  /** Diff for modify actions */
  diff?: string;
  /** Error message if failed */
  error?: string;
  /** Execution timestamps */
  startedAt?: Date;
  completedAt?: Date;
}

export type TaskActionType = 'create' | 'modify' | 'delete';

export type TaskStatus =
  | 'pending'
  | 'running'
  | 'awaiting-approval'
  | 'done'
  | 'skipped'
  | 'error';

```

</details>


## extension/src/core/errors/base.error.ts

*Size: 897 bytes | Modified: 2025-12-14T01:23:45.565Z*

<details>
<summary>View code</summary>

```typescript
export type ErrorCategory =
  | 'connection'
  | 'indexing'
  | 'llm'
  | 'file'
  | 'validation';

/**
 * Base error class for all LocalPilot errors.
 * Enforces structured, serializable errors.
 */
export abstract class LocalPilotError extends Error {
  abstract readonly code: string;
  abstract readonly category: ErrorCategory;
  abstract readonly recoverable: boolean;

  constructor(
    message: string,
    public readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;

    // Preserve stack trace
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }

  toJSON(): Record<string, unknown> {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      category: this.category,
      recoverable: this.recoverable,
      details: this.details,
    };
  }
}

```

</details>


## extension/src/core/errors/index.ts

*Size: 62 bytes | Modified: 2025-12-14T01:24:26.720Z*

<details>
<summary>View code</summary>

```typescript
export * from './base.error';
export * from './ollama.error';

```

</details>


## extension/src/core/errors/ollama.error.ts

*Size: 1,160 bytes | Modified: 2025-12-14T01:24:06.218Z*

<details>
<summary>View code</summary>

```typescript
import { LocalPilotError } from './base.error';

/**
 * Thrown when Ollama cannot be reached.
 */
export class OllamaConnectionError extends LocalPilotError {
  readonly code = 'OLLAMA_CONNECTION_FAILED';
  readonly category = 'connection' as const;
  readonly recoverable = true;

  constructor(url: string, cause?: Error) {
    super(
      `Cannot connect to Ollama at ${url}. Make sure Ollama is running.`,
      { url, cause: cause?.message }
    );
  }
}

/**
 * Thrown when a requested model is missing.
 */
export class OllamaModelNotFoundError extends LocalPilotError {
  readonly code = 'OLLAMA_MODEL_NOT_FOUND';
  readonly category = 'llm' as const;
  readonly recoverable = true;

  constructor(model: string) {
    super(
      `Model "${model}" not found. Run "ollama pull ${model}" to install it.`,
      { model }
    );
  }
}

/**
 * Thrown when generation fails unexpectedly.
 */
export class OllamaGenerationError extends LocalPilotError {
  readonly code = 'OLLAMA_GENERATION_FAILED';
  readonly category = 'llm' as const;
  readonly recoverable = true;

  constructor(message: string, model: string) {
    super(message, { model });
  }
}

```

</details>


## extension/src/core/interfaces/file-system.interface.ts

*Size: 1,062 bytes | Modified: 2025-12-13T19:57:29.901Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Interface for file system operations
 */
export interface IFileSystem {
  /** Read file content */
  readFile(filePath: string): Promise<string>;
  /** Write content to file (creates if not exists) */
  writeFile(filePath: string, content: string): Promise<void>;
  /** Delete a file */
  deleteFile(filePath: string): Promise<void>;
  /** Check if file exists */
  exists(filePath: string): Promise<boolean>;
  /** Create directory (recursive) */
  createDirectory(dirPath: string): Promise<void>;
  /** List files in directory */
  listFiles(dirPath: string, recursive?: boolean): Promise<string[]>;
  /** Get file stats */
  stat(filePath: string): Promise<FileStat>;
  /** Create backup of a file */
  backup(filePath: string): Promise<string>;
  /** Restore file from backup */
  restore(backupPath: string, targetPath: string): Promise<void>;
  /** Get workspace root path */
  getWorkspaceRoot(): string | undefined;
}

export interface FileStat {
  isFile: boolean;
  isDirectory: boolean;
  size: number;
  modifiedAt: Date;
  createdAt: Date;
}

```

</details>


## extension/src/core/interfaces/index.ts

*Size: 125 bytes | Modified: 2025-12-13T19:57:30.519Z*

<details>
<summary>View code</summary>

```typescript
export * from './llm-provider.interface';
export * from './rag-provider.interface';
export * from './file-system.interface';

```

</details>


## extension/src/core/interfaces/llm-provider.interface.ts

*Size: 1,094 bytes | Modified: 2025-12-13T19:57:24.071Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Interface for LLM provider operations
 */
export interface ILLMProvider {
  /** Check if the LLM provider is available */
  isAvailable(): Promise<boolean>;
  /** Get list of available models */
  listModels(): Promise<ModelInfo[]>;
  /** Generate chat completion (non-streaming) */
  chat(request: ChatRequest): Promise<ChatResponse>;
  /** Generate chat completion with streaming */
  chatStream(request: ChatRequest): AsyncGenerator<string, void, unknown>;
  /** Generate embeddings for text */
  embed(text: string, model?: string): Promise<number[]>;
}

export interface ModelInfo {
  name: string;
  size: number;
  modifiedAt: Date;
  family: string;
  parameterSize: string;
  quantizationLevel: string;
}

export interface ChatRequest {
  model: string;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  options?: {
    temperature?: number;
    topP?: number;
    maxTokens?: number;
  };
}

export interface ChatResponse {
  content: string;
  model: string;
  totalDuration: number;
  promptEvalCount: number;
  evalCount: number;
}

```

</details>


## extension/src/core/interfaces/rag-provider.interface.ts

*Size: 1,947 bytes | Modified: 2025-12-13T19:57:27.428Z*

<details>
<summary>View code</summary>

```typescript
import type { RetrievedChunk, ChunkType, ProjectStats } from '../entities';

/**
 * Interface for RAG operations
 */
export interface IRAGProvider {
  /** Start indexing a workspace */
  startIndexing(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: IndexProgress) => void
  ): Promise<IndexResult>;
  /** Sync index (re-index only changed files) */
  syncIndex(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: SyncProgress) => void
  ): Promise<SyncResult>;
  /** Query for relevant code chunks */
  query(
    projectId: string,
    queryText: string,
    topK?: number,
    filters?: QueryFilters
  ): Promise<RetrievedChunk[]>;
  /** Get project summary after indexing */
  getProjectSummary(projectId: string): Promise<ProjectSummary>;
  /** Check if project is indexed */
  isIndexed(projectId: string): Promise<boolean>;
  /** Clear project index */
  clearIndex(projectId: string): Promise<void>;
}

export interface IndexProgress {
  phase: 'scanning' | 'parsing' | 'embedding' | 'storing';
  current: number;
  total: number;
  currentFile?: string;
  message?: string;
}

export interface IndexResult {
  success: boolean;
  filesIndexed: number;
  chunksCreated: number;
  durationSeconds: number;
  languages: string[];
  error?: string;
}

export interface SyncProgress {
  phase: 'scanning' | 'comparing' | 'updating';
  changedFiles: number;
  deletedFiles: number;
  processed: number;
  total: number;
}

export interface SyncResult {
  success: boolean;
  filesUpdated: number;
  filesDeleted: number;
  chunksUpdated: number;
  durationSeconds: number;
}

export interface QueryFilters {
  fileTypes?: string[];
  chunkTypes?: ChunkType[];
  filePaths?: string[];
}

export interface ProjectSummary {
  projectName: string;
  description: string;
  mainLanguages: string[];
  keyFiles: string[];
  architecture: string;
  frameworks: string[];
  stats: ProjectStats;
}

```

</details>


## extension/src/extension.ts

*Size: 250 bytes | Modified: 2025-12-13T20:06:08.167Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { MainPanel } from './panels/main-panel';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  MainPanel.register(context);
}

export function deactivate() {}

```

</details>


## extension/src/features/ollama/connection-manager.ts

*Size: 487 bytes | Modified: 2025-12-14T01:25:14.715Z*

<details>
<summary>View code</summary>

```typescript
import { OllamaConnectionError } from '../../core/errors';

const DEFAULT_OLLAMA_URL = 'http://localhost:11434';

/**
 * Checks whether Ollama is reachable.
 * Phase 0: connectivity only (no model logic).
 */
export async function checkOllamaAvailability(
  baseUrl: string = DEFAULT_OLLAMA_URL
): Promise<boolean> {
  try {
    const res = await fetch(`${baseUrl}/api/version`);
    return res.ok;
  } catch (error) {
    throw new OllamaConnectionError(baseUrl, error as Error);
  }
}

```

</details>


## extension/src/infrastructure/http/api-client.ts

*Size: 141 bytes | Modified: 2025-12-13T19:57:32.651Z*

<details>
<summary>View code</summary>

```typescript
export async function checkServerHealth(): Promise<boolean> {
  const res = await fetch('http://localhost:52741/health');
  return res.ok;
}

```

</details>


## extension/src/panels/main-panel.ts

*Size: 390 bytes | Modified: 2025-12-13T19:59:04.642Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';

export class MainPanel {
  static register(context: vscode.ExtensionContext) {
    context.subscriptions.push(
      vscode.window.registerWebviewViewProvider(
        'localpilot.sidebar',
        {
          resolveWebviewView(view: vscode.WebviewView) {
            view.webview.html = `<h1>LocalPilot</h1>`;
          }
        }
      )
    );
  }
}

```

</details>


## extension/test/activation.test.ts

*Size: 570 bytes | Modified: 2025-12-13T20:09:45.371Z*

<details>
<summary>View code</summary>

```typescript
import { describe, it, expect, vi } from 'vitest';

vi.mock('vscode', () => {
  return {
    window: {
      registerWebviewViewProvider: vi.fn(() => ({ dispose: vi.fn() })),
    },
  };
});

import { activate } from '../src/extension';

describe('Extension activation', () => {
  it('should activate without throwing and register the panel', () => {
    const subscriptions: { dispose?: () => void }[] = [];
    const context = { subscriptions } as any;

    expect(() => activate(context)).not.toThrow();
    expect(subscriptions.length).toBeGreaterThan(0);
  });
});

```

</details>


## extension/tsconfig.json

*Size: 283 bytes | Modified: 2025-12-13T20:08:50.447Z*

<details>
<summary>View code</summary>

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "strict": true,
    "outDir": "dist",
    "rootDir": "src",
    "lib": ["ES2020", "DOM"],
    "skipLibCheck": true,
    "resolveJsonModule": true
  },
  "include": ["src"]
}

```

</details>


## README.md

*Size: 253 bytes | Modified: 2025-12-14T23:00:06.468Z*

<details>
<summary>View code</summary>

```markdown
# LocalPilot

[![Windows CI](https://github.com/TarekRefaei/LocalPilot/actions/workflows/windows-ci.yml/badge.svg)](https://github.com/TarekRefaei/LocalPilot/actions/workflows/windows-ci.yml)

Privacy-first AI coding agent for VS Code using local LLMs.

```

</details>


## server/.pytest_cache/README.md

*Size: 310 bytes | Modified: 2025-12-13T20:24:55.581Z*

<details>
<summary>View code</summary>

```markdown
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

```

</details>


## server/indexing/__init__.py

*Size: 0 bytes | Modified: 2025-12-14T23:22:00.906Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/indexing/chunk.py

*Size: 236 bytes | Modified: 2025-12-14T23:22:03.164Z*

<details>
<summary>View code</summary>

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CodeChunk:
    id: str
    file_path: str
    language: str
    start_line: int
    end_line: int
    content: str
    symbol_type: str  # function, class, module, block

```

</details>


## server/indexing/chunker.py

*Size: 1,008 bytes | Modified: 2025-12-14T23:22:04.526Z*

<details>
<summary>View code</summary>

```python
import hashlib
from typing import List

from .chunk import CodeChunk


class SemanticChunker:
    def chunk_file(
        self,
        file_path: str,
        language: str,
        source: str
    ) -> List[CodeChunk]:
        """
        Fallback semantic chunking:
        - Entire file = single chunk
        - Used until AST-aware chunkers are plugged in
        """

        lines = source.splitlines()
        content = source.strip()

        chunk_id = self._stable_id(file_path, content)

        return [
            CodeChunk(
                id=chunk_id,
                file_path=file_path,
                language=language,
                start_line=1,
                end_line=len(lines),
                content=content,
                symbol_type="file"
            )
        ]

    def _stable_id(self, file_path: str, content: str) -> str:
        h = hashlib.sha256()
        h.update(file_path.encode("utf-8"))
        h.update(content.encode("utf-8"))
        return h.hexdigest()

```

</details>


## server/indexing/embeddings/__init__.py

*Size: 0 bytes | Modified: 2025-12-14T23:22:07.070Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/indexing/embeddings/base.py

*Size: 331 bytes | Modified: 2025-12-14T23:22:07.971Z*

<details>
<summary>View code</summary>

```python
from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        Must be deterministic for identical inputs.
        """
        raise NotImplementedError

```

</details>


## server/indexing/embeddings/ollama.py

*Size: 768 bytes | Modified: 2025-12-14T23:22:09.267Z*

<details>
<summary>View code</summary>

```python
import requests
from typing import List

from .base import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []

        for text in texts:
            res = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text
                },
                timeout=60
            )
            res.raise_for_status()
            data = res.json()
            embeddings.append(data["embedding"])

        return embeddings

```

</details>


## server/indexing/hash_tracker.py

*Size: 240 bytes | Modified: 2025-12-14T23:22:05.031Z*

<details>
<summary>View code</summary>

```python
import hashlib
from pathlib import Path


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

```

</details>


## server/indexing/language.py

*Size: 291 bytes | Modified: 2025-12-14T23:22:01.807Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path


EXTENSION_LANGUAGE_MAP = {
    ".ts": "typescript",
    ".js": "javascript",
    ".py": "python",
    ".dart": "dart",
    ".json": "json",
    ".md": "markdown"
}


def detect_language(path: Path) -> str | None:
    return EXTENSION_LANGUAGE_MAP.get(path.suffix)

```

</details>


## server/indexing/parsers/__init__.py

*Size: 0 bytes | Modified: 2025-12-14T23:22:02.063Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/indexing/parsers/base.py

*Size: 322 bytes | Modified: 2025-12-14T23:22:02.635Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from typing import Any


class ParseResult:
    def __init__(self, ast: Any, source: str):
        self.ast = ast
        self.source = source


class BaseParser:
    language: str

    def parse(self, path: Path) -> ParseResult:
        raise NotImplementedError("Parser must implement parse()")

```

</details>


## server/indexing/progress.py

*Size: 343 bytes | Modified: 2025-12-14T23:22:06.765Z*

<details>
<summary>View code</summary>

```python
from typing import Callable, Literal

Phase = Literal["scan", "parse", "chunk", "hash", "complete"]


class ProgressTracker:
    def __init__(self, callback: Callable[[Phase, int, int], None]):
        self.callback = callback

    def report(self, phase: Phase, current: int, total: int) -> None:
        self.callback(phase, current, total)

```

</details>


## server/indexing/scanner.py

*Size: 691 bytes | Modified: 2025-12-14T23:22:01.398Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from typing import List

EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "__pycache__",
    ".localpilot"
}

SUPPORTED_EXTENSIONS = {
    ".ts", ".js", ".py", ".json", ".md", ".dart"
}


class WorkspaceScanner:
    def scan(self, root: Path) -> List[Path]:
        files: List[Path] = []

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if any(part in EXCLUDED_DIRS for part in path.parts):
                continue

            if path.suffix not in SUPPORTED_EXTENSIONS:
                continue

            files.append(path)

        return sorted(files)

```

</details>


## server/indexing/service.py

*Size: 1,910 bytes | Modified: 2025-12-14T23:22:13.978Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path

from .scanner import WorkspaceScanner
from .language import detect_language
from .chunker import SemanticChunker
from .hash_tracker import hash_file
from .state import IndexState
from .vector_store import VectorStore


class IndexingService:
    def __init__(
        self,
        workspace: Path,
        index_root: Path,
        embedder,
        progress=None
    ):
        self.workspace = workspace
        self.index_root = index_root
        self.embedder = embedder
        self.progress = progress

        self.scanner = WorkspaceScanner()
        self.chunker = SemanticChunker()

    def run(self) -> None:
        state = IndexState(self.index_root)
        state.load()

        files = self.scanner.scan(self.workspace)

        all_chunks = []
        texts = []

        for idx, path in enumerate(files, start=1):
            if self.progress:
                self.progress.report("scan", idx, len(files))

            current_hash = hash_file(path)
            stored_hash = state.file_hashes.get(str(path))

            if stored_hash == current_hash:
                continue

            language = detect_language(path)
            if not language:
                continue

            source = path.read_text(encoding="utf-8", errors="ignore")

            chunks = self.chunker.chunk_file(
                file_path=str(path),
                language=language,
                source=source
            )

            all_chunks.extend(chunks)
            texts.extend([c.content for c in chunks])

            state.file_hashes[str(path)] = current_hash

        if not all_chunks:
            return

        embeddings = self.embedder.embed(texts)

        store = VectorStore(
            persist_dir=str(self.index_root / "chroma"),
            collection_name="code_chunks"
        )
        store.add(all_chunks, embeddings)

        state.save()

```

</details>


## server/indexing/state.py

*Size: 714 bytes | Modified: 2025-12-14T23:22:06.101Z*

<details>
<summary>View code</summary>

```python
import json
from pathlib import Path
from typing import Dict


class IndexState:
    def __init__(self, root: Path):
        self.path = root / "state.json"
        self.file_hashes: Dict[str, str] = {}

    def load(self) -> None:
        if not self.path.exists():
            return
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.file_hashes = data.get("file_hashes", {})

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                {"file_hashes": self.file_hashes},
                f,
                indent=2
            )

```

</details>


## server/indexing/vector_store.py

*Size: 1,102 bytes | Modified: 2025-12-14T23:22:10.961Z*

<details>
<summary>View code</summary>

```python
from typing import List

import chromadb

from .chunk import CodeChunk


class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.Client(
            settings=chromadb.Settings(
                persist_directory=persist_dir,
                anonymized_telemetry=False
            )
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        chunks: List[CodeChunk],
        embeddings: List[List[float]]
    ) -> None:
        self.collection.add(
            ids=[c.id for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[
                {
                    "file_path": c.file_path,
                    "language": c.language,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "symbol_type": c.symbol_type
                }
                for c in chunks
            ],
            embeddings=embeddings
        )
        self.client.persist()

```

</details>


## server/main.py

*Size: 108 bytes | Modified: 2025-12-13T19:51:08.149Z*

<details>
<summary>View code</summary>

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

```

</details>


## server/requirements.txt

*Size: 42 bytes | Modified: 2025-12-14T23:29:11.052Z*

<details>
<summary>View code</summary>

```text
fastapi
uvicorn
httpx
requests
chromadb

```

</details>


## server/tests/test_health.py

*Size: 451 bytes | Modified: 2025-12-13T20:25:32.942Z*

<details>
<summary>View code</summary>

```python
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Add the server root to sys.path so `main` can be imported regardless of CWD
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import app


def test_health_ok():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

```

</details>


## tools/export-to-md.mjs

*Size: 14,591 bytes | Modified: 2025-12-07T18:23:00.571Z*

<details>
<summary>View code</summary>

````javascript
#!/usr/bin/env node
import fs from 'node:fs/promises';
import { createWriteStream } from 'node:fs';
import path from 'node:path';
// Optional dependency handling
let ignoreModule = null;
try {
  // Dynamic import for the ignore package
  ignoreModule = await import('ignore').then(m => m.default);
} catch (error) {
  console.warn('Warning: "ignore" package not installed. .gitignore support disabled.');
}

// --- Default Configuration (and other functions like parseArgs, walk, langForExt, etc.) ---
const DEFAULT_ROOTS = ['.'];
const DEFAULT_EXCLUDE_DIRS = new Set([
  '.git', 'node_modules', 'dist', 'build', 'out', 'target', 'vendor',
  '.idea', '.vscode', '.DS_Store', 'coverage', '.cache', 'bin', 'obj',
  '.venv', '__pycache__', '.tox',
  'Pods', 'DerivedData', '.swiftpm', 'Carthage',
  '.gradle',
  'Library', 'Temp', 'Logs', 'Packages',
  'Intermediate', 'Saved',
]);
const DEFAULT_ALLOW_EXTS = new Set([
  '.ts', '.tsx', '.js', '.jsx', '.json', '.mjs', '.cjs', '.html', '.css', '.scss', '.less',
  '.yml', '.yaml', '.toml', '.ini', '.env', '.config',
  '.md', '.mdx', '.txt','csv','.json',
  '.sh', '.bash', '.ps1', 'Dockerfile',
  '.c', '.cpp', '.h', '.hpp',
  '.py', '.go', '.rs', '.rb', '.php', '.sql',
  '.cs', '.gd', '.lua', '.glsl', '.hlsl', '.metal', '.shader', '.tscn', '.tres',
  '.swift', '.m', '.storyboard', '.xib', '.plist', 'Podfile',
  '.kt', '.kts', '.java', '.xml', '.gradle', '.gradle.kts',
  '.dart', '.xaml',
]);
const DEFAULT_EXCLUDE_FILE_BASENAMES = new Set([
  'package-lock.json', 'pnpm-lock.yaml', 'yarn.lock', 'Podfile.lock', 'Cargo.lock',
  'composer.lock', 'Gemfile.lock' , 'reviewer.md'
]);
const langForExt = (ext) => ({
  '.ts': 'typescript', '.tsx': 'tsx', '.js': 'javascript', '.jsx': 'jsx', '.mjs': 'javascript', '.cjs': 'javascript',
  '.json': 'json', '.yml': 'yaml', '.yaml': 'yaml', '.toml':'toml', '.ini':'ini',
  '.md': 'markdown', '.mdx': 'mdx', '.txt': 'text',
  '.sh': 'bash', '.bash': 'bash', '.ps1': 'powershell', 'Dockerfile':'dockerfile',
  '.py': 'python', '.go': 'go', '.rs': 'rust',
  '.java': 'java', '.kt': 'kotlin', '.kts': 'kotlin', '.scala': 'scala', '.gradle': 'groovy', '.gradle.kts': 'kotlin',
  '.cs': 'csharp', '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp',
  '.rb': 'ruby', 'Podfile': 'ruby', '.php': 'php', '.sql': 'sql',
  '.html': 'html', '.css': 'css', '.scss': 'scss', '.less': 'less',
  '.gd': 'gdscript', '.lua': 'lua', '.glsl': 'glsl', '.hlsl': 'hlsl', '.metal': 'c++', '.shader': 'csharp', '.tscn': 'ini', '.tres': 'ini',
  '.swift': 'swift', '.m': 'objectivec',
  '.xml': 'xml', '.storyboard': 'xml', '.xib': 'xml', '.plist': 'xml', '.xaml': 'xml',
  '.dart': 'dart',
}[ext] || '');

function parseArgs(argv) {
  const config = {
    roots: [], out: '', maxBytes: 524288, help: false,
    excludeDirs: new Set(DEFAULT_EXCLUDE_DIRS),
    useGitignore: true,
    allowExts: new Set(DEFAULT_ALLOW_EXTS),
    excludeFiles: new Set(DEFAULT_EXCLUDE_FILE_BASENAMES),
  };
  const parseList = (arg, prefix) => arg.slice(prefix.length).split(',').filter(Boolean);
  for (const arg of argv) {
    if (arg === '-h' || arg === '--help') { config.help = true; continue; }
    if (arg.startsWith('--out=')) { config.out = arg.slice('--out='.length); continue; }
    if (arg === '--no-gitignore') { config.useGitignore = false; continue; }
    if (arg.startsWith('--max-bytes=')) {
      const n = Number(arg.slice('--max-bytes='.length));
      if (Number.isFinite(n) && n >= 0) config.maxBytes = Math.trunc(n);
      continue;
    }
    if (arg.startsWith('--exclude-dir=')) { parseList(arg, '--exclude-dir=').forEach(d => config.excludeDirs.add(d)); continue; }
    if (arg.startsWith('--include-ext=')) {
      if (config.allowExts === DEFAULT_ALLOW_EXTS) config.allowExts = new Set();
      parseList(arg, '--include-ext=').forEach(e => config.allowExts.add(e.startsWith('.') ? e : `.${e}`));
      continue;
    }
    if (arg.startsWith('--exclude-file=')) { parseList(arg, '--exclude-file=').forEach(f => config.excludeFiles.add(f)); continue; }
    if (!arg.startsWith('--')) { config.roots.push(arg); }
  }
  if (config.roots.length === 0) { config.roots = DEFAULT_ROOTS; }
  return config;
}

/**
 * Load and parse .gitignore file for a given directory
 * @param {string} rootDir - The directory containing the .gitignore file
 * @returns {object|null} An ignore instance that can be used to test paths, or null if not available
 */
async function loadGitignore(rootDir) {
  if (!ignoreModule) return null;
  
  const ig = ignoreModule();
  try {
    const content = await fs.readFile(path.join(rootDir, '.gitignore'), 'utf8');
    ig.add(content);
  } catch {
    // No .gitignore found or couldn't read it
  }
  return ig;
}

async function walk(dir, allowExts, excludeDirs, gitignore = null, rootDir = '', files = []) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const absPath = path.join(dir, entry.name);
      const relPath = rootDir ? path.relative(rootDir, absPath) : absPath;
      
      // Check gitignore if available
      if (gitignore && gitignore.ignores(relPath.split(path.sep).join('/'))) {
        continue;
      }
      
      if (entry.isDirectory()) {
        if (!excludeDirs.has(entry.name)) {
          await walk(absPath, allowExts, excludeDirs, gitignore, rootDir, files);
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name);
        if (allowExts.has(ext) || allowExts.has(entry.name)) {
          files.push(absPath);
        }
      }
    }
  } catch (error) {
    console.warn(`Warning: Could not read directory "${dir}": ${error.message}`);
  }
  return files;
}

async function isTextFile(filePath) {
  try {
    const fd = await fs.open(filePath, 'r');
    const buffer = Buffer.alloc(4096);
    const { bytesRead } = await fd.read(buffer, 0, 4096, 0);
    await fd.close();
    
    // Check for NULL bytes which indicate binary content
    for (let i = 0; i < bytesRead; i++) {
      if (buffer[i] === 0) return false;
    }
    return true;
  } catch {
    return false;
  }
}

/**
 * Generates a table of contents for easier navigation
 * @param {Array} fileEntries - Array of file entry objects
 * @returns {string} Markdown formatted table of contents
 */
function generateTableOfContents(fileEntries) {
  let toc = "## Table of Contents\n\n";
  fileEntries.forEach(({ rel }) => {
    // Create markdown heading link using the file path
    const linkText = rel.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();
    toc += `- [${rel}](#${linkText})\n`;
  });
  return toc + "\n\n---\n\n";
}

/**
 * Generates a visually appealing and informative text-based tree structure.
 * - Directories are marked with a trailing '/'
 * - Entries are sorted with directories first, then files, all alphabetically.
 * - Provides a header with the root name and total file count.
 * @param {string[]} files - An array of relative file paths (using '/' as separator).
 * @param {string} rootDisplayName - The name to display for the root of the tree.
 * @returns {string} The formatted tree string.
 */
function generateTree(files, rootDisplayName = '.') {
    const tree = {};

    for (const file of files) {
        // *** THE FIX IS HERE: Using '/' explicitly ***
        const parts = file.split('/'); 
        let currentLevel = tree;
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            const isLast = i === parts.length - 1;

            if (!currentLevel[part]) {
                currentLevel[part] = {
                    type: isLast ? 'file' : 'directory',
                    children: isLast ? null : {},
                };
            }
            currentLevel = currentLevel[part].children;
        }
    }

    const buildTreeString = (node, prefix = '') => {
        let result = '';
        const entries = Object.entries(node).sort(([aName, aNode], [bName, bNode]) => {
            if (aNode.type === bNode.type) {
                return aName.localeCompare(bName);
            }
            return aNode.type === 'directory' ? -1 : 1;
        });

        entries.forEach(([name, childNode], index) => {
            const isLast = index === entries.length - 1;
            const connector = isLast ? '└── ' : '├── ';
            const displayName = childNode.type === 'directory' ? `${name}/` : name;
            
            result += `${prefix}${connector}${displayName}\n`;

            if (childNode.children) {
                const childPrefix = prefix + (isLast ? '    ' : '│   ');
                result += buildTreeString(childNode.children, childPrefix);
            }
        });
        return result;
    };

    const fileCount = files.length === 1 ? '1 file' : `${files.length} files`;
    const header = `${rootDisplayName} (${fileCount})\n`;
    return header + buildTreeString(tree);
}

async function main() {
  const config = parseArgs(process.argv.slice(2));

  if (config.help) {
    console.log(`
Usage: export-to-mdnew.mjs [options] [directories...]

Options:
  --out=FILE               Output file path (default: docs/code-snapshot.md)
  --max-bytes=N            Skip files larger than N bytes (default: 524288)
  --exclude-dir=A,B,C      Exclude directories (comma-separated)
  --include-ext=.a,.b,.c   Include only files with these extensions
  --exclude-file=A,B,C     Exclude files by name (comma-separated)
  --no-gitignore           Don't respect .gitignore files
  -h, --help               Show this help message
`);
    return;
  }

  const roots = config.roots.map((p) => path.resolve(p));
  const allFiles = [];
  
  // Load gitignore for each root if enabled and module is available
  const gitignores = {};
  if (config.useGitignore && ignoreModule) {
    for (const root of roots) {
      gitignores[root] = await loadGitignore(root);
    }
  } else if (config.useGitignore) {
    console.warn('Warning: .gitignore support is disabled because the "ignore" package is not installed.');
  }
  
  for (const r of roots) {
    const stat = await fs.stat(r).catch(() => null);
    if (stat?.isDirectory()) {
      const gitignore = config.useGitignore ? gitignores[r] : null;
      await walk(r, config.allowExts, config.excludeDirs, gitignore, r, allFiles);
    }
  }

  const filePairs = allFiles.map((abs) => {
    // This part correctly normalizes paths to use '/'
    const rel = path.relative(process.cwd(), abs).split(path.sep).join('/');
    return { abs, rel };
  }).sort((a, b) => a.rel.localeCompare(b.rel));
  
  const rootDisplayNames = roots.map(r => path.relative(process.cwd(), r) || '.').join(', ');
  const tree = generateTree(filePairs.map(p => p.rel), rootDisplayNames);
  
  const header = `# Code Snapshot

**Generated:** ${new Date().toISOString()}
**Roots:** ${rootDisplayNames}
**Max file size:** ${config.maxBytes === 0 ? 'unlimited' : config.maxBytes.toLocaleString() + ' bytes'}

## Project Structure

\`\`\`
${tree}
\`\`\`

---
`;
  
  const fenceFor = (content) => content.includes('```') ? '````' : '```';
  
  let skippedLarge = 0;
  let skippedNamed = 0;
  let skippedBinary = 0;
  let included = 0;
  const fileEntries = [];
  
  // Add progress indicator
  const totalFiles = filePairs.length;
  console.log(`Processing ${totalFiles} files...`);
  let processedCount = 0;
  
  for (const { abs, rel } of filePairs) {
    // Update progress
    processedCount++;
    if (processedCount % 10 === 0 || processedCount === totalFiles) {
      process.stdout.write(`\rProcessing: ${processedCount}/${totalFiles} (${Math.round(processedCount/totalFiles*100)}%)`);
    }
   
    const base = path.basename(abs);
   
    if (config.excludeFiles.has(base)) { 
      skippedNamed++; 
      continue; 
    }
   
    // Check if it's a binary file
    if (!(await isTextFile(abs))) {
      skippedBinary++;
      continue;
    }
   
    if (config.maxBytes > 0) {
      try {
        const stats = await fs.stat(abs);
        if (stats.size > config.maxBytes) {
          skippedLarge++;
          continue;
        }
      } catch {
        continue;
      }
    }
    
    try {
      const content = await fs.readFile(abs, 'utf8');
      included++;
      const lang = langForExt(path.extname(abs) || path.basename(abs));
      const fence = fenceFor(content);
      const stats = await fs.stat(abs);
      fileEntries.push({ 
        rel, 
        lang, 
        fence, 
        content,
        size: stats.size,
        modified: stats.mtime.toISOString()
      });
    } catch {
      // Skip files we can't read
    }
  }

  console.log('\nGenerating markdown output...');
  const target = path.resolve(config.out || 'docs/code-snapshot.md');
  await fs.mkdir(path.dirname(target), { recursive: true });
  
  // Use stream for better performance with large files
  const writeStream = createWriteStream(target);
  writeStream.write(header);
  
  // Add table of contents
  writeStream.write(generateTableOfContents(fileEntries));
  
  for (const { rel, lang, fence, content, size, modified } of fileEntries) {
    // Write the file section with collapsible details tag
    writeStream.write(`## ${rel}\n\n`);
    writeStream.write(`*Size: ${size.toLocaleString()} bytes | Modified: ${modified}*\n\n`);
    writeStream.write(`<details>\n<summary>View code</summary>\n\n`);
    writeStream.write(`${fence}${lang}\n${content}\n${fence}\n\n`);
    writeStream.write(`</details>\n\n\n`);
  }
  
  // Close the stream
  writeStream.end();
  
  // Wait for the write to complete
  await new Promise((resolve) => writeStream.on('finish', resolve));
  
  const summaryParts = [`${included} files included`]; 
  if (skippedLarge > 0) summaryParts.push(`${skippedLarge} skipped (> ${config.maxBytes.toLocaleString()} bytes)`);
  if (skippedNamed > 0) summaryParts.push(`${skippedNamed} skipped by name`);
  if (skippedBinary > 0) summaryParts.push(`${skippedBinary} skipped (binary files)`);

  console.log(`Wrote to ${target} (${summaryParts.join(', ')})`);
}

// This is the entry point of the script
(async function() {
  try {
    await main();
  } catch (e) {
    console.error('An unexpected error occurred:', e);
    process.exit(1);
  }
})();
````

</details>


