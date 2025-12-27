## Project Structure

```
. (135 files)
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
│   ├── .plan/
│   │   ├── phase0/
│   │   │   ├── phase0.md
│   │   │   ├── phase0patch.md
│   │   │   └── task0-phase.md
│   │   ├── phase1/
│   │   │   └── phase1patch.md
│   │   ├── phase2/
│   │   │   └── phase2patch.md
│   │   ├── phase3/
│   │   │   ├── modificationsPhase.md
│   │   │   └── phase3patch.md
│   │   ├── phase4/
│   │   │   ├── new-act-plan.md
│   │   │   └── phase4patch.md
│   │   ├── master-execution-roadmap.md
│   │   └── Phase-by-Phase-TODO-List.md
│   ├── decisions/
│   │   ├── ADR-001-monorepo-structure.md
│   │   ├── ADR-002-llamaindex-over-langchain.md
│   │   └── ADR-003-chromadb-for-vectors.md
│   └── ProjectDocuments/
│       ├── architecture.md
│       ├── commit-convention.md
│       ├── development-setup.md
│       ├── indexing-spec.md
│       ├── modifications.md
│       ├── overview.md
│       ├── prompt-engineer.md
│       ├── release-policy.md
│       ├── security-model.md
│       ├── state-model.md
│       ├── structure.md
│       ├── testing-strategy.md
│       ├── troubleshooting.md
│       └── webview-protocol.md
├── extension/
│   ├── src/
│   │   ├── commands/
│   │   │   └── plan.commands.ts
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
│   │   │   ├── interfaces/
│   │   │   │   ├── file-system.interface.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── llm-provider.interface.ts
│   │   │   │   └── rag-provider.interface.ts
│   │   │   ├── schemas/
│   │   │   │   └── plan.schema.ts
│   │   │   └── project-context.ts
│   │   ├── features/
│   │   │   ├── act/
│   │   │   │   ├── __tests__/
│   │   │   │   │   └── act-contract.test.ts
│   │   │   │   ├── act-controller.ts
│   │   │   │   ├── act-events.ts
│   │   │   │   ├── act-persistence.ts
│   │   │   │   ├── act-prompts.ts
│   │   │   │   ├── act-service.ts
│   │   │   │   ├── act-session.ts
│   │   │   │   ├── act-state.ts
│   │   │   │   ├── act-types.ts
│   │   │   │   ├── backup-manager.ts
│   │   │   │   ├── code-generator.ts
│   │   │   │   ├── diff-generator.ts
│   │   │   │   ├── file-writer.ts
│   │   │   │   └── index-sync.ts
│   │   │   ├── chat/
│   │   │   │   ├── chat-service.ts
│   │   │   │   ├── chat-session.store.ts
│   │   │   │   ├── prompt-builder.ts
│   │   │   │   └── rag-client.ts
│   │   │   ├── ollama/
│   │   │   │   └── connection-manager.ts
│   │   │   └── plan/
│   │   │       ├── plan-approval.ts
│   │   │       ├── plan-client.ts
│   │   │       ├── plan-controller.ts
│   │   │       ├── plan-parser.ts
│   │   │       ├── plan-registry.ts
│   │   │       ├── plan-state.ts
│   │   │       ├── plan-validator.ts
│   │   │       └── plan-view-controller.ts
│   │   ├── infrastructure/
│   │   │   └── http/
│   │   │       └── api-client.ts
│   │   ├── panels/
│   │   │   └── main-panel.ts
│   │   ├── prompts/
│   │   │   └── system/
│   │   │       └── plan.system.ts
│   │   ├── views/
│   │   │   ├── act/
│   │   │   │   └── act-view.ts
│   │   │   ├── chat/
│   │   │   │   └── chat-view.ts
│   │   │   └── plan/
│   │   │       └── plan-view.ts
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
│   │   ├── dependencies.py
│   │   └── plan.py
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
│   ├── plan/
│   │   ├── __init__.py
│   │   ├── plan_parser.py
│   │   └── plan_service.py
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

*Size: 3,204 bytes | Modified: 2025-12-26T21:28:01.072Z*

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
    "scripts": {
        "build": "esbuild src/extension.ts --bundle --outfile=dist/extension.js --platform=node --external:vscode --format=cjs",
        "test": "vitest run"
    },
    "dependencies": {
        "uuid": "^13.0.0",
        "ws": "^8.16.0",
        "diff": "^5.2.0"
    },
    "devDependencies": {
        "@types/node": "^20.0.0",
        "@types/uuid": "^10.0.0",
        "@types/vscode": "^1.85.0",
        "@types/ws": "^8.5.12",
        "esbuild": "^0.27.1",
        "vitest": "^4.0.15",
        "@types/diff": "^5.2.1"
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
                    "name": "Chat",
                    "id": "localpilot.chat",
                    "type": "webview",
                    "icon": "./media/icon-localpilot.svg"
                },
                {
                    "name": "Plan",
                    "id": "localpilot.plan",
                    "type": "webview",
                    "icon": "./media/icon-localpilot.svg"
                },
                {
                    "name": "Act",
                    "id": "localpilot.act",
                    "type": "webview",
                    "icon": "./media/icon-localpilot.svg"
                }
            ]
        },
        "commands": [
            {
                "command": "localpilot.plan.createFromChat",
                "title": "LocalPilot: Create Plan from Chat"
            },
            {
                "command": "localpilot.chat.clear",
                "title": "LocalPilot: Clear Chat Session"
            },
            {
                "command": "localpilot.act.start",
                "title": "LocalPilot: Start Act Mode"
            },
            {
                "command": "localpilot.act.focus",
                "title": "LocalPilot: Focus Act View"
            },
            {
                "command": "localpilot.plan.fixJsonById",
                "title": "LocalPilot: Fix Plan JSON"
            }
        ],
        "menus": {
            "view/title": [
                {
                    "command": "localpilot.plan.createFromChat",
                    "when": "view == localpilot.plan",
                    "group": "navigation"
                },
                {
                    "command": "localpilot.act.start",
                    "when": "view == localpilot.plan",
                    "group": "navigation@3"
                },
                {
                    "command": "localpilot.chat.clear",
                    "when": "view == localpilot.chat",
                    "group": "navigation@2"
                }
            ]
        }
    }
}

```

</details>


## extension/src/commands/plan.commands.ts

*Size: 1,306 bytes | Modified: 2025-12-24T19:15:35.114Z*

<details>
<summary>View code</summary>

```typescript
﻿import * as vscode from 'vscode';
import { createPlanFromChat, validateCurrentPlan, approveCurrentPlan, discardCurrentPlan, regeneratePlan } from '../features/plan/plan-controller';
import { ChatSessionStore } from '../features/chat/chat-session.store';

export function registerPlanCommands(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand(
      'localpilot.plan.createFromChat',
      async () => {
        const chatMessages = ChatSessionStore.getMessages();
        if (!chatMessages || chatMessages.length === 0) {
          vscode.window.showWarningMessage('No chat history available to generate a plan.');
          return;
        }
        await createPlanFromChat(chatMessages);
      }
    ),
    vscode.commands.registerCommand(
      'localpilot.plan.validate',
      async () => { await validateCurrentPlan(); }
    ),
    vscode.commands.registerCommand(
      'localpilot.plan.approve',
      async () => { await approveCurrentPlan(); }
    ),
    vscode.commands.registerCommand(
      'localpilot.plan.discard',
      async () => { await discardCurrentPlan(); }
    ),
    vscode.commands.registerCommand(
      'localpilot.plan.regenerate',
      async () => { await regeneratePlan(ChatSessionStore.getMessages()); }
    )
  );
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

*Size: 401 bytes | Modified: 2025-12-24T19:15:35.116Z*

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
  /** Current plan status */
  status: PlanStatus;
}

export type PlanStatus =
  | 'draft'
  | 'approved';

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

*Size: 570 bytes | Modified: 2025-12-24T19:15:35.118Z*

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
}

export type TaskActionType = 'create' | 'modify' | 'delete';

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


## extension/src/core/project-context.ts

*Size: 246 bytes | Modified: 2025-12-24T19:15:35.119Z*

<details>
<summary>View code</summary>

```typescript
/**
 * Project Context
 * ----------------
 * Phase 3: single-project mode.
 * This is the canonical source of truth for projectId.
 *
 * DO NOT inline projectId elsewhere.
 */
export function getActiveProjectId(): string {
  return 'default';
}

```

</details>


## extension/src/core/schemas/plan.schema.ts

*Size: 347 bytes | Modified: 2025-12-24T19:15:35.119Z*

<details>
<summary>View code</summary>

```typescript
export interface PlanSchema {
  id: string;
  title: string;
  overview: string;
  status: 'draft';
  tasks: TaskSchema[];
}

export interface TaskSchema {
  id: string;
  orderIndex: number;
  title: string;
  description: string;
  filePath: string;
  actionType: 'create' | 'modify' | 'delete';
  details: string[];
  dependencies: string[];
}

```

</details>


## extension/src/extension.ts

*Size: 3,111 bytes | Modified: 2025-12-26T21:26:43.786Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { registerPlanCommands } from './commands/plan.commands';
import { ChatSessionStore } from './features/chat/chat-session.store';
import { ChatViewProvider } from './views/chat/chat-view';
import { PlanViewProvider } from './views/plan/plan-view';
import { ActViewProvider } from './views/act/act-view';
import { getAllPlans, selectPlan, openPlan, validatePlanById, approvePlanById, discardPlanById, regeneratePlanById, fixPlanJsonById } from './features/plan/plan-controller';
import { ActPersistence } from './features/act/act-persistence';
import { actState } from './features/act/act-state';
import { startActByPlanId } from './features/act/act-controller';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  const planViewProvider = new PlanViewProvider();
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      ChatViewProvider.viewId,
      new ChatViewProvider()
    ),
    vscode.window.registerWebviewViewProvider(
      PlanViewProvider.viewId,
      planViewProvider
    ),
    vscode.window.registerWebviewViewProvider(
      ActViewProvider.viewId,
      new ActViewProvider()
    )
  );
  registerPlanCommands(context);
  context.subscriptions.push(
    vscode.commands.registerCommand('localpilot.plan.refresh', () => {
      const plans = getAllPlans();
      planViewProvider.update(plans);
    }),
    vscode.commands.registerCommand('localpilot.plan.select', selectPlan),
    vscode.commands.registerCommand('localpilot.plan.open', openPlan),
    vscode.commands.registerCommand('localpilot.plan.validateById', validatePlanById),
    vscode.commands.registerCommand('localpilot.plan.approveById', approvePlanById),
    vscode.commands.registerCommand('localpilot.plan.discardById', discardPlanById),
    vscode.commands.registerCommand('localpilot.plan.regenerateById', (planId: string) => regeneratePlanById(planId, ChatSessionStore.getMessages())),
    vscode.commands.registerCommand('localpilot.plan.fixJsonById', fixPlanJsonById)
  );
  const clearChat = vscode.commands.registerCommand('localpilot.chat.clear', () => {
    ChatSessionStore.clear();
    vscode.window.showInformationMessage('LocalPilot chat cleared.');
  });
  context.subscriptions.push(clearChat);

  context.subscriptions.push(
    vscode.workspace.onDidChangeWorkspaceFolders(() => {
      ChatSessionStore.clear();
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand(
      'localpilot.act.start',
      startActByPlanId
    ),
    vscode.commands.registerCommand(
      'localpilot.act.focus',
      () => vscode.commands.executeCommand('workbench.view.extension.localpilot.act')
    )
  );

  // Act Mode: load persisted session on startup and save on deactivate
  const persistence = new ActPersistence(context);
  const restored = persistence.load();
  if (restored) {
    actState.set(restored);
  }

  context.subscriptions.push({
    dispose() {
      const s = actState.get();
      if (s) persistence.save(s);
    },
  });
}

export function deactivate() {}

```

