Excellent — this is the **right order** to do it.
We’ll treat this as a **design + migration milestone**, not coding yet.

I’ll proceed in **three clear layers**, exactly as you asked:

---

# PART A — Project documentation updates (what must change)

This ensures your **docs, architecture, and code stay aligned**.

## Documents that MUST be updated

### 1️⃣ `architecture.md` (REQUIRED)

**Why:**
Your architecture currently describes *modes* implicitly.
You are now making them **explicit UI views with hard boundaries**.

**Add a new section:**

#### 🔹 “UI Modes & Responsibility Separation”

Content to add (conceptual):

* Chat Mode = read-only understanding
* Plan Mode = intent authoring
* Act Mode = execution
* Modes are **UI-separated AND prompt-separated**
* One-way lifecycle: `Chat → Plan → Act`

---

### 2️⃣ `state-model.md` (REQUIRED)

**Why:**
You now have **multiple UI states** sharing some data and isolating others.

**Add:**

* View-scoped state
* Cross-view shared read-only state
* Promotion rules between states

We’ll define this precisely in **Part B** below.

---

### 3️⃣ `security-model.md` (REQUIRED)

**Why:**
This change strengthens security — and should be documented.

**Add a section:**

#### 🔹 “Mode-based Capability Isolation”

Key points:

* Chat View cannot create plans
* Plan View cannot execute
* Act View cannot hallucinate intent
* Capabilities are unlocked by **view + approval state**, not LLM output

This makes your system defensible and auditable.

---

### 4️⃣ `structure.md` (REQUIRED)

**Why:**
You’re moving from *one sidebar* → *multiple views in one container*.

**Update structure to include:**

```
extension/src/views/
  ├── chat/
  ├── plan/
  └── act/
```

Even if Act is empty for now, it must be reserved.

---

### 5️⃣ `overview.md` (RECOMMENDED)

**Why:**
New contributors must understand this immediately.

Add a short diagram-style explanation:

```
Chat View  →  Plan View  →  Act View
(read)        (decide)      (execute)
```

---

# PART B — Design of VS Code views & contribution points

This is the **canonical UI design** going forward.

---

## 🎛️ Sidebar container (single)

You keep **one Activity Bar icon**:

```json
"viewsContainers": {
  "activitybar": [
    {
      "id": "localpilot",
      "title": "LocalPilot",
      "icon": "./media/icon-localpilot.svg"
    }
  ]
}
```

✅ Good — do NOT change this.

---

## 📂 Views inside the container (TABBED)

### Chat / Plan / Act as **sibling views**

```json
"views": {
  "localpilot": [
    {
      "id": "localpilot.chat",
      "name": "Chat",
      "type": "webview"
    },
    {
      "id": "localpilot.plan",
      "name": "Plan",
      "type": "webview"
    },
    {
      "id": "localpilot.act",
      "name": "Act",
      "type": "webview"
    }
  ]
}
```

### Why this is correct

* Native VS Code tabs
* No custom tab logic
* Built-in persistence
* Predictable UX

---

## 🗨️ Chat View — Contribution rules

**View ID:** `localpilot.chat`

### Responsibilities

* Chat UI
* RAG queries
* Status checks
* Indexing trigger

### Forbidden

* Plan creation
* Execution
* Markdown editing

### Commands visible

* Index workspace
* Clear chat

---

## 🧩 Plan View — Contribution rules

**View ID:** `localpilot.plan`

### Responsibilities

* Planning conversation
* Generate plan
* Markdown editor
* Validate / approve

### Commands visible

* Create Plan
* Validate Plan
* Approve Plan

### Uses

* `PLAN_SYSTEM_PROMPT`
* Plan API only

---

## ⚙️ Act View — Contribution rules (future)

**View ID:** `localpilot.act`

### Responsibilities

* Task list
* Diff preview
* Execute approved tasks

### Entry condition

* Approved plan exists

### Default state (Phase 3)

* Disabled / placeholder

---

# PART C — Shared vs Isolated State Contracts

This is **critical**. Here is the exact contract.

---

## 🔗 Shared (Read-only across tabs)

| State           | Owner   | Notes                    |
| --------------- | ------- | ------------------------ |
| Project summary | Server  | Immutable after indexing |
| Symbols index   | Server  | Immutable after indexing |
| Indexing status | Server  | Single source of truth   |
| Workspace ID    | VS Code | Global                   |

---

## 🔒 Isolated per tab (STRICT)

### Chat View

* ChatSessionStore (chat messages)
* Chat WebSocket connection
* Chat prompt only

### Plan View

* Plan markdown (authoritative)
* Parsed Plan object
* Validation warnings
* Approval state

### Act View

* Execution cursor
* Task status
* Diffs
* Rollback state

🚨 No tab can mutate another tab’s state directly.

---

## 🔁 Allowed promotions (one-way)

| From        | To             | Condition       |
| ----------- | -------------- | --------------- |
| Chat → Plan | User-triggered | Indexed project |
| Plan → Act  | User-approved  | Valid plan      |
| Act → Chat  | ❌              | Forbidden       |
| Act → Plan  | ❌              | Forbidden       |

---

# PART D — Migration strategy (single sidebar → tabbed views)

This is **low risk** if done correctly.

---

## Step 1 — Extract Chat View

* Move current `MainPanel` logic into:

  ```
  views/chat/chat-view.ts
  ```
* Register it as `localpilot.chat`

---

## Step 2 — Introduce Plan View (empty shell)

* Create:

  ```
  views/plan/plan-view.ts
  ```
* Move existing Plan WebView logic here
* No behavior change yet

---

## Step 3 — Add Act View placeholder

* Static HTML:

  > “Act Mode will be available once a plan is approved.”

This avoids later breaking changes.

---

## Step 4 — Update command visibility

Commands appear **only in relevant views** using `when` clauses:

```json
"when": "view == localpilot.plan"
```

---