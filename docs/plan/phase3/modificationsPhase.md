Perfect — your answers are **consistent, conservative, and Phase-3 correct**.
Below is the **exact migration patch proposal**, written so you can hand it directly to your AI coding agent or apply it yourself step-by-step.

This proposal:

* ✅ Keeps **Phase 3 guarantees intact**
* ✅ Separates Chat / Plan / Act at the **UI + capability level**
* ✅ Uses **native VS Code tabbed views**
* ✅ Avoids refactors that would destabilize your current working code

---

# 🧩 MIGRATION PATCH PROPOSAL

## From Single Sidebar → Tabbed Chat / Plan / Act Views (Phase 3–Safe)

---

## 🎯 Migration Goals (Locked)

1. Separate **Chat**, **Plan**, and **Act** into distinct VS Code views
2. Preserve existing Chat behavior (read-only understanding)
3. Move Plan functionality into a dedicated Plan view
4. Introduce Act view as **visible but disabled**
5. Prevent capability leakage between views
6. Maintain current backend contracts unchanged

---

## 🔒 Phase 3 Invariants (Reconfirmed)

* ❌ Chat cannot create plans
* ❌ Plan cannot execute
* ❌ Act cannot run without approval (Phase 4)
* ✅ All transitions are user-triggered
* ✅ Markdown remains authoritative for plans

---

# 1️⃣ `package.json` — View Contributions (CRITICAL)

### 🔧 Replace existing `views` contribution

**File:** `extension/package.json`

```diff
"contributes": {
  "viewsContainers": {
    "activitybar": [
      {
        "id": "localpilot",
        "title": "LocalPilot",
        "icon": "./media/icon-localpilot.svg"
      }
    ]
  },
- "views": {
-   "localpilot": [
-     {
-       "id": "localpilot.sidebar",
-       "name": "LocalPilot",
-       "type": "webview"
-     }
-   ]
- },
+ "views": {
+   "localpilot": [
+     {
+       "id": "localpilot.chat",
+       "name": "Chat",
+       "type": "webview"
+     },
+     {
+       "id": "localpilot.plan",
+       "name": "Plan",
+       "type": "webview"
+     },
+     {
+       "id": "localpilot.act",
+       "name": "Act",
+       "type": "webview"
+     }
+   ]
+ },
```

### ✅ Result

* Native VS Code tabs
* No custom tab logic
* Built-in switching & persistence

---

## 2️⃣ Command Visibility Rules (STRICT)

### 🔧 Update `menus.view/title`

```diff
"menus": {
  "view/title": [
    {
      "command": "localpilot.plan.createFromChat",
-     "when": "view == localpilot.sidebar",
+     "when": "view == localpilot.plan",
      "group": "navigation"
    },
    {
      "command": "localpilot.chat.clear",
-     "when": "view == localpilot.sidebar",
+     "when": "view == localpilot.chat",
      "group": "navigation@2"
    }
  ]
}
```

### ✅ Result

* Chat commands appear only in Chat
* Plan commands appear only in Plan
* No accidental misuse

---

## 3️⃣ Chat View Registration (EXTRACT CURRENT SIDEBAR)

### 🧱 New file

**File:** `extension/src/views/chat/chat-view.ts`

```ts
import * as vscode from 'vscode';
import { initChat } from '../../webview/chat-controller';

export class ChatViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.chat';

  resolveWebviewView(view: vscode.WebviewView) {
    view.webview.options = { enableScripts: true };
    view.webview.html = getHtml();
    initChat(view, 'default');
  }
}

function getHtml(): string {
  // MOVE existing HTML from main-panel.ts here unchanged
  return /* existing chat HTML */;
}
```

---

## 4️⃣ Plan View Registration (BUTTON-ONLY MODE)

### 🧱 New file

**File:** `extension/src/views/plan/plan-view.ts`

```ts
import * as vscode from 'vscode';
import { openPlanView } from '../../features/plan/plan-view-controller';

export class PlanViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.plan';

  resolveWebviewView(view: vscode.WebviewView) {
    view.webview.options = { enableScripts: true };
    view.webview.html = render();
  }
}

function render(): string {
  return `
    <html>
      <body>
        <h3>Plan Mode</h3>
        <p>Create, edit, and approve implementation plans.</p>
        <p><em>Use the toolbar to create a plan from chat.</em></p>
      </body>
    </html>
  `;
}
```

### 🧠 Design rationale

* Plan creation is **command-driven**
* No chat input here (per Q1)
* Markdown editor opens in separate panel (already implemented)

---

## 5️⃣ Act View (DISABLED PLACEHOLDER)

### 🧱 New file

**File:** `extension/src/views/act/act-view.ts`

```ts
import * as vscode from 'vscode';

export class ActViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.act';

  resolveWebviewView(view: vscode.WebviewView) {
    view.webview.html = `
      <html>
        <body>
          <h3>Act Mode</h3>
          <p>Act Mode will be available once a plan is approved.</p>
        </body>
      </html>
    `;
  }
}
```

---

## 6️⃣ Extension Activation Wiring

### 🔧 Update `extension/src/extension.ts`

```diff
import { ChatViewProvider } from './views/chat/chat-view';
import { PlanViewProvider } from './views/plan/plan-view';
import { ActViewProvider } from './views/act/act-view';

export function activate(context: vscode.ExtensionContext) {
  MainPanel.unregister?.(); // optional if you remove it

+ context.subscriptions.push(
+   vscode.window.registerWebviewViewProvider(
+     ChatViewProvider.viewId,
+     new ChatViewProvider()
+   ),
+   vscode.window.registerWebviewViewProvider(
+     PlanViewProvider.viewId,
+     new PlanViewProvider()
+   ),
+   vscode.window.registerWebviewViewProvider(
+     ActViewProvider.viewId,
+     new ActViewProvider()
+   )
+ );

  registerPlanCommands(context);
}
```

---

## 7️⃣ Chat → Plan Navigation Hint (Q4)

### 🔧 Modify Chat refusal behavior

When Chat detects planning intent:

```ts
panel.webview.postMessage({
  type: 'hint',
  message: 'Planning is available in the Plan tab.',
  action: {
    label: 'Open Plan Tab',
    command: 'workbench.view.extension.localpilot'
  }
});
```

### UX Result

* No auto-switch
* User remains in control
* Discoverable, not intrusive

---

# 🧠 Shared vs Isolated State (Final Contract)

### 🔗 Shared (read-only)

* Project summary
* Symbols
* Index status
* Chat history (snapshot only)

### 🔒 Isolated

* Chat messages (Chat view)
* Plan markdown + approval (Plan view)
* Execution state (Act view, later)

---

# 🧪 Migration Test Checklist

Before freezing Phase 3:

* [ ] Chat tab works exactly as before
* [ ] Plan tab visible, no chat input
* [ ] Create Plan works only from Plan tab
* [ ] Act tab visible but inert
* [ ] Chat suggests switching to Plan
* [ ] No execution paths exist

---

# 🟢 Final State

After this patch:

✔ UI reflects system modes
✔ User confusion eliminated
✔ Phase 4 enabled without refactor
✔ Architecture & docs aligned

---

If you want next, I can:

* Update **architecture.md / state-model.md / security-model.md** with exact text
* Generate **Phase 4 Act Mode design**
* Or create a **diff-ready patch set** split per commit

Just tell me the next step.
