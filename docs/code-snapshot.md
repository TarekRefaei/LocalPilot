## Project Structure

```
. (97 files)
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── issue_template.md
│   ├── workflows/
│   │   └── windows-ci.yml
│   └── pull_request_template.md
├── docs/
│   ├── .notes/
│   │   ├── notes.md
│   │   └── patch.md
│   ├── decisions/
│   │   ├── ADR-001-monorepo-structure.md
│   │   ├── ADR-002-llamaindex-over-langchain.md
│   │   └── ADR-003-chromadb-for-vectors.md
│   ├── plan/
│   │   ├── phase0/
│   │   │   ├── phase0.md
│   │   │   ├── phase0patch.md
│   │   │   └── task0-phase.md
│   │   ├── phase1/
│   │   │   └── phase1patch.md
│   │   ├── phase2/
│   │   │   └── phase2patch.md
│   │   ├── master-execution-roadmap.md
│   │   └── Phase-by-Phase-TODO-List.md
│   ├── ProjectDocuments/
│   │   ├── architecture.md
│   │   ├── commit-convention.md
│   │   ├── development-setup.md
│   │   ├── indexing-spec.md
│   │   ├── overview.md
│   │   ├── prompt-engineer.md
│   │   ├── release-policy.md
│   │   ├── security-model.md
│   │   ├── state-model.md
│   │   ├── structure.md
│   │   ├── testing-strategy.md
│   │   ├── troubleshooting.md
│   │   └── webview-protocol.md
│   └── code-snapshot.md
├── extension/
│   ├── src/
│   │   ├── core/
│   │   │   ├── entities/
│   │   │   │   ├── index.ts
│   │   │   │   ├── message.entity.ts
│   │   │   │   ├── plan.entity.ts
│   │   │   │   ├── project.entity.ts
│   │   │   │   └── task.entity.ts
│   │   │   ├── errors/
│   │   │   │   ├── base.error.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── ollama.error.ts
│   │   │   └── interfaces/
│   │   │       ├── file-system.interface.ts
│   │   │       ├── index.ts
│   │   │       ├── llm-provider.interface.ts
│   │   │       └── rag-provider.interface.ts
│   │   ├── features/
│   │   │   ├── chat/
│   │   │   │   ├── chat-service.ts
│   │   │   │   ├── prompt-builder.ts
│   │   │   │   └── rag-client.ts
│   │   │   └── ollama/
│   │   │       └── connection-manager.ts
│   │   ├── infrastructure/
│   │   │   └── http/
│   │   │       └── api-client.ts
│   │   ├── panels/
│   │   │   └── main-panel.ts
│   │   ├── webview/
│   │   │   ├── chat-controller.ts
│   │   │   └── chat-view.ts
│   │   └── extension.ts
│   ├── test/
│   │   └── activation.test.ts
│   ├── package-lock.json
│   ├── package.json
│   └── tsconfig.json
├── scripts/
│   └── dev.ps1
├── server/
│   ├── .pytest_cache/
│   │   └── README.md
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat_ws.py
│   │   │   ├── index.py
│   │   │   ├── project.py
│   │   │   └── query.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── query.py
│   │   ├── __init__.py
│   │   └── dependencies.py
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   ├── ollama_chat_client.py
│   │   └── prompt_builder.py
│   ├── indexing/
│   │   ├── embeddings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── ollama.py
│   │   ├── parsers/
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   ├── __init__.py
│   │   ├── chunk.py
│   │   ├── chunker.py
│   │   ├── hash_tracker.py
│   │   ├── language.py
│   │   ├── progress.py
│   │   ├── query_service.py
│   │   ├── README.md
│   │   ├── scanner.py
│   │   ├── service.py
│   │   ├── state.py
│   │   ├── summary_service.py
│   │   ├── symbol_index.py
│   │   └── vector_store.py
│   ├── tests/
│   │   └── test_health.py
│   ├── __init__.py
│   ├── main.py
│   └── requirements.txt
├── test_project/
│   ├── app.py
│   └── utils.py
├── tools/
│   └── export-to-md.mjs
├── CONTRIBUTING.md
└── README.md

```

---

## extension/package.json

*Size: 1,084 bytes | Modified: 2025-12-20T00:00:18.132Z*

<details>
<summary>View code</summary>

```json
{
  "name": "localpilot",
  "displayName": "LocalPilot",
  "description": "Privacy-first AI coding agent using local LLMs",
  "version": "0.1.0",
  "publisher": "localpilot",
  "engines": {
    "vscode": "^1.85.0"
  },
  "main": "./dist/extension.js",
  "activationEvents": [
    "onView:localpilot.sidebar"
  ],
  "scripts": {
    "build": "esbuild src/extension.ts --bundle --outfile=dist/extension.js --platform=node --external:vscode --format=cjs",
    "test": "vitest run"
  },
  "dependencies": {
    "ws": "^8.16.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/vscode": "^1.85.0",
    "@types/ws": "^8.5.12",
    "esbuild": "^0.27.1",
    "vitest": "^4.0.15"
  },
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
    "views": {
      "localpilot": [
        {
          "id": "localpilot.sidebar",
          "name": "LocalPilot",
          "type": "webview"
        }
      ]
    }
  }
}

```

</details>


## extension/src/core/entities/index.ts

*Size: 130 bytes | Modified: 2025-12-13T19:55:55.762Z*

<details>
<summary>View code</summary>

```typescript
export * from './message.entity';
export * from './plan.entity';
export * from './task.entity';
export * from './project.entity';

```

</details>


## extension/src/core/entities/message.entity.ts

*Size: 1,341 bytes | Modified: 2025-12-13T19:55:19.325Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Represents a single chat message.
 */
export interface Message {
  /** Unique message ID */
  id: string;
  /** Who sent the message */
  role: 'user' | 'assistant' | 'system';
  /** Message content (may include markdown) */
  content: string;
  /** When the message was created */
  timestamp: Date;
  /** If this message used RAG context */
  ragContext?: RAGContext;
  /** Status for assistant messages (streaming) */
  status?: 'streaming' | 'complete' | 'error';
  /** Error details if status is 'error' */
  error?: string;
}

export interface RAGContext {
  /** Chunks used to generate response */
  chunks: RetrievedChunk[];
  /** Query that was sent to RAG */
  query: string;
}

export interface RetrievedChunk {
  /** Chunk ID in vector store */
  id: string;
  /** Code content */
  content: string;
  /** File path relative to workspace */
  filePath: string;
  /** Starting line number */
  lineStart: number;
  /** Ending line number */
  lineEnd: number;
  /** Type of code unit */
  chunkType: ChunkType;
  /** Symbol name (function/class name) */
  symbolName?: string;
  /** Programming language */
  language: string;
  /** Similarity score (0-1) */
  score: number;
}

export type ChunkType =
  | 'function'
  | 'class'
  | 'method'
  | 'interface'
  | 'type'
  | 'variable'
  | 'import'
  | 'module'
  | 'file';

```

</details>


## extension/src/core/entities/plan.entity.ts

*Size: 662 bytes | Modified: 2025-12-13T19:56:33.211Z*

<details>
<summary>View code</summary>

```typescript
import type { Task } from './task.entity';
/**
 * Represents an implementation plan
 */
export interface Plan {
  /** Unique plan ID */
  id: string;
  /** Plan title */
  title: string;
  /** Brief description/overview */
  overview: string;
  /** List of tasks to execute */
  tasks: Task[];
  /** When the plan was created */
  createdAt: Date;
  /** When the plan was last modified */
  updatedAt: Date;
  /** Current plan status */
  status: PlanStatus;
  /** Original conversation that led to this plan */
  sourceConversationId?: string;
}

export type PlanStatus =
  | 'draft'
  | 'approved'
  | 'executing'
  | 'paused'
  | 'completed'
  | 'cancelled';

```

</details>


## extension/src/core/entities/project.entity.ts

*Size: 755 bytes | Modified: 2025-12-13T19:55:55.126Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Represents an indexed project/workspace
 */
export interface Project {
  /** Unique identifier (hash of workspace path) */
  id: string;
  /** Display name (folder name) */
  name: string;
  /** Absolute path to workspace */
  workspacePath: string;
  /** Index status */
  indexStatus: IndexStatus;
  /** When indexing was last completed */
  lastIndexedAt: Date | null;
  /** Statistics about indexed content */
  stats: ProjectStats;
  /** Languages detected in project */
  languages: string[];
}

export type IndexStatus =
  | 'not-indexed'
  | 'indexing'
  | 'indexed'
  | 'sync-required'
  | 'error';

export interface ProjectStats {
  filesCount: number;
  chunksCount: number;
  totalLines: number;
  byLanguage: Record<string, number>;
}

```

