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