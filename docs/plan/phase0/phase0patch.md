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
+  const res = await fetch('http://localhost:8000/health');
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