</details>


## extension/src/core/entities/task.entity.ts

*Size: 984 bytes | Modified: 2025-12-13T19:55:54.016Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Represents a single task in a plan
 */
export interface Task {
  /** Unique task ID */
  id: string;
  /** Order in the plan (0-based) */
  orderIndex: number;
  /** Short task title */
  title: string;
  /** Detailed description */
  description: string;
  /** File to create/modify/delete */
  filePath: string;
  /** What action to take */
  actionType: TaskActionType;
  /** Additional details/requirements */
  details: string[];
  /** IDs of tasks this depends on */
  dependencies: string[];
  /** Current task status */
  status: TaskStatus;
  /** Generated code (after code generation) */
  generatedCode?: string;
  /** Diff for modify actions */
  diff?: string;
  /** Error message if failed */
  error?: string;
  /** Execution timestamps */
  startedAt?: Date;
  completedAt?: Date;
}

export type TaskActionType = 'create' | 'modify' | 'delete';

export type TaskStatus =
  | 'pending'
  | 'running'
  | 'awaiting-approval'
  | 'done'
  | 'skipped'
  | 'error';

```

</details>


## extension/src/core/errors/base.error.ts

*Size: 897 bytes | Modified: 2025-12-14T01:23:45.565Z*

<details>
<summary>View code</summary>

```typescript
export type ErrorCategory =
  | 'connection'
  | 'indexing'
  | 'llm'
  | 'file'
  | 'validation';

/**
 * Base error class for all LocalPilot errors.
 * Enforces structured, serializable errors.
 */
export abstract class LocalPilotError extends Error {
  abstract readonly code: string;
  abstract readonly category: ErrorCategory;
  abstract readonly recoverable: boolean;

  constructor(
    message: string,
    public readonly details?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;

    // Preserve stack trace
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }

  toJSON(): Record<string, unknown> {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      category: this.category,
      recoverable: this.recoverable,
      details: this.details,
    };
  }
}

```

</details>


## extension/src/core/errors/index.ts

*Size: 62 bytes | Modified: 2025-12-14T01:24:26.720Z*

<details>
<summary>View code</summary>

```typescript
export * from './base.error';
export * from './ollama.error';

```

</details>


## extension/src/core/errors/ollama.error.ts

*Size: 1,160 bytes | Modified: 2025-12-14T01:24:06.218Z*

<details>
<summary>View code</summary>

```typescript
import { LocalPilotError } from './base.error';

/**
 * Thrown when Ollama cannot be reached.
 */
export class OllamaConnectionError extends LocalPilotError {
  readonly code = 'OLLAMA_CONNECTION_FAILED';
  readonly category = 'connection' as const;
  readonly recoverable = true;

  constructor(url: string, cause?: Error) {
    super(
      `Cannot connect to Ollama at ${url}. Make sure Ollama is running.`,
      { url, cause: cause?.message }
    );
  }
}

/**
 * Thrown when a requested model is missing.
 */
export class OllamaModelNotFoundError extends LocalPilotError {
  readonly code = 'OLLAMA_MODEL_NOT_FOUND';
  readonly category = 'llm' as const;
  readonly recoverable = true;

  constructor(model: string) {
    super(
      `Model "${model}" not found. Run "ollama pull ${model}" to install it.`,
      { model }
    );
  }
}

/**
 * Thrown when generation fails unexpectedly.
 */
export class OllamaGenerationError extends LocalPilotError {
  readonly code = 'OLLAMA_GENERATION_FAILED';
  readonly category = 'llm' as const;
  readonly recoverable = true;

  constructor(message: string, model: string) {
    super(message, { model });
  }
}

```

</details>


## extension/src/core/interfaces/file-system.interface.ts

*Size: 1,062 bytes | Modified: 2025-12-13T19:57:29.901Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Interface for file system operations
 */
export interface IFileSystem {
  /** Read file content */
  readFile(filePath: string): Promise<string>;
  /** Write content to file (creates if not exists) */
  writeFile(filePath: string, content: string): Promise<void>;
  /** Delete a file */
  deleteFile(filePath: string): Promise<void>;
  /** Check if file exists */
  exists(filePath: string): Promise<boolean>;
  /** Create directory (recursive) */
  createDirectory(dirPath: string): Promise<void>;
  /** List files in directory */
  listFiles(dirPath: string, recursive?: boolean): Promise<string[]>;
  /** Get file stats */
  stat(filePath: string): Promise<FileStat>;
  /** Create backup of a file */
  backup(filePath: string): Promise<string>;
  /** Restore file from backup */
  restore(backupPath: string, targetPath: string): Promise<void>;
  /** Get workspace root path */
  getWorkspaceRoot(): string | undefined;
}

export interface FileStat {
  isFile: boolean;
  isDirectory: boolean;
  size: number;
  modifiedAt: Date;
  createdAt: Date;
}

```

</details>


## extension/src/core/interfaces/index.ts

*Size: 125 bytes | Modified: 2025-12-13T19:57:30.519Z*

<details>
<summary>View code</summary>

```typescript
export * from './llm-provider.interface';
export * from './rag-provider.interface';
export * from './file-system.interface';

```

</details>


## extension/src/core/interfaces/llm-provider.interface.ts

*Size: 1,094 bytes | Modified: 2025-12-13T19:57:24.071Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Interface for LLM provider operations
 */
export interface ILLMProvider {
  /** Check if the LLM provider is available */
  isAvailable(): Promise<boolean>;
  /** Get list of available models */
  listModels(): Promise<ModelInfo[]>;
  /** Generate chat completion (non-streaming) */
  chat(request: ChatRequest): Promise<ChatResponse>;
  /** Generate chat completion with streaming */
  chatStream(request: ChatRequest): AsyncGenerator<string, void, unknown>;
  /** Generate embeddings for text */
  embed(text: string, model?: string): Promise<number[]>;
}

export interface ModelInfo {
  name: string;
  size: number;
  modifiedAt: Date;
  family: string;
  parameterSize: string;
  quantizationLevel: string;
}

export interface ChatRequest {
  model: string;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  options?: {
    temperature?: number;
    topP?: number;
    maxTokens?: number;
  };
}

export interface ChatResponse {
  content: string;
  model: string;
  totalDuration: number;
  promptEvalCount: number;
  evalCount: number;
}

```

</details>


## extension/src/core/interfaces/rag-provider.interface.ts

*Size: 1,947 bytes | Modified: 2025-12-13T19:57:27.428Z*

<details>
<summary>View code</summary>

```typescript
import type { RetrievedChunk, ChunkType, ProjectStats } from '../entities';

/**
 * Interface for RAG operations
 */
export interface IRAGProvider {
  /** Start indexing a workspace */
  startIndexing(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: IndexProgress) => void
  ): Promise<IndexResult>;
  /** Sync index (re-index only changed files) */
  syncIndex(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: SyncProgress) => void
  ): Promise<SyncResult>;
  /** Query for relevant code chunks */
  query(
    projectId: string,
    queryText: string,
    topK?: number,
    filters?: QueryFilters
  ): Promise<RetrievedChunk[]>;
  /** Get project summary after indexing */
  getProjectSummary(projectId: string): Promise<ProjectSummary>;
  /** Check if project is indexed */
  isIndexed(projectId: string): Promise<boolean>;
  /** Clear project index */
  clearIndex(projectId: string): Promise<void>;
}

export interface IndexProgress {
  phase: 'scanning' | 'parsing' | 'embedding' | 'storing';
  current: number;
  total: number;
  currentFile?: string;
  message?: string;
}

export interface IndexResult {
  success: boolean;
  filesIndexed: number;
  chunksCreated: number;
  durationSeconds: number;
  languages: string[];
  error?: string;
}

export interface SyncProgress {
  phase: 'scanning' | 'comparing' | 'updating';
  changedFiles: number;
  deletedFiles: number;
  processed: number;
  total: number;
}

export interface SyncResult {
  success: boolean;
  filesUpdated: number;
  filesDeleted: number;
  chunksUpdated: number;
  durationSeconds: number;
}

export interface QueryFilters {
  fileTypes?: string[];
  chunkTypes?: ChunkType[];
  filePaths?: string[];
}

export interface ProjectSummary {
  projectName: string;
  description: string;
  mainLanguages: string[];
  keyFiles: string[];
  architecture: string;
  frameworks: string[];
  stats: ProjectStats;
}

