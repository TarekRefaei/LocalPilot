## Project Structure

```
. (180 files)
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
│   │   ├── phase5/
│   │   │   └── phase5patch.md
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
│   │   │   │   ├── act-apply.ts
│   │   │   │   ├── act-controller.ts
│   │   │   │   ├── act-events.ts
│   │   │   │   ├── act-executor.ts
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
│   │   │   ├── execute_v2/
│   │   │   │   ├── execute-client.ts
│   │   │   │   ├── execute-controller.ts
│   │   │   │   ├── execute-state.ts
│   │   │   │   └── execute-types.ts
│   │   │   ├── ollama/
│   │   │   │   └── connection-manager.ts
│   │   │   └── plan/
│   │   │       ├── plan-approval.ts
│   │   │       ├── plan-client.ts
│   │   │       ├── plan-controller.ts
│   │   │       ├── plan-diff.d.ts
│   │   │       ├── plan-diff.ts
│   │   │       ├── plan-normalizer.ts
│   │   │       ├── plan-parser.ts
│   │   │       ├── plan-registry.ts
│   │   │       ├── plan-state.ts
│   │   │       ├── plan-validator.ts
│   │   │       └── plan-view-controller.ts
│   │   ├── infrastructure/
│   │   │   └── http/
│   │   │       └── api-client.ts
│   │   ├── ollama/
│   │   │   └── ollama-chat-client.ts
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
│   │   │   ├── execute/
│   │   │   │   └── execute-view.ts
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
│   ├── act_v2/
│   │   ├── apply/
│   │   │   ├── __init__.py
│   │   │   ├── apply_errors.py
│   │   │   ├── patch_applier.py
│   │   │   └── workspace_guard.py
│   │   ├── compiler/
│   │   │   ├── __init__.py
│   │   │   ├── plan_compiler.py
│   │   │   └── task_graph.py
│   │   ├── context/
│   │   │   ├── __init__.py
│   │   │   ├── task_context_builder.py
│   │   │   └── workspace_reader.py
│   │   ├── ledger/
│   │   │   ├── __init__.py
│   │   │   ├── execution_ledger.py
│   │   │   └── models.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── confined_prompt.py
│   │   │   ├── invocation_service.py
│   │   │   ├── llm_client_stub.py
│   │   │   └── ollama_client.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── execution_state.py
│   │   │   └── execution_task.py
│   │   ├── validation/
│   │   │   ├── __init__.py
│   │   │   ├── diff_parser.py
│   │   │   ├── diff_validator.py
│   │   │   └── validation_errors.py
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── apply_engine.py
│   │   ├── diff_validator.py
│   │   ├── errors.py
│   │   └── index_hook.py
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
│   │   ├── auto_fix/
│   │   │   ├── __init__.py
│   │   │   └── plan_auto_fixer.py
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

*Size: 4,035 bytes | Modified: 2025-12-28T18:51:15.237Z*

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
                },
                {
                    "name": "Execute",
                    "id": "localpilot.execute",
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
            },
            {
                "command": "localpilot.execute.start",
                "title": "LocalPilot: Start Execution (v2)"
            },
            {
                "command": "localpilot.execute.apply",
                "title": "LocalPilot: Apply Approved Diff"
            },
            {
                "command": "localpilot.execute.refresh",
                "title": "LocalPilot: Refresh Execute View"
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
                    "when": "false",
                    "group": "navigation@3"
                },
                {
                    "command": "localpilot.execute.start",
                    "when": "view == localpilot.plan",
                    "group": "navigation@4"
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

*Size: 4,452 bytes | Modified: 2025-12-29T18:53:18.853Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { registerPlanCommands } from './commands/plan.commands';
import { ChatSessionStore } from './features/chat/chat-session.store';
import { ChatViewProvider } from './views/chat/chat-view';
import { PlanViewProvider } from './views/plan/plan-view';
import { ActViewProvider } from './views/act/act-view';
import { ExecuteViewProvider } from './views/execute/execute-view';
import { startPlanExecution, approveAndApply } from './features/execute_v2/execute-controller';
import { getAllPlans, selectPlan, openPlan, validatePlanById, approvePlanById, discardPlanById, regeneratePlanById, fixPlanJsonById } from './features/plan/plan-controller';
import { ActPersistence } from './features/act/act-persistence';
import { actState } from './features/act/act-state';
import { startActByPlanId, runActTask, runAllActTasks, skipActTask } from './features/act/act-controller';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot activated');
  const planViewProvider = new PlanViewProvider();
  const actViewProvider = new ActViewProvider();
  const executeViewProvider = new ExecuteViewProvider();
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
      actViewProvider
    ),
    vscode.window.registerWebviewViewProvider(
      ExecuteViewProvider.viewId,
      executeViewProvider
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
      () => {
        vscode.window.showWarningMessage('Act v1 is deprecated. Use Execute (v2).');
      }
    ),
    vscode.commands.registerCommand(
      'localpilot.act.focus',
      () => vscode.commands.executeCommand('workbench.view.extension.localpilot')
    ),
    vscode.commands.registerCommand(
      'localpilot.act.refresh',
      () => actViewProvider.render()
    ),
    vscode.commands.registerCommand(
      'localpilot.act.runTask',
      runActTask
    ),
    vscode.commands.registerCommand(
      'localpilot.act.skipTask',
      skipActTask
    ),
    vscode.commands.registerCommand(
      'localpilot.act.runAll',
      runAllActTasks
    ),
    vscode.commands.registerCommand(
      'localpilot.index.sync',
      async () => { /* no-op placeholder */ }
    ),
    vscode.commands.registerCommand(
      'localpilot.execute.start',
      startPlanExecution
    ),
    vscode.commands.registerCommand(
      'localpilot.execute.apply',
      approveAndApply
    ),
    vscode.commands.registerCommand(
      'localpilot.execute.refresh',
      () => executeViewProvider.render()
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

*Size: 1,281 bytes | Modified: 2025-12-28T21:40:41.225Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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


## extension/src/features/act/act-apply.ts

*Size: 2,163 bytes | Modified: 2025-12-28T21:40:41.189Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import * as vscode from 'vscode';
import * as path from 'path';

/**
 * VERY SMALL unified diff applier.
 * Supports add/replace lines.
 * (Enough for Phase 4.8; full patch engine can come later.)
 */
export async function applyDiff(diff: string): Promise<boolean> {
  if (!diff.trim().startsWith('---')) {
    // empty or invalid diff = no-op success
    return true;
  }

  const lines = diff.split('\n');

  let targetFile: string | null = null;
  const hunks: string[] = [];

  for (const line of lines) {
    if (line.startsWith('+++ ')) {
      targetFile = line.replace('+++ ', '').trim();
      continue;
    }
    if (targetFile) hunks.push(line);
  }

  if (!targetFile) {
    vscode.window.showErrorMessage('Invalid diff: no target file.');
    return false;
  }

  const ws = vscode.workspace.workspaceFolders?.[0];
  if (!ws) {
    vscode.window.showErrorMessage('No workspace open.');
    return false;
  }

  const filePath = vscode.Uri.file(
    path.join(ws.uri.fsPath, targetFile.replace(/^b\//, ''))
  );

  const doc = await vscode.workspace.openTextDocument(filePath);
  const text = doc.getText();
  const newText = applyUnifiedDiff(text, hunks);

  if (newText === null) {
    vscode.window.showErrorMessage('Failed to apply diff.');
    return false;
  }

  const edit = new vscode.WorkspaceEdit();
  edit.replace(
    filePath,
    new vscode.Range(
      doc.positionAt(0),
      doc.positionAt(text.length)
    ),
    newText
  );

  return vscode.workspace.applyEdit(edit);
}

/**
 * VERY BASIC unified diff applier.
 * (Insert/remove lines only; safe for generated code.)
 */
function applyUnifiedDiff(original: string, diffLines: string[]): string | null {
  const out: string[] = [];
  const src = original.split('\n');
  let srcIndex = 0;

  for (const line of diffLines) {
    if (line.startsWith('@@')) continue;

    if (line.startsWith('+')) {
      out.push(line.slice(1));
    } else if (line.startsWith('-')) {
      srcIndex++;
    } else {
      out.push(src[srcIndex] ?? '');
      srcIndex++;
    }
  }

  return out.join('\n');
}


```

</details>


## extension/src/features/act/act-controller.ts

*Size: 2,085 bytes | Modified: 2025-12-28T21:40:41.190Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import * as vscode from 'vscode';
import { planRegistry } from '../plan/plan-registry';
import { ActService } from './act-service';

const actService = new ActService();

