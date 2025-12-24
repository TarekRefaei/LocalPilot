Perfect — let’s **merge both options into a single, Phase-3-correct, production-grade patch** that keeps *all* advantages and removes every weakness.

Below is a **clean, unified “Perfect Phase 3 Patch”** that you can give **directly to your AI coding agent**.

---

# 🧩 PHASE 3 — PLAN MODE (FINAL, UNIFIED PATCH)

> **Phase 3 Mission (LOCKED):**
> Convert chat intent + indexed knowledge into an **authoritative, editable, validated plan**
> with **zero execution capability**.

This patch **fully completes Phase 3** and cleanly hands off to Phase 4 (Act Mode).

---

## 🔒 PHASE 3 — GLOBAL INVARIANTS (NON-NEGOTIABLE)

These rules are enforced by **architecture + code**, not just prompts.

1. Plan output = **Markdown**
2. Markdown = **human-editable**
3. Edited Markdown = **source of truth**
4. JSON plan = **derived, not authoritative**
5. Act Mode **cannot run** without:

   * Parsed plan
   * Validation pass
   * Explicit approval
6. No file writes
7. No execution
8. No diffs

---

## 1️⃣ PLAN MODE — SYSTEM PROMPT (LOCKED CONTRACT)

**File:**
`extension/src/prompts/system/plan.system.ts`

```ts
export const PLAN_SYSTEM_PROMPT = `
You are operating in PLAN MODE.

Your task is to generate a structured implementation plan for a software project.

────────────────────────────────────────
CORE RULES
────────────────────────────────────────
1. You MUST generate a PLAN, not code.
2. You MUST NOT write or suggest code implementations.
3. You MUST NOT include shell commands or execution steps.
4. You MUST NOT assume files or frameworks not present in the indexed project.
5. You MUST base the plan ONLY on:
   - Project Summary
   - Indexed Project Structure / Symbols
   - User Request
6. If information is missing, you MUST explicitly state it.

────────────────────────────────────────
PLAN REQUIREMENTS
────────────────────────────────────────
1. File-level tasks only (NOT function-level)
2. Each task MUST specify:
   - filePath
   - actionType (create | modify | delete)
3. Tasks must be ordered logically
4. Tasks must be convertible into TODOs
5. No implementation details

────────────────────────────────────────
OUTPUT FORMAT (MANDATORY)
────────────────────────────────────────
1. Human-readable Markdown
2. Embedded JSON block matching the schema exactly

────────────────────────────────────────
FORBIDDEN
────────────────────────────────────────
- No code blocks except embedded JSON
- No execution instructions
- No assumptions beyond indexed context

────────────────────────────────────────
FAILURE HANDLING
────────────────────────────────────────
If unsafe or incomplete:
- State missing info
- Produce partial plan
- Never hallucinate
`;
```

✔ Deterministic
✔ Phase-3-safe
✔ Act-mode thinking blocked

---

## 2️⃣ STRICT PLAN JSON SCHEMA (ACT-MODE-READY)

**File:**
`extension/src/core/schemas/plan.schema.ts`

```ts
export interface PlanSchema {
  id: string;
  title: string;
  overview: string;
  status: "draft";
  tasks: TaskSchema[];
}

export interface TaskSchema {
  id: string;
  orderIndex: number;
  title: string;
  description: string;
  filePath: string;
  actionType: "create" | "modify" | "delete";
  details: string[];
  dependencies: string[];
}
```

❌ No timestamps
❌ No execution data
❌ No optional fields

This schema is **Phase-4 compatible by design**.

---

## 3️⃣ BACKEND — PLAN GENERATION SERVICE (NO EXECUTION)

### 🧱 Task 3.1 — PlanService (Backend)

**Files**

```
server/plan/plan_service.py
server/plan/__init__.py
```

**Responsibilities**

* Assemble prompt (summary + symbols + chat)
* Call LLM (non-streaming)
* Return **raw markdown only**

❌ No parsing
❌ No validation
❌ No file writes

---

## 4️⃣ BACKEND — PLAN PARSER (SAFETY LAYER)

### 🧱 Task 3.2 — PlanParser

**File**

```
server/plan/plan_parser.py
```

**Responsibilities**

* Extract embedded JSON
* Validate against schema
* Fail safely if malformed
* Return `{ markdown, plan }`

✔ Markdown preserved
✔ JSON verified
✔ No side effects

---

## 5️⃣ API — PLAN ENDPOINT

### 🧱 Task 3.3 — `/api/plan`