```

</details>


## extension/src/extension.ts

*Size: 297 bytes | Modified: 2025-12-20T00:00:18.133Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { MainPanel } from './panels/main-panel';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  MainPanel.register(context);
  context.globalState.update('indexed', true);
}

export function deactivate() {}

```

</details>


## extension/src/features/chat/chat-service.ts

*Size: 959 bytes | Modified: 2025-12-20T23:56:57.475Z*

<details>
<summary>View code</summary>

```typescript
import { queryRAG } from "./rag-client";
import { PromptBuilder } from "./prompt-builder";
import { getProjectSummary } from "../../infrastructure/http/api-client";

export class ChatService {
  async sendMessage(
    userMessage: string,
    onEvent: (event: any) => void,
    projectId: string
  ): Promise<void> {

    const chunks = await queryRAG(projectId, userMessage);
    const summary = await getProjectSummary(projectId);
    const messages = new PromptBuilder().build(userMessage, chunks, summary);

    const WS = require("ws");
    const ws = new WS("ws://localhost:8000/ws/chat");

    ws.on("open", () => {
      ws.send(JSON.stringify({
        model: "qwen2.5-coder:7b-instruct-q4_K_M",
        messages
      }));
    });

    ws.on("message", (raw: any) => {
      const msg = JSON.parse(raw.toString());
      onEvent(msg);
    });

    ws.on("error", (err: any) => {
      onEvent({ type: "error", message: String(err) });
    });
  }
}

```

</details>


## extension/src/features/chat/prompt-builder.ts

*Size: 1,527 bytes | Modified: 2025-12-20T23:56:57.475Z*

<details>
<summary>View code</summary>

```typescript
export class PromptBuilder {
  private static SYSTEM_PROMPT = (
    "You are a helpful AI assistant answering questions about a codebase.\n" +
    "You must base your answers ONLY on the provided context.\n" +
    "If the answer is not in the context, say \"I don't know\".\n" +
    "Do NOT suggest code changes or plans."
  );

  build(userMessage: string, chunks: any[], projectSummary?: any): Array<{ role: string; content: string }> {
    const messages: Array<{ role: string; content: string }> = [
      { role: "system", content: PromptBuilder.SYSTEM_PROMPT }
    ];

    if (projectSummary) {
      const summaryText = typeof projectSummary === "string" 
        ? projectSummary 
        : JSON.stringify(projectSummary, null, 2);
      messages.push({
        role: "system",
        content: "PROJECT SUMMARY (facts only):\n\n" + summaryText
      });
    }

    if (chunks && chunks.length > 0) {
      const blocks = chunks.map((c: any) => {
        const m = c.metadata || {};
        const lang = m.language || "";
        const file = m.file_path || "";
        const start = m.start_line ?? "";
        const end = m.end_line ?? "";
        const content = c.content ?? "";
        return `File: ${file} (lines ${start}–${end})\n\u0060\u0060\u0060${lang}\n${content}\n\u0060\u0060\u0060`;
      });

      messages.push({
        role: "system",
        content: "CODE CONTEXT:\n\n" + blocks.join("\n\n")
      });
    }

    messages.push({ role: "user", content: userMessage });
    return messages;
  }
}

```

</details>


## extension/src/features/chat/rag-client.ts

*Size: 836 bytes | Modified: 2025-12-20T00:00:18.135Z*

<details>
<summary>View code</summary>

```typescript
export type RetrievedChunk = {
  id: string;
  content: string;
  metadata: Record<string, any>;
  distance: number;
};

export async function queryRAG(
  projectId: string,
  text: string,
  topK: number = 5,
  filters?: Record<string, any>
): Promise<RetrievedChunk[]> {
  const res = await fetch("http://localhost:8000/api/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      project_id: projectId,
      query: text,
      top_k: topK,
      filters: filters ?? null
    })
  });

  if (!res.ok) {
    let detail = "";
    try {
      detail = await res.text();
    } catch {}
    throw new Error(`RAG query failed: ${res.status} ${detail}`);
  }

  const json = await res.json();
  return (json && Array.isArray(json.chunks)) ? json.chunks as RetrievedChunk[] : [];
}

```

</details>


## extension/src/features/ollama/connection-manager.ts

*Size: 487 bytes | Modified: 2025-12-14T01:25:14.715Z*

<details>
<summary>View code</summary>

```typescript
import { OllamaConnectionError } from '../../core/errors';

const DEFAULT_OLLAMA_URL = 'http://localhost:11434';

/**
 * Checks whether Ollama is reachable.
 * Phase 0: connectivity only (no model logic).
 */
export async function checkOllamaAvailability(
  baseUrl: string = DEFAULT_OLLAMA_URL
): Promise<boolean> {
  try {
    const res = await fetch(`${baseUrl}/api/version`);
    return res.ok;
  } catch (error) {
    throw new OllamaConnectionError(baseUrl, error as Error);
  }
}

```

</details>


## extension/src/infrastructure/http/api-client.ts

*Size: 989 bytes | Modified: 2025-12-20T23:56:57.476Z*

<details>
<summary>View code</summary>

```typescript
export async function checkServerHealth(): Promise<boolean> {
  const res = await fetch('http://localhost:8000/health');
  return res.ok;
}

export async function checkOllamaHealth(): Promise<boolean> {
  try {
    const res = await fetch('http://localhost:8000/health/ollama');
    const json = await res.json();
    return json.status === 'ok';
  } catch {
    return false;
  }
}

export async function getProjectSummary(projectId: string): Promise<any> {
  const res = await fetch(`http://localhost:8000/api/project/${encodeURIComponent(projectId)}/summary`);
  if (res.status === 404) {
    throw new Error('summary_not_found');
  }
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`summary_fetch_failed: ${res.status} ${text}`);
  }
  return await res.json();
}

export async function isIndexed(projectId: string): Promise<boolean> {
  try {
    await getProjectSummary(projectId);
    return true;
  } catch (e: any) {
    return false;
  }
}

```

</details>


## extension/src/panels/main-panel.ts

*Size: 3,943 bytes | Modified: 2025-12-20T23:56:57.477Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from "vscode";
import { initChat } from "../webview/chat-controller";

export class MainPanel {
  static register(context: vscode.ExtensionContext) {
    context.subscriptions.push(
      vscode.window.registerWebviewViewProvider(
        "localpilot.sidebar",
        {
          resolveWebviewView(view) {
            view.webview.options = {
              enableScripts: true
            };

            view.webview.html = getHtml();
            initChat(view, "default");
          }
        }
      )
    );
  }
}

function getHtml(): string {
  return `