export async function startActByPlanId(planId?: string) {
  let targetId = planId;

  if (!targetId) {
    const selected = planRegistry.getSelected();
    if (selected.length === 1) {
      targetId = selected[0].id;
    } else {
      const ready = planRegistry
        .getPlans()
        .find(p => p.status === 'approved' && p.plan && (!p.warnings || !p.warnings.length));
      if (ready) targetId = ready.id;
    }
  }

  if (!targetId) {
    vscode.window.showErrorMessage('Plan not found.');
    return;
  }

  const stored = planRegistry.getPlan(targetId);

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

  if (stored.plan.id !== targetId) {
    vscode.window.showErrorMessage(
      'Internal error: plan identity mismatch. Please revalidate the plan.'
    );
    return;
  }

  try {
    // Lock plan
    planRegistry.update(targetId, { status: 'acting' });
    // Start Act Session BEFORE refresh to ensure view has session
    actService.start(stored.plan);

    // Then refresh and focus
    await vscode.commands.executeCommand('localpilot.plan.refresh');
    await vscode.commands.executeCommand('localpilot.act.refresh');
    await vscode.commands.executeCommand('localpilot.act.focus');
  } catch (err: any) {
    vscode.window.showErrorMessage(err?.message ?? 'Failed to start Act Mode.');
  }
}

export async function runActTask(taskId: string) {
  await actService.runTask(taskId);
}

export async function runAllActTasks() {
  await actService.runAll();
}

export function skipActTask(taskId: string) {
  actService.skip(taskId);
}


```

</details>


## extension/src/features/act/act-events.ts

*Size: 300 bytes | Modified: 2025-12-28T21:40:41.191Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
export type ActEvent =
  | { type: 'act:started' }
  | { type: 'act:paused' }
  | { type: 'act:resumed' }
  | { type: 'act:cancelled' }
  | { type: 'act:completed' }
  | { type: 'task:advance'; index: number };


```

</details>


## extension/src/features/act/act-executor.ts

*Size: 912 bytes | Modified: 2025-12-28T21:40:41.192Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import * as vscode from 'vscode';
import { OllamaChatClient, type ChatMessage } from '../../ollama/ollama-chat-client.js';
import { ACT_MODE_SYSTEM_PROMPT } from './act-prompts.js';
import type { Task } from '../../core/entities/task.entity';

export async function executeTask(
  task: Task,
  workspaceRoot: vscode.Uri
): Promise<string> {
  const client = new OllamaChatClient();

  const messages: ChatMessage[] = [
    { role: 'system', content: ACT_MODE_SYSTEM_PROMPT },
    {
      role: 'user',
      content: JSON.stringify({
        task: {
          id: task.id,
          title: task.title,
          filePath: task.filePath,
          actionType: task.actionType,
          details: task.details,
        },
        workspaceRoot: workspaceRoot.fsPath,
      }),
    },
  ];

  return client.chat(messages);
}


```

</details>


## extension/src/features/act/act-persistence.ts

*Size: 599 bytes | Modified: 2025-12-28T21:40:41.195Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import * as vscode from 'vscode';
import type { ActSession } from './act-state';

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

*Size: 609 bytes | Modified: 2025-12-28T21:40:41.197Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
export const ACT_MODE_SYSTEM_PROMPT = `
You are operating in ACT MODE.


Your task:
- Implement EXACTLY ONE task from an approved implementation plan.
- Generate a UNIFIED DIFF ONLY.
- Modify ONLY the files specified in the task.
- Do NOT explain anything.
- Do NOT include markdown.
- Do NOT include JSON.
- Do NOT repeat the plan.


Rules:
- Output MUST start with --- and +++ lines.
- The diff MUST be valid.
- If no changes are required, output an empty diff.


Failure to follow these rules is a critical error.
`;


```

</details>


## extension/src/features/act/act-service.ts

*Size: 2,337 bytes | Modified: 2025-12-28T21:40:41.197Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import { actState } from './act-state';
import type { Plan } from '../../core/entities/plan.entity';
import * as vscode from 'vscode';
import { planRegistry } from '../plan/plan-registry';
import { executeTask } from './act-executor.js';
import { applyDiff } from './act-apply.js';

// Phase 4.7 backbone: simplified execution state and actions

export class ActService {
  start(plan: Plan) {
    actState.set({
      planId: plan.id,
      planTitle: (plan as any).title ?? 'Plan',
      currentIndex: 0,
      tasks: [...plan.tasks]
        .sort((a, b) => a.orderIndex - b.orderIndex)
        .map(t => ({ id: t.id, title: t.title, status: 'pending' as const }))
    });
  }

  // Legacy run/pause/resume no-ops retained for compatibility
  run() {}
  pause() {}
  resume() {}

  async runTask(taskId: string) {
    const s = actState.get();
    if (!s) return;

    const plan = planRegistry.getPlan(s.planId)?.plan;
    if (!plan) throw new Error('Plan missing');
    const task = plan.tasks.find(t => t.id === taskId);
    if (!task) throw new Error('Task missing');

    actState.updateTask(taskId, 'running');
    await vscode.commands.executeCommand('localpilot.act.refresh');

    try {
      const root = vscode.workspace.workspaceFolders?.[0]?.uri;
      if (!root) throw new Error('No workspace folder is open.');

      const diff = await executeTask(task as any, root);
      const applied = await applyDiff(diff);
      if (!applied) {
        actState.updateTask(taskId, 'skipped');
        return;
      }

      actState.updateTask(taskId, 'done');
    } catch {
      actState.updateTask(taskId, 'failed');
    }

    await vscode.commands.executeCommand('localpilot.act.refresh');
  }

  async runAll() {
    const s = actState.get();
    if (!s) return;
    for (const t of s.tasks) {
      if (t.status !== 'pending') continue;
      await this.runTask(t.id);
      const updated = actState.get();
      const after = updated?.tasks.find(x => x.id === t.id);
      if (after?.status === 'failed') break;
    }
    try {
      await vscode.commands.executeCommand('localpilot.index.sync');
    } catch {}
  }

  skip(taskId: string) {
    actState.updateTask(taskId, 'skipped');
  }

  cancel() {
    actState.clear();
  }
}


```

</details>


## extension/src/features/act/act-session.ts

*Size: 359 bytes | Modified: 2025-12-28T21:40:41.198Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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

*Size: 1,178 bytes | Modified: 2025-12-28T21:40:41.200Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import type { Plan } from '../../core/entities/plan.entity';

export type ActTaskStatus =
  | 'pending'
  | 'running'
  | 'done'
  | 'failed'
  | 'skipped';

export interface ActTask {
  id: string;
  title: string;
  status: ActTaskStatus;
}

export interface ActSession {
  planId: string;
  planTitle: string;
  tasks: ActTask[];
  currentIndex: number;
}

let session: ActSession | null = null;

export const actState = {
  set(s: ActSession) {
    session = s;
  },
  get() {
    return session;
  },
  // Back-compat: allow legacy service to merge arbitrary fields (e.g., status)
  update(patch: any) {
    if (!session) return;
    session = { ...(session as any), ...(patch as any) } as ActSession;
  },
  // Back-compat: signal if there is any active session
  hasActiveSession(): boolean {
    return !!session;
  },
  updateTask(id: string, status: ActTaskStatus) {
    if (!session) return;
    const t = session.tasks.find(t => t.id === id);
    if (t) t.status = status;
  },
  advance() {
    if (session) session.currentIndex++;
  },
  clear() {
    session = null;
  }
};


```

</details>


## extension/src/features/act/act-types.ts

*Size: 574 bytes | Modified: 2025-12-28T21:40:41.201Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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

*Size: 791 bytes | Modified: 2025-12-28T21:40:41.204Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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

*Size: 1,250 bytes | Modified: 2025-12-28T21:40:41.205Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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

*Size: 785 bytes | Modified: 2025-12-28T21:40:41.207Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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

*Size: 463 bytes | Modified: 2025-12-28T21:40:41.209Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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

*Size: 485 bytes | Modified: 2025-12-28T21:40:41.211Z*

<details>
<summary>View code</summary>

```typescript
﻿/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
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


## extension/src/features/execute_v2/execute-client.ts

*Size: 1,361 bytes | Modified: 2025-12-29T21:27:46.216Z*

<details>
<summary>View code</summary>

```typescript
const API = 'http://localhost:8000/api';

export async function startExecution(payload: { planId: string; markdown: string ; workspaceRoot: string}) {
  // Backend expects both planId and plan markdown; it will parse and bind identity.
  return post(`/execute/plan`, payload);
}

export async function applyDiff(executionId: string) {
  return post(`/execute/${executionId}/apply`);
}