</details>


## extension/src/features/act/__tests__/act-contract.test.ts

*Size: 1,192 bytes | Modified: 2025-12-26T22:50:34.047Z*

<details>
<summary>View code</summary>

```typescript
import { describe, it, expect } from 'vitest';
import { validatePlan } from '../../plan/plan-validator';

describe('Plan → Act Contract', () => {
  it('blocks Act when plan has semantic warnings', () => {
    const plan = {
      id: 'p1',
      title: 'Test',
      overview: '',
      status: 'draft',
      tasks: [
        {
          id: 'task1',
          orderIndex: 0,
          title: 'Bad Task',
          description: '',
          filePath: '',
          actionType: 'create',
          details: ['x'],
          dependencies: []
        }
      ]
    } as any;

    const warnings = validatePlan(plan);
    expect(warnings.length).toBeGreaterThan(0);
  });

  it('allows Act when plan is fully valid', () => {
    const plan = {
      id: 'p1',
      title: 'Test',
      overview: '',
      status: 'draft',
      tasks: [
        {
          id: 'task1',
          orderIndex: 0,
          title: 'Good Task',
          description: '',
          filePath: 'utils.py',
          actionType: 'modify',
          details: ['x'],
          dependencies: []
        }
      ]
    } as any;

    const warnings = validatePlan(plan);
    expect(warnings.length).toBe(0);
  });
});

```

</details>


## extension/src/features/act/act-controller.ts

*Size: 1,133 bytes | Modified: 2025-12-26T23:11:07.540Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { planRegistry } from '../plan/plan-registry';
import { ActService } from './act-service';

const actService = new ActService();

export function startActByPlanId(planId: string) {
  const stored = planRegistry.getPlan(planId);

  if (!stored) {
    vscode.window.showErrorMessage('Plan not found.');
    return;
  }

  if (stored.status !== 'approved' || !stored.plan || (stored.warnings && stored.warnings.length)) {
    vscode.window.showErrorMessage(
      'Plan is not ready for Act Mode. Fix all plan issues first.'
    );
    return;
  }

  if (stored.plan.id !== planId) {
    vscode.window.showErrorMessage(
      'Internal error: plan identity mismatch. Please revalidate the plan.'
    );
    return;
  }

  try {
    // Lock plan
    planRegistry.update(planId, { status: 'acting' });

    // Start Act Session
    actService.start(stored.plan);

    // Focus Act view
    vscode.commands.executeCommand('localpilot.act.focus');
  } catch (err: any) {
    vscode.window.showErrorMessage(err?.message ?? 'Failed to start Act Mode.');
  }
}

```

</details>


## extension/src/features/act/act-events.ts

*Size: 211 bytes | Modified: 2025-12-26T19:26:35.823Z*

<details>
<summary>View code</summary>

```typescript
export type ActEvent =
  | { type: 'act:started' }
  | { type: 'act:paused' }
  | { type: 'act:resumed' }
  | { type: 'act:cancelled' }
  | { type: 'act:completed' }
  | { type: 'task:advance'; index: number };

```

</details>


## extension/src/features/act/act-persistence.ts

*Size: 512 bytes | Modified: 2025-12-26T19:26:35.750Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import type { ActSession } from './act-session';

const STORAGE_KEY = 'localpilot.act.session';

export class ActPersistence {
  constructor(private readonly context: vscode.ExtensionContext) {}

  load(): ActSession | null {
    return this.context.globalState.get<ActSession>(STORAGE_KEY) ?? null;
  }

  save(session: ActSession) {
    this.context.globalState.update(STORAGE_KEY, session);
  }

  clear() {
    this.context.globalState.update(STORAGE_KEY, undefined);
  }
}

```

</details>


## extension/src/features/act/act-prompts.ts

*Size: 1,201 bytes | Modified: 2025-12-26T19:35:34.314Z*

<details>
<summary>View code</summary>

```typescript
export const ACT_SYSTEM_PROMPT = `
You are operating in ACT MODE.


You must generate CODE ONLY for a SINGLE FILE.


RULES (MANDATORY):
- Output ONLY raw file content.
- NO markdown.
- NO explanations.
- NO comments about what you did.
- NO multiple files.
- Respect the given filePath and actionType.
- If modifying, preserve unrelated code.
- If information is missing, return the BEST SAFE IMPLEMENTATION based on context.
`;

export function buildActPrompt(args: {
  actionType: 'create' | 'modify' | 'delete';
  filePath: string;
  taskTitle: string;
  taskDescription: string;
  details: string[];
  existingContent?: string;
  ragContext?: string;
}) {
  const parts: string[] = [];

  parts.push(`Task: ${args.taskTitle}`);
  parts.push(`Description: ${args.taskDescription}`);
  parts.push(`Action: ${args.actionType}`);
  parts.push(`Target file: ${args.filePath}`);

  if (args.details?.length) {
    parts.push(`Details:\n- ${args.details.join('\n- ')}`);
  }

  if (args.existingContent) {
    parts.push(`Existing file content:\n${args.existingContent}`);
  }

  if (args.ragContext) {
    parts.push(`Relevant project context:\n${args.ragContext}`);
  }

  return parts.join('\n\n');
}

```

</details>


## extension/src/features/act/act-service.ts

*Size: 4,940 bytes | Modified: 2025-12-26T19:50:12.573Z*

<details>
<summary>View code</summary>

```typescript
import { actState } from './act-state';
import type { ActSession } from './act-session';
import type { Plan } from '../../core/entities/plan.entity';
import { CodeGenerator } from './code-generator';
import { generatePreview } from './diff-generator';
import * as path from 'path';
import * as vscode from 'vscode';
import { BackupManager } from './backup-manager';
import { FileWriter } from './file-writer';
import { triggerIndexSync } from './index-sync';

function genId(): string {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export class ActService {
  start(plan: Plan): ActSession {
    if (actState.hasActiveSession()) {
      throw new Error('Act session already active.');
    }

    const session: ActSession = {
      sessionId: genId(),
      planId: plan.id,
      status: 'idle',
      currentTaskIndex: 0,
      tasks: plan.tasks.map(t => ({
        task: t,
        state: 'pending',
      })),
      startedAt: Date.now(),
      lastUpdatedAt: Date.now(),
    };

    actState.set(session);
    return session;
  }

  run() {
    const s = actState.get();
    if (!s) return;
    actState.update({ status: 'running' });
  }

  pause() {
    const s = actState.get();
    if (!s) return;
    actState.update({ status: 'paused' });
  }

  resume() {
    const s = actState.get();
    if (!s) return;
    actState.update({ status: 'running' });
  }

  cancel() {
    actState.clear();
  }

  advanceTask() {
    const s = actState.get();
    if (!s) return;
    const next = s.currentTaskIndex + 1;
    if (next >= s.tasks.length) {
      actState.update({ status: 'completed' });
    } else {
      actState.update({ currentTaskIndex: next });
    }
  }

  getSession(): ActSession | null {
    return actState.get();
  }

  async generateCurrentPreview(model: string) {
    const s = actState.get();
    if (!s) return;

    const idx = s.currentTaskIndex;
    const et = s.tasks[idx];
    if (!et || et.state !== 'pending') return;

    const generator = new CodeGenerator();

    const code = await generator.generate({
      model,
      actionType: et.task.actionType,
      filePath: et.task.filePath,
      taskTitle: et.task.title,
      taskDescription: et.task.description,
      details: et.task.details,
      // existingContent to be provided in Phase 4.4 when reading from FS
    });

    const preview = generatePreview(
      et.task.actionType,
      undefined,
      code
    );

    s.tasks[idx] = {
      ...et,
      state: 'generated',
      preview,
    };

    actState.update({ tasks: s.tasks });
  }

  async applyCurrent(projectId: string, workspaceRoot: string) {
    const s = actState.get();
    if (!s) return;

    const idx = s.currentTaskIndex;
    const et = s.tasks[idx];
    if (!et || et.state !== 'generated') return;

    const targetPath = path.join(workspaceRoot, et.task.filePath);
    const backupMgr = new BackupManager(workspaceRoot);
    const writer = new FileWriter();

    let backup: string | null = null;
    try {
      backup = backupMgr.backup(targetPath);

      if (et.task.actionType === 'delete') {
        writer.delete(targetPath);
      } else {
        // Phase 4.3 stores preview content; use it for writing
        writer.write(targetPath, et.preview!.content);
      }

      s.tasks[idx] = { ...et, state: 'applied', backupPath: backup ?? undefined };
      actState.update({ tasks: s.tasks });

      await triggerIndexSync(projectId);

      this.advanceTask();
      // Auto-continue: generate next preview if not completed
      const after = actState.get();
      if (after && after.status !== 'completed') {
        try {
          await this.generateCurrentPreview('qwen2.5-coder:7b');
        } catch {}
      }
    } catch (err: any) {
      if (backup) {
        backupMgr.restore(backup, targetPath);
      }
      s.tasks[idx] = { ...et, state: 'error', error: String(err) };
      actState.update({ tasks: s.tasks, status: 'paused' });
      vscode.window.showErrorMessage('Apply failed. Changes rolled back.');
    }
  }

  async editCurrent(workspaceRoot: string) {
    const s = actState.get();
    if (!s) return;

    const et = s.tasks[s.currentTaskIndex];
    if (!et || et.state !== 'generated') return;

    const fileUri = vscode.Uri.file(path.join(workspaceRoot, et.task.filePath));
    const doc = await vscode.workspace.openTextDocument(fileUri);
    await vscode.window.showTextDocument(doc);

    s.tasks[s.currentTaskIndex] = { ...et, state: 'applied' };
    actState.update({ tasks: s.tasks });
  }

  skipCurrent() {
    const s = actState.get();
    if (!s) return;

    const idx = s.currentTaskIndex;
    s.tasks[idx] = { ...s.tasks[idx], state: 'skipped' };
    actState.update({ tasks: s.tasks });
    this.advanceTask();

    const after = actState.get();
    if (after && after.status !== 'completed') {
      this.generateCurrentPreview('qwen2.5-coder:7b').catch(() => {});
    }
  }
}

```