<!DOCTYPE html>
<html>
<head>
<style>
body { background:#1e1e1e; color:#d4d4d4; font-family:sans-serif; padding:10px; }
.hidden { display:none; }
progress { width:100%; }
#out { height:240px; overflow:auto; border:1px solid #333; padding:8px; }
#in { width:100%; margin-top:8px; }
#status { margin-bottom:8px; font-size:12px; }
.status-ok { color:#6ee7b7; }
.status-error { color:#f87171; }
</style>
</head>

<body>

<div id="onboarding">
  <h3>Welcome to LocalPilot</h3>
  <div id="status">Checking system status…</div>
  <button id="indexBtn">Index Current Workspace</button>
  <progress id="progress" max="100" value="0" class="hidden"></progress>
</div>

<div id="chat" class="hidden">
  <div id="out"></div>
  <input id="in" placeholder="Ask about your project..." />
</div>

<script>
const vscode = acquireVsCodeApi();

const onboarding = document.getElementById("onboarding");
const chat = document.getElementById("chat");
const out = document.getElementById("out");
const input = document.getElementById("in");
const progress = document.getElementById("progress");
const indexBtn = document.getElementById("indexBtn");

let state = "onboarding";

function render() {
  onboarding.classList.toggle("hidden", state !== "onboarding");
  chat.classList.toggle("hidden", state !== "chat");
}

render();

// ------------------------
// INDEXING (SSE)
// ------------------------
indexBtn.onclick = () => {
  progress.classList.remove("hidden");
  progress.value = 0;

  const es = new EventSource("http://localhost:8000/api/index/default");

  es.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);

    if (msg.type === "index:progress") {
      const pct = Math.round((msg.current / msg.total) * 100);
      progress.value = pct;
    }

    if (msg.type === "index:done") {
      progress.value = 100;
      es.close();
      state = "chat";
      render();
    }

    if (msg.type === "error") {
      es.close();
      alert(msg.message || "Indexing failed");
    }
  };

  es.onerror = () => {
    es.close();
    alert("Indexing connection failed");
  };
};

// ------------------------
// CHAT INPUT
// ------------------------
input.addEventListener("keydown", (e) => {
  if (e.key !== "Enter") return;

  const message = input.value.trim();
  if (!message) return;

  input.value = "";
  out.innerHTML += "<div><b>You:</b> " + message + "</div>";

  vscode.postMessage({
    type: "chat:send",
    payload: { message }
  });
});

// ------------------------
// EXTENSION EVENTS
// ------------------------
window.addEventListener("message", (e) => {
  const msg = e.data;

  if (msg.type === "token") {
    out.innerHTML += msg.value;
  }

  if (msg.type === "done") {
    input.disabled = false;
    input.focus();
  }

  if (msg.type === "ui:lock") {
    input.disabled = true;
  }

  if (msg.type === "error") {
    out.innerHTML += "<div class='error'>[error]</div>";
    input.disabled = false;
  }

  if (msg.type === "status:update") {
    const el = document.getElementById("status");
    if (!msg.backendOk) {
      el.textContent = "Backend not running";
      el.className = "status-error";
    } else if (!msg.ollamaOk) {
      el.textContent = "Ollama not available";
      el.className = "status-error";
    } else {
      el.textContent = "Ready";
      el.className = "status-ok";
    }
  }
});
</script>

</body>
</html>
`;
}

```

</details>


## extension/src/webview/chat-controller.ts

*Size: 1,468 bytes | Modified: 2025-12-20T23:56:57.478Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from "vscode";
import { ChatService } from "../features/chat/chat-service";
import {
  checkServerHealth,
  checkOllamaHealth,
  isIndexed,
  getProjectSummary
} from "../infrastructure/http/api-client";

export function initChat(panel: vscode.WebviewView, projectId: string) {
  const chat = new ChatService();

  // Initial status check
  (async () => {
    const backendOk = await checkServerHealth();
    const ollamaOk = await checkOllamaHealth();

    panel.webview.postMessage({
      type: "status:update",
      backendOk,
      ollamaOk
    });
  })();

  panel.webview.onDidReceiveMessage(async (msg: any) => {
    if (!msg) return;

    // ------------------------
    // CHAT ONLY
    // ------------------------
    if (msg.type === "chat:send") {
      const indexed = await isIndexed(projectId);
      if (!indexed) {
        panel.webview.postMessage({
          type: "error",
          message: "Project not indexed. Please index the workspace first."
        });
        return;
      }

      try {
        await getProjectSummary(projectId);
      } catch {
        panel.webview.postMessage({
          type: "error",
          message: "Project summary missing. Please re-index."
        });
        return;
      }

      panel.webview.postMessage({ type: "ui:lock" });

      await chat.sendMessage(
        msg.payload.message,
        (event) => panel.webview.postMessage(event),
        projectId
      );
    }
  });
}

```

</details>


## extension/src/webview/chat-view.ts

*Size: 3,504 bytes | Modified: 2025-12-20T23:56:57.478Z*

<details>
<summary>View code</summary>

```typescript
// ------------------------------------------------------------
// VS Code Webview API declaration (TypeScript-only)
// ------------------------------------------------------------
declare function acquireVsCodeApi(): {
  postMessage(message: any): void;
};

// Acquire VS Code API
const vscode = acquireVsCodeApi();

export function renderChat(container: HTMLElement) {
  // ============================
  // Index button
  // ============================
  const indexBtn = document.createElement("button");
  indexBtn.textContent = "Index Current Workspace";
  indexBtn.style.width = "100%";
  indexBtn.style.marginBottom = "6px";

  container.appendChild(indexBtn);

  indexBtn.onclick = () => {
    vscode.postMessage({ type: "index:start" });
  };

  // ============================
  // Progress bar
  // ============================
  const progress = document.createElement("progress");
  progress.max = 100;
  progress.value = 0;
  progress.style.width = "100%";
  progress.style.display = "none";

  container.appendChild(progress);

  // ============================
  // Output
  // ============================
  const output = document.createElement("div");
  output.style.marginTop = "8px";
  output.style.fontFamily = "monospace";
  container.appendChild(output);

  // ============================
  // Input
  // ============================
  const input = document.createElement("input");
  input.placeholder = "Ask about your project...";
  input.style.width = "100%";
  input.style.marginTop = "8px";
  container.appendChild(input);

  input.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;

    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    output.innerHTML += `<div><b>You:</b> ${message}</div>`;

    vscode.postMessage({
      type: "chat:send",
      payload: { message },
    });
  });

  // ============================
  // Incoming messages
  // ============================
  window.addEventListener("message", (event) => {
    const msg = event.data;
    if (!msg || !msg.type) return;

    // ----------------------------
    // Indexing begins
    // ----------------------------
    if (msg.type === "index:begin") {
      progress.value = 0;
      progress.style.display = "block";

      const es = new EventSource(
        `http://localhost:8000/api/index/${encodeURIComponent(
          msg.projectId
        )}`
      );

      es.onmessage = (ev) => {
        const data = JSON.parse(ev.data);

        if (data.type === "index:progress") {
          progress.value =
            data.total > 0
              ? Math.round((data.current / data.total) * 100)
              : 0;
        }

        if (data.type === "index:done") {
          progress.value = 100;
          es.close();
        }

        if (data.type === "error") {
          output.innerHTML += `<div style="color:red">${data.message}</div>`;
          es.close();
        }
      };

      es.onerror = () => {
        output.innerHTML += `<div style="color:red">Indexing failed</div>`;
        es.close();
      };
    }

    // ----------------------------
    // Chat stream
    // ----------------------------
    if (msg.type === "chat:chunk") {
      output.innerHTML += `<div>${msg.content}</div>`;
    }

    if (msg.type === "chat:done") {
      output.innerHTML += `<div><i>Done.</i></div>`;
    }

    if (msg.type === "error") {
      output.innerHTML += `<div style="color:red">${msg.message}</div>`;
    }
  });
}

```

</details>


## extension/test/activation.test.ts

*Size: 570 bytes | Modified: 2025-12-13T20:09:45.371Z*

<details>
<summary>View code</summary>

```typescript
import { describe, it, expect, vi } from 'vitest';

vi.mock('vscode', () => {
  return {
    window: {
      registerWebviewViewProvider: vi.fn(() => ({ dispose: vi.fn() })),
    },
  };
});

import { activate } from '../src/extension';

describe('Extension activation', () => {
  it('should activate without throwing and register the panel', () => {
    const subscriptions: { dispose?: () => void }[] = [];
    const context = { subscriptions } as any;

    expect(() => activate(context)).not.toThrow();
    expect(subscriptions.length).toBeGreaterThan(0);
  });
});

```

</details>


## extension/tsconfig.json

*Size: 285 bytes | Modified: 2025-12-20T00:00:18.138Z*

<details>
<summary>View code</summary>

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "Node16",
    "moduleResolution": "node16",
    "strict": true,
    "outDir": "dist",
    "rootDir": "src",
    "lib": ["ES2020", "DOM"],
    "skipLibCheck": true,
    "resolveJsonModule": true
  },
  "include": ["src"]
}

```

</details>


## README.md

*Size: 253 bytes | Modified: 2025-12-16T19:21:50.556Z*

<details>
<summary>View code</summary>

```markdown
# LocalPilot

[![Windows CI](https://github.com/TarekRefaei/LocalPilot/actions/workflows/windows-ci.yml/badge.svg)](https://github.com/TarekRefaei/LocalPilot/actions/workflows/windows-ci.yml)

Privacy-first AI coding agent for VS Code using local LLMs.

```

</details>


## scripts/dev.ps1

*Size: 4,918 bytes | Modified: 2025-12-20T00:00:18.138Z*

<details>
<summary>View code</summary>