export async function reindex(executionId: string) {
  return post(`/execute/${executionId}/reindex`);
}

export async function getExecution(executionId: string) {
  return get(`/execute/${executionId}`);
}

export async function prepareTask(executionId: string, taskId: string) {
  return post(`/execute/${executionId}/prepare/${taskId}`);
}

export async function invokeTask(executionId: string, taskId: string) {
  return post(`/execute/${executionId}/invoke/${taskId}`);
}

async function post(path: string, body?: any) {
  const res = await fetch(API + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(await res.text().catch(() => `${res.status}`));
  return res.json();
}

async function get(path: string) {
  const res = await fetch(API + path);
  if (!res.ok) throw new Error(await res.text().catch(() => `${res.status}`));
  return res.json();
}

```

</details>


## extension/src/features/execute_v2/execute-controller.ts

*Size: 2,944 bytes | Modified: 2025-12-29T21:27:48.966Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import * as api from './execute-client';
import { executionState } from './execute-state';
import { planRegistry } from '../plan/plan-registry';

export async function startPlanExecution(planId?: string) {
  try {
    let targetId = planId;

    // 1) If no planId passed, resolve from selection
    if (!targetId) {
      const selected = planRegistry.getSelected();
      if (selected.length === 1) {
        targetId = selected[0].id;
      }
    }

    // 2) Fallback: first approved plan
    if (!targetId) {
      const approved = planRegistry
        .getPlans()
        .find((p) => p.status === 'approved' && p.plan);
      if (approved) {
        targetId = approved.id;
      }
    }

    // 3) Final guard
    if (!targetId) {
      vscode.window.showErrorMessage('No approved plan selected. Please select a plan first.');
      return;
    }

    const stored = planRegistry.getPlan(targetId);

    if (!stored || !stored.plan) {
      vscode.window.showErrorMessage(`Plan ${targetId} not found or not approved.`);
      return;
    }

    if (stored.status !== 'approved') {
      vscode.window.showErrorMessage(`Plan ${targetId} must be approved before execution.`);
      return;
    }

    // Start execution
    const workspace = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspace) {
      vscode.window.showErrorMessage('No workspace folder open.');
      return;
    }
    const exec = await api.startExecution({
      planId: stored.id,
      markdown: stored.markdown,
      workspaceRoot: workspace,
    });


    executionState.set({
      executionId: exec.execution_id,
      planTitle: stored.title || 'Plan',
      status: exec.status,
    });
    vscode.commands.executeCommand('localpilot.execute.refresh');

    const firstTask = exec.tasks?.[0];
    if (firstTask) {
      await api.prepareTask(exec.execution_id, firstTask.task_id);
      const invokeRes = await api.invokeTask(exec.execution_id, firstTask.task_id);
      executionState.set({
        executionId: exec.execution_id,
        planTitle: stored.title || 'Plan',
        status: 'awaiting_human',
        currentTask: firstTask.task_id,
        diff: invokeRes.diff,
      });
      vscode.commands.executeCommand('localpilot.execute.refresh');
    }

    vscode.commands.executeCommand('localpilot.execute.refresh');
  } catch (err: any) {
    vscode.window.showErrorMessage(`Failed to start execution: ${err?.message ?? err}`);
  }
}

export async function approveAndApply() {
  try {
    const s = executionState.get();
    if (!s) return;

    await api.applyDiff(s.executionId);
    await api.reindex(s.executionId);

    vscode.window.showInformationMessage('Changes applied & indexed');
    executionState.clear();
    vscode.commands.executeCommand('localpilot.execute.refresh');
  } catch (err: any) {
    vscode.window.showErrorMessage(`Apply failed: ${err?.message ?? err}`);
  }
}

```

</details>


## extension/src/features/execute_v2/execute-state.ts

*Size: 319 bytes | Modified: 2025-12-27T22:47:04.998Z*

<details>
<summary>View code</summary>

```typescript
export interface ExecutionUIState {
  executionId: string;
  planTitle: string;
  status: string;
  currentTask?: string;
  diff?: string;
}

let state: ExecutionUIState | null = null;

export const executionState = {
  set(s: ExecutionUIState) { state = s; },
  get() { return state; },
  clear() { state = null; }
};

```

</details>


## extension/src/features/execute_v2/execute-types.ts

*Size: 180 bytes | Modified: 2025-12-27T22:49:53.075Z*

<details>
<summary>View code</summary>

```typescript
export interface BackendExecution {
  execution_id: string;
  plan_id: string;
  status: string;
  current_task_id?: string;
  tasks?: Array<{ task_id: string; title: string }>;
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

*Size: 10,948 bytes | Modified: 2025-12-30T20:41:25.783Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { generatePlan } from './plan-client';
import { openPlanView } from './plan-view-controller';
import { isIndexed } from '../../infrastructure/http/api-client';
import { getActiveProjectId } from '../../core/project-context';
import { parsePlanMarkdown } from './plan-parser';
import { validatePlan, type ValidationWarning } from './plan-validator';
import { normalizePlan } from './plan-normalizer';
import { buildPlanFixDiff } from './plan-diff';
import { approvePlan } from './plan-approval';
import { planState } from './plan-state';
import { planRegistry } from './plan-registry';
import { autoFixPlanPreview } from '../../infrastructure/http/api-client';

function genId(): string {
  const rnd = (globalThis as any).crypto?.randomUUID?.();
  return rnd || (Math.random().toString(36).slice(2) + Date.now().toString(36));
}

export async function autoFixPreviewById(planId: string) {
  const stored = planRegistry.getPlan(planId);
  if (!stored) return;
  if (!stored.markdown) {
    vscode.window.showWarningMessage('No plan markdown to auto-fix.');
    return;
  }

  try {
    const res = await autoFixPlanPreview(stored.markdown);
    // Preview unified diff
    const doc = await vscode.workspace.openTextDocument({ content: res.diff, language: 'diff' });
    await vscode.window.showTextDocument(doc, { preview: true });

    // Surface warnings inline in the Plan view without mutating plan/markdown
    const mapped = (res.warnings || []).map(w => ({ code: 'auto_fix', message: w }));
    planRegistry.update(planId, { warnings: mapped as any });
    await vscode.commands.executeCommand('localpilot.plan.refresh');

    if (mapped.length) {
      vscode.window.showInformationMessage(`Auto-fix preview generated with ${mapped.length} warning(s).`);
    } else {
      vscode.window.showInformationMessage('Auto-fix preview generated.');
    }
  } catch (err: any) {
    vscode.window.showErrorMessage(`Auto-fix preview failed: ${err?.message ?? err}`);
  }
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

  // Normalize paths to workspace-relative
  const norm = normalizePlan(parsed.plan as any);

  // Structural validation
  const structural = validatePlan(norm.plan);
  const normAsValidation: ValidationWarning[] = (norm.warnings || []).map(w => ({
    code: 'normalized_path',
    message: w.message,
    taskId: w.taskId,
    path: w.field ? `tasks[].${w.field}` : undefined,
  }));
  const warnings: ValidationWarning[] = [...normAsValidation, ...structural];

  planRegistry.update(planId, {
    plan: {
      ...norm.plan,
      id: planId,
    },
    warnings,
    status: 'draft',
  });

  if (norm.changed) {
    vscode.window.showInformationMessage(
      'Plan paths were normalized to workspace-relative paths.'
    );
    try {
      const diff = buildPlanFixDiff(
        stored.markdown,
        JSON.stringify(norm.plan, null, 2)
      );
      const doc = await vscode.workspace.openTextDocument({ content: diff, language: 'diff' });
      await vscode.window.showTextDocument(doc, { preview: true });
    } catch {}
  }

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
    if (w.code === 'invalid_action_type' || w.code === 'missing_action_type') {
      const task = plan.tasks.find((t) => t.id === w.taskId);
      if (task) {
        task.actionType = 'modify';
      }
    }
  }

  // Re-run validation
  const afterFixWarnings = validatePlan(plan);

  // Normalize after fixes
  const norm = normalizePlan(plan as any);
  const normAsValidation: ValidationWarning[] = (norm.warnings || []).map(w => ({
    code: 'normalized_path',
    message: w.message,
    taskId: w.taskId,
    path: w.field ? `tasks[].${w.field}` : undefined,
  }));

  planRegistry.update(planId, {
    plan: {
      ...plan,
      id: planId,
    },
    markdown: stored.markdown,
    warnings: [...normAsValidation, ...afterFixWarnings],
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
  if (!stored) {
    vscode.window.showErrorMessage('Plan not found.');
    return;
  }

  const parsed = parsePlanMarkdown(stored.markdown);
  if (!parsed.plan) {
    vscode.window.showErrorMessage('Cannot approve: plan JSON is invalid.');
    return;
  }

  // Normalize before approval
  const norm = normalizePlan(parsed.plan as any);
  if (norm.changed) {
    vscode.window.showInformationMessage(
      'Plan paths were normalized to workspace-relative paths.'
    );
    try {
      const diff = buildPlanFixDiff(
        stored.markdown,
        JSON.stringify(norm.plan, null, 2)
      );
      const doc = await vscode.workspace.openTextDocument({ content: diff, language: 'diff' });
      await vscode.window.showTextDocument(doc, { preview: true });
    } catch {}
  }

  const structural = validatePlan(norm.plan);
  const normAsValidation: ValidationWarning[] = (norm.warnings || []).map(w => ({
    code: 'normalized_path',
    message: w.message,
    taskId: w.taskId,
    path: w.field ? `tasks[].${w.field}` : undefined,
  }));
  if (structural.length) {
    vscode.window.showWarningMessage(
      'Cannot approve: plan has validation warnings.'
    );
    return;
  }

  const approved = approvePlan({
    ...norm.plan,
    id: planId, // enforce identity
  });

  // Sync back into registry authoritatively
  planRegistry.update(planId, {
    markdown: stored.markdown,
    plan: approved,
    status: 'approved',
    warnings: normAsValidation,
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


## extension/src/features/plan/plan-diff.d.ts

*Size: 73 bytes | Modified: 2025-12-29T22:28:56.634Z*

<details>
<summary>View code</summary>

```typescript
export function buildPlanFixDiff(before: string, after: string): string;

```

</details>


## extension/src/features/plan/plan-diff.ts

*Size: 385 bytes | Modified: 2025-12-29T22:24:23.431Z*

<details>
<summary>View code</summary>

```typescript
import { diffLines } from 'diff';

export function buildPlanFixDiff(before: string, after: string): string {
  const diff = diffLines(before ?? '', after ?? '');
  let out = '';

  diff.forEach(part => {
    const prefix = part.added ? '+' : part.removed ? '-' : ' ';
    out += part.value
      .split('\n')
      .map(line => prefix + line)
      .join('\n');
  });

  return out;
}

```

</details>


## extension/src/features/plan/plan-normalizer.ts

*Size: 1,002 bytes | Modified: 2025-12-29T22:17:56.387Z*

<details>
<summary>View code</summary>

```typescript
import * as path from 'path';

export interface PlanLintWarning {
  message: string;
  taskId?: string;
  field?: string;
}

export function normalizePlan(plan: any): {
  plan: any;
  warnings: PlanLintWarning[];
  changed: boolean;
} {
  const warnings: PlanLintWarning[] = [];
  let changed = false;

  if (!plan?.tasks) {
    return { plan, warnings, changed };
  }

  for (const task of plan.tasks) {
    if (!task.filePath) continue;

    const original = task.filePath;

    // Windows absolute path
    if (/^[A-Za-z]:[\\/]/.test(task.filePath)) {
      task.filePath = path.basename(task.filePath);
    }

    // Unix absolute path
    if (task.filePath.startsWith('/')) {
      task.filePath = path.basename(task.filePath);
    }

    if (original !== task.filePath) {
      warnings.push({
        taskId: task.id,
        field: 'filePath',
        message: `Absolute path normalized to '${task.filePath}'`,
      });
      changed = true;
    }
  }

  return { plan, warnings, changed };
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

*Size: 1,595 bytes | Modified: 2025-12-27T21:27:36.011Z*

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

*Size: 2,413 bytes | Modified: 2025-12-27T21:27:36.011Z*

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

export function isPlanActReady(plan: Plan | null | undefined, warnings: ValidationWarning[] = []): boolean {
  return !!plan && (warnings?.length ?? 0) === 0;
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

*Size: 1,468 bytes | Modified: 2025-12-30T20:41:53.510Z*

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

export async function autoFixPlanPreview(markdown: string): Promise<{ fixedPlan: any; warnings: string[]; diff: string }>
{
  const res = await fetch('http://localhost:8000/api/plan/auto-fix', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ markdown }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`auto_fix_failed: ${res.status} ${text}`);
  }
  return await res.json();
}

```

</details>


## extension/src/ollama/ollama-chat-client.ts

*Size: 1,210 bytes | Modified: 2025-12-27T21:27:36.012Z*

<details>
<summary>View code</summary>

```typescript
export type ChatMessage = { role: 'system' | 'user' | 'assistant'; content: string };

export class OllamaChatClient {
  async chat(messages: ChatMessage[]): Promise<string> {
    const WS = require('ws');
    const ws = new WS('ws://localhost:8000/ws/chat');

    return new Promise<string>((resolve, reject) => {
      let buffer = '';

      ws.on('open', () => {
        try {
          ws.send(
            JSON.stringify({
              model: 'qwen2.5-coder:7b-instruct-q4_K_M',
              messages,
            })
          );
        } catch (e) {
          reject(e);
        }
      });

      ws.on('message', (raw: any) => {
        try {
          const msg = JSON.parse(raw.toString());
          if (msg.type === 'token' && typeof msg.value === 'string') {
            buffer += msg.value;
          }
          if (msg.type === 'done') {
            resolve(buffer);
            ws.close();
          }
        } catch (e) {
          // ignore malformed frames
        }
      });

      ws.on('error', (err: any) => {
        reject(err);
      });

      ws.on('close', () => {
        // if closed without done, resolve whatever we have
        resolve(buffer);
      });
    });
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

*Size: 3,350 bytes | Modified: 2025-12-27T21:27:36.013Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { actState } from '../../features/act/act-state';

export class ActViewProvider implements vscode.WebviewViewProvider {
  static readonly viewId = 'localpilot.act';
  private view?: vscode.WebviewView;

  resolveWebviewView(view: vscode.WebviewView) {
    this.view = view;
    view.webview.options = { enableScripts: true };

    view.webview.onDidReceiveMessage(async (msg) => {
      if (!msg?.command) return;

      await vscode.commands.executeCommand(msg.command, msg.taskId);
      await vscode.commands.executeCommand('localpilot.act.refresh');
    });

    this.render();
  }

  render() {
    if (!this.view) return;

    const session = actState.get();

    if (!session) {
      this.view.webview.html = `
        <style>
          body { color: #888; font-family: sans-serif; padding: 8px; }
        </style>
        <em>No active Act session.</em>
      `;
      return;
    }

    this.view.webview.html = `
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body {
            background: #1e1e1e;
            color: #d4d4d4;
            font-family: sans-serif;
            padding: 8px;
          }
          h3 { margin-bottom: 4px; }
          .plan {
            font-size: 12px;
            color: #9cdcfe;
            margin-bottom: 8px;
          }
          ul {
            list-style: none;
            padding-left: 0;
          }
          li {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 0;
          }
          button {
            background: none;
            border: none;
            cursor: pointer;
            color: #d4d4d4;
          }
          button:hover { color: white; }
          .status {
            width: 18px;
            text-align: center;
          }
        </style>
      </head>
      <body>
        <h3>Act Mode</h3>
        <div class="plan"><b>Plan:</b> ${escapeHtml(session.planTitle)}</div>

        <button onclick="runAll()">▶ Run All</button>

        <ul>
          ${session.tasks.map(t => `
            <li>
              <span class="status">${icon(t.status)}</span>
              <span>${escapeHtml(t.title)}</span>
              <button onclick="run('${t.id}')" title="Run">▶</button>
              <button onclick="skip('${t.id}')" title="Skip">⏭</button>
            </li>
          `).join('')}
        </ul>

        <script>
          const vscode = acquireVsCodeApi();
          function run(id) {
            vscode.postMessage({ command: 'localpilot.act.runTask', taskId: id });
          }
          function skip(id) {
            vscode.postMessage({ command: 'localpilot.act.skipTask', taskId: id });
          }
          function runAll() {
            vscode.postMessage({ command: 'localpilot.act.runAll' });
          }
        </script>
      </body>
      </html>
    `;
  }
}

function icon(status: string): string {
  switch (status) {
    case 'pending': return '⬜';
    case 'running': return '⏳';
    case 'done': return '✅';
    case 'failed': return '❌';
    case 'skipped': return '⏭';
    default: return '⬜';
  }
}

function escapeHtml(str: string): string {
  return str.replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[m]!));
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


## extension/src/views/execute/execute-view.ts

*Size: 1,466 bytes | Modified: 2025-12-29T18:54:39.898Z*

<details>
<summary>View code</summary>

```typescript
import * as vscode from 'vscode';
import { executionState } from '../../features/execute_v2/execute-state';

export class ExecuteViewProvider implements vscode.WebviewViewProvider {
  static viewId = 'localpilot.execute';
  private view?: vscode.WebviewView;

  resolveWebviewView(view: vscode.WebviewView) {
    this.view = view;
    view.webview.options = { enableScripts: true };
    this.render();
  }

  render() {
    if (!this.view) return;

    const s = executionState.get();

    if (!s) {
      this.view.webview.html = '<em>No active execution</em>';
      return;
    }

    this.view.webview.html = `
      <h3>Execution: ${escapeHtml(s.planTitle)}</h3>

      <p>Status: <b>${s.status}</b></p>

      ${s.diff ? `
        <h4>Proposed Changes</h4>
        <pre>${escapeHtml(s.diff)}</pre>
        <button onclick="approve()">Apply</button>
      ` : ` 
        <em>Waiting for task output…</em>
      `}

      <script>
        const vscode = acquireVsCodeApi();
        function approve() {
          vscode.postMessage({ command: 'apply' });
        }
      </script>
    `;

    this.view.webview.onDidReceiveMessage(msg => {
      if (msg.command === 'apply') {
        vscode.commands.executeCommand('localpilot.execute.apply');
      }
    });
  }
}

function escapeHtml(str: string): string {
  return str.replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  } as any)[m]);
}

```

</details>


## extension/src/views/plan/plan-view.ts

*Size: 6,539 bytes | Modified: 2025-12-27T21:27:36.014Z*

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
            <b>${w.path ?? (w.taskId ? `task ${w.taskId}` : 'task')}</b>: ${w.message}
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


## server/act_v2/__init__.py

*Size: 0 bytes | Modified: 2025-12-27T22:07:07.793Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/act_v2/api.py

*Size: 5,854 bytes | Modified: 2025-12-29T21:59:11.921Z*

<details>
<summary>View code</summary>

```python
from fastapi import APIRouter, HTTPException
from typing import Dict
from pathlib import Path

from server.plan.plan_parser import PlanParser
from server.act_v2.compiler.plan_compiler import compile_plan
from server.act_v2.ledger.execution_ledger import ExecutionLedger
from server.act_v2.context.task_context_builder import build_task_context
from server.act_v2.llm.invocation_service import InvocationService
from server.act_v2.llm.ollama_client import OllamaClient
from server.act_v2.validation.validation_errors import DiffValidationError
from server.act_v2.diff_validator import DiffValidationError as StrictDiffValidationError
from server.act_v2.apply.apply_errors import ApplyError
from server.act_v2.apply_engine import ApplyEngine
from server.act_v2.index_hook import reindex_files
from server.act_v2.errors import PlanCompilationError


router = APIRouter(prefix="/api/execute", tags=["act_v2"])

ledger = ExecutionLedger()

client = OllamaClient(
    base_url="http://127.0.0.1:11434",
    model="qwen2.5-coder:7b-instruct-q4_K_M",
)
invoker = InvocationService(client)


@router.post("/plan")
def compile_plan_endpoint(payload: Dict):
    """
    Compile an APPROVED plan into an execution graph.
    """
    try:
        plan_id = payload.get("planId")
        markdown = payload.get("markdown")
        workspace_root = payload.get("workspaceRoot")

        if not workspace_root:
            raise HTTPException(status_code=400, detail="workspaceRoot required")

        if not plan_id or not markdown:
            raise HTTPException(status_code=400, detail="planId and markdown required")

        parser = PlanParser()
        parsed = parser.parse(markdown)

        if not parsed.get("plan"):
            raise HTTPException(status_code=400, detail="Invalid plan JSON")

        execution = compile_plan(parsed["plan"], workspace_root)
        execution.plan_id = plan_id  # canonical identity
        ledger.create(execution)
        return execution.model_dump()

    except PlanCompilationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{execution_id}")
def get_execution_state(execution_id: str):
    state = ledger.get(execution_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution not found")
    return state.dict()


@router.post("/{execution_id}/prepare/{task_id}")
def prepare_task_context(execution_id: str, task_id: str):
    state = ledger.get(execution_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution not found")

    task = next((t for t in state.tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    workspace = Path(state.workspace_root)  # TEMP: Phase 5.3 will formalize workspace root
    context = build_task_context(task, workspace)
    context["workspace_root"] = str(workspace)

    state.status = "context_ready"
    state.current_task_id = task_id
    state.context = context
    ledger.update(execution_id, state)

    return {
        "execution_id": execution_id,
        "task_id": task_id,
        "context": context,
    }


@router.post("/{execution_id}/invoke/{task_id}")
def invoke_task(execution_id: str, task_id: str):
    state = ledger.get(execution_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution not found")

    task = next((t for t in state.tasks if t.task_id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if state.status != "context_ready":
        raise HTTPException(status_code=400, detail="Context not prepared")

    try:
        diff = invoker.invoke_task(task, state.context or {})
        state.status = "awaiting_human"
        state.last_diff = diff
        state.last_error = None
        ledger.update(execution_id, state)
        return {
            "status": "awaiting_human",
            "diff": diff,
        }

    except (DiffValidationError, StrictDiffValidationError) as e:
        state.status = "failed"
        state.last_error = str(e)
        ledger.update(execution_id, state)
        raise HTTPException(
            status_code=422,
            detail=f"Execution blocked by safety rule: {e}",
        )


@router.post("/{execution_id}/apply")
def apply_execution(execution_id: str):
    state = ledger.get(execution_id)
    if not state:
        raise HTTPException(status_code=404, detail="Execution not found")

    if state.status != "awaiting_human":
        raise HTTPException(
            status_code=400,
            detail="Execution not awaiting approval",
        )

    try:
        workspace = Path(state.context["workspace_root"])  # type: ignore[index]
        engine = ApplyEngine(workspace)
        changed = engine.apply(state.last_diff or "")
        reindex_files(state.plan_id, changed, workspace)

        state.status = "completed"
        ledger.update(execution_id, state)

        return {"status": "applied"}

    except ApplyError as e:
        state.status = "failed"
        state.last_error = str(e)
        ledger.update(execution_id, state)
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/{execution_id}/reindex")
def reindex_after_apply(execution_id: str):
    state = ledger.get(execution_id)
    if not state or state.status != "completed":
        raise HTTPException(status_code=400, detail="Execution not completed")

    workspace = Path(state.context["workspace_root"])  # type: ignore[index]
    reindex_files(state.plan_id, [], workspace)

    return {"status": "indexed"}


# Human Gate (Final)
act_router = APIRouter(prefix="/api/act", tags=["act_v2"])

@act_router.post("/approve")
def approve_task(task_id: str):
    # block until user approval recorded (placeholder)
    return {"approved": True}

```

</details>


## server/act_v2/apply_engine.py

*Size: 1,368 bytes | Modified: 2025-12-30T20:23:21.934Z*

<details>
<summary>View code</summary>

```python
import subprocess
import tempfile
import shutil
from pathlib import Path
import logging
from server.act_v2.apply.apply_errors import ApplyError


logger = logging.getLogger(__name__)


class ApplyEngine:
    def __init__(self, workspace: Path):
        self.workspace = workspace

    def apply(self, diff: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            shutil.copytree(self.workspace, tmp_path / "repo", dirs_exist_ok=True)

            proc = subprocess.run(
                ["git", "apply", "--whitespace=nowarn"],
                input=diff,
                text=True,
                cwd=tmp_path / "repo",
                capture_output=True,
            )

            if proc.returncode != 0:
                logger.error("GIT APPLY ERROR:\n%s", proc.stderr)
                raise ApplyError(
                    "Patch could not be applied cleanly.\n"
                    "Reason:\n" + proc.stderr
                )

            shutil.copytree(
                tmp_path / "repo",
                self.workspace,
                dirs_exist_ok=True,
            )

        return self._changed_files(diff)

    def _changed_files(self, diff: str) -> list[str]:
        return [
            line[6:]
            for line in diff.splitlines()
            if line.startswith("+++ b/")
        ]

```

</details>


## server/act_v2/apply/__init__.py

*Size: 0 bytes | Modified: 2025-12-27T22:36:17.244Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/act_v2/apply/apply_errors.py

*Size: 139 bytes | Modified: 2025-12-27T22:36:43.056Z*

<details>
<summary>View code</summary>

```python
class ApplyError(Exception):
    pass


class PatchApplyFailed(ApplyError):
    pass


class WorkspaceWriteViolation(ApplyError):
    pass

```

</details>


## server/act_v2/apply/patch_applier.py

*Size: 852 bytes | Modified: 2025-12-27T22:38:25.188Z*

<details>
<summary>View code</summary>

```python
import subprocess
from pathlib import Path

from .apply_errors import PatchApplyFailed


def apply_patch(diff: str, workspace_root: Path) -> None:
    if not diff.strip():
        return

    # Safety: ensure git repo exists
    if not (workspace_root / ".git").exists():
        raise PatchApplyFailed("Workspace is not a git repository")

    # Dry-run first
    dry = subprocess.run(
        ["git", "apply", "--check"],
        input=diff,
        cwd=workspace_root,
        text=True,
        capture_output=True,
    )

    if dry.returncode != 0:
        raise PatchApplyFailed(dry.stderr)

    # Apply for real
    apply = subprocess.run(
        ["git", "apply"],
        input=diff,
        cwd=workspace_root,
        text=True,
        capture_output=True,
    )

    if apply.returncode != 0:
        raise PatchApplyFailed(apply.stderr)

```

</details>


## server/act_v2/apply/workspace_guard.py

*Size: 279 bytes | Modified: 2025-12-27T22:37:13.850Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path


def assert_path_allowed(root: Path, target: Path):
    root = root.resolve()
    target = target.resolve()

    if not str(target).startswith(str(root)):
        raise PermissionError(
            f"Write outside workspace blocked: {target}"
        )

```

</details>


## server/act_v2/compiler/__init__.py

*Size: 0 bytes | Modified: 2025-12-27T22:07:08.538Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/act_v2/compiler/plan_compiler.py

*Size: 1,616 bytes | Modified: 2025-12-29T21:58:49.739Z*

<details>
<summary>View code</summary>

```python
from typing import Dict, Union
from uuid import uuid4


from server.plan.plan_parser import PlanSchema
from server.act_v2.models.execution_state import ExecutionState
from server.act_v2.compiler.task_graph import build_task_graph
from server.act_v2.errors import PlanCompilationError
from pathlib import Path



ALLOWED_ACTIONS = {"create", "modify", "delete"}


def compile_plan(plan: Union[PlanSchema, Dict], workspace_root: str) -> ExecutionState:
    """
    Deterministically compile a validated Plan into an executable task graph.
    Accepts either a PlanSchema or a dict conforming to PlanSchema.
    Only executable tasks (create/modify/delete with a non-empty filePath) are included.
    """
    if isinstance(plan, dict):
        plan = PlanSchema(**plan)

    executable_tasks = []

    for t in plan.tasks:
        if t.actionType not in ALLOWED_ACTIONS:
            continue
        if not t.filePath:
            continue
        executable_tasks.append(t)

    if not executable_tasks:
        raise PlanCompilationError("No executable tasks found in plan")

    tasks = build_task_graph(
        plan.copy(update={"tasks": executable_tasks})
    )

    # Enforce workspace-relative paths
    for t in tasks:
        if Path(t.file_path).is_absolute():
            raise PlanCompilationError(
                f"Illegal absolute path in plan task '{t.task_id}': {t.file_path}"
            )

    return ExecutionState(
        execution_id=str(uuid4()),
        plan_id=plan.id,
        workspace_root=workspace_root,
        status="pending",
        current_task_id=None,
        tasks=tasks,
    )

```

</details>


## server/act_v2/compiler/task_graph.py

*Size: 812 bytes | Modified: 2025-12-29T21:39:53.308Z*

<details>
<summary>View code</summary>

```python
from typing import List
from server.plan.plan_parser import PlanSchema
from server.act_v2.models.execution_task import ExecutionTask
from pathlib import Path


def build_task_graph(plan: PlanSchema) -> List[ExecutionTask]:
    """
    Converts plan.tasks into a strictly ordered, dependency-safe graph.
    """
    sorted_tasks = sorted(plan.tasks, key=lambda t: t.orderIndex)

    graph: List[ExecutionTask] = []

    for t in sorted_tasks:
        rel_path = Path(t.filePath).as_posix()
        graph.append(
            ExecutionTask(
                task_id=t.id,
                title=t.title,
                file_path=rel_path,
                action_type=t.actionType,
                dependencies=t.dependencies or [],
                order_index=t.orderIndex,
            )
        )

    return graph

```

</details>


## server/act_v2/context/__init__.py

*Size: 0 bytes | Modified: 2025-12-27T22:17:39.817Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/act_v2/context/task_context_builder.py

*Size: 1,359 bytes | Modified: 2025-12-29T21:40:21.137Z*

<details>
<summary>View code</summary>

```python
from typing import Dict
from pathlib import Path


from server.act_v2.models.execution_task import ExecutionTask
from .workspace_reader import WorkspaceReader


MAX_CONTEXT_CHARS = 12_000


def build_task_context(
    task: ExecutionTask,
    workspace_root: Path
) -> Dict:
    """
    Builds the minimal deterministic context for ONE task.
    """

    reader = WorkspaceReader(workspace_root)

    context_files: Dict[str, str] = {}

    # Only the task-declared file is allowed
    if Path(task.file_path).is_absolute():
        raise RuntimeError(
            f"Absolute paths are forbidden: {task.file_path}"
        )

    try:
        content = reader.read_file(task.file_path)
        context_files[task.file_path] = content[:MAX_CONTEXT_CHARS]
    except FileNotFoundError:
        # File may not exist yet (create action)
        context_files[task.file_path] = ""
    except PermissionError:
        raise RuntimeError("Illegal file access attempted")

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "action": task.action_type,
            "file_path": task.file_path,
            "dependencies": task.dependencies,
        },
        "files": context_files,
        "rules": {
            "allowed_files": [task.file_path],
            "action_type": task.action_type,
        }
    }