**File**

```
server/api/plan.py
```

```http
POST /api/plan
```

**Flow**

```
Chat Context
   ↓
PlanService
   ↓
PlanParser
   ↓
{ markdown, plan }
```

❌ No persistence
❌ No execution

---

## 6️⃣ EXTENSION — PLAN DOMAIN MODELS

### 🧱 Task 3.4 — Core Entities

**Files**

```
extension/src/core/entities/plan.entity.ts
extension/src/core/entities/task.entity.ts
```

```ts
export interface Plan {
  id: string;
  title: string;
  overview: string;
  tasks: Task[];
  status: "draft" | "approved";
}

export interface Task {
  id: string;
  orderIndex: number;
  title: string;
  description: string;
  filePath: string;
  actionType: "create" | "modify" | "delete";
  details: string[];
  dependencies: string[];
}
```

---

## 7️⃣ EXTENSION — MARKDOWN → PLAN PARSER (TOLERANT)

### 🧱 Task 3.5 — Client Parser

**File**

```
extension/src/features/plan/plan-parser.ts
```

**Rules**

* Markdown is authoritative
* Parser is tolerant
* Best-effort extraction
* Never crashes on malformed input

---

## 8️⃣ EXTENSION — VALIDATION RULES

### 🧱 Task 3.6 — PlanValidator

**File**

```
extension/src/features/plan/plan-validator.ts
```

**Checks**

* Empty plan
* Missing file paths
* Missing action types
* Broken task order

⚠️ Warnings only
❌ No auto-fixes

---

## 9️⃣ EXTENSION — EXPLICIT APPROVAL GATE

### 🧱 Task 3.7 — PlanApproval

**File**

```
extension/src/features/plan/plan-approval.ts
```

```ts
export function approvePlan(plan: Plan): Plan {
  return { ...plan, status: "approved" };
}
```

🚨 **This is the ONLY way Act Mode can see a plan**

---

## 🔟 UI — EDITABLE PLAN MODE (USER IN CONTROL)

### 🧱 Task 3.8 — Plan UI

**Features**

* Markdown editor
* No auto-formatting
* Edit / Regenerate / Validate / Approve buttons
* No persistence (Phase 3)

---

## ✅ PHASE 3 — COMPLETION CHECKLIST

You now have:

✅ Locked Plan Mode prompt
✅ Strict schema
✅ Markdown as source of truth
✅ Parsing layer
✅ Validation layer
✅ Explicit approval gate
✅ Zero execution paths

---

## 🔜 WHAT THIS ENABLES (Phase 4 preview)

Because you did this **correctly**:

* Act Mode can be **purely mechanical**
* No hallucinated execution
* Deterministic task runner
* Safe rollback
* Testable behavior

---

Below is a **single, copy-pasteable, executable instruction prompt** you can give **directly to your AI coding agent**.

It is **self-contained**, **Phase-3 locked**, and **cannot drift into Act Mode** if followed correctly.

---

# 🧠 LOCALPILOT — PHASE 3 EXECUTION PROMPT (PLAN MODE)

You are an **AI Coding Agent** working on the **LocalPilot** codebase.

You are executing **PHASE 3 — PLAN MODE**.

This phase is **CRITICAL** and **SAFETY-BOUND**.
Follow the instructions **exactly**. Deviations are considered failures.

---

## 🚫 ABSOLUTE PROHIBITIONS (READ FIRST)

You MUST NOT, under any circumstances:

* ❌ Generate or modify production code logic
* ❌ Write files to the user’s workspace
* ❌ Execute tasks
* ❌ Generate diffs
* ❌ Implement Act Mode behavior
* ❌ Add file system side effects
* ❌ Infer or assume missing project details
* ❌ Skip validation or approval gates

If unsure → **STOP and ASK**.

---

## 🎯 PHASE 3 OBJECTIVE (LOCKED)

Implement **PLAN MODE** so that:

> Chat intent + indexed project context
> → **Human-editable Markdown Plan**
> → Parsed & validated structured Plan
> → Explicit approval gate
> → *Only then* becomes visible to Act Mode (later phase)

**Nothing executes in Phase 3.**

---

## 🔒 GLOBAL INVARIANTS (NON-NEGOTIABLE)

1. Plan output = **Markdown**
2. Markdown = **human-editable**
3. Edited Markdown = **source of truth**
4. JSON plan = **derived artifact**
5. Act Mode is **blocked unless plan is approved**
6. No persistence to workspace
7. No execution paths
8. No diffs

