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