```

</details>


## server/act_v2/context/workspace_reader.py

*Size: 616 bytes | Modified: 2025-12-27T22:18:28.998Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from typing import Dict


class WorkspaceReader:
    """
    Read-only, allowlist-based workspace access.
    """

    def __init__(self, workspace_root: Path):
        self.root = workspace_root.resolve()

    def read_file(self, relative_path: str) -> str:
        path = (self.root / relative_path).resolve()

        if not path.exists() or not path.is_file():
            raise FileNotFoundError(relative_path)

        if self.root not in path.parents:
            raise PermissionError("Path escape attempt detected")

        return path.read_text(encoding="utf-8", errors="ignore")

```

</details>


## server/act_v2/diff_validator.py

*Size: 2,040 bytes | Modified: 2025-12-30T20:24:39.214Z*

<details>
<summary>View code</summary>

```python
import re
from dataclasses import dataclass
from typing import List
from pathlib import Path

from server.act_v2.models.execution_task import ExecutionTask
from server.act_v2.validation.validation_errors import ContextMismatchViolation


@dataclass
class ValidatedDiff:
    diff: str
    files_changed: List[str]


class DiffValidationError(Exception):
    pass


class DiffValidator:
    FILE_RE = re.compile(r"^\+\+\+\s+b/(.+)$", re.MULTILINE)

    def validate(self, diff: str, task: ExecutionTask, workspace: Path) -> ValidatedDiff:
        # Prevent hallucinated/empty diffs for modify tasks
        if task.action_type == "modify" and not diff.strip():
            raise ContextMismatchViolation(
                "Modify task produced no valid diff against existing file"
            )

        if not diff.strip():
            raise DiffValidationError("Empty diff")

        files = self.FILE_RE.findall(diff)
        if not files:
            raise DiffValidationError("No files modified")

        for f in files:
            if f != task.file_path:
                raise DiffValidationError(
                    f"Illegal file modification: {f}"
                )

        if task.action_type == "create" and not any("--- /dev/null" in diff for _ in [0]):
            raise DiffValidationError("Create task must add new file")

        if task.action_type == "delete" and not any("+++ /dev/null" in diff for _ in [0]):
            raise DiffValidationError("Delete task must remove file")

        # Workspace-aware checks
        target = workspace / task.file_path
        exists = target.exists()

        if task.action_type == "create" and exists:
            raise DiffValidationError(
                f"Create task attempted on existing file: {task.file_path}"
            )

        if task.action_type == "modify" and not exists:
            raise DiffValidationError(
                f"Modify task attempted on missing file: {task.file_path}"
            )

        return ValidatedDiff(diff=diff, files_changed=files)

```