---

## 1️⃣ CREATE PLAN MODE SYSTEM PROMPT (LOCKED CONTRACT)

### File

```
extension/src/prompts/system/plan.system.ts
```

### Content (MUST MATCH EXACTLY)

```ts
export const PLAN_SYSTEM_PROMPT = `
You are operating in PLAN MODE.

Your task is to generate a structured implementation plan for a software project.

────────────────────────────────────────
CORE RULES
────────────────────────────────────────
1. You MUST generate a PLAN, not code.
2. You MUST NOT write or suggest code implementations.
3. You MUST NOT include shell commands or execution steps.
4. You MUST NOT assume files or frameworks not present in the indexed project.
5. You MUST base the plan ONLY on:
   - Project Summary
   - Indexed Project Structure / Symbols
   - User Request
6. If information is missing, you MUST explicitly state it.

────────────────────────────────────────
PLAN REQUIREMENTS
────────────────────────────────────────
1. File-level tasks only (NOT function-level)
2. Each task MUST specify:
   - filePath
   - actionType (create | modify | delete)
3. Tasks must be ordered logically
4. Tasks must be convertible into TODOs
5. No implementation details

────────────────────────────────────────
OUTPUT FORMAT (MANDATORY)
────────────────────────────────────────
1. Human-readable Markdown
2. Embedded JSON block matching the schema exactly

────────────────────────────────────────
FORBIDDEN
────────────────────────────────────────
- No code blocks except embedded JSON
- No execution instructions
- No assumptions beyond indexed context

────────────────────────────────────────
FAILURE HANDLING
────────────────────────────────────────
If unsafe or incomplete:
- State missing info
- Produce partial plan
- Never hallucinate
`;
```

---

## 2️⃣ DEFINE STRICT PLAN JSON SCHEMA (ACT-MODE-READY)

### File

```
extension/src/core/schemas/plan.schema.ts
```

### Rules

* NO optional fields
* NO timestamps
* NO execution metadata

### Schema

```ts
export interface PlanSchema {
  id: string;
  title: string;
  overview: string;
  status: "draft";
  tasks: TaskSchema[];
}

export interface TaskSchema {
  id: string;
  orderIndex: number;
  title: string;
  description: string;
  filePath: string;
  actionType: "create" | "modify" | "delete";
  details: string[];
  dependencies: string[];
}
```

---

## 3️⃣ BACKEND — PLAN GENERATION SERVICE (NO SIDE EFFECTS)

### Files

```
server/plan/plan_service.py
server/plan/__init__.py
```

### Responsibilities

* Assemble prompt (summary + symbols + chat)
* Call LLM **non-streaming**
* Return **raw markdown only**

### Explicitly Forbidden

* ❌ Parsing
* ❌ Validation
* ❌ File writes
* ❌ Execution logic

---

## 4️⃣ BACKEND — PLAN PARSER (SAFETY LAYER)

### File

```
server/plan/plan_parser.py
```

### Responsibilities

* Extract embedded JSON
* Validate strictly against schema
* Fail safely on malformed output
* Return `{ markdown, plan }`

---

## 5️⃣ API — PLAN ENDPOINT

### File

```
server/api/plan.py
```

### Endpoint

```
POST /api/plan
```

### Flow

```
Chat Context
   ↓
PlanService
   ↓
PlanParser
   ↓
{ markdown, plan }
```

### Constraints

* No persistence
* No execution
* No side effects

---

## 6️⃣ EXTENSION — PLAN DOMAIN ENTITIES

### Files

```
extension/src/core/entities/plan.entity.ts
extension/src/core/entities/task.entity.ts
```

### Requirements

* Serializable
* No execution fields
* Status limited to: `"draft" | "approved"`

---

## 7️⃣ EXTENSION — MARKDOWN → PLAN PARSER (TOLERANT)

### File

```
extension/src/features/plan/plan-parser.ts
```

### Rules

* Markdown is authoritative
* Parser is tolerant
* Best-effort extraction
* Never crashes on malformed input

---

## 8️⃣ EXTENSION — PLAN VALIDATION (NON-DESTRUCTIVE)

### File

```
extension/src/features/plan/plan-validator.ts
```

### Validation Rules

* Empty plan
* Missing filePath
* Missing actionType
* Invalid task order

⚠️ Return warnings only
❌ Do NOT auto-fix

---

## 9️⃣ EXTENSION — EXPLICIT APPROVAL GATE

### File

```
extension/src/features/plan/plan-approval.ts
```