```powershell
#requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
function Clear-Port {
  param (
    [Parameter(Mandatory)]
    [int]$Port
  )

  Write-Host "Checking if port $Port is in use..."

  try {
    $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
  } catch {
    Write-Warning "Get-NetTCPConnection failed. Cannot auto-clear port."
    return
  }

  if (-not $connections) {
    Write-Host "Port $Port is free."
    return
  }

  $owningProcessIds = $connections |
    Select-Object -ExpandProperty OwningProcess -Unique

  foreach ($processId in $owningProcessIds) {
    try {
      $proc = Get-Process -Id $processId -ErrorAction Stop
      Write-Warning "Stopping process $($proc.ProcessName) (PID $processId) using port $Port"
      Stop-Process -Id $processId -Force -ErrorAction Stop
    } catch {
      Write-Warning "Failed to stop process with PID $processId"
    }
  }

  Start-Sleep -Milliseconds 500

  # Verify
  $stillUsed = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
  if ($stillUsed) {
    throw "Port $Port is still in use after cleanup."
  }

  Write-Host "Port $Port successfully cleared."
}


# =========================
# CONFIGURATION
# =========================
$Port        = 8000
$BindHost    = '0.0.0.0'
$HealthPath  = '/health'
$OllamaUrl   = 'http://127.0.0.1:11434'
$DevReload  = $false   # set to $true ONLY when running backend in foreground

# =========================
# PATHS
# =========================
$RepoRoot     = Split-Path -Parent $PSScriptRoot
$ServerDir    = Join-Path $RepoRoot 'server'
$ExtensionDir = Join-Path $RepoRoot 'extension'
$VenvPython   = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $VenvPython)) { $VenvPython = 'python' }

$HostUrl = "http://localhost:${Port}"

Write-Host "== LocalPilot Dev Runner ==" -ForegroundColor Cyan
Write-Host "Repo:     $RepoRoot"
Write-Host "Backend:  $HostUrl"
Write-Host "Ollama:   $OllamaUrl"
Write-Host ""

# =========================
# 1) BACKEND DEPENDENCIES
# =========================
$Requirements = Join-Path $ServerDir 'requirements.txt'
if (Test-Path $Requirements) {
  Write-Host "Installing backend requirements..."
  & $VenvPython -m pip install -r $Requirements | Out-Host
}

# =========================
# 2) PORT CHECK
# =========================
Write-Host "Checking port $Port availability..."
try {
  Clear-Port -Port $Port
} catch {
  Write-Error $_
  exit 1
}

# =========================
# 3) START BACKEND
# =========================
Write-Host "Starting backend..."

$BackendArgs = @(
  '-m', 'uvicorn',
  'server.main:app',
  '--host', $BindHost,
  '--port', $Port,
  '--log-level', 'debug'
)

if ($DevReload) {
  $BackendArgs += '--reload'
}

$BackendProcess = Start-Process `
  -FilePath $VenvPython `
  -ArgumentList $BackendArgs `
  -WorkingDirectory $RepoRoot `
  -NoNewWindow `
  -PassThru

# =========================
# 4) HEALTH CHECK
# =========================
Write-Host "Waiting for backend to accept connections..."

$Deadline = (Get-Date).AddSeconds(30)
$Healthy = $false

while ((Get-Date) -lt $Deadline) {
  try {
    $client = New-Object System.Net.Sockets.TcpClient
    $client.Connect("localhost", $Port)
    $client.Close()
    $Healthy = $true
    break
  } catch {
    Start-Sleep -Milliseconds 500
  }

  if ($BackendProcess.HasExited) {
    Write-Error "Backend exited during startup."
    exit 1
  }
}

if (-not $Healthy) {
  Write-Error "Backend did not open port $Port within timeout."
  Stop-Process -Id $BackendProcess.Id -Force -ErrorAction SilentlyContinue
  exit 1
}

Write-Host "Backend is accepting connections." -ForegroundColor Green

# =========================
# 5) BUILD EXTENSION
# =========================
Write-Host "Preparing extension..."
Set-Location $ExtensionDir

if (-not (Test-Path 'node_modules')) {
  npm install
}

npm run build
if ($LASTEXITCODE -ne 0) {
  Write-Error "Extension build failed."
  Stop-Process -Id $BackendProcess.Id -Force
  exit 1
}

# =========================
# 6) LAUNCH VS CODE
# =========================
$codeCmd = Get-Command code -ErrorAction SilentlyContinue
if (-not $codeCmd) {
  Write-Warning "VS Code CLI 'code' not found."
  Write-Host "Run manually:"
  Write-Host "  code --extensionDevelopmentPath `"$ExtensionDir`""
} else {
  Write-Host "Launching VS Code Extension Development Host..."
  Start-Process "code" "--disable-extensions --extensionDevelopmentPath `"$ExtensionDir`""
  # & code --disable-extensions --extensionDevelopmentPath $ExtensionDir
}

Write-Host ""
Write-Host "== Backend running. Press Ctrl+C to stop ==" -ForegroundColor Cyan

# =========================
# 7) SHUTDOWN HANDLING
# =========================
try {
  while ($true) {
    Start-Sleep -Seconds 1
  }
}
finally {
  Write-Host "Stopping backend..."
  try {
    Stop-Process -Id $BackendProcess.Id -Force
  } catch {}
}




```

</details>


## server/__init__.py

*Size: 0 bytes | Modified: 2025-12-16T19:21:50.561Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/.pytest_cache/README.md

*Size: 310 bytes | Modified: 2025-12-13T20:24:55.581Z*

<details>
<summary>View code</summary>

```markdown
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

```

</details>


## server/api/__init__.py

*Size: 0 bytes | Modified: 2025-12-16T19:21:50.561Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/api/dependencies.py

*Size: 456 bytes | Modified: 2025-12-20T23:56:57.480Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from functools import lru_cache

try:
    from ..indexing.embeddings.ollama import OllamaEmbeddingProvider
except ImportError:
    from indexing.embeddings.ollama import OllamaEmbeddingProvider


@lru_cache()
def get_embedder():
    return OllamaEmbeddingProvider(
        base_url="http://127.0.0.1:11434",
        model="mxbai-embed-large"
    )


def get_index_root() -> Path:
    return Path.home() / ".localpilot" / "indexes"

```

</details>


## server/api/routes/__init__.py

*Size: 0 bytes | Modified: 2025-12-16T19:21:50.562Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/api/routes/chat_ws.py

*Size: 1,024 bytes | Modified: 2025-12-20T23:56:57.481Z*

<details>
<summary>View code</summary>

```python
from fastapi import APIRouter, WebSocket
import json

from server.chat.ollama_chat_client import OllamaChatClient

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    payload = await websocket.receive_json()

    model = payload.get("model")
    messages = payload.get("messages")

    try:
        client = OllamaChatClient(
            base_url="http://127.0.0.1:11434",
            model=model,
        )

        for token in client.stream_chat(messages):
            await websocket.send_text(json.dumps({
                "type": "token",
                "value": token
            }))

        await websocket.send_text(json.dumps({ "type": "done" }))

    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "source": "backend",
            "message": str(e)
        }))
        await websocket.send_text(json.dumps({ "type": "done" }))

    finally:
        await websocket.close()

```

</details>


## server/api/routes/index.py

*Size: 1,825 bytes | Modified: 2025-12-20T23:56:57.481Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import json
import queue
import threading

from server.api.dependencies import get_index_root, get_embedder
from server.indexing.service import IndexingService
from server.indexing.progress import ProgressTracker

router = APIRouter()


@router.get("/index/{project_id}")
def index_project(
    project_id: str,
    index_root: Path = Depends(get_index_root),
    embedder = Depends(get_embedder),
):
    q: queue.Queue = queue.Queue()

    def run_indexing():
        try:
            workspace = Path(
                r"C:\Users\super\OneDrive\Desktop\My Projects\LocalPilot\test_project"
            )

            def on_progress(phase: str, current: int, total: int):
                q.put({
                    "type": "index:progress",
                    "phase": phase,
                    "current": current,
                    "total": total,
                })

            tracker = ProgressTracker(on_progress)

            service = IndexingService(
                workspace=workspace,
                index_root=index_root / project_id,
                embedder=embedder,
                progress=tracker,
            )

            service.run()

            q.put({ "type": "index:done" })

        except Exception as e:
            q.put({
                "type": "error",
                "message": str(e),
            })

    threading.Thread(target=run_indexing, daemon=True).start()

    def event_stream():
        while True:
            event = q.get()
            yield f"data: {json.dumps(event)}\n\n"
            if event["type"] in ("index:done", "error"):
                break

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )

```

</details>


## server/api/routes/project.py

*Size: 648 bytes | Modified: 2025-12-20T23:56:57.482Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException

try:
    from server.api.dependencies import get_index_root
except ImportError:
    from server.api.dependencies import get_index_root

router = APIRouter()


@router.get("/project/{project_id}/summary")
def get_project_summary(
    project_id: str,
    index_root: Path = Depends(get_index_root),
):
    summary_path = index_root / project_id / "summary.json"
    if not summary_path.exists():
        raise HTTPException(status_code=404, detail="summary not found")

    with open(summary_path, "r", encoding="utf-8") as f:
        return __import__("json").load(f)

```

</details>


## server/api/routes/query.py

