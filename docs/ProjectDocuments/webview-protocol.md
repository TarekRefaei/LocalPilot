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