</details>


## server/act_v2/errors.py

*Size: 97 bytes | Modified: 2025-12-27T22:07:13.611Z*

<details>
<summary>View code</summary>

```python
class ExecutionError(Exception):
    pass


class PlanCompilationError(ExecutionError):
    pass

```

</details>


## server/act_v2/index_hook.py

*Size: 382 bytes | Modified: 2025-12-27T23:17:56.510Z*

<details>
<summary>View code</summary>

```python
from server.indexing.service import IndexingService
from server.api.dependencies import get_embedder, get_index_root
from pathlib import Path


def reindex_files(project_id: str, files: list[str], workspace: Path):
    service = IndexingService(
        workspace=workspace,
        index_root=get_index_root() / project_id,
        embedder=get_embedder(),
    )
    service.run()

```

</details>


## server/act_v2/ledger/__init__.py

*Size: 0 bytes | Modified: 2025-12-27T22:07:11.595Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/act_v2/ledger/execution_ledger.py

*Size: 2,399 bytes | Modified: 2025-12-27T23:07:31.717Z*

<details>
<summary>View code</summary>

```python
from typing import Dict, Optional
from threading import Lock
from server.act_v2.models.execution_state import ExecutionState
from pathlib import Path
import json
import uuid
from .models import ExecutionLedgerModel, TaskRecord


class ExecutionLedger:
    """
    In-memory authoritative execution registry.
    Persistent backend will replace this later.
    """

    def __init__(self):
        self._lock = Lock()
        self._executions: Dict[str, ExecutionState] = {}

    def create(self, state: ExecutionState) -> ExecutionState:
        with self._lock:
            self._executions[state.execution_id] = state
        return state

    def get(self, execution_id: str) -> Optional[ExecutionState]:
        return self._executions.get(execution_id)

    def update(self, execution_id: str, state: ExecutionState) -> None:
        with self._lock:
            self._executions[execution_id] = state


# Persistent ledger foundation (Phase 5.9)
LEDGER_ROOT = Path.home() / ".localpilot" / "executions"


class PersistentExecutionLedger:
    def __init__(self, plan_id: str):
        self.execution_id = str(uuid.uuid4())
        self.path = LEDGER_ROOT / f"{self.execution_id}.json"
        self.model = ExecutionLedgerModel(
            execution_id=self.execution_id,
            plan_id=plan_id,
            status="running",
        )

    def save(self):
        LEDGER_ROOT.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self.model.json(indent=2), encoding="utf-8")

    @classmethod
    def load(cls, execution_id: str):
        path = LEDGER_ROOT / f"{execution_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        ledger = cls(data["plan_id"])
        ledger.execution_id = execution_id
        ledger.path = path
        ledger.model = ExecutionLedgerModel(**data)
        return ledger

    def record_task(
        self,
        task_id: str,
        status: str,
        diff_hash: str | None = None,
        files_changed: list[str] | None = None,
    ):
        self.model.tasks.append(
            TaskRecord(
                task_id=task_id,
                status=status, 
                diff_hash=diff_hash,
                files_changed=files_changed or [],
            )
        )
        self.model.current_task = task_id
        self.save()

    def complete(self):
        self.model.status = "completed"
        self.save()

```