*Size: 739 bytes | Modified: 2025-12-20T23:56:57.483Z*

<details>
<summary>View code</summary>

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pathlib import Path

from server.api.dependencies import get_index_root, get_embedder
from server.indexing.query_service import QueryService

router = APIRouter()


class QueryRequest(BaseModel):
    project_id: str
    query: str
    top_k: int = 5


@router.post("/query")
def query_index(
    request: QueryRequest,
    index_root: Path = Depends(get_index_root),
    embedder = Depends(get_embedder),
):
    service = QueryService(
        index_root=index_root,
        project_id=request.project_id,
        embedder=embedder,
    )

    results = service.query(
        text=request.query,
        top_k=request.top_k,
    )

    return {"chunks": results}

```

</details>


## server/api/schemas/__init__.py

*Size: 0 bytes | Modified: 2025-12-16T19:21:50.563Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/api/schemas/query.py

*Size: 357 bytes | Modified: 2025-12-16T19:21:50.563Z*

<details>
<summary>View code</summary>

```python
from typing import List, Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    project_id: str
    query: str
    top_k: int = 5
    filters: Optional[dict] = None


class RetrievedChunk(BaseModel):
    id: str
    content: str
    metadata: dict
    distance: float


class QueryResponse(BaseModel):
    chunks: List[RetrievedChunk]

```

</details>


## server/chat/__init__.py

*Size: 0 bytes | Modified: 2025-12-16T19:21:50.563Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/chat/chat_service.py

*Size: 1,276 bytes | Modified: 2025-12-16T19:21:50.564Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from typing import Iterable

from .prompt_builder import PromptBuilder
from .ollama_chat_client import OllamaChatClient
try:
    from ..indexing.query_service import QueryService
except ImportError:
    from indexing.query_service import QueryService


class ChatService:
    """
    Phase 1.2
    ----------
    Orchestrates:
    - RAG retrieval
    - Prompt building
    - Streaming chat response
    """

    def __init__(
        self,
        index_root: Path,
        embedder,
        ollama_base_url: str,
        chat_model: str
    ):
        self.query_service = QueryService(
            index_root=index_root,
            embedder=embedder
        )
        self.prompt_builder = PromptBuilder()
        self.chat_client = OllamaChatClient(
            base_url=ollama_base_url,
            model=chat_model
        )

    def stream_chat(
        self,
        project_id: str,
        user_message: str,
        top_k: int = 5
    ) -> Iterable[str]:
        chunks = self.query_service.query(
            text=user_message,
            top_k=top_k
        )

        messages = self.prompt_builder.build(
            user_message=user_message,
            chunks=chunks
        )

        return self.chat_client.stream_chat(messages)

```

</details>


## server/chat/ollama_chat_client.py

*Size: 917 bytes | Modified: 2025-12-20T00:00:18.140Z*

<details>
<summary>View code</summary>

```python
import json
import requests
from typing import Iterable, Dict

class OllamaChatClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def stream_chat(self, messages: Iterable[Dict]) -> Iterable[str]:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": list(messages),
                "stream": True
            },
            stream=True,
            timeout=300
        )

        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line.decode("utf-8"))
            if data.get("done"):
                return

            content = data.get("message", {}).get("content")
            if content:
                yield content

```

</details>


## server/chat/prompt_builder.py

*Size: 1,367 bytes | Modified: 2025-12-16T19:21:50.564Z*

<details>
<summary>View code</summary>

````python
from typing import List, Dict


class PromptBuilder:
    """
    Phase 1.2
    ----------
    Builds a chat prompt with injected RAG context.
    No planning, no execution, no file writes.
    """

    SYSTEM_PROMPT = (
        "You are a helpful AI assistant answering questions about a codebase.\n"
        "You must base your answers ONLY on the provided code context.\n"
        "If the answer is not in the context, say you don't know.\n"
        "Do NOT suggest code changes or plans."
    )

    def build(
        self,
        user_message: str,
        chunks: List[Dict]
    ) -> List[Dict]:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]

        if chunks:
            context_blocks = []
            for c in chunks:
                meta = c.get("metadata", {})
                context_blocks.append(
                    f"File: {meta.get('file_path')} "
                    f"(lines {meta.get('start_line')}–{meta.get('end_line')})\n"
                    f"```{meta.get('language', '')}\n"
                    f"{c.get('content')}\n```"
                )

            messages.append({
                "role": "system",
                "content": "CODE CONTEXT:\n\n" + "\n\n".join(context_blocks)
            })

        messages.append({"role": "user", "content": user_message})
        return messages

````

</details>


## server/indexing/__init__.py

*Size: 0 bytes | Modified: 2025-12-16T19:21:50.564Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/indexing/chunk.py

*Size: 236 bytes | Modified: 2025-12-16T19:21:50.564Z*

<details>
<summary>View code</summary>

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CodeChunk:
    id: str
    file_path: str
    language: str
    start_line: int
    end_line: int
    content: str
    symbol_type: str  # function, class, module, block

```

</details>


## server/indexing/chunker.py

*Size: 6,782 bytes | Modified: 2025-12-20T23:56:57.485Z*

<details>
<summary>View code</summary>

```python
import hashlib
import re
from typing import List

from .chunk import CodeChunk


class SemanticChunker:
    """
    Phase 2.5
    ----------
    Semantic, regex-based chunker.

    Guarantees:
    - File-level chunk always exists
    - Symbol-level chunks are non-overlapping
    - Chunk IDs are deterministic and UNIQUE
    """

    def chunk_file(
        self,
        file_path: str,
        language: str,
        source: str
    ) -> List[CodeChunk]:

        lines = source.splitlines()
        total_lines = len(lines)
        chunks: List[CodeChunk] = []

        # -------------------------
        # File-level chunk
        # -------------------------
        file_content = source.strip()
        if file_content:
            chunks.append(
                CodeChunk(
                    id=self._stable_id(
                        file_path,
                        1,
                        total_lines,
                        "file",
                        file_content,
                    ),
                    file_path=file_path,
                    language=language,
                    start_line=1,
                    end_line=total_lines,
                    content=file_content,
                    symbol_type="file",
                )
            )

        # -------------------------
        # Symbol-level chunking
        # -------------------------
        if language == "python":
            chunks.extend(self._chunk_python(source, file_path, language))
        elif language in {"typescript", "javascript"}:
            chunks.extend(self._chunk_js_ts(source, file_path, language))

        return chunks

    # ==========================================================
    # ID generation (CRITICAL)
    # ==========================================================
    def _stable_id(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        symbol_type: str,
        content: str,
    ) -> str:
        """
        Deterministic & unique chunk identity.
        """
        h = hashlib.sha256()
        h.update(file_path.encode("utf-8"))
        h.update(str(start_line).encode("utf-8"))
        h.update(str(end_line).encode("utf-8"))
        h.update(symbol_type.encode("utf-8"))
        h.update(content.encode("utf-8"))
        return h.hexdigest()

    # ==========================================================
    # Helpers
    # ==========================================================
    def _slice_content(self, src: str, start_line: int, end_line: int) -> str:
        lines = src.splitlines()
        return "\n".join(lines[start_line - 1 : end_line]).strip()

    # ==========================================================
    # Python chunking
    # ==========================================================
    def _chunk_python(
        self,
        source: str,
        file_path: str,
        language: str
    ) -> List[CodeChunk]:

        lines = source.splitlines()
        n = len(lines)
        chunks: List[CodeChunk] = []

        def indent(s: str) -> int:
            return len(s.replace("\t", "    ")) - len(s.lstrip(" "))

        symbols: List[tuple[int, str]] = []  # (line_no, type)

        for i, line in enumerate(lines, start=1):
            if indent(line) != 0:
                continue
            if re.match(r"^\s*class\s+\w+", line):
                symbols.append((i, "class"))
            elif re.match(r"^\s*def\s+\w+\s*\(", line):
                symbols.append((i, "function"))

        for idx, (start, symbol_type) in enumerate(symbols):
            end = n
            start_indent = indent(lines[start - 1])

            for j in range(idx + 1, len(symbols)):
                next_line = symbols[j][0]
                if indent(lines[next_line - 1]) <= start_indent:
                    end = next_line - 1
                    break

            content = self._slice_content(source, start, end)
            if not content or len(content.strip()) < 10:
                continue

            chunks.append(
                CodeChunk(
                    id=self._stable_id(
                        file_path,
                        start,
                        end,
                        symbol_type,
                        content,
                    ),
                    file_path=file_path,
                    language=language,
                    start_line=start,
                    end_line=end,
                    content=content,
                    symbol_type=symbol_type,
                )
            )

        return chunks

    # ==========================================================
    # JS / TS chunking
    # ==========================================================
    def _find_block_end(self, lines: List[str], start_idx: int) -> int:
        depth = 0
        for i in range(start_idx, len(lines)):
            depth += lines[i].count("{")
            depth -= lines[i].count("}")
            if depth == 0 and "{" in lines[start_idx]:
                return i + 1
        return len(lines)

    def _chunk_js_ts(
        self,
        source: str,
        file_path: str,
        language: str
    ) -> List[CodeChunk]:

        lines = source.splitlines()
        chunks: List[CodeChunk] = []

        patterns = {
            "class": re.compile(r"^\s*(export\s+)?class\s+\w+"),
            "function": re.compile(r"^\s*(export\s+)?function\s+\w+"),
            "interface": re.compile(r"^\s*(export\s+)?interface\s+\w+"),
        }

        i = 0
        while i < len(lines):
            line = lines[i]

            for symbol_type, pat in patterns.items():
                if pat.match(line):
                    start = i + 1
                    end = self._find_block_end(lines, i)
                    content = self._slice_content(source, start, end)

                    if content and len(content.strip()) >= 10:
                        chunks.append(
                            CodeChunk(
                                id=self._stable_id(
                                    file_path,
                                    start,
                                    end,
                                    symbol_type,
                                    content,
                                ),
                                file_path=file_path,
                                language=language,
                                start_line=start,
                                end_line=end,
                                content=content,
                                symbol_type=symbol_type,
                            )
                        )
                    i = end
                    break
            else:
                i += 1

        return chunks