</details>


## extension/src/features/act/act-session.ts

*Size: 270 bytes | Modified: 2025-12-24T23:44:55.227Z*

<details>
<summary>View code</summary>

```typescript
import type { ExecutableTask, ActSessionStatus } from './act-types';

export interface ActSession {
  sessionId: string;
  planId: string;
  status: ActSessionStatus;
  currentTaskIndex: number;
  tasks: ExecutableTask[];
  startedAt: number;
  lastUpdatedAt: number;
}

```

</details>


## extension/src/features/act/act-state.ts

*Size: 583 bytes | Modified: 2025-12-26T19:26:58.900Z*

<details>
<summary>View code</summary>

```typescript
import type { ActSession } from './act-session';

class ActStateStore {
  private session: ActSession | null = null;

  get(): ActSession | null {
    return this.session;
  }

  set(session: ActSession) {
    this.session = session;
  }

  update(patch: Partial<ActSession>) {
    if (!this.session) return;
    this.session = { ...this.session, ...patch, lastUpdatedAt: Date.now() };
  }

  clear() {
    this.session = null;
  }

  hasActiveSession(): boolean {
    return !!this.session && this.session.status !== 'completed';
  }
}

export const actState = new ActStateStore();

```

</details>


## extension/src/features/act/act-types.ts

*Size: 485 bytes | Modified: 2025-12-26T19:52:28.259Z*

<details>
<summary>View code</summary>

```typescript
import type { Task } from '../../core/entities/task.entity';
import type { Preview } from './diff-generator';

export type ActSessionStatus =
  | 'idle'
  | 'running'
  | 'paused'
  | 'completed'
  | 'error';

export type TaskExecutionState =
  | 'pending'
  | 'generated'
  | 'applied'
  | 'skipped'
  | 'error';

export interface ExecutableTask {
  task: Task;
  state: TaskExecutionState;
  preview?: Preview;
  backupPath?: string;
  error?: string;
  generatedContent?: string;
}

```

</details>


## extension/src/features/act/backup-manager.ts

*Size: 702 bytes | Modified: 2025-12-26T19:47:18.055Z*

<details>
<summary>View code</summary>

```typescript
import * as fs from 'fs';
import * as path from 'path';

export class BackupManager {
  private baseDir: string;

  constructor(private readonly workspaceRoot: string) {
    this.baseDir = path.join(workspaceRoot, '.localpilot', 'backups');
    fs.mkdirSync(this.baseDir, { recursive: true });
  }

  backup(filePath: string): string | null {
    if (!fs.existsSync(filePath)) return null;

    const ts = Date.now().toString();
    const name = path.basename(filePath) + '.' + ts + '.bak';
    const dest = path.join(this.baseDir, name);

    fs.copyFileSync(filePath, dest);
    return dest;
  }

  restore(backupPath: string, targetPath: string) {
    fs.copyFileSync(backupPath, targetPath);
  }
}

```

</details>


## extension/src/features/act/code-generator.ts

*Size: 1,161 bytes | Modified: 2025-12-26T19:36:51.551Z*

<details>
<summary>View code</summary>

```typescript
import { ACT_SYSTEM_PROMPT, buildActPrompt } from './act-prompts';

type GenerateArgs = {
  model: string;
  actionType: 'create' | 'modify' | 'delete';
  filePath: string;
  taskTitle: string;
  taskDescription: string;
  details: string[];
  existingContent?: string;
  ragContext?: string;
};

export class CodeGenerator {
  constructor(private readonly baseUrl = 'http://127.0.0.1:11434') {}

  async generate(args: GenerateArgs): Promise<string> {
    const res = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: args.model,
        messages: [
          { role: 'system', content: ACT_SYSTEM_PROMPT },
          { role: 'user', content: buildActPrompt(args) }
        ],
        stream: false,
        options: { temperature: 0 }
      })
    });

    if (!res.ok) {
      throw new Error(`LLM generation failed: ${res.status}`);
    }

    const data = await res.json();
    const content = (data?.message?.content ?? '').trim();

    if (!content) {
      throw new Error('Empty code generation output.');
    }

    return content;
  }
}

```

</details>


## extension/src/features/act/diff-generator.ts

*Size: 696 bytes | Modified: 2025-12-26T19:37:15.696Z*

<details>
<summary>View code</summary>

```typescript
import * as Diff from 'diff';

export type Preview =
  | { kind: 'full'; content: string }
  | { kind: 'diff'; content: string }
  | { kind: 'snapshot'; content: string };

export function generatePreview(
  actionType: 'create' | 'modify' | 'delete',
  existingContent: string | undefined,
  generatedContent: string
): Preview {
  if (actionType === 'create') {
    return { kind: 'full', content: generatedContent };
  }

  if (actionType === 'delete') {
    return { kind: 'snapshot', content: existingContent ?? '' };
  }

  const patch = Diff.createTwoFilesPatch(
    'before',
    'after',
    existingContent ?? '',
    generatedContent
  );

  return { kind: 'diff', content: patch };
}

```

</details>


## extension/src/features/act/file-writer.ts

*Size: 374 bytes | Modified: 2025-12-26T19:48:30.286Z*

<details>
<summary>View code</summary>

```typescript
import * as fs from 'fs';
import * as path from 'path';

export class FileWriter {
  write(filePath: string, content: string) {
    const dir = path.dirname(filePath);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(filePath, content, 'utf-8');
  }

  delete(filePath: string) {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  }
}

```

</details>


## extension/src/features/act/index-sync.ts

*Size: 396 bytes | Modified: 2025-12-26T19:49:13.299Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';

export async function triggerIndexSync(projectId: string) {
  const url = `http://127.0.0.1:8000/api/index/${encodeURIComponent(projectId)}`;
  try {
    await fetch(url);
    vscode.window.showInformationMessage('Index updated for applied changes.');
  } catch (e) {
    vscode.window.showWarningMessage('Index sync failed. You may re-index manually.');
  }
}

```

</details>


## extension/src/features/chat/chat-service.ts

*Size: 1,435 bytes | Modified: 2025-12-24T19:15:35.123Z*

<details>
<summary>View code</summary>

```typescript
import { queryRAG } from "./rag-client";
import { PromptBuilder } from "./prompt-builder";
import { getProjectSummary } from "../../infrastructure/http/api-client";
import { ChatSessionStore } from "./chat-session.store";

export class ChatService {
  async sendMessage(
    userMessage: string,
    onEvent: (event: any) => void,
    projectId: string
  ): Promise<void> {

    ChatSessionStore.addMessage({ role: 'user', content: userMessage });
    const chunks = await queryRAG(projectId, userMessage);
    const summary = await getProjectSummary(projectId);
    const messages = new PromptBuilder().build(userMessage, chunks, summary);

    const WS = require("ws");
    const ws = new WS("ws://localhost:8000/ws/chat");

    let assistantBuffer = "";

    ws.on("open", () => {
      ws.send(JSON.stringify({
        model: "qwen2.5-coder:7b-instruct-q4_K_M",
        messages
      }));
    });

    ws.on("message", (raw: any) => {
      const msg = JSON.parse(raw.toString());
      if (msg.type === "token" && typeof msg.value === "string") {
        assistantBuffer += msg.value;
      }
      onEvent(msg);
      if (msg.type === "done") {
        if (assistantBuffer) {
          ChatSessionStore.addMessage({ role: 'assistant', content: assistantBuffer });
          assistantBuffer = "";
        }
      }
    });

    ws.on("error", (err: any) => {
      onEvent({ type: "error", message: String(err) });
    });
  }
}

```

</details>


## extension/src/features/chat/chat-session.store.ts

*Size: 473 bytes | Modified: 2025-12-24T19:15:35.124Z*

<details>
<summary>View code</summary>

```typescript
export type ChatMessage = { role: 'system' | 'user' | 'assistant'; content: string };

export class ChatSessionStore {
  private static messages: ChatMessage[] = [];

  static addMessage(msg: ChatMessage) {
    if (!msg || !msg.role || typeof msg.content !== 'string') return;
    this.messages.push({ role: msg.role, content: msg.content });
  }

  static getMessages(): ChatMessage[] {
    return [...this.messages];
  }