</details>


## server/act_v2/ledger/models.py

*Size: 559 bytes | Modified: 2025-12-27T23:06:49.533Z*

<details>
<summary>View code</summary>

```python
from typing import List, Literal
from pydantic import BaseModel
import time


TaskStatus = Literal["pending", "done", "failed", "skipped"]
ExecutionStatus = Literal["running", "paused", "failed", "completed"]


class TaskRecord(BaseModel):
    task_id: str
    status: TaskStatus
    diff_hash: str | None = None
    files_changed: List[str] = []
    timestamp: float = time.time()


class ExecutionLedgerModel(BaseModel):
    execution_id: str
    plan_id: str
    status: ExecutionStatus
    current_task: str | None = None
    tasks: List[TaskRecord] = []

```

</details>


## server/act_v2/llm/__init__.py

*Size: 0 bytes | Modified: 2025-12-27T22:19:20.811Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/act_v2/llm/confined_prompt.py

*Size: 844 bytes | Modified: 2025-12-29T21:08:53.595Z*

<details>
<summary>View code</summary>

```python
import json
from typing import Dict, List


SYSTEM_PROMPT = """
You are operating in EXECUTION MODE.


Rules:
- You are executing EXACTLY ONE task.
- You may modify ONLY the allowed files.
- Output a VALID unified diff ONLY.
- Do NOT explain.
- Do NOT output markdown.
- Do NOT include JSON.
- If no changes are required, output an empty diff.

 - If the target file already exists, you MUST use a modify diff.
 - NEVER use /dev/null for existing files.
 - NEVER recreate an existing file.


Violating any rule is a critical failure.
""".strip()


def build_confined_prompt(context: Dict) -> List[Dict]:
    """
    Returns a sealed message list for the LLM.
    """

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": json.dumps(context, indent=2),
        },
    ]

```