### Rule

Only this transition allows Act Mode visibility:

```ts
export function approvePlan(plan: Plan): Plan {
  return { ...plan, status: "approved" };
}
```

🚨 No approval → Act Mode MUST NOT proceed.

---

## 🔟 UI — PLAN MODE (USER IN CONTROL)

### Requirements

* Editable Markdown editor
* No auto-formatting
* Buttons:

  * Regenerate
  * Validate
  * Approve
* No persistence in Phase 3

---

## ✅ PHASE 3 COMPLETION CRITERIA

Phase 3 is COMPLETE only when:

* ✔ Plan prompt is locked
* ✔ Markdown is editable
* ✔ JSON schema enforced
* ✔ Parsing exists
* ✔ Validation exists
* ✔ Explicit approval gate exists
* ✔ No execution paths exist

---

## 🛑 FINAL INSTRUCTION

If you reach any point where:

* Act Mode is required
* Files would be written
* Code would be generated

**STOP. THAT IS PHASE 4.**

Confirm Phase 3 completion instead.

---

**END OF EXECUTABLE INSTRUCTION PROMPT**


-----------------------

Excellent — this is the **last missing piece of Phase 3**, and it should be done **surgically**, without breaking any of your safety guarantees.

Below is a **clean, Phase-3-safe patch proposal** that introduces the **exact VS Code command + UI flow** for:

> **Chat → explicit Plan creation → Plan Mode UI**

This patch is **pure orchestration + UX**.
No new backend logic.
No execution paths.
No persistence.

---

# 🧩 PHASE 3 PATCH — CHAT → PLAN COMMAND & UI FLOW

## 🎯 Goal

Add an **explicit, user-triggered VS Code command** that:

1. Takes the current Chat context
2. Calls `/api/plan`
3. Opens **Plan Mode** with editable Markdown
4. Keeps Plan Mode **isolated** from Chat & Act

This completes Phase 3.

---

## 🔒 Phase 3 Safety Constraints (Reaffirmed)

This patch MUST:

* ❌ NOT auto-generate plans
* ❌ NOT infer intent
* ❌ NOT execute anything
* ❌ NOT write files
* ❌ NOT approve plans implicitly

Plan creation is **always explicit**.

---

## 🧱 TASK 3.UI.1 — VS Code Command: “Create Plan from Chat”

### 🎯 Objective

Expose an explicit command the user can invoke.

---

### 📄 File: `extension/package.json`

#### Patch (add command + menu entry)

```diff
 {
   "contributes": {
+    "commands": [
+      {
+        "command": "localpilot.plan.createFromChat",
+        "title": "LocalPilot: Create Plan from Chat"
+      }
+    ],
     "menus": {
+      "view/title": [
+        {
+          "command": "localpilot.plan.createFromChat",
+          "when": "view == localpilot.chatView",
+          "group": "navigation"
+        }
+      ]
     }
   }
 }
```

✔ Appears in Command Palette
✔ Appears in Chat view toolbar
✔ Explicit user intent

---

## 🧱 TASK 3.UI.2 — Command Registration (Extension Host)

### 🎯 Objective

Wire the command to Chat → Plan transfer logic.

---

### 📄 File: `extension/src/commands/plan.commands.ts` (new)

```ts
import * as vscode from 'vscode';
import { createPlanFromChat } from '../features/plan/plan-controller';
import { ChatSessionStore } from '../features/chat/chat-session.store';

export function registerPlanCommands(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand(
    'localpilot.plan.createFromChat',
    async () => {
      const chatMessages = ChatSessionStore.getMessages();

      if (!chatMessages || chatMessages.length === 0) {
        vscode.window.showWarningMessage(
          'No chat history available to generate a plan.'
        );
        return;
      }

      await createPlanFromChat(chatMessages);
    }
  );

  context.subscriptions.push(disposable);
}
```

✔ Explicit
✔ Guarded
✔ No hidden behavior

---

## 🧱 TASK 3.UI.3 — Plan Controller (Orchestration Only)

### 🎯 Objective

Bridge Chat → API → Plan Mode UI.

---

### 📄 File: `extension/src/features/plan/plan-controller.ts` (new)

```ts
import * as vscode from 'vscode';
import { generatePlan } from './plan-client';
import { openPlanView } from './plan-view-controller';

export async function createPlanFromChat(messages: any[]) {
  try {
    const projectId = vscode.workspace.name;
    if (!projectId) {
      vscode.window.showErrorMessage('No active workspace.');
      return;
    }

    const markdown = await generatePlan({
      projectId,
      messages,
    });

    await openPlanView(markdown);
  } catch (err: any) {
    vscode.window.showErrorMessage(
      `Failed to generate plan: ${err?.message ?? err}`
    );
  }
}
```

