# 🧱 LocalPilot

## Phase 0: Foundation & Skeleton (Detailed, AI-Agent Ready)

> **Phase 0 Principle:**
> No intelligence. No autonomy. No shortcuts.
> Only *structure, contracts, and verified plumbing*.

**Hard Rules for the AI Agent:**

* Execute tasks **in order**
* Do not merge tasks
* Do not “optimize” ahead
* Stop immediately if verification fails
* Do not invent APIs or behavior not specified

📌 Architecture reference 
📌 Phase definition 

---

## 🔹 TASK 0.1 — Initialize Monorepo & Tooling

### 🎯 Objective

Create a clean monorepo with **zero logic**, but correct tooling.

### 📂 Actions

1. Initialize git repository
2. Create root folders:

   * `extension/`
   * `server/`
   * `docs/`
   * `scripts/`
3. Add root config files:

   * `.gitignore`
   * `.editorconfig`
   * `README.md`
4. Add package managers:

   * `pnpm` for extension
   * `uv` / `pip` for server

### ✅ Verification

* [ ] `git status` clean
* [ ] No missing root folders
* [ ] No code yet

---

## 🔹 TASK 0.2 — Create Extension Project Skeleton

### 🎯 Objective

VS Code extension builds and activates.

### 📂 Actions

1. Inside `extension/`:

   * Initialize `package.json`
   * Add `engines.vscode`
   * Define activation events
2. Add TypeScript config:

   * `tsconfig.json`
3. Add build tooling:

   * esbuild
   * Vitest
4. Create `src/extension.ts` with:

   * empty `activate`
   * empty `deactivate`

### ❗ Rules

* No WebView yet
* No services yet

### ✅ Verification

* [ ] `pnpm run build` succeeds
* [ ] Extension activates in VS Code dev host
* [ ] No runtime errors

---

## 🔹 TASK 0.3 — Create Server Project Skeleton

### 🎯 Objective

Python FastAPI server starts cleanly.

### 📂 Actions

1. Inside `server/`:

   * Initialize Python package
   * Create virtual environment
2. Add dependencies:

   * `fastapi`
   * `uvicorn`
3. Create `main.py`:

   * Initialize FastAPI app
   * Add `/health` endpoint

### ❗ Rules

* No indexing logic
* No Ollama calls

### ✅ Verification

* [ ] `uvicorn main:app` runs
* [ ] `/health` returns `{ status: "ok" }`
* [ ] No warnings or stack traces

---

## 🔹 TASK 0.4 — Define Core Domain Entities (Extension)

### 🎯 Objective

Create **pure domain models**.

### 📂 Files to Create

* `Message`
* `Project`
* `Plan`
* `Task`

📌 Entity definitions per architecture spec 

### ❗ Rules

* Interfaces only
* No logic
* No imports from Features/UI
* JSDoc on every field

### ✅ Verification

* [ ] TypeScript compiles
* [ ] Entities exportable via barrel
* [ ] No circular imports

---

## 🔹 TASK 0.5 — Define Core Interfaces (Ports)

### 🎯 Objective

Define **contracts**, not implementations.

### 📂 Interfaces

* `ILLMProvider`
* `IRAGProvider`
* `IFileSystem`
* `ISettings`

📌 Interface rules 

### ❗ Rules

* No Node.js APIs
* No VS Code APIs
* Async signatures only

### ✅ Verification

* [ ] Interfaces compile
* [ ] Can be imported by Features
* [ ] No default implementations

---

## 🔹 TASK 0.6 — Define Core Error Model

### 🎯 Objective

Unify error handling across extension.

### 📂 Files

* `LocalPilotError` (base)
* Error categories:

  * connection
  * indexing
  * llm
  * file
  * validation

📌 Error handling strategy 

### ❗ Rules

* All errors serializable
* Include `recoverable` flag
* No throwing raw `Error`

### ✅ Verification

* [ ] Errors can be logged as JSON
* [ ] Errors preserve stack trace

---

## 🔹 TASK 0.7 — Create API Client (Extension → Server)

### 🎯 Objective

Allow extension to talk to server.

### 📂 Actions

1. Create HTTP client wrapper
2. Implement:

   * `checkHealth()`
3. Log responses to Output Channel

### ❗ Rules

* No retries yet
* No WebSocket yet

### ✅ Verification

* [ ] Extension calls `/health`
* [ ] Server response logged
* [ ] Failure handled gracefully

---

## 🔹 TASK 0.8 — Implement Ollama Availability Check

### 🎯 Objective

Detect Ollama runtime **without using it**.

### 📂 Actions

1. Call:

   * `GET http://localhost:11434/api/version`
2. Parse response
3. Expose boolean status

📌 Ollama dependency rules 

### ❗ Rules

* No generation
* No embeddings
* No model listing yet

### ✅ Verification

* [ ] Correct detection when Ollama running
* [ ] Clear error when not running

---

## 🔹 TASK 0.9 — Create Minimal WebView Panel

### 🎯 Objective

Show a sidebar panel without logic.

### 📂 Actions

1. Register WebViewViewProvider
2. Render static HTML:

   * “LocalPilot”
   * Server status
   * Ollama status

### ❗ Rules

* No React yet
* No state management

### ✅ Verification

* [ ] Panel loads
* [ ] Status updates visible
* [ ] No console errors

---

## 🔹 TASK 0.10 — Wire Extension Composition Root

### 🎯 Objective

Respect Clean Architecture dependency flow.

### 📂 Actions

1. In `activate()`:

   * Instantiate infrastructure
   * Inject into features (even if empty)
2. Do NOT create global singletons

📌 Dependency rules 

### ✅ Verification

* [ ] No feature imports infrastructure directly
* [ ] Clear composition root

---

## 🔹 TASK 0.11 — Add Baseline Tests

### 🎯 Objective

Ensure foundation is testable.

### 📂 Tests

* Extension activation test
* Server `/health` test

📌 Testing strategy 

### ❗ Rules

* No mocks for core entities
* Tests must pass in CI

### ✅ Verification

* [ ] `pnpm test` passes
* [ ] `pytest` passes

---

## 🔹 TASK 0.12 — Phase 0 Exit Validation

### 🎯 Objective

Lock Phase 0 as stable.

### Validation Checklist

* [ ] Extension activates
* [ ] WebView loads
* [ ] Server responds
* [ ] Ollama detected
* [ ] No indexing code exists
* [ ] All tests pass

---

## ✅ Phase 0 — COMPLETE

At this point:

* You have a **living skeleton**
* Architecture boundaries are enforced
* You are safe to build intelligence on top

---