  static clear() {
    this.messages = [];
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


## extension/src/features/plan/plan-approval.ts

*Size: 154 bytes | Modified: 2025-12-24T19:15:35.124Z*

<details>
<summary>View code</summary>

```typescript
import type { Plan } from '../../core/entities/plan.entity';

export function approvePlan(plan: Plan): Plan {
  return { ...plan, status: 'approved' };
}

```

</details>


## extension/src/features/plan/plan-client.ts

*Size: 595 bytes | Modified: 2025-12-24T19:15:35.126Z*

<details>
<summary>View code</summary>

```typescript
interface GeneratePlanRequest {
  projectId: string;
  messages: any[];
}

export async function generatePlan(
  req: GeneratePlanRequest
): Promise<string> {
  const res = await fetch('http://localhost:8000/api/plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      project_id: req.projectId,
      model: 'qwen2.5-coder:7b-instruct-q4_K_M',
      messages: req.messages,
    }),
  });

  if (!res.ok) {
    throw new Error(`Plan API failed (${res.status})`);
  }

  const data = await res.json();
  return data.markdown as string;
}

```

</details>


## extension/src/features/plan/plan-controller.ts

*Size: 7,543 bytes | Modified: 2025-12-26T23:10:43.519Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { generatePlan } from './plan-client';
import { openPlanView } from './plan-view-controller';
import { isIndexed } from '../../infrastructure/http/api-client';
import { getActiveProjectId } from '../../core/project-context';
import { parsePlanMarkdown } from './plan-parser';
import { validatePlan } from './plan-validator';
import { approvePlan } from './plan-approval';
import { planState } from './plan-state';
import { planRegistry } from './plan-registry';

function genId(): string {
  const rnd = (globalThis as any).crypto?.randomUUID?.();
  return rnd || (Math.random().toString(36).slice(2) + Date.now().toString(36));
}

export async function createPlanFromChat(messages: any[]) {
  try {
    const projectId = getActiveProjectId();

    const indexed = await isIndexed(projectId);
    if (!indexed) {
      vscode.window.showWarningMessage(
        'Project must be indexed before creating a plan.'
      );
      return;
    }

    const markdown = await generatePlan({ projectId, messages });
    const id = genId();
    planRegistry.addPlan({
      id,
      title: 'New Plan',
      markdown,
      plan: null,
      status: 'draft',
      warnings: [],
      createdAt: Date.now(),
    });
    // await openPlanView(markdown);
    await vscode.commands.executeCommand('localpilot.plan.refresh');
    await openPlanView(markdown);
  } catch (err: any) {
    vscode.window.showErrorMessage(
      `Failed to generate plan: ${err?.message ?? err}`
    );
  }
}

export async function validateCurrentPlan() {
  const state = planState.get();
  if (!state.markdown) {
    vscode.window.showWarningMessage('No plan to validate.');
    return;
  }

  const result = parsePlanMarkdown(state.markdown);
  if (!result.plan) {
    vscode.window.showErrorMessage('Plan JSON is invalid or missing.');
    return;
  }

  const warnings = validatePlan(result.plan);
  planState.set({ plan: result.plan, warnings, status: 'draft' });

  vscode.window.showInformationMessage(
    warnings.length
      ? `Plan validated with ${warnings.length} warning(s).`
      : 'Plan validated successfully.'
  );
}

export async function approveCurrentPlan() {
  const state = planState.get();
  if (!state.plan) {
    vscode.window.showWarningMessage('Validate the plan before approval.');
    return;
  }

  const approved = approvePlan(state.plan);
  planState.set({ plan: approved, status: 'approved' });
  vscode.window.showInformationMessage('Plan approved.');
}

export async function discardCurrentPlan() {
  planState.clear();
  vscode.window.showInformationMessage('Plan discarded.');
  await openPlanView('');
}

export async function regeneratePlan(messages: any[]) {
  const state = planState.get();
  if (state.markdown) {
    const choice = await vscode.window.showWarningMessage(
      'Regenerating will replace the current plan.',
      { modal: true },
      'Regenerate'
    );
    if (choice !== 'Regenerate') return;
  }
  await createPlanFromChat(messages);
}


// ------------------------------
// Plan List helpers (read-only)
// ------------------------------
export function getAllPlans() {
  return planRegistry.getPlans();
}

export function selectPlan(planId: string, multi: boolean) {
  planRegistry.select(planId, multi);
}

export async function openPlan(planId: string) {
  const plan = planRegistry.getPlan(planId);
  if (!plan) return;
  await openPlanView(plan.markdown);
}

/* ---------------------------
   Per-plan actions (3.C-3)
---------------------------- */
export async function validatePlanById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;

  const parsed = parsePlanMarkdown(stored.markdown);
  if (!parsed.plan) {
    vscode.window.showErrorMessage('Invalid or missing plan JSON.');
    return;
  }

  const warnings = validatePlan(parsed.plan);
  planRegistry.update(planId, {
    plan: {
      ...parsed.plan,
      id: planId,
    },
    warnings,
    status: 'draft',
  });

  vscode.window.showInformationMessage(
    warnings.length
      ? `Plan validated with ${warnings.length} warning(s).`
      : 'Plan validated successfully.'
  );
  await vscode.commands.executeCommand('localpilot.plan.refresh');
}

export async function fixPlanJsonById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;

  const parsed = parsePlanMarkdown(stored.markdown);
  if (!parsed.plan) {
    vscode.window.showErrorMessage('Plan structure is invalid. Please regenerate the plan.');
    return;
  }

  const plan = parsed.plan;
  const warnings = validatePlan(plan);

  if (!warnings.length) {
    vscode.window.showInformationMessage('Plan JSON is already valid.');
    return;
  }

  // Auto-fix semantic issues in place
  for (const w of warnings) {
    if (w.code === 'missing_file_path') {
      const task = plan.tasks.find((t) => t.id === w.taskId);
      if (task) {
        const prev = plan.tasks.find((t) => t.orderIndex === task.orderIndex - 1);
        task.filePath = prev?.filePath || 'TODO_FILE_PATH';
      }
    }
    if (w.code === 'invalid_action_type') {
      const task = plan.tasks.find((t) => t.id === w.taskId);
      if (task) {
        task.actionType = 'modify';
      }
    }
  }

  // Re-run validation
  const afterFixWarnings = validatePlan(plan);

  planRegistry.update(planId, {
    plan: {
      ...plan,
      id: planId,
    },
    markdown: stored.markdown,
    warnings: afterFixWarnings,
    status: 'draft',
  });

  await vscode.commands.executeCommand('localpilot.plan.refresh');
  vscode.window.showInformationMessage(
    afterFixWarnings.length
      ? 'Plan partially fixed. Review remaining issues.'
      : 'Plan fixed successfully. You may now approve.'
  );
}

export async function approvePlanById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;

  // Auto-parse & validate
  const parsed = parsePlanMarkdown(stored.markdown);
  if (!parsed.plan) {
    vscode.window.showErrorMessage(
      'Cannot approve: plan JSON is invalid. Please fix and validate.'
    );
    return;
  }

  const warnings = validatePlan(parsed.plan);
  if (warnings.length) {
    vscode.window.showWarningMessage(
      'Cannot approve: plan has validation warnings.'
    );
    return;
  }

  const approved = {
    ...approvePlan(parsed.plan),
    id: planId,
  };

  planRegistry.update(planId, {
    plan: approved,
    status: 'approved',
    warnings: [],
  });

  await vscode.commands.executeCommand('localpilot.plan.refresh');
  vscode.window.showInformationMessage('Plan validated and approved.');
}

export async function discardPlanById(planId: string) {
  planRegistry.removePlan(planId);
  await vscode.commands.executeCommand('localpilot.plan.refresh');
  vscode.window.showInformationMessage('Plan discarded.');
}

export async function regeneratePlanById(planId: string, messages: any[]) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;

  const choice = await vscode.window.showWarningMessage(
    'Regenerating will create a new plan.',
    { modal: true },
    'Regenerate'
  );
  if (choice !== 'Regenerate') return;

  const projectId = getActiveProjectId();
  const markdown = await generatePlan({ projectId, messages });

  planRegistry.addPlan({
    id: genId(),
    title: stored.title + ' (regenerated)',
    markdown,
    plan: null,
    status: 'draft',
    warnings: [],
    createdAt: Date.now(),
  });

  await vscode.commands.executeCommand('localpilot.plan.refresh');
}

```

</details>


## extension/src/features/plan/plan-parser.ts

*Size: 2,465 bytes | Modified: 2025-12-24T19:15:35.128Z*

<details>
<summary>View code</summary>

````typescript
import type { Plan } from '../../core/entities/plan.entity';
import type { Task } from '../../core/entities/task.entity';
import type { PlanSchema, TaskSchema } from '../../core/schemas/plan.schema';

export interface ParseResult {
  markdown: string;
  plan: Plan | null;
}

export function parsePlanMarkdown(markdown: string): ParseResult {
  try {
    const json = extractJsonBlock(markdown || '');
    if (!json) return { markdown, plan: null };
    const data = JSON.parse(json) as PlanSchema;
    if (!isValidPlanSchema(data)) return { markdown, plan: null };
    const plan: Plan = {
      id: data.id,
      title: data.title,
      overview: data.overview,
      tasks: data.tasks.map(mapTask),
      status: 'draft',
    };
    return { markdown, plan };
  } catch {
    return { markdown, plan: null };
  }
}

function extractJsonBlock(markdown: string): string | null {
  // Prefer ```json fenced block explicitly
  const jsonFence = /```json\s*([\s\S]*?)```/i;
  const m = jsonFence.exec(markdown);
  if (m && m[1]) {
    return m[1].trim();
  }

  // Fallback: try to locate a raw JSON object
  const start = markdown.indexOf('{');
  const end = markdown.lastIndexOf('}');
  if (start !== -1 && end !== -1 && end > start) {
    const candidate = markdown.slice(start, end + 1).trim();
    if (candidate.startsWith('{')) return candidate;
  }

  return null;
}

function isValidPlanSchema(p: any): p is PlanSchema {
  return (
    p &&
    typeof p.id === 'string' &&
    typeof p.title === 'string' &&
    typeof p.overview === 'string' &&
    p.status === 'draft' &&
    Array.isArray(p.tasks) &&
    p.tasks.every(isValidTaskSchema)
  );
}

function isValidTaskSchema(t: any): t is TaskSchema {
  return (
    t &&
    typeof t.id === 'string' &&
    typeof t.orderIndex === 'number' &&
    typeof t.title === 'string' &&
    typeof t.description === 'string' &&
    typeof t.filePath === 'string' &&
    (t.actionType === 'create' || t.actionType === 'modify' || t.actionType === 'delete') &&
    Array.isArray(t.details) && t.details.every((d: any) => typeof d === 'string') &&
    Array.isArray(t.dependencies) && t.dependencies.every((d: any) => typeof d === 'string')
  );
}

function mapTask(t: TaskSchema): Task {
  return {
    id: t.id,
    orderIndex: t.orderIndex,
    title: t.title,
    description: t.description,
    filePath: t.filePath,
    actionType: t.actionType,
    details: t.details,
    dependencies: t.dependencies,
  };
}

````

</details>


## extension/src/features/plan/plan-registry.ts

*Size: 1,595 bytes | Modified: 2025-12-24T23:48:06.656Z*

<details>
<summary>View code</summary>