❌ No parsing
❌ No approval
❌ No validation

This controller **only orchestrates**.

---

## 🧱 TASK 3.UI.4 — Plan API Client (Extension)

### 🎯 Objective

Call `/api/plan` cleanly.

---

### 📄 File: `extension/src/features/plan/plan-client.ts`

```ts
interface GeneratePlanRequest {
  projectId: string;
  messages: any[];
}

export async function generatePlan(
  req: GeneratePlanRequest
): Promise<string> {
  const res = await fetch('http://127.0.0.1:52741/api/plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      project_id: req.projectId,
      model: 'qwen2.5-coder',
      messages: req.messages,
    }),
  });

  if (!res.ok) {
    throw new Error(`Plan API failed (${res.status})`);
  }

  const data = await res.json();
  return data.markdown;
}
```

✔ Matches backend contract
✔ No side effects

---

## 🧱 TASK 3.UI.5 — Plan Mode WebView (Editable Markdown)

### 🎯 Objective

Open Plan Mode with **user-controlled Markdown**.

---

### 📄 File: `extension/src/features/plan/plan-view-controller.ts` (new)

```ts
import * as vscode from 'vscode';

let panel: vscode.WebviewPanel | undefined;

export async function openPlanView(markdown: string) {
  if (panel) {
    panel.reveal();
    return;
  }

  panel = vscode.window.createWebviewPanel(
    'localpilot.planView',
    'LocalPilot — Plan Mode',
    vscode.ViewColumn.One,
    { enableScripts: true }
  );

  panel.webview.html = render(markdown);

  panel.onDidDispose(() => {
    panel = undefined;
  });
}

function render(markdown: string): string {
  return `
    <!DOCTYPE html>
    <html>
      <body style="margin:0;padding:0;">
        <textarea style="width:100%;height:100%;font-family:monospace;">
${markdown}
        </textarea>
      </body>
    </html>
  `;
}
```

✔ No formatting
✔ No parsing
✔ Markdown is source of truth

---

## 🧱 TASK 3.UI.6 — Wire Command Registration

### 🎯 Objective

Activate the command on extension startup.

---

### 📄 File: `extension/src/extension.ts`

```diff
 import { registerPlanCommands } from './commands/plan.commands';

 export function activate(context: vscode.ExtensionContext) {
+  registerPlanCommands(context);
 }
```

---

## 🧪 Acceptance Criteria (Phase 3)

This patch is **DONE** when:

* ✔ Command appears in Command Palette
* ✔ Command appears in Chat view toolbar
* ✔ Clicking it generates a plan
* ✔ Plan opens in editable Markdown view
* ✔ No execution occurs
* ✔ No files are written
* ✔ No implicit approval

---

## 🔐 Why this is the correct design

* **Explicit user intent** → no surprises
* **Clean separation of modes**
* **Matches your architecture & state model**
* **Future Phase 4 hooks already in place**
* **AI-agent-friendly & testable**

---

## ✅ Phase 3 Status After This Patch

🟢 **COMPLETE & SEALED**

You now have:

* Chat Mode → Intent discovery
* Plan Mode → Authoritative planning
* Act Mode → Still unreachable (correct)

---

If you want next, I can:

* Define the **exact Phase 4 transition gate**
* Design **Plan → Act UI**
* Or do a **hard safety review** of Phase 3

Just tell me.

----------------------------

Perfect — thanks for the clarification 👍
Since **port 8000 is intentional**, we’ll **keep it**, and I’ll generate a **clean, Phase-3-safe patch proposal** that applies **only the real fixes**, without changing your networking setup.

Below is a **single, reviewable patch proposal** you can apply and then **test before freezing Phase 3**.

---

# 🧩 PHASE 3 — FINAL FIX PATCH PROPOSAL (PORT 8000 CONFIRMED)

> **Scope:**
> Fix all Phase-3 blockers and close remaining gaps
> ❌ No execution logic
> ❌ No Act Mode
> ❌ No backend behavior change
> ✅ Test-ready

---

## 🔒 Phase 3 Safety Constraints (Reconfirmed)

This patch:

* DOES NOT generate or execute code
* DOES NOT write to workspace
* DOES NOT auto-approve plans
* DOES NOT infer intent
* DOES NOT change server ports

