# LocalPilot — WebSocket Contract (Indexing & Progress)

This document specifies the WebSocket events and example payloads used by the LocalPilot backend to stream indexing progress and related indexing lifecycle events to the extension UI (side-panel).

## Overview
- Connection: UI opens a single persistent websocket to the backend for realtime events.
- Events follow `{ "event": "<name>", "data": { ... } }` JSON envelope.
- All timestamps are ISO-8601 UTC strings.

## Event list (server -> client)

### `indexing.start`
Sent when an indexing job begins.
**Payload**
```json
{
  "event": "indexing.start",
  "data": {
    "jobId": "uuid",
    "workspaceRoot": "/path/to/repo",
    "startedAt": "2025-11-15T02:00:00Z",
    "estimatedFiles": 123
  }
}
```

### `indexing.progress`
Progress update during indexing phases.
**payload**
```json
{
  "event": "indexing.progress",
  "data": {
    "jobId": "uuid",
    "phase": "embedding",
    "percent": 57,
    "currentFile": "src/app/main.py",
    "filesScanned": 234,
    "filesIndexed": 87,
    "indexedChunks": 342,
    "vectorCount": 342,
    "estimatedRemainingSeconds": 42,
    "message": "Embedding in progress",
    "timestamp": "2025-11-15T02:12:00Z"
  }
}
```

### `indexing.partial_ready`
Indicates a partial docs-only index is available (enable read-only docs mode).
**payload**
```json
{
  "event": "indexing.partial_ready",
  "data": {
    "jobId": "uuid",
    "scope": "docs", // e.g., "docs" or "readme_only"
    "availableAt": "2025-11-15T02:05:00Z",
    "message": "Docs-only partial index ready. Chat limited to README/docs."
  }
}
```

### `indexing.complete`
Indexing finished successfully.
**payload**
```json
{
  "event": "indexing.complete",
  "data": {
    "jobId": "uuid",
    "indexedFiles": 412,
    "indexedChunks": 3290,
    "vectorSize": 3290,
    "durationSeconds": 121,
    "summaryPath": ".localpilot/project_summary.md",
    "partialDocsReady": false,
    "timestamp": "2025-11-15T02:14:00Z"
  }
}
```

### `indexing.error`
Indexing failed or encountered an irrecoverable error.
**payload**
```json
{
  "event": "indexing.error",
  "data": {
    "jobId": "uuid",
    "errorCode": "EMBED_FAIL",
    "message": "Embedding process crashed",
    "details": {
      "phase": "embedding",
      "lastFile": "src/lib/hugefile.js"
    },
    "timestamp": "2025-11-15T02:09:45Z"
  }
}
```

### `indexing.cancelled`
Sent when user or system cancels the indexing job.
**payload**
```json
{
  "event": "indexing.cancelled",
  "data": {
    "jobId": "uuid",
    "cancelledBy": "user",
    "timestamp": "2025-11-15T02:10:00Z",
    "message": "User requested cancel"
  }
}
```


---

# 2) `shared/types/indexing.ts` (shared/types/indexing.ts)

```ts
// shared/types/indexing.ts
export type IndexingPhase =
  | 'discovery'
  | 'analysis'
  | 'chunking'
  | 'embedding'
  | 'summarization'
  | 'complete'
  | 'error';

export interface IndexingProgress {
  jobId: string; // uuid
  phase: IndexingPhase;
  percent: number; // 0-100
  currentFile?: string; // full path
  filesScanned?: number;
  filesIndexed?: number;
  indexedChunks?: number;
  vectorCount?: number;
  estimatedRemainingSeconds?: number;
  message?: string;
  timestamp: string; // ISO-8601 UTC
}

export interface IndexingResult {
  jobId: string;
  indexedFiles: number;
  indexedChunks: number;
  vectorSize: number;
  durationSeconds: number;
  summaryPath?: string;
  partialDocsReady?: boolean;
  timestamp: string;
}

export interface IndexingError {
  jobId: string;
  errorCode: string;
  message: string;
  details?: Record<string, any>;
  timestamp: string;
}

// Envelope used over websocket
export interface WSMessage<T = any> {
  event: string;
  data: T;
}