```typescript
import type { Plan } from '../../core/entities/plan.entity';
import type { ValidationWarning } from './plan-validator';

export interface StoredPlan {
  id: string;
  title: string;
  markdown: string;
  plan: Plan | null;
  status: 'draft' | 'approved' | 'acting';
  warnings: ValidationWarning[];
  createdAt: number;
}

interface PlanRegistryState {
  plans: StoredPlan[];
  selectedPlanIds: Set<string>;
}

class PlanRegistry {
  private state: PlanRegistryState = {
    plans: [],
    selectedPlanIds: new Set(),
  };

  getPlans(): StoredPlan[] {
    return [...this.state.plans];
  }

  getPlan(id: string): StoredPlan | undefined {
    return this.state.plans.find((p) => p.id === id);
  }

  addPlan(plan: StoredPlan) {
    this.state.plans.unshift(plan);
    this.state.selectedPlanIds.clear();
    this.state.selectedPlanIds.add(plan.id);
  }

  removePlan(id: string) {
    this.state.plans = this.state.plans.filter((p) => p.id !== id);
    this.state.selectedPlanIds.delete(id);
  }

  select(id: string, multi = false) {
    if (!multi) this.state.selectedPlanIds.clear();
    this.state.selectedPlanIds.add(id);
  }

  deselect(id: string) {
    this.state.selectedPlanIds.delete(id);
  }

  getSelected(): StoredPlan[] {
    return this.state.plans.filter((p) => this.state.selectedPlanIds.has(p.id));
  }

  update(id: string, patch: Partial<StoredPlan>) {
    const p = this.getPlan(id);
    if (!p) return;
    Object.assign(p, patch);
  }

  clear() {
    this.state.plans = [];
    this.state.selectedPlanIds.clear();
  }
}

export const planRegistry = new PlanRegistry();

```

</details>


## extension/src/features/plan/plan-state.ts

*Size: 715 bytes | Modified: 2025-12-24T19:15:35.130Z*

<details>
<summary>View code</summary>

```typescript
import type { Plan } from '../../core/entities/plan.entity';
import type { ValidationWarning } from './plan-validator';

export interface PlanState {
  markdown: string | null;
  plan: Plan | null;
  status: 'draft' | 'approved';
  warnings: ValidationWarning[];
}

class PlanStateStore {
  private state: PlanState = {
    markdown: null,
    plan: null,
    status: 'draft',
    warnings: [],
  };

  get(): PlanState {
    return this.state;
  }

  set(partial: Partial<PlanState>) {
    this.state = { ...this.state, ...partial };
  }

  clear() {
    this.state = {
      markdown: null,
      plan: null,
      status: 'draft',
      warnings: [],
    };
  }
}

export const planState = new PlanStateStore();

```

</details>


## extension/src/features/plan/plan-validator.ts

*Size: 2,251 bytes | Modified: 2025-12-26T22:47:40.915Z*

<details>
<summary>View code</summary>

```typescript
import type { Plan } from '../../core/entities/plan.entity';
import type { Task } from '../../core/entities/task.entity';

export interface ValidationWarning {
  code: string;
  message: string;
  path?: string;
  taskId?: string;
  suggestion?: string;
}

export function validatePlan(plan: Plan | null | undefined): ValidationWarning[] {
  const warnings: ValidationWarning[] = [];
  if (!plan) {
    warnings.push({ code: 'empty_plan', message: 'Plan is empty or could not be parsed.' });
    return warnings;
  }

  if (!Array.isArray(plan.tasks) || plan.tasks.length === 0) {
    warnings.push({ code: 'no_tasks', message: 'Plan has no tasks.' });
    return warnings;
  }

  plan.tasks.forEach((t: Task, idx: number) => {
    if (!t.filePath) {
      warnings.push({
        code: 'missing_file_path',
        message: `Task ${t.id} is missing filePath.`,
        path: `tasks[${idx}].filePath`,
        taskId: t.id,
        suggestion: 'Set filePath to the same file as the previous task.'
      });
    }
    const validActions = ['create', 'modify', 'delete'];
    if (!t.actionType) {
      warnings.push({
        code: 'missing_action_type',
        message: `Task ${t.id} is missing actionType.`,
        path: `tasks[${idx}].actionType`,
        taskId: t.id,
        suggestion: 'Set actionType to create | modify | delete based on intent.'
      });
    } else if (!validActions.includes(t.actionType as any)) {
      warnings.push({
        code: 'invalid_action_type',
        message: `Task ${t.id} has an invalid actionType: ${t.actionType}.`,
        path: `tasks[${idx}].actionType`,
        taskId: t.id,
        suggestion: 'Use a valid actionType, e.g. modify.'
      });
    }
  });

  const order = plan.tasks.map(t => t.orderIndex);
  const sorted = [...order].sort((a, b) => a - b);
  const same = order.every((v, i) => v === sorted[i]);
  if (!same) {
    warnings.push({ code: 'invalid_order', message: 'Task orderIndex values are not in ascending order.' });
  }

  const ids = new Set<string>();
  for (const t of plan.tasks) {
    if (ids.has(t.id)) {
      warnings.push({ code: 'duplicate_task_id', message: `Duplicate task id detected: ${t.id}` });
      break;
    }
    ids.add(t.id);
  }

  return warnings;
}

```

</details>


## extension/src/features/plan/plan-view-controller.ts

*Size: 1,698 bytes | Modified: 2025-12-24T19:15:35.131Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';

let panel: vscode.WebviewPanel | undefined;