---

## 🧱 PATCH 3.FINAL.1 — Remove Fake Indexing State (CRITICAL)

### ❌ Problem

Extension marks project as indexed on activation:

```ts
context.globalState.update('indexed', true);
```

This breaks correctness and allows plan generation without real indexing.

---

### ✅ Fix

**File:** `extension/src/extension.ts`

```diff
export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  MainPanel.register(context);
  registerPlanCommands(context);
- context.globalState.update('indexed', true);
}
```

---

### ✅ Result

* Indexing state reflects reality
* Plan Mode cannot be used prematurely
* Phase-3 invariant preserved

---

## 🧱 PATCH 3.FINAL.2 — Enforce “Indexed Before Plan” Rule

### ❌ Problem

User can generate a plan without indexing.

---

### ✅ Fix

**File:** `extension/src/features/plan/plan-controller.ts`

```diff
export async function createPlanFromChat(messages: any[]) {
  try {
+   const indexed = vscode.workspace
+     .getConfiguration('localpilot')
+     .get<boolean>('indexed');
+
+   if (!indexed) {
+     vscode.window.showWarningMessage(
+       'Project must be indexed before creating a plan.'
+     );
+     return;
+   }

    const projectId = vscode.workspace.name;
    if (!projectId) {
      vscode.window.showErrorMessage('No active workspace.');
      return;
    }

    const markdown = await generatePlan({ projectId, messages });
    await openPlanView(markdown);
  } catch (err: any) {
    vscode.window.showErrorMessage(
      `Failed to generate plan: ${err?.message ?? err}`
    );
  }
}
```

---

### ✅ Result

* Chat → Index → Plan order enforced
* Prevents hallucinated planning
* User feedback is explicit

---

## 🧱 PATCH 3.FINAL.3 — Make Edited Plan Markdown Retrievable

### ❌ Problem

User edits plan, but extension cannot read it back.

This blocks:

* validation
* approval
* Phase 4

---

### ✅ Fix (Phase-3 safe)

**File:** `extension/src/features/plan/plan-view-controller.ts`

#### 🔧 Add outbound message support

```diff
<script>
  const vscode = acquireVsCodeApi();

  window.addEventListener('message', (e) => {
    if (e.data?.type === 'plan:update') {
      document.getElementById('md').value = e.data.markdown || '';
    }
  });

+ function sendPlanContent() {
+   vscode.postMessage({
+     type: 'plan:content',
+     markdown: document.getElementById('md').value
+   });
+ }

+ window.addEventListener('beforeunload', sendPlanContent);
</script>
```

---

### ✅ Result

* Markdown remains authoritative
* Extension can later retrieve plan content
* No behavior change yet (safe for Phase 3)

---

## 🧱 PATCH 3.FINAL.4 — Clear Chat State on Project Lifecycle

### ❌ Problem

Chat messages can leak across:

* reindex
* workspace changes

---

### ✅ Fix (Recommended, Safe)

**Wherever indexing completes successfully** (IndexingService or command):

```ts
ChatSessionStore.clear();
```
also add:

* a “Clear Chat” command
* workspace change hook

---

## 🧪 POST-PATCH TEST CHECKLIST (REQUIRED)

Run these **before freezing Phase 3**:

### ✅ Test 1 — No indexing → no plan

* Open project
* Do not index
* Try “Create Plan from Chat”
* ❗ Warning shown

### ✅ Test 2 — Indexed → plan works

* Index project
* Chat
* Create plan
* Editable Markdown appears

### ✅ Test 3 — Edit plan

* Modify Markdown
* Close view
* Reopen (same session)
* Content preserved in memory

### ✅ Test 4 — Broken JSON

* Break embedded JSON
* Plan still opens
* `plan === null`
* No crash

---

## 🟢 Phase 3 Status After This Patch

When applied + tested:

✔ Plan Mode sealed
✔ Explicit intent only
✔ Markdown authoritative
✔ Validation & approval possible
✔ Zero execution paths

➡️ **Phase 3 can be tagged and frozen**

---

## 🔜 What’s next (after confirmation)

Once you say **“Phase 3 fixes applied and tested”**, I can:

* Design **Phase 4 Act Mode (safe execution)**
* Add **Plan Approval → Act Gate**
* Create **diff-based execution patches**
* Or do a **final security review**

If you want me to wire the `indexed` flag correctly and you’re unsure where it’s set,
upload the **indexing completion code** and I’ll handle it cleanly.

You’re in a very good place.