</details>


## server/act_v2/llm/invocation_service.py

*Size: 763 bytes | Modified: 2025-12-29T21:08:20.849Z*

<details>
<summary>View code</summary>

```python
from pathlib import Path
from server.act_v2.llm.ollama_client import OllamaClient
from server.act_v2.llm.confined_prompt import build_confined_prompt
from server.act_v2.validation.diff_parser import extract_diff
from server.act_v2.diff_validator import DiffValidator


class InvocationService:
    def __init__(self, client: OllamaClient):
        self.client = client

    def invoke_task(self, task, context: dict) -> str:
        if not context:
            raise RuntimeError("Context missing")

        messages = build_confined_prompt(context)
        raw = self.client.invoke(messages)
        diff = extract_diff(raw)
        workspace = Path(context.get("workspace_root", "."))
        DiffValidator().validate(diff, task, workspace)
        return diff

```

</details>


## server/act_v2/llm/llm_client_stub.py

*Size: 239 bytes | Modified: 2025-12-27T22:19:53.245Z*

<details>
<summary>View code</summary>

```python
from typing import List, Dict


class LLMClientStub:
    """
    Placeholder for real LLM invocation (Phase 5.3).
    """

    def invoke(self, messages: List[Dict]) -> str:
        raise NotImplementedError("LLM execution not wired yet")

```

</details>


## server/act_v2/llm/ollama_client.py

*Size: 779 bytes | Modified: 2025-12-28T18:46:24.303Z*

<details>
<summary>View code</summary>

```python
import requests
from typing import List, Dict


class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def invoke(self, messages: List[Dict]) -> str:
        r = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "top_p": 1,
                    "num_ctx": 8192,
                    "repeat_penalty": 1.0,
                }
            },
            timeout=180
        )
        r.raise_for_status()
        return (r.json().get("message") or {}).get("content", "")

```

</details>


## server/act_v2/models/__init__.py

*Size: 0 bytes | Modified: 2025-12-27T22:07:07.894Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/act_v2/models/execution_state.py

*Size: 585 bytes | Modified: 2025-12-29T21:37:01.728Z*

<details>
<summary>View code</summary>

```python
from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any
from .execution_task import ExecutionTask


class ExecutionState(BaseModel):
    execution_id: str
    plan_id: str
    workspace_root: str
    status: Literal[
        "pending",
        "context_ready",
        "validated",
        "running",
        "awaiting_human",
        "failed",
        "completed",
    ]
    current_task_id: Optional[str]
    tasks: List[ExecutionTask]
    context: Optional[Dict[str, Any]] = None
    last_error: Optional[str] = None
    last_diff: Optional[str] = None

```

</details>


## server/act_v2/models/execution_task.py

*Size: 253 bytes | Modified: 2025-12-27T22:07:08.020Z*

<details>
<summary>View code</summary>

```python
from pydantic import BaseModel
from typing import List, Literal


class ExecutionTask(BaseModel):
    task_id: str
    title: str
    file_path: str
    action_type: Literal["create", "modify", "delete"]
    dependencies: List[str]
    order_index: int

```

</details>


## server/act_v2/validation/__init__.py

*Size: 0 bytes | Modified: 2025-12-27T22:28:14.134Z*

<details>
<summary>View code</summary>

```python

```

</details>


## server/act_v2/validation/diff_parser.py

*Size: 305 bytes | Modified: 2025-12-27T22:28:31.507Z*

<details>
<summary>View code</summary>

```python
import re


DIFF_HEADER = re.compile(r"^---\s+.+\n\+\+\+\s+.+", re.MULTILINE)


def extract_diff(diff_text: str) -> str:
    if not diff_text.strip():
        return ""

    if not DIFF_HEADER.search(diff_text):
        raise ValueError("Output is not a valid unified diff")

    return diff_text.strip()

```

</details>


## server/act_v2/validation/diff_validator.py

*Size: 920 bytes | Modified: 2025-12-27T22:29:20.254Z*

<details>
<summary>View code</summary>