```

</details>


## server/indexing/embeddings/__init__.py

*Size: 0 bytes | Modified: 2025-12-16T19:21:50.566Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/indexing/embeddings/base.py

*Size: 331 bytes | Modified: 2025-12-16T19:21:50.566Z*

<details>
<summary>View code</summary>

```python
from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        Must be deterministic for identical inputs.
        """
        raise NotImplementedError

```

</details>


## server/indexing/embeddings/ollama.py

*Size: 768 bytes | Modified: 2025-12-16T19:21:50.567Z*

<details>
<summary>View code</summary>

```python
import requests
from typing import List

from .base import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []

        for text in texts:
            res = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text
                },
                timeout=60
            )
            res.raise_for_status()
            data = res.json()
            embeddings.append(data["embedding"])

        return embeddings

```

</details>


## server/indexing/hash_tracker.py

*Size: 240 bytes | Modified: 2025-12-16T19:21:50.567Z*

<details>
<summary>View code</summary>

```python
import hashlib
from pathlib import Path


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

```

</details>


## server/indexing/language.py

*Size: 291 bytes | Modified: 2025-12-16T19:21:50.567Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path


EXTENSION_LANGUAGE_MAP = {
    ".ts": "typescript",
    ".js": "javascript",
    ".py": "python",
    ".dart": "dart",
    ".json": "json",
    ".md": "markdown"
}


def detect_language(path: Path) -> str | None:
    return EXTENSION_LANGUAGE_MAP.get(path.suffix)

```

</details>


## server/indexing/parsers/__init__.py

*Size: 0 bytes | Modified: 2025-12-16T19:21:50.567Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/indexing/parsers/base.py

*Size: 322 bytes | Modified: 2025-12-16T19:21:50.568Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from typing import Any


class ParseResult:
    def __init__(self, ast: Any, source: str):
        self.ast = ast
        self.source = source


class BaseParser:
    language: str

    def parse(self, path: Path) -> ParseResult:
        raise NotImplementedError("Parser must implement parse()")

```

</details>


## server/indexing/progress.py

*Size: 417 bytes | Modified: 2025-12-20T23:56:57.485Z*

<details>
<summary>View code</summary>

```python
from typing import Callable, Optional


class ProgressTracker:
    """
    Phase 2.5
    ----------
    Lightweight progress reporter used by indexing services.
    """

    def __init__(self, callback: Callable[[str, int, int], None]):
        self._callback = callback

    def report(self, phase: str, current: int, total: int) -> None:
        if self._callback:
            self._callback(phase, current, total)

```

</details>


## server/indexing/query_service.py

*Size: 608 bytes | Modified: 2025-12-20T23:56:57.486Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from .vector_store import VectorStore

class QueryService:
    def __init__(
        self,
        index_root: Path,
        project_id: str,
        embedder,
    ):
        self.index_root = index_root
        self.project_id = project_id
        self.embedder = embedder

        self.store = VectorStore(
            persist_dir=str(index_root / project_id / "chroma"),
            collection_name="code_chunks",
        )

    def query(self, text: str, top_k: int = 5):
        embedding = self.embedder.embed([text])[0]
        return self.store.query(embedding, top_k=top_k)

```

</details>


## server/indexing/README.md

*Size: 521 bytes | Modified: 2025-12-16T19:21:50.564Z*

<details>
<summary>View code</summary>

```markdown
# Indexing (Phase 1)


## Status
Phase 1 – MVP indexing backend


## Supported
- Workspace scanning
- Hash-based incremental indexing
- Deterministic chunk IDs
- Ollama embeddings
- ChromaDB persistence
- Vector querying for Chat RAG


## Known Limitations (Expected)
- File-level chunking only (AST chunking in Phase 2)
- Deleted files are not yet purged from index
- One-request-per-embedding (batching later)


## Guarantees
- Index survives restart
- Same file → same chunk ID
- Read-only (no workspace mutation)

```

</details>


## server/indexing/scanner.py

*Size: 691 bytes | Modified: 2025-12-16T19:21:50.569Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from typing import List

EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "__pycache__",
    ".localpilot"
}

SUPPORTED_EXTENSIONS = {
    ".ts", ".js", ".py", ".json", ".md", ".dart"
}


class WorkspaceScanner:
    def scan(self, root: Path) -> List[Path]:
        files: List[Path] = []

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if any(part in EXCLUDED_DIRS for part in path.parts):
                continue

            if path.suffix not in SUPPORTED_EXTENSIONS:
                continue

            files.append(path)

        return sorted(files)

```

</details>


## server/indexing/service.py

*Size: 4,407 bytes | Modified: 2025-12-20T23:56:57.486Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path

from .scanner import WorkspaceScanner
from .language import detect_language
from .chunker import SemanticChunker
from .hash_tracker import hash_file
from .state import IndexState
from .vector_store import VectorStore
from .symbol_index import SymbolIndex
from .summary_service import SummaryService


class IndexingService:
    """
    Phase 2.5
    ----------
    Produces:
    - Vector index (semantic chunks)
    - Symbol index (structure)
    - Project summary (knowledge)
    """

    def __init__(
        self,
        workspace: Path,
        index_root: Path,
        embedder,
        progress=None,
    ):
        self.workspace = workspace
        self.index_root = index_root
        self.embedder = embedder
        self.progress = progress

        self.scanner = WorkspaceScanner()
        self.chunker = SemanticChunker()

    def run(self) -> None:
        state = IndexState(self.index_root)
        state.load()

        files = self.scanner.scan(self.workspace)
        total_files = len(files)

        all_chunks = []
        texts = []
        symbol_index = SymbolIndex(self.index_root)

        # ==================================================
        # Scan & chunk
        # ==================================================
        for idx, path in enumerate(files, start=1):
            if self.progress:
                self.progress.report("scan", idx, total_files)

            current_hash = hash_file(path)
            if state.file_hashes.get(str(path)) == current_hash:
                continue

            language = detect_language(path)
            if not language:
                continue

            source = path.read_text(encoding="utf-8", errors="ignore")

            chunks = self.chunker.chunk_file(
                file_path=str(path),
                language=language,
                source=source,
            )

            for c in chunks:
                if not c.content or not c.content.strip():
                    continue
                if len(c.content.strip()) < 10:
                    continue

                all_chunks.append(c)
                texts.append(c.content)

                if c.symbol_type != "file":
                    symbol_index.add_chunk(c)

            state.file_hashes[str(path)] = current_hash

            if self.progress:
                self.progress.report("chunk", idx, total_files)

        # ==================================================
        # Nothing new → still persist structure
        # ==================================================
        if not all_chunks:
            symbol_index.save()
            state.save()
            if self.progress:
                self.progress.report("complete", total_files, total_files)
            return

        # ==================================================
        # Embed
        # ==================================================
        embeddings = self.embedder.embed(texts)

        if len(embeddings) != len(all_chunks):
            raise RuntimeError(
                f"Embedding mismatch: {len(embeddings)} embeddings "
                f"for {len(all_chunks)} chunks"
            )

        for i, emb in enumerate(embeddings):
            if not emb:
                c = all_chunks[i]
                raise RuntimeError(
                    f"Empty embedding for chunk "
                    f"{c.file_path}:{c.start_line}-{c.end_line}"
                )

        # ==================================================
        # Store vectors
        # ==================================================
        ids = [c.id for c in all_chunks]
        if len(ids) != len(set(ids)):
            raise RuntimeError("Duplicate chunk IDs detected before vector insert")

        store = VectorStore(
            persist_dir=str(self.index_root / "chroma"),
            collection_name="code_chunks",
        )
        store.add(all_chunks, embeddings)

        # ==================================================
        # Persist structure & knowledge
        # ==================================================
        symbol_index.save()

        SummaryService(
            workspace=self.workspace,
            index_root=self.index_root,
        ).generate_and_save()

        state.save()

        if self.progress:
            self.progress.report("complete", total_files, total_files)
    
```

</details>


## server/indexing/state.py

*Size: 714 bytes | Modified: 2025-12-16T19:21:50.570Z*

<details>
<summary>View code</summary>

```python
import json
from pathlib import Path
from typing import Dict


class IndexState:
    def __init__(self, root: Path):
        self.path = root / "state.json"
        self.file_hashes: Dict[str, str] = {}

    def load(self) -> None:
        if not self.path.exists():
            return
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.file_hashes = data.get("file_hashes", {})

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(
                {"file_hashes": self.file_hashes},
                f,
                indent=2
            )

```

</details>


## server/indexing/summary_service.py

*Size: 4,014 bytes | Modified: 2025-12-20T23:56:57.488Z*

<details>
<summary>View code</summary>

```python
import json
from pathlib import Path
from typing import List, Dict

import requests

from .scanner import WorkspaceScanner
from .language import detect_language


class SummaryService:
    """
    Phase 2.5 (FINAL)
    -----------------
    Deterministic project summary generator with OPTIONAL LLM refinement.
    Indexing MUST NOT fail if LLM misbehaves.
    """

    def __init__(
        self,
        workspace: Path,
        index_root: Path,
        ollama_base_url: str = "http://127.0.0.1:11434",
        model: str = "qwen2.5-coder:7b-instruct-q4_K_M",
    ):
        self.workspace = workspace
        self.index_root = index_root
        self.base_url = ollama_base_url.rstrip("/")
        self.model = model
        self.scanner = WorkspaceScanner()

    # ==========================================================
    # Deterministic facts
    # ==========================================================
    def _scan_files(self) -> List[Dict]:
        files = []
        for p in self.scanner.scan(self.workspace):
            files.append({
                "file": str(p.relative_to(self.workspace)),
                "language": detect_language(p) or "unknown"
            })
        return files

    def _load_symbols(self) -> List[Dict]:
        path = self.index_root / "symbols.json"
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    # ==========================================================
    # Deterministic fallback summary (ALWAYS VALID)
    # ==========================================================
    def _deterministic_summary(self) -> Dict:
        files = self._scan_files()
        symbols = self._load_symbols()

        languages = sorted({f["language"] for f in files})
        key_files = [f["file"] for f in files[:10]]

        return {
            "project_name": self.workspace.name,
            "description": "Indexed software project.",
            "main_languages": languages,
            "key_files": key_files,
            "architecture": "Workspace indexed into semantic code chunks and symbols.",
            "frameworks": [],
        }

    # ==========================================================
    # Optional LLM refinement (best-effort)
    # ==========================================================
    def _try_llm_summary(self, base_summary: Dict) -> Dict | None:
        system = (
            "You refine project summaries.\n"
            "Return ONLY valid JSON.\n"
            "No explanations.\n"
            "Schema must remain identical."
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(base_summary, indent=2)},
        ]

        try:
            resp = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0},
                },
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            content = (data.get("message") or {}).get("content", "").strip()
            if not content.startswith("{"):
                return None
            return json.loads(content)
        except Exception:
            return None

    # ==========================================================
    # Public API
    # ==========================================================
    def generate_and_save(self) -> Path:
        summary = self._deterministic_summary()

        # Try LLM enhancement, but NEVER fail indexing
        refined = self._try_llm_summary(summary)
        if isinstance(refined, dict):
            summary = refined

        out = self.index_root / "summary.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        return out

```

</details>


## server/indexing/symbol_index.py

*Size: 1,037 bytes | Modified: 2025-12-20T23:56:57.488Z*

<details>
<summary>View code</summary>

```python
import json
from pathlib import Path
from typing import List, Dict

from .chunk import CodeChunk


class SymbolIndex:
    def __init__(self, root: Path):
        self.path = root / "symbols.json"
        self._symbols: List[Dict] = []

    def add(self, file: str, symbol_type: str, start_line: int, end_line: int) -> None:
        self._symbols.append(
            {
                "file": file,
                "symbol_type": symbol_type,
                "start_line": start_line,
                "end_line": end_line,
            }
        )

    def add_chunk(self, chunk: CodeChunk) -> None:
        if chunk.symbol_type == "file":
            return
        self.add(
            file=chunk.file_path,
            symbol_type=chunk.symbol_type,
            start_line=chunk.start_line,
            end_line=chunk.end_line,
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._symbols, f, indent=2)

```

</details>


## server/indexing/vector_store.py

*Size: 1,945 bytes | Modified: 2025-12-20T23:56:57.489Z*

<details>
<summary>View code</summary>

```python
from typing import List, Optional, Dict, Any
import chromadb
from chromadb.config import Settings

from .chunk import CodeChunk


class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        chunks: List[CodeChunk],
        embeddings: List[List[float]],
    ) -> None:
        if not chunks:
            return

        self.collection.add(
            ids=[c.id for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[
                {
                    "file_path": c.file_path,
                    "language": c.language,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "symbol_type": c.symbol_type,
                }
                for c in chunks
            ],
            embeddings=embeddings,
        )
        # PersistentClient auto-persists

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        if self.collection.count() == 0:
            return []

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

        hits: List[Dict] = []
        for i in range(len(result["ids"][0])):
            hits.append(
                {
                    "id": result["ids"][0][i],
                    "content": result["documents"][0][i],
                    "metadata": result["metadatas"][0][i],
                    "distance": result["distances"][0][i],
                }
            )

        return hits

```

</details>


## server/main.py

*Size: 1,592 bytes | Modified: 2025-12-20T23:56:57.490Z*

<details>
<summary>View code</summary>

```python
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import requests

from server.api.routes import query as query_routes
from server.api.routes import chat_ws
from server.api.routes import project as project_routes
from server.api.routes import index as index_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup check: Ollama
    try:
        r = requests.get("http://127.0.0.1:11434/api/version", timeout=3)
        r.raise_for_status()
        print("Ollama detected")
    except Exception as e:
        print(f"Warning: Could not connect to Ollama: {e}")

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # OK for local dev
    allow_credentials=True,
    allow_methods=["*"],          # IMPORTANT: allows OPTIONS
    allow_headers=["*"],
)


# --------------------
# Routers
# --------------------
app.include_router(query_routes.router, prefix="/api")
app.include_router(project_routes.router, prefix="/api")
app.include_router(chat_ws.router)
app.include_router(index_routes.router, prefix="/api")

# --------------------
# Health endpoints
# --------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/ollama")
def ollama_health():
    try:
        r = requests.get("http://127.0.0.1:11434/api/version", timeout=2)
        r.raise_for_status()
        return {"status": "ok", "ollama": r.json()}
    except Exception as e:
        return {"status": "error", "error": str(e)}

```

</details>


## server/requirements.txt

*Size: 45 bytes | Modified: 2025-12-16T19:21:50.572Z*

<details>
<summary>View code</summary>

```text
fastapi
uvicorn
httpx
requests
chromadb

```

</details>


## server/tests/test_health.py

*Size: 451 bytes | Modified: 2025-12-13T20:25:32.942Z*

<details>
<summary>View code</summary>

```python
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Add the server root to sys.path so `main` can be imported regardless of CWD
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import app


def test_health_ok():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

```

</details>


## test_project/app.py

*Size: 39 bytes | Modified: 2025-12-20T23:56:57.490Z*

<details>
<summary>View code</summary>

```python
from utils import add

print(add(2, 3))
```

</details>


## test_project/utils.py

*Size: 32 bytes | Modified: 2025-12-20T23:56:57.490Z*

<details>
<summary>View code</summary>

```python
def add(a, b):
    return a + b

```

</details>