export async function openPlanView(markdown: string) {
  if (panel) {
    panel.reveal();
    panel.webview.postMessage({ type: 'plan:update', markdown });
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
  const escaped = markdown.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <style>
          html, body, textarea { height: 100%; }
          body { margin: 0; padding: 0; }
          textarea { width: 100%; box-sizing: border-box; font-family: monospace; }
        </style>
      </head>
      <body>
        <textarea id="md">${escaped}</textarea>
        <script>
          const vscode = acquireVsCodeApi();
          window.addEventListener('message', (e) => {
            const msg = e.data;
            if (msg && msg.type === 'plan:update') {
              const el = document.getElementById('md');
              if (el) el.value = msg.markdown || '';
            }
          });
          function sendPlanContent() {
            const el = document.getElementById('md');
            const markdown = el && el.value ? el.value : '';
            vscode.postMessage({ type: 'plan:content', markdown });
          }
          window.addEventListener('beforeunload', sendPlanContent);
        </script>
      </body>
    </html>
  `;
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

*Size: 3,993 bytes | Modified: 2025-12-24T19:15:35.133Z*

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
      vscode.postMessage({ type: "index:done" });
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


## extension/src/prompts/system/plan.system.ts

*Size: 2,371 bytes | Modified: 2025-12-24T19:15:35.135Z*

<details>
<summary>View code</summary>

```typescript
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

</details>


## extension/src/views/act/act-view.ts

*Size: 4,346 bytes | Modified: 2025-12-26T19:51:37.049Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { actState } from '../../features/act/act-state';
import { ActService } from '../../features/act/act-service';
import { getActiveProjectId } from '../../core/project-context';

export class ActViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.act';
  private service = new ActService();

  resolveWebviewView(view: vscode.WebviewView) {
    view.webview.options = { enableScripts: true };
    view.webview.onDidReceiveMessage(async (msg) => {
      if (!msg || !msg.type) return;
      switch (msg.type) {
        case 'act:run': {
          this.service.run();
          try {
            await this.service.generateCurrentPreview('qwen2.5-coder:7b');
          } catch (e) {
            // silent for Phase 4.3
          }
          this.render(view);
          break;
        }
        case 'act:resume': {
          this.service.resume();
          this.render(view);
          break;
        }
        case 'act:apply': {
          const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
          if (!root) {
            vscode.window.showErrorMessage('No workspace folder is open.');
            return;
          }
          const projectId = getActiveProjectId();
          await this.service.applyCurrent(projectId, root);
          this.render(view);
          break;
        }
        case 'act:edit': {
          const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
          if (!root) {
            vscode.window.showErrorMessage('No workspace folder is open.');
            return;
          }
          await this.service.editCurrent(root);
          this.render(view);
          break;
        }
        case 'act:skip': {
          this.service.skipCurrent();
          this.render(view);
          break;
        }
      }
    });
    this.render(view);
  }

  private render(view: vscode.WebviewView) {
    const s = actState.get();

    if (!s) {
      view.webview.html = `
        <h3>Act Mode</h3><p>No active session.</p>
      `;
      return;
    }

    const controls =
      s.status === 'idle'
        ? `<button id="runAll">▶ Run All</button>`
        : s.status === 'paused'
        ? `<button id="resume">▶ Resume</button>`
        : `<button disabled>Generating…</button>`;

    const tasks = s.tasks
      .map((t, i) => {
        const marker =
          i === s.currentTaskIndex ? '➡️' :
          t.state === 'pending' ? '⬜' : '✅';
        return `<li>${marker} ${t.task.title}</li>`;
      })
      .join('');

    const current = s.tasks[s.currentTaskIndex];

    let review = '';
    if (current?.state === 'generated') {
      const body =
        current.preview?.kind === 'diff'
          ? `<pre>${current.preview.content}</pre>`
          : `<pre>${current.preview?.content ?? ''}</pre>`;

      review = `
        <h4>Review</h4>
        ${body}
        <button id="applyBtn">✓ Apply</button>
        <button id="editBtn">✏ Edit</button>
        <button id="skipBtn">⏭ Skip</button>
      `;
    }

    view.webview.html = `
      <h3>Act Mode</h3>
      <p><b>Plan:</b> ${s.planId}</p>
      <p>Status: ${s.status}</p>
      ${controls}
      <ul>${tasks}</ul>
      ${review}
      <p><small>Backups before writes; index sync after apply.</small></p>
      <script>
        const vscode = acquireVsCodeApi();
        const runAll = document.getElementById('runAll');
        if (runAll) runAll.addEventListener('click', () => {
          vscode.postMessage({ type: 'act:run' });
        });
        const resume = document.getElementById('resume');
        if (resume) resume.addEventListener('click', () => {
          vscode.postMessage({ type: 'act:resume' });
        });
        const applyBtn = document.getElementById('applyBtn');
        if (applyBtn) applyBtn.addEventListener('click', () => {
          vscode.postMessage({ type: 'act:apply' });
        });
        const editBtn = document.getElementById('editBtn');
        if (editBtn) editBtn.addEventListener('click', () => {
          vscode.postMessage({ type: 'act:edit' });
        });
        const skipBtn = document.getElementById('skipBtn');
        if (skipBtn) skipBtn.addEventListener('click', () => {
          vscode.postMessage({ type: 'act:skip' });
        });
      </script>
    `;
  }
}

```

</details>


## extension/src/views/chat/chat-view.ts

*Size: 4,713 bytes | Modified: 2025-12-24T19:15:35.137Z*

<details>
<summary>View code</summary>

```typescript
﻿import * as vscode from 'vscode';
import { initChat } from '../../webview/chat-controller';
import { getActiveProjectId } from '../../core/project-context';

export class ChatViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.chat';

  resolveWebviewView(view: vscode.WebviewView) {
    view.webview.options = { enableScripts: true };
    view.webview.html = getHtml();
    initChat(view, getActiveProjectId());
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
      vscode.postMessage({ type: "index:done" });
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

      if (msg.type === "hint") {
      const bar = document.createElement("div");
      bar.style.marginTop = "8px";
      bar.style.padding = "8px";
      bar.style.border = "1px solid #555";
      bar.style.background = "#252525";
      bar.style.display = "flex";
      bar.style.justifyContent = "space-between";
      bar.style.alignItems = "center";
      const span = document.createElement("span");
      span.textContent = msg.message || "";
      const btn = document.createElement("button");
      btn.textContent = (msg.action && msg.action.label) || "Open Plan Tab";
      btn.onclick = () => {
        vscode.postMessage({ type: "open:planTab" });
        bar.remove();
      };
      bar.appendChild(span);
      bar.appendChild(btn);
      document.body.appendChild(bar);
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


## extension/src/views/plan/plan-view.ts

*Size: 6,509 bytes | Modified: 2025-12-26T22:49:50.511Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';

export class PlanViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.plan';
  private view?: vscode.WebviewView;

  resolveWebviewView(view: vscode.WebviewView) {
    this.view = view;
    view.webview.options = { enableScripts: true };
    view.webview.html = render([]);

    view.webview.onDidReceiveMessage((msg) => {
      if (!msg || !msg.type) return;

      switch (msg.type) {
        case 'plan:select':
          vscode.commands.executeCommand(
            'localpilot.plan.select',
            msg.planId,
            msg.multi
          );
          break;
        case 'plan:open':
          vscode.commands.executeCommand(
            'localpilot.plan.open',
            msg.planId
          );
          break;
        case 'plan:validateById':
          vscode.commands.executeCommand(
            'localpilot.plan.validateById',
            msg.planId
          );
          break;
        case 'plan:approveById':
          vscode.commands.executeCommand(
            'localpilot.plan.approveById',
            msg.planId
          );
          break;
        case 'plan:regenerateById':
          vscode.commands.executeCommand(
            'localpilot.plan.regenerateById',
            msg.planId
          );
          break;
        case 'plan:discardById':
          vscode.commands.executeCommand(
            'localpilot.plan.discardById',
            msg.planId
          );
          break;
        case 'plan:act':
          vscode.commands.executeCommand(
            'localpilot.act.start',
            msg.planId
          );
          break;
        case 'plan:fixJsonById':
          vscode.commands.executeCommand(
            'localpilot.plan.fixJsonById',
            msg.planId
          );
          break;
      }
    });

    // Initial render
    vscode.commands.executeCommand('localpilot.plan.refresh');
  }

  /** called by controller via command to update list */
  update(plans: any[]) {
    if (!this.view) return;
    this.view.webview.html = render(plans);
  }
}

function render(plans: any[]): string {
  function readiness(p: any): string {
    if (p.status === 'acting') return '⚙ ACTING';
    if (p.status === 'approved' && p.plan) return '✅ READY';
    if (p.status === 'approved') return '⚠ NEEDS VALIDATION';
    return '✏ DRAFT';
  }
  function renderJsonError(p: any): string {
    if (!p.warnings || !p.warnings.length) return '';
    return `
    <div class="json-error">
      ⚠ Plan issues detected:
      <ul>
        ${p.warnings
          .map(
            (w: any) => `
          <li>
            <b>Task ${w.taskId ?? '?'}</b>: ${w.message}
            ${w.suggestion ? `<em>→ ${w.suggestion}</em>` : ''}
          </li>`
          )
          .join('')}
      </ul>
    </div>`;
  }
  const rows = plans
    .map(
      (p) => `
    <div class="plan-row">
      <input type="checkbox" data-id="${p.id}" />
      <span class="title">${p.title}</span>
      <span class="status ${p.status}">${readiness(p)} </span>
      <div class="actions">
        <button data-open="${p.id}" title="Open">🔍</button>
        <button data-validate="${p.id}" title="Validate">✔</button>
        <button data-approve="${p.id}" title="Approve">🔐</button>
        <button data-regenerate="${p.id}" title="Regenerate">🔄</button>
        <button data-discard="${p.id}" title="Discard">🗑</button>
        ${p.status === 'approved' && p.plan && (!p.warnings || !p.warnings.length)
          ? `<button data-act="${p.id}" title="Act">⚙</button>`
          : `<button disabled title="Fix plan before acting">⚙</button>`}
        ${p.warnings && p.warnings.length ? `<button data-fix="${p.id}" title="Fix JSON">🛠</button>` : ''}
      </div>
    </div>
    ${renderJsonError(p)}
  `
    )
    .join('');

  return `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { background: #1e1e1e; color: #d4d4d4; font-family: sans-serif; padding: 8px; }
    .plan-row { display: grid; grid-template-columns: auto 1fr auto auto; gap: 6px; align-items: center; padding: 4px; border-bottom: 1px solid #333; }
    .plan-row:hover { background: #252525; }
    .title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .status { font-size: 11px; }
    .status.draft { color: #facc15; }
    .status.approved { color: #4ade80; }
    .status.acting { color: #60a5fa; }
    .json-error { color: #f87171; font-size: 11px; margin-left: 22px; }
    .actions { display: flex; gap: 6px; }
    button { background: none; border: none; cursor: pointer; color: #d4d4d4; }
    button:hover { color: white; }
  </style>
</head>
<body>
<h3>Plans</h3>
<div id="list">
  ${rows || '<em>No plans yet</em>'}
</div>
<script>
  const vscode = acquireVsCodeApi();
  document.querySelectorAll('input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', (e) => {
      vscode.postMessage({
        type: 'plan:select',
        planId: e.target.dataset.id,
        multi: e.ctrlKey || e.metaKey
      });
    });
  });
  document.querySelectorAll('button[data-open]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:open', planId: btn.dataset.open });
    });
  });

  document.querySelectorAll('[data-validate]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:validateById', planId: btn.dataset.validate });
    });
  });

  document.querySelectorAll('[data-approve]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:approveById', planId: btn.dataset.approve });
    });
  });

  document.querySelectorAll('[data-regenerate]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:regenerateById', planId: btn.dataset.regenerate });
    });
  });

  document.querySelectorAll('[data-discard]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:discardById', planId: btn.dataset.discard });
    });
  });

  document.querySelectorAll('[data-act]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:act', planId: btn.dataset.act });
    });
  });

  document.querySelectorAll('[data-fix]').forEach(btn => {
    btn.addEventListener('click', () => {
      vscode.postMessage({ type: 'plan:fixJsonById', planId: btn.dataset.fix });
    });
  });
</script>
</body>
</html>
`;
}

```

</details>


## extension/src/webview/chat-controller.ts

*Size: 2,709 bytes | Modified: 2025-12-24T19:15:35.140Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from "vscode";
import { ChatService } from "../features/chat/chat-service";
import { ChatSessionStore } from "../features/chat/chat-session.store";
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
    // CHAT → PLAN: open Plan tab
    // ------------------------
    if (msg.type === "open:planTab") {
      await vscode.commands.executeCommand("workbench.view.extension.localpilot");
      return;
    }

    if (msg.type === "index:done") {
      ChatSessionStore.clear();
      return;
    }

    // ------------------------
    // CHAT ONLY
    // ------------------------
    if (msg.type === "chat:send") {
      // Planning intent hint (non-blocking)
      const text: string = msg.payload?.message || "";
      const planningIntent = /(\bplan\b|planning|implementation plan|create plan|propose plan|migration plan|write a plan)/i;
      if (planningIntent.test(text)) {
        panel.webview.postMessage({
          type: "hint",
          message: "Planning is available in the Plan tab.",
          action: { label: "Open Plan Tab" }
        });
        vscode.window
          .showInformationMessage(
            "Planning is available in the Plan tab.",
            "Open Plan Tab"
          )
          .then(async (choice) => {
            if (choice === "Open Plan Tab") {
              await vscode.commands.executeCommand(
                "workbench.view.extension.localpilot"
              );
            }
          });
      }

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

*Size: 788 bytes | Modified: 2025-12-24T19:15:35.143Z*

<details>
<summary>View code</summary>

```typescript
import { describe, it, expect, vi } from 'vitest';

vi.mock('vscode', () => {
  return {
    window: {
      registerWebviewViewProvider: vi.fn(() => ({ dispose: vi.fn() })),
      showInformationMessage: vi.fn(),
    },
    commands: {
      registerCommand: vi.fn(() => ({ dispose: vi.fn() })),
    },
    workspace: {
      onDidChangeWorkspaceFolders: vi.fn(() => ({ dispose: vi.fn() })),
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


## server/api/plan.py

*Size: 811 bytes | Modified: 2025-12-24T19:15:35.144Z*

<details>
<summary>View code</summary>

```python
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from server.api.dependencies import get_index_root
from server.plan.plan_service import PlanService
from server.plan.plan_parser import PlanParser


router = APIRouter()


class PlanRequest(BaseModel):
    project_id: str
    model: str
    messages: List[Dict[str, str]]


@router.post("/plan")
def generate_plan(request: PlanRequest, index_root: Path = Depends(get_index_root)) -> Dict[str, Any]:
    service = PlanService(index_root=index_root, project_id=request.project_id, model=request.model)
    markdown = service.generate(chat_messages=request.messages)
    parser = PlanParser()
    result = parser.parse(markdown)
    return result

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

*Size: 1,464 bytes | Modified: 2025-12-24T19:15:35.146Z*

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

    def chat(self, messages: Iterable[Dict]) -> str:
        """
        Perform a non-streaming chat request and return the full message content.
        """
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": list(messages),
                "stream": False,
            },
            timeout=300,
        )
        response.raise_for_status()
        data = response.json()
        return (data.get("message") or {}).get("content", "")

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

*Size: 1,683 bytes | Modified: 2025-12-24T19:15:35.147Z*

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
from server.api import plan as plan_api


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
app.include_router(plan_api.router, prefix="/api")

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


## server/plan/__init__.py

*Size: 23 bytes | Modified: 2025-12-24T19:15:35.149Z*

<details>
<summary>View code</summary>

```python
# Phase 3 Plan package

```

</details>


## server/plan/plan_parser.py

*Size: 1,514 bytes | Modified: 2025-12-24T19:15:35.150Z*

<details>
<summary>View code</summary>

````python
from __future__ import annotations
import json
import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Literal


class TaskSchema(BaseModel):
    id: str
    orderIndex: int
    title: str
    description: str
    filePath: str
    actionType: Literal["create", "modify", "delete"]
    details: List[str]
    dependencies: List[str]

    class Config:
        extra = "forbid"


class PlanSchema(BaseModel):
    id: str
    title: str
    overview: str
    status: Literal["draft"]
    tasks: List[TaskSchema]

    class Config:
        extra = "forbid"


class PlanParser:
    def _extract_json(self, markdown: str) -> Optional[str]:
        fence = re.compile(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", re.IGNORECASE)
        m = fence.search(markdown)
        if m:
            return m.group(1)
        start = markdown.find("{")
        end = markdown.rfind("}")
        if start != -1 and end != -1 and end > start:
            return markdown[start : end + 1]
        return None

    def parse(self, markdown: str) -> Dict[str, Any]:
        raw = self._extract_json(markdown or "")
        if raw is None:
            return {"markdown": markdown, "plan": None}
        try:
            data = json.loads(raw)
            plan = PlanSchema(**data)
            return {"markdown": markdown, "plan": plan.dict()}
        except (json.JSONDecodeError, ValidationError):
            return {"markdown": markdown, "plan": None}

````

</details>


## server/plan/plan_service.py

*Size: 5,456 bytes | Modified: 2025-12-26T21:23:16.303Z*

<details>
<summary>View code</summary>

````python
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
import json

from server.chat.ollama_chat_client import OllamaChatClient

PLAN_MODE_SYSTEM = (
    "You are operating in PLAN MODE.\n\n"

    "Your job is to produce a VALID IMPLEMENTATION PLAN.\n"
    "You MUST output ONE and ONLY ONE valid JSON object matching the schema below.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "CRITICAL RULES (NON-NEGOTIABLE)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "1. Output MUST contain EXACTLY ONE JSON object.\n"
    "2. JSON MUST be syntactically valid.\n"
    "3. ALL fields are REQUIRED.\n"
    "4. NO extra fields are allowed.\n"
    "5. Arrays MUST ALWAYS be arrays, even with one item.\n"
    "6. NEVER output a string where an array is required.\n"
    "7. NEVER omit required fields.\n"
    "8. status MUST be \"draft\".\n"
    "9. orderIndex MUST start at 0 and be sequential.\n"
    "10. tasks MUST NOT be empty.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "STRICT JSON SCHEMA (MANDATORY)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "{\n"
    "  \"id\": \"string\",\n"
    "  \"title\": \"string\",\n"
    "  \"overview\": \"string\",\n"
    "  \"status\": \"draft\",\n"
    "  \"tasks\": [\n"
    "    {\n"
    "      \"id\": \"string\",\n"
    "      \"orderIndex\": number,\n"
    "      \"title\": \"string\",\n"
    "      \"description\": \"string\",\n"
    "      \"filePath\": \"string\",\n"
    "      \"actionType\": \"create | modify | delete\",\n"
    "      \"details\": [\"string\"],\n"
    "      \"dependencies\": [\"string\"]\n"
    "    }\n"
    "  ]\n"
    "}\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "SELF-CHECK REQUIREMENT\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "Before responding:\n"
    "- Validate your JSON against the schema.\n"
    "- If ANY field is missing or invalid, FIX IT before output.\n"
    "- Do NOT explain. Do NOT apologize.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "OUTPUT FORMAT\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "1. Short Markdown summary.\n"
    "2. ONE fenced ```json block containing ONLY the JSON.\n"
)


class PlanService:
    def __init__(self, index_root: Path, project_id: str, model: str, base_url: str = "http://127.0.0.1:11434"):
        self.index_root = index_root
        self.project_id = project_id
        self.model = model
        self.base_url = base_url.rstrip("/")

    def _extract_planning_intent(
        self, messages: List[Dict[str, str]]
    ) -> str:
        """
        Extract the most recent USER intent for planning.
        Assistant messages are intentionally ignored to
        avoid Chat-mode refusals poisoning Plan Mode.
        """
        for m in reversed(messages or []):
            if m.get("role") == "user" and m.get("content"):
                return m["content"]
        return ""

    def _read_json(self, path: Path) -> Any:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _build_messages(self, chat_messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        project_dir = self.index_root / self.project_id
        summary = self._read_json(project_dir / "summary.json") or {}
        symbols = self._read_json(project_dir / "symbols.json") or []

        preface = (
            "Project Summary:\n" + json.dumps(summary, indent=2) +
            "\n\nIndexed Symbols:\n" + json.dumps(symbols, indent=2)
        )

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": PLAN_MODE_SYSTEM},
            {"role": "user", "content": preface},
        ]
        # IMPORTANT:
        # Only pass the latest USER planning intent into Plan Mode.
        # Do NOT include assistant messages or full chat history.
        intent = self._extract_planning_intent(chat_messages)
        if intent:
            messages.append({"role": "user", "content": intent})
        return messages

    def generate(self, chat_messages: List[Dict[str, str]]) -> str:
        client = OllamaChatClient(base_url=self.base_url, model=self.model)
        messages = self._build_messages(chat_messages)

        output = ""
        for attempt in range(2):  # one retry max
            output = client.chat(messages)

            # Validate JSON via parser
            from server.plan.plan_parser import PlanParser
            parser = PlanParser()
            parsed = parser.parse(output)

            if parsed.get("plan"):
                return output

            # Self-repair instruction for the model
            messages.append({
                "role": "system",
                "content": (
                    "The previous JSON was INVALID.\n"
                    "Fix ALL schema violations and output VALID JSON ONLY."
                )
            })

        return output  # last attempt (will fail validation visibly)

````

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


## tools/export-to-md.mjs

*Size: 14,591 bytes | Modified: 2025-12-07T18:23:00.571Z*

<details>
<summary>View code</summary>

````javascript
#!/usr/bin/env node
import fs from 'node:fs/promises';
import { createWriteStream } from 'node:fs';
import path from 'node:path';
// Optional dependency handling
let ignoreModule = null;
try {
  // Dynamic import for the ignore package
  ignoreModule = await import('ignore').then(m => m.default);
} catch (error) {
  console.warn('Warning: "ignore" package not installed. .gitignore support disabled.');
}

// --- Default Configuration (and other functions like parseArgs, walk, langForExt, etc.) ---
const DEFAULT_ROOTS = ['.'];
const DEFAULT_EXCLUDE_DIRS = new Set([
  '.git', 'node_modules', 'dist', 'build', 'out', 'target', 'vendor',
  '.idea', '.vscode', '.DS_Store', 'coverage', '.cache', 'bin', 'obj',
  '.venv', '__pycache__', '.tox',
  'Pods', 'DerivedData', '.swiftpm', 'Carthage',
  '.gradle',
  'Library', 'Temp', 'Logs', 'Packages',
  'Intermediate', 'Saved',
]);
const DEFAULT_ALLOW_EXTS = new Set([
  '.ts', '.tsx', '.js', '.jsx', '.json', '.mjs', '.cjs', '.html', '.css', '.scss', '.less',
  '.yml', '.yaml', '.toml', '.ini', '.env', '.config',
  '.md', '.mdx', '.txt','csv','.json',
  '.sh', '.bash', '.ps1', 'Dockerfile',
  '.c', '.cpp', '.h', '.hpp',
  '.py', '.go', '.rs', '.rb', '.php', '.sql',
  '.cs', '.gd', '.lua', '.glsl', '.hlsl', '.metal', '.shader', '.tscn', '.tres',
  '.swift', '.m', '.storyboard', '.xib', '.plist', 'Podfile',
  '.kt', '.kts', '.java', '.xml', '.gradle', '.gradle.kts',
  '.dart', '.xaml',
]);
const DEFAULT_EXCLUDE_FILE_BASENAMES = new Set([
  'package-lock.json', 'pnpm-lock.yaml', 'yarn.lock', 'Podfile.lock', 'Cargo.lock',
  'composer.lock', 'Gemfile.lock' , 'reviewer.md'
]);
const langForExt = (ext) => ({
  '.ts': 'typescript', '.tsx': 'tsx', '.js': 'javascript', '.jsx': 'jsx', '.mjs': 'javascript', '.cjs': 'javascript',
  '.json': 'json', '.yml': 'yaml', '.yaml': 'yaml', '.toml':'toml', '.ini':'ini',
  '.md': 'markdown', '.mdx': 'mdx', '.txt': 'text',
  '.sh': 'bash', '.bash': 'bash', '.ps1': 'powershell', 'Dockerfile':'dockerfile',
  '.py': 'python', '.go': 'go', '.rs': 'rust',
  '.java': 'java', '.kt': 'kotlin', '.kts': 'kotlin', '.scala': 'scala', '.gradle': 'groovy', '.gradle.kts': 'kotlin',
  '.cs': 'csharp', '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp',
  '.rb': 'ruby', 'Podfile': 'ruby', '.php': 'php', '.sql': 'sql',
  '.html': 'html', '.css': 'css', '.scss': 'scss', '.less': 'less',
  '.gd': 'gdscript', '.lua': 'lua', '.glsl': 'glsl', '.hlsl': 'hlsl', '.metal': 'c++', '.shader': 'csharp', '.tscn': 'ini', '.tres': 'ini',
  '.swift': 'swift', '.m': 'objectivec',
  '.xml': 'xml', '.storyboard': 'xml', '.xib': 'xml', '.plist': 'xml', '.xaml': 'xml',
  '.dart': 'dart',
}[ext] || '');

function parseArgs(argv) {
  const config = {
    roots: [], out: '', maxBytes: 524288, help: false,
    excludeDirs: new Set(DEFAULT_EXCLUDE_DIRS),
    useGitignore: true,
    allowExts: new Set(DEFAULT_ALLOW_EXTS),
    excludeFiles: new Set(DEFAULT_EXCLUDE_FILE_BASENAMES),
  };
  const parseList = (arg, prefix) => arg.slice(prefix.length).split(',').filter(Boolean);
  for (const arg of argv) {
    if (arg === '-h' || arg === '--help') { config.help = true; continue; }
    if (arg.startsWith('--out=')) { config.out = arg.slice('--out='.length); continue; }
    if (arg === '--no-gitignore') { config.useGitignore = false; continue; }
    if (arg.startsWith('--max-bytes=')) {
      const n = Number(arg.slice('--max-bytes='.length));
      if (Number.isFinite(n) && n >= 0) config.maxBytes = Math.trunc(n);
      continue;
    }
    if (arg.startsWith('--exclude-dir=')) { parseList(arg, '--exclude-dir=').forEach(d => config.excludeDirs.add(d)); continue; }
    if (arg.startsWith('--include-ext=')) {
      if (config.allowExts === DEFAULT_ALLOW_EXTS) config.allowExts = new Set();
      parseList(arg, '--include-ext=').forEach(e => config.allowExts.add(e.startsWith('.') ? e : `.${e}`));
      continue;
    }
    if (arg.startsWith('--exclude-file=')) { parseList(arg, '--exclude-file=').forEach(f => config.excludeFiles.add(f)); continue; }
    if (!arg.startsWith('--')) { config.roots.push(arg); }
  }
  if (config.roots.length === 0) { config.roots = DEFAULT_ROOTS; }
  return config;
}

/**
 * Load and parse .gitignore file for a given directory
 * @param {string} rootDir - The directory containing the .gitignore file
 * @returns {object|null} An ignore instance that can be used to test paths, or null if not available
 */
async function loadGitignore(rootDir) {
  if (!ignoreModule) return null;
  
  const ig = ignoreModule();
  try {
    const content = await fs.readFile(path.join(rootDir, '.gitignore'), 'utf8');
    ig.add(content);
  } catch {
    // No .gitignore found or couldn't read it
  }
  return ig;
}

async function walk(dir, allowExts, excludeDirs, gitignore = null, rootDir = '', files = []) {
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const absPath = path.join(dir, entry.name);
      const relPath = rootDir ? path.relative(rootDir, absPath) : absPath;
      
      // Check gitignore if available
      if (gitignore && gitignore.ignores(relPath.split(path.sep).join('/'))) {
        continue;
      }
      
      if (entry.isDirectory()) {
        if (!excludeDirs.has(entry.name)) {
          await walk(absPath, allowExts, excludeDirs, gitignore, rootDir, files);
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name);
        if (allowExts.has(ext) || allowExts.has(entry.name)) {
          files.push(absPath);
        }
      }
    }
  } catch (error) {
    console.warn(`Warning: Could not read directory "${dir}": ${error.message}`);
  }
  return files;
}

async function isTextFile(filePath) {
  try {
    const fd = await fs.open(filePath, 'r');
    const buffer = Buffer.alloc(4096);
    const { bytesRead } = await fd.read(buffer, 0, 4096, 0);
    await fd.close();
    
    // Check for NULL bytes which indicate binary content
    for (let i = 0; i < bytesRead; i++) {
      if (buffer[i] === 0) return false;
    }
    return true;
  } catch {
    return false;
  }
}

/**
 * Generates a table of contents for easier navigation
 * @param {Array} fileEntries - Array of file entry objects
 * @returns {string} Markdown formatted table of contents
 */
function generateTableOfContents(fileEntries) {
  let toc = "## Table of Contents\n\n";
  fileEntries.forEach(({ rel }) => {
    // Create markdown heading link using the file path
    const linkText = rel.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();
    toc += `- [${rel}](#${linkText})\n`;
  });
  return toc + "\n\n---\n\n";
}

/**
 * Generates a visually appealing and informative text-based tree structure.
 * - Directories are marked with a trailing '/'
 * - Entries are sorted with directories first, then files, all alphabetically.
 * - Provides a header with the root name and total file count.
 * @param {string[]} files - An array of relative file paths (using '/' as separator).
 * @param {string} rootDisplayName - The name to display for the root of the tree.
 * @returns {string} The formatted tree string.
 */
function generateTree(files, rootDisplayName = '.') {
    const tree = {};

    for (const file of files) {
        // *** THE FIX IS HERE: Using '/' explicitly ***
        const parts = file.split('/'); 
        let currentLevel = tree;
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            const isLast = i === parts.length - 1;

            if (!currentLevel[part]) {
                currentLevel[part] = {
                    type: isLast ? 'file' : 'directory',
                    children: isLast ? null : {},
                };
            }
            currentLevel = currentLevel[part].children;
        }
    }

    const buildTreeString = (node, prefix = '') => {
        let result = '';
        const entries = Object.entries(node).sort(([aName, aNode], [bName, bNode]) => {
            if (aNode.type === bNode.type) {
                return aName.localeCompare(bName);
            }
            return aNode.type === 'directory' ? -1 : 1;
        });

        entries.forEach(([name, childNode], index) => {
            const isLast = index === entries.length - 1;
            const connector = isLast ? '└── ' : '├── ';
            const displayName = childNode.type === 'directory' ? `${name}/` : name;
            
            result += `${prefix}${connector}${displayName}\n`;

            if (childNode.children) {
                const childPrefix = prefix + (isLast ? '    ' : '│   ');
                result += buildTreeString(childNode.children, childPrefix);
            }
        });
        return result;
    };

    const fileCount = files.length === 1 ? '1 file' : `${files.length} files`;
    const header = `${rootDisplayName} (${fileCount})\n`;
    return header + buildTreeString(tree);
}

async function main() {
  const config = parseArgs(process.argv.slice(2));

  if (config.help) {
    console.log(`
Usage: export-to-mdnew.mjs [options] [directories...]

Options:
  --out=FILE               Output file path (default: docs/code-snapshot.md)
  --max-bytes=N            Skip files larger than N bytes (default: 524288)
  --exclude-dir=A,B,C      Exclude directories (comma-separated)
  --include-ext=.a,.b,.c   Include only files with these extensions
  --exclude-file=A,B,C     Exclude files by name (comma-separated)
  --no-gitignore           Don't respect .gitignore files
  -h, --help               Show this help message
`);
    return;
  }

  const roots = config.roots.map((p) => path.resolve(p));
  const allFiles = [];
  
  // Load gitignore for each root if enabled and module is available
  const gitignores = {};
  if (config.useGitignore && ignoreModule) {
    for (const root of roots) {
      gitignores[root] = await loadGitignore(root);
    }
  } else if (config.useGitignore) {
    console.warn('Warning: .gitignore support is disabled because the "ignore" package is not installed.');
  }
  
  for (const r of roots) {
    const stat = await fs.stat(r).catch(() => null);
    if (stat?.isDirectory()) {
      const gitignore = config.useGitignore ? gitignores[r] : null;
      await walk(r, config.allowExts, config.excludeDirs, gitignore, r, allFiles);
    }
  }

  const filePairs = allFiles.map((abs) => {
    // This part correctly normalizes paths to use '/'
    const rel = path.relative(process.cwd(), abs).split(path.sep).join('/');
    return { abs, rel };
  }).sort((a, b) => a.rel.localeCompare(b.rel));
  
  const rootDisplayNames = roots.map(r => path.relative(process.cwd(), r) || '.').join(', ');
  const tree = generateTree(filePairs.map(p => p.rel), rootDisplayNames);
  
  const header = `# Code Snapshot

**Generated:** ${new Date().toISOString()}
**Roots:** ${rootDisplayNames}
**Max file size:** ${config.maxBytes === 0 ? 'unlimited' : config.maxBytes.toLocaleString() + ' bytes'}

## Project Structure

\`\`\`
${tree}
\`\`\`

---
`;
  
  const fenceFor = (content) => content.includes('```') ? '````' : '```';
  
  let skippedLarge = 0;
  let skippedNamed = 0;
  let skippedBinary = 0;
  let included = 0;
  const fileEntries = [];
  
  // Add progress indicator
  const totalFiles = filePairs.length;
  console.log(`Processing ${totalFiles} files...`);
  let processedCount = 0;
  
  for (const { abs, rel } of filePairs) {
    // Update progress
    processedCount++;
    if (processedCount % 10 === 0 || processedCount === totalFiles) {
      process.stdout.write(`\rProcessing: ${processedCount}/${totalFiles} (${Math.round(processedCount/totalFiles*100)}%)`);
    }
   
    const base = path.basename(abs);
   
    if (config.excludeFiles.has(base)) { 
      skippedNamed++; 
      continue; 
    }
   
    // Check if it's a binary file
    if (!(await isTextFile(abs))) {
      skippedBinary++;
      continue;
    }
   
    if (config.maxBytes > 0) {
      try {
        const stats = await fs.stat(abs);
        if (stats.size > config.maxBytes) {
          skippedLarge++;
          continue;
        }
      } catch {
        continue;
      }
    }
    
    try {
      const content = await fs.readFile(abs, 'utf8');
      included++;
      const lang = langForExt(path.extname(abs) || path.basename(abs));
      const fence = fenceFor(content);
      const stats = await fs.stat(abs);
      fileEntries.push({ 
        rel, 
        lang, 
        fence, 
        content,
        size: stats.size,
        modified: stats.mtime.toISOString()
      });
    } catch {
      // Skip files we can't read
    }
  }

  console.log('\nGenerating markdown output...');
  const target = path.resolve(config.out || 'docs/code-snapshot.md');
  await fs.mkdir(path.dirname(target), { recursive: true });
  
  // Use stream for better performance with large files
  const writeStream = createWriteStream(target);
  writeStream.write(header);
  
  // Add table of contents
  writeStream.write(generateTableOfContents(fileEntries));
  
  for (const { rel, lang, fence, content, size, modified } of fileEntries) {
    // Write the file section with collapsible details tag
    writeStream.write(`## ${rel}\n\n`);
    writeStream.write(`*Size: ${size.toLocaleString()} bytes | Modified: ${modified}*\n\n`);
    writeStream.write(`<details>\n<summary>View code</summary>\n\n`);
    writeStream.write(`${fence}${lang}\n${content}\n${fence}\n\n`);
    writeStream.write(`</details>\n\n\n`);
  }
  
  // Close the stream
  writeStream.end();
  
  // Wait for the write to complete
  await new Promise((resolve) => writeStream.on('finish', resolve));
  
  const summaryParts = [`${included} files included`]; 
  if (skippedLarge > 0) summaryParts.push(`${skippedLarge} skipped (> ${config.maxBytes.toLocaleString()} bytes)`);
  if (skippedNamed > 0) summaryParts.push(`${skippedNamed} skipped by name`);
  if (skippedBinary > 0) summaryParts.push(`${skippedBinary} skipped (binary files)`);

  console.log(`Wrote to ${target} (${summaryParts.join(', ')})`);
}

// This is the entry point of the script
(async function() {
  try {
    await main();
  } catch (e) {
    console.error('An unexpected error occurred:', e);
    process.exit(1);
  }
})();
````

</details>