```python
import re

from server.act_v2.models.execution_task import ExecutionTask
from .validation_errors import (
    FileScopeViolation,
    ActionTypeViolation,
    EmptyDiffNotAllowed,
)


FILE_HEADER = re.compile(r"^\+\+\+\s+b/(.+)", re.MULTILINE)


def validate_diff(diff: str, task: ExecutionTask) -> None:
    if not diff.strip():
        if task.action_type != "create":
            raise EmptyDiffNotAllowed("Task requires changes but diff is empty")
        return

    files = FILE_HEADER.findall(diff)
    if not files:
        raise FileScopeViolation("No target files detected")

    for f in files:
        if f != task.file_path:
            raise FileScopeViolation(
                f"Diff modifies unauthorized file: {f}"
            )

    if task.action_type == "delete":
        if not re.search(r"^---\s+b/", diff, re.MULTILINE):
            raise ActionTypeViolation("Delete action missing file removal")

```

</details>


## server/act_v2/validation/validation_errors.py

*Size: 287 bytes | Modified: 2025-12-30T20:23:55.572Z*

<details>
<summary>View code</summary>

```python
class DiffValidationError(Exception):
    pass


class FileScopeViolation(DiffValidationError):
    pass


class ActionTypeViolation(DiffValidationError):
    pass


class EmptyDiffNotAllowed(DiffValidationError):
    pass


class ContextMismatchViolation(DiffValidationError):
    pass

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

*Size: 1,530 bytes | Modified: 2025-12-30T20:29:40.978Z*

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
from server.plan.auto_fix import PlanAutoFixer


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


class AutoFixRequest(BaseModel):
    markdown: str


@router.post("/plan/auto-fix")
def auto_fix_plan(request: AutoFixRequest) -> Dict[str, Any]:
    parser = PlanParser()
    parsed = parser.parse(request.markdown)
    if not parsed.get("plan"):
        # keep consistent 400 style used above
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid plan JSON")

    workspace = Path.cwd()
    fixer = PlanAutoFixer(workspace)
    result = fixer.auto_fix(parsed["plan"])  # type: ignore[arg-type]

    return {
        "fixedPlan": result.fixed_plan,
        "warnings": result.warnings,
        "diff": result.diff,
    }

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

*Size: 1,439 bytes | Modified: 2025-12-29T19:01:47.233Z*

<details>
<summary>View code</summary>

```python
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState
import json

from server.chat.ollama_chat_client import OllamaChatClient

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        payload = await websocket.receive_json()

        model = payload.get("model")
        messages = payload.get("messages")

        client = OllamaChatClient(
            base_url="http://127.0.0.1:11434",
            model=model,
        )

        for token in client.stream_chat(messages):
            await websocket.send_text(json.dumps({
                "type": "token",
                "value": token
            }))

        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(json.dumps({ "type": "done" }))

    except (WebSocketDisconnect, ConnectionResetError):
        # Client disconnected; nothing to do
        pass
    except Exception as e:
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.send_text(json.dumps({
                "type": "error",
                "source": "backend",
                "message": str(e)
            }))
            await websocket.send_text(json.dumps({ "type": "done" }))
    finally:
        if websocket.client_state == WebSocketState.CONNECTED:
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

*Size: 2,120 bytes | Modified: 2025-12-29T19:00:02.422Z*

<details>
<summary>View code</summary>

```python
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import requests
import sys
import asyncio

from server.api.routes import query as query_routes
from server.api.routes import chat_ws
from server.api.routes import project as project_routes
from server.api.routes import index as index_routes
from server.api import plan as plan_api
from server.act_v2.api import router as act_v2_router

# Windows: prefer selector event loop to reduce WinError 10054 during client disconnects
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass


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
app.include_router(act_v2_router)

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


## server/plan/auto_fix/__init__.py

*Size: 62 bytes | Modified: 2025-12-30T20:29:29.817Z*

<details>
<summary>View code</summary>

```python
from .plan_auto_fixer import PlanAutoFixer, PlanAutoFixResult

```

</details>


## server/plan/auto_fix/plan_auto_fixer.py

*Size: 3,606 bytes | Modified: 2025-12-30T20:39:21.240Z*

<details>
<summary>View code</summary>

```python
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from copy import deepcopy
import json
import difflib


class PlanAutoFixResult:
    def __init__(self, fixed_plan: Dict[str, Any], warnings: List[str], diff: str):
        self.fixed_plan = fixed_plan
        self.warnings = warnings
        self.diff = diff


class PlanAutoFixer:
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()

    def auto_fix(self, plan: Dict[str, Any]) -> PlanAutoFixResult:
        original = deepcopy(plan)
        fixed = deepcopy(plan)
        warnings: List[str] = []

        tasks = fixed.get("tasks", []) or []
        for task in tasks:
            file_path = task.get("filePath")
            if not file_path:
                continue

            # Rule A — Absolute Paths → Relative Paths
            p = Path(file_path)
            if p.is_absolute():
                try:
                    task["filePath"] = str(p.resolve().relative_to(self.workspace_root))
                except Exception:
                    warnings.append(
                        f"Task '{task.get('id', '?')}' uses illegal absolute path: {file_path}"
                    )
                    # leave as-is; surfaced to user
                    continue

            # Normalize separators to POSIX style for consistency
            task["filePath"] = task["filePath"].replace("\\", "/")

            # Rule C — Directory in filePath → error (no auto-fix)
            if task["filePath"].endswith("/"):
                warnings.append(
                    f"Task '{task.get('id', '?')}' filePath points to a directory"
                )

            # Rule D — Multi-file paths in single task → warning only
            if "," in task["filePath"]:
                warnings.append(
                    f"Task '{task.get('id', '?')}' filePath appears to reference multiple files"
                )

            # Rule B — Modify on missing file → Create
            target = self.workspace_root / task["filePath"]
            if task.get("actionType") == "modify" and not target.exists():
                task["actionType"] = "create"
                warnings.append(
                    f"Task '{task.get('id', '?')}': actionType changed modify → create (file not found)"
                )

            # Rule F — Create on existing file → Modify
            if task.get("actionType") == "create" and target.exists():
                task["actionType"] = "modify"
                warnings.append(
                    f"Task '{task.get('id', '?')}': actionType changed create → modify (file already exists)"
                )

        # Rule E — Task ordering normalization (contiguous 0..N)
        try:
            tasks.sort(key=lambda t: t.get("orderIndex", 0))
            for i, t in enumerate(tasks):
                t["orderIndex"] = i
        except Exception:
            # if tasks not sortable, leave as-is
            pass

        diff = self._generate_diff(original, fixed)
        return PlanAutoFixResult(fixed, warnings, diff)

    def _generate_diff(self, before: Dict[str, Any], after: Dict[str, Any]) -> str:
        before_json = json.dumps(before, indent=2).splitlines(keepends=True)
        after_json = json.dumps(after, indent=2).splitlines(keepends=True)
        return "".join(
            difflib.unified_diff(
                before_json,
                after_json,
                fromfile="plan.json (original)",
                tofile="plan.json (auto-fixed)",
            )
        )

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

*Size: 5,435 bytes | Modified: 2025-12-28T22:16:33.008Z*

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

    "Your task is to output ONE VALID IMPLEMENTATION PLAN.\n"
    "You MUST output EXACTLY ONE JSON object inside a fenced ```json block.\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "ABSOLUTE RULES (NO EXCEPTIONS)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "1. Output ONE and ONLY ONE JSON object.\n"
    "2. JSON MUST be syntactically valid.\n"
    "3. JSON MUST match the schema EXACTLY.\n"
    "4. ALL fields are REQUIRED.\n"
    "5. NO extra fields are allowed.\n"
    "6. status MUST be \"draft\".\n"
    "7. orderIndex MUST start at 0 and increment by 1.\n"
    "8. tasks MUST NOT be empty.\n"
    "9. filePath MUST NEVER be empty.\n"
    "10. actionType MUST be create | modify | delete.\n\n"

    "STRICT RULES:\n"
    "- actionType MUST be one of: create | modify | delete\n"
    "- NEVER use actionType \"run\", \"test\", \"execute\", or similar\n"
    "- Tasks that describe running tests must be expressed as code changes\n"
    "  (e.g. adding test files), not execution steps\n"
    "- filePath MUST NEVER be empty\n\n"

    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "STRICT JSON SCHEMA\n"
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
    "SELF-CHECK LOOP (MANDATORY)\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "- Validate JSON against the schema.\n"
    "- Fix ALL errors BEFORE responding.\n"
    "- Do NOT explain.\n"
    "- Do NOT apologize.\n"
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
        for attempt in range(3):  # increase to 3 attempts
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
                    "The previous output was INVALID.\n"
                    "You MUST fix ALL schema violations.\n"
                    "Output ONLY a valid JSON plan."
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


