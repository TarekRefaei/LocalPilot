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

## 🔹 Phase 2.5 — “Backbone Hardening” (Recommended Name)

### Goal:

> Make *any* indexed workspace **explainable** to the LLM.

### Scope (non-negotiable):

### 1️⃣ Introduce Semantic Chunk Types

* Replace `symbol_type="file"` monopoly
* Even regex-based chunking is acceptable initially
* Must produce **multiple chunks per file**

---

### 2️⃣ Generate & Persist Project Summary

* After indexing completes:

  * Ask LLM to summarize the project
  * Save it to:

    ```
    ~/.localpilot/<projectId>/summary.json
    ```
* Inject this summary into **every chat session**

This alone will dramatically change behavior.

---

### 3️⃣ Enforce Index Coverage Checks

Before chat:

* If index empty → block chat
* If summary missing → regenerate
* If sync required → warn user

This keeps the backbone honest.

---

### 4️⃣ Add Backbone Validation Queries (Internal)

Examples:

* “What is the main purpose of this project?”
* “List key files”
* “Where is indexing implemented?”

If these fail → indexing is broken.

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