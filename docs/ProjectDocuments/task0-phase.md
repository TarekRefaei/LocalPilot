# 📄 PHASE_0_TASKS.md

# LocalPilot - Phase 0: Foundation Setup

> First sprint tasks to establish project foundation

---

## Document Information

| Field | Value |
|-------|-------|
| **Phase** | 0 - Foundation |
| **Goal** | Working project skeleton |
| **Est. Duration** | 1-2 weeks |
| **Prerequisites** | DEVELOPMENT_SETUP.md completed |

---

## Phase 0 Objectives

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 0 GOALS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  By the end of Phase 0, you will have:                          │
│                                                                  │
│  ✓ Complete project structure created                           │
│  ✓ Extension that activates in VS Code                          │
│  ✓ Python server that starts and responds                       │
│  ✓ Extension ↔ Server communication working                     │
│  ✓ Ollama connection verified                                   │
│  ✓ Basic WebView panel showing                                  │
│  ✓ All core entities and interfaces defined                    │
│  ✓ Tests running for both extension and server                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Task Overview

| # | Task | Type | Est. Time | NEW? |
|---|------|------|-----------|------|
| 0.1 | Create folder structure | Setup | 30 min | |
| 0.2 | Create core entities | Code | 1 hour | |
| 0.3 | Create core interfaces | Code | 1 hour | |
| 0.4 | Create core errors | Code | 30 min | |
| 0.5 | Create message protocol types | Code | 30 min | 
| 0.6 | Create Ollama service | Code | 2 hours | |
| 0.7 | Create Python server skeleton | Code | 1 hour | 
| 0.8 | Create Tree-sitter query files | Code | 1 hour |
| 0.9 | Create start-server script | Setup | 30 min | 
| 0.10 | Create API client | Code | 1 hour | |
| 0.11 | Create basic WebView | Code | 2 hours | |
| 0.12 | Wire extension activation | Code | 1 hour | |
| 0.13 | End-to-end verification | Test | 1 hour | |

---

## Task 0.1: Create Folder Structure

### Objective
Create all folders from PROJECT_STRUCTURE.md

### Instructions for Windsurf

```
Create the following folder structure inside the extension/ folder:

extension/src/
├── core/
│   ├── entities/
│   ├── interfaces/
│   ├── errors/
│   └── types/
├── features/
│   ├── indexing/
│   │   └── __tests__/
│   ├── chat/
│   │   └── __tests__/
│   ├── plan/
│   │   └── __tests__/
│   ├── act/
│   │   └── __tests__/
│   ├── ollama/
│   │   └── __tests__/
│   └── settings/
│       └── __tests__/
├── infrastructure/
│   ├── vscode/
│   ├── http/
│   └── websocket/
├── ui/
│   ├── webview/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── chat/
│   │   │   ├── plan/
│   │   │   ├── act/
│   │   │   ├── onboarding/
│   │   │   └── layout/
│   │   ├── hooks/
│   │   ├── store/
│   │   ├── styles/
│   │   ├── utils/
│   │   └── types/
│   ├── panels/
│   └── commands/
├── prompts/
└── utils/

Also create placeholder index.ts files in each folder that exports nothing for now:
// index.ts
export {};
```

### Verification
- [ ] All folders exist
- [ ] Each folder has an index.ts file
- [ ] No TypeScript errors

---

## Task 0.2: Create Core Entities

### Objective
Create all entity types from ARCHITECTURE.md

### Task 0.2.1: Message Entity

**File:** `extension/src/core/entities/message.entity.ts`

```
Create the Message entity file with these interfaces:

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  ragContext?: RAGContext;
  status?: 'streaming' | 'complete' | 'error';
  error?: string;
}

export interface RAGContext {
  chunks: RetrievedChunk[];
  query: string;
}

export interface RetrievedChunk {
  id: string;
  content: string;
  filePath: string;
  lineStart: number;
  lineEnd: number;
  chunkType: ChunkType;
  symbolName?: string;
  language: string;
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

Include JSDoc comments for each interface and type.
```

### Task 0.2.2: Plan Entity

**File:** `extension/src/core/entities/plan.entity.ts`

```
Create the Plan entity file with these interfaces:

export interface Plan {
  id: string;
  title: string;
  overview: string;
  tasks: Task[];
  createdAt: Date;
  updatedAt: Date;
  status: PlanStatus;
  sourceConversationId?: string;
}

export type PlanStatus = 
  | 'draft'
  | 'approved'
  | 'executing'
  | 'paused'
  | 'completed'
  | 'cancelled';

Include JSDoc comments.
```

### Task 0.2.3: Task Entity

**File:** `extension/src/core/entities/task.entity.ts`

```
Create the Task entity file:

export interface Task {
  id: string;
  orderIndex: number;
  title: string;
  description: string;
  filePath: string;
  actionType: TaskActionType;
  details: string[];
  dependencies: string[];
  status: TaskStatus;
  generatedCode?: string;
  diff?: string;
  error?: string;
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

Include JSDoc comments.
```

### Task 0.2.4: Project Entity

**File:** `extension/src/core/entities/project.entity.ts`

```
Create the Project entity file:

export interface Project {
  id: string;
  name: string;
  workspacePath: string;
  indexStatus: IndexStatus;
  lastIndexedAt: Date | null;
  stats: ProjectStats;
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

Include JSDoc comments.
```

### Task 0.2.5: Entities Index

**File:** `extension/src/core/entities/index.ts`

```
Create the entities barrel export file:

export * from './message.entity';
export * from './plan.entity';
export * from './task.entity';
export * from './project.entity';
```

### Verification
- [ ] All 4 entity files created
- [ ] index.ts exports all entities
- [ ] No TypeScript errors
- [ ] Can import: `import { Message, Plan, Task, Project } from '@core/entities'`

---

## Task 0.3: Create Core Interfaces

### Task 0.3.1: LLM Provider Interface

**File:** `extension/src/core/interfaces/llm-provider.interface.ts`

```
Create the LLM provider interface:

export interface ILLMProvider {
  isAvailable(): Promise<boolean>;
  listModels(): Promise<ModelInfo[]>;
  chat(request: ChatRequest): Promise<ChatResponse>;
  chatStream(request: ChatRequest): AsyncGenerator<string, void, unknown>;
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

Include JSDoc comments explaining what each interface is for.
```

### Task 0.3.2: RAG Provider Interface

**File:** `extension/src/core/interfaces/rag-provider.interface.ts`

```
Create the RAG provider interface:

import { RetrievedChunk, ChunkType, ProjectStats } from '../entities';

export interface IRAGProvider {
  startIndexing(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: IndexProgress) => void
  ): Promise<IndexResult>;
  
  syncIndex(
    workspacePath: string,
    projectId: string,
    onProgress: (progress: SyncProgress) => void
  ): Promise<SyncResult>;
  
  query(
    projectId: string,
    queryText: string,
    topK?: number,
    filters?: QueryFilters
  ): Promise<RetrievedChunk[]>;
  
  getProjectSummary(projectId: string): Promise<ProjectSummary>;
  isIndexed(projectId: string): Promise<boolean>;
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

Include JSDoc comments.
```

### Task 0.3.3: File System Interface

**File:** `extension/src/core/interfaces/file-system.interface.ts`

```
Create the file system interface:

export interface IFileSystem {
  readFile(filePath: string): Promise<string>;
  writeFile(filePath: string, content: string): Promise<void>;
  deleteFile(filePath: string): Promise<void>;
  exists(filePath: string): Promise<boolean>;
  createDirectory(dirPath: string): Promise<void>;
  listFiles(dirPath: string, recursive?: boolean): Promise<string[]>;
  stat(filePath: string): Promise<FileStat>;
  backup(filePath: string): Promise<string>;
  restore(backupPath: string, targetPath: string): Promise<void>;
  getWorkspaceRoot(): string | undefined;
}

export interface FileStat {
  isFile: boolean;
  isDirectory: boolean;
  size: number;
  modifiedAt: Date;
  createdAt: Date;
}

Include JSDoc comments.
```

### Task 0.3.4: Interfaces Index

**File:** `extension/src/core/interfaces/index.ts`

```
Create the interfaces barrel export:

export * from './llm-provider.interface';
export * from './rag-provider.interface';
export * from './file-system.interface';
```

### Verification
- [ ] All 3 interface files created
- [ ] index.ts exports all interfaces
- [ ] No TypeScript errors

---

## Task 0.4: Create Core Errors

### Task 0.4.1: Base Error

**File:** `extension/src/core/errors/base.error.ts`

```
Create the base error class:

export type ErrorCategory = 
  | 'connection'
  | 'indexing'
  | 'llm'
  | 'file'
  | 'validation';

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
    
    // Maintains proper stack trace in V8
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
      details: this.details
    };
  }
}
```

### Task 0.4.2: Ollama Errors

**File:** `extension/src/core/errors/ollama.error.ts`

```
Create Ollama-specific errors:

import { LocalPilotError } from './base.error';

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

export class OllamaModelNotFoundError extends LocalPilotError {
  readonly code = 'OLLAMA_MODEL_NOT_FOUND';
  readonly category = 'llm' as const;
  readonly recoverable = true;
  
  constructor(model: string) {
    super(
      `Model "${model}" not found. Run "ollama pull ${model}" to install.`,
      { model }
    );
  }
}

export class OllamaGenerationError extends LocalPilotError {
  readonly code = 'OLLAMA_GENERATION_FAILED';
  readonly category = 'llm' as const;
  readonly recoverable = true;
  
  constructor(message: string, model: string) {
    super(message, { model });
  }
}
```

### Task 0.4.3: Errors Index

**File:** `extension/src/core/errors/index.ts`

```
Create the errors barrel export:

export * from './base.error';
export * from './ollama.error';
```

### Verification
- [ ] Base error and Ollama errors created
- [ ] Exports working
- [ ] No TypeScript errors

---

## Task 0.5: Create Ollama Service

### Objective
Create the service that communicates with Ollama

### Task 0.5.1: Ollama Service Implementation

**File:** `extension/src/features/ollama/ollama.service.ts`

```
Create the Ollama service that implements ILLMProvider:

import { 
  ILLMProvider, 
  ModelInfo, 
  ChatRequest, 
  ChatResponse 
} from '@core/interfaces';
import { 
  OllamaConnectionError, 
  OllamaModelNotFoundError,
  OllamaGenerationError 
} from '@core/errors';

const DEFAULT_OLLAMA_URL = 'http://localhost:11434';

export class OllamaService implements ILLMProvider {
  private baseUrl: string;
  
  constructor(baseUrl: string = DEFAULT_OLLAMA_URL) {
    this.baseUrl = baseUrl;
  }
  
  async isAvailable(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/version`);
      return response.ok;
    } catch {
      return false;
    }
  }
  
  async listModels(): Promise<ModelInfo[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`);
      if (!response.ok) {
        throw new OllamaConnectionError(this.baseUrl);
      }
      
      const data = await response.json();
      return (data.models || []).map((model: any) => ({
        name: model.name,
        size: model.size,
        modifiedAt: new Date(model.modified_at),
        family: model.details?.family || 'unknown',
        parameterSize: model.details?.parameter_size || 'unknown',
        quantizationLevel: model.details?.quantization_level || 'unknown'
      }));
    } catch (error) {
      if (error instanceof OllamaConnectionError) throw error;
      throw new OllamaConnectionError(this.baseUrl, error as Error);
    }
  }
  
  async chat(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: request.model,
          messages: request.messages,
          stream: false,
          options: request.options
        })
      });
      
      if (!response.ok) {
        const error = await response.text();
        if (error.includes('model') && error.includes('not found')) {
          throw new OllamaModelNotFoundError(request.model);
        }
        throw new OllamaGenerationError(error, request.model);
      }
      
      const data = await response.json();
      return {
        content: data.message?.content || '',
        model: data.model,
        totalDuration: data.total_duration || 0,
        promptEvalCount: data.prompt_eval_count || 0,
        evalCount: data.eval_count || 0
      };
    } catch (error) {
      if (error instanceof OllamaConnectionError || 
          error instanceof OllamaModelNotFoundError ||
          error instanceof OllamaGenerationError) {
        throw error;
      }
      throw new OllamaConnectionError(this.baseUrl, error as Error);
    }
  }
  
  async *chatStream(request: ChatRequest): AsyncGenerator<string, void, unknown> {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: request.model,
        messages: request.messages,
        stream: true,
        options: request.options
      })
    });
    
    if (!response.ok || !response.body) {
      throw new OllamaConnectionError(this.baseUrl);
    }
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(line => line.trim());
      
      for (const line of lines) {
        try {
          const json = JSON.parse(line);
          if (json.message?.content) {
            yield json.message.content;
          }
        } catch {
          // Skip invalid JSON lines
        }
      }
    }
  }
  
  async embed(text: string, model: string = 'mxbai-embed-large'): Promise<number[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/embeddings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, prompt: text })
      });
      
      if (!response.ok) {
        throw new OllamaModelNotFoundError(model);
      }
      
      const data = await response.json();
      return data.embedding || [];
    } catch (error) {
      if (error instanceof OllamaModelNotFoundError) throw error;
      throw new OllamaConnectionError(this.baseUrl, error as Error);
    }
  }
}
```

### Task 0.5.2: Ollama Feature Index

**File:** `extension/src/features/ollama/index.ts`

```
Export the Ollama feature:

export { OllamaService } from './ollama.service';
```

### Task 0.5.3: Ollama Service Tests

**File:** `extension/src/features/ollama/__tests__/ollama.service.test.ts`

```
Create basic tests for OllamaService:

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { OllamaService } from '../ollama.service';

describe('OllamaService', () => {
  let service: OllamaService;
  
  beforeEach(() => {
    service = new OllamaService('http://localhost:11434');
  });
  
  describe('isAvailable', () => {
    it('should return true when Ollama is running', async () => {
      // Mock fetch
      global.fetch = vi.fn().mockResolvedValue({
        ok: true
      });
      
      const result = await service.isAvailable();
      expect(result).toBe(true);
    });
    
    it('should return false when Ollama is not running', async () => {
      global.fetch = vi.fn().mockRejectedValue(new Error('Connection refused'));
      
      const result = await service.isAvailable();
      expect(result).toBe(false);
    });
  });
  
  describe('listModels', () => {
    it('should return list of models', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({
          models: [
            { 
              name: 'qwen2.5-coder:7b', 
              size: 4700000000,
              modified_at: '2024-01-01T00:00:00Z',
              details: { family: 'qwen2', parameter_size: '7B' }
            }
          ]
        })
      });
      
      const models = await service.listModels();
      
      expect(models).toHaveLength(1);
      expect(models[0].name).toBe('qwen2.5-coder:7b');
    });
  });
});
```

### Verification
- [ ] OllamaService created and exports correctly
- [ ] Tests pass: `cd extension && pnpm test`
- [ ] No TypeScript errors

---

## Task 0.6: Create Python Server Skeleton

### Task 0.6.1: Server Structure

```
Create the following structure in server/src/:

server/src/
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── models.py
│   └── schemas/
│       ├── __init__.py
│       └── common.py
├── core/
│   ├── __init__.py
│   ├── entities/
│   │   └── __init__.py
│   ├── interfaces/
│   │   └── __init__.py
│   └── errors/
│       └── __init__.py
├── services/
│   └── __init__.py
├── infrastructure/
│   ├── __init__.py
│   └── ollama/
│       ├── __init__.py
│       └── client.py
└── config.py
```

### Task 0.6.2: Main FastAPI App

**File:** `server/src/api/main.py`

```python
"""
LocalPilot RAG Server

Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health, models

app = FastAPI(
    title="LocalPilot RAG Server",
    description="Local RAG server for LocalPilot VS Code extension",
    version="0.1.0"
)

# CORS for VS Code extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(models.router, prefix="/api", tags=["Models"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=52741)
```

### Task 0.6.3: Health Route

**File:** `server/src/api/routes/health.py`

```python
"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }
```

### Task 0.6.4: Models Route

**File:** `server/src/api/routes/models.py`

```python
"""Model-related endpoints."""

from fastapi import APIRouter
from typing import List
import httpx

router = APIRouter()

OLLAMA_URL = "http://localhost:11434"


@router.get("/models")
async def list_models():
    """List available Ollama models."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return {"models": data.get("models", [])}
            return {"models": [], "error": "Failed to fetch models"}
    except Exception as e:
        return {"models": [], "error": str(e)}
```

### Task 0.6.5: Routes Init

**File:** `server/src/api/routes/__init__.py`

```python
"""API routes."""
from . import health, models
```

### Verification
- [ ] Server starts: `cd server/src/api && python main.py`
- [ ] Health check works: `curl http://localhost:52741/health`
- [ ] Models endpoint works: `curl http://localhost:52741/api/models`

---

## Task 0.7: Create API Client

### Objective
Create HTTP client in extension to communicate with Python server

### Task 0.7.1: API Client

**File:** `extension/src/infrastructure/http/api-client.ts`

```
Create the API client:

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  status: number;
}

export class ApiClient {
  private baseUrl: string;
  
  constructor(baseUrl: string = 'http://localhost:52741') {
    this.baseUrl = baseUrl;
  }
  
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`);
      const data = await response.json();
      
      return {
        data: response.ok ? data : null,
        error: response.ok ? null : data.error || 'Request failed',
        status: response.status
      };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 0
      };
    }
  }
  
  async post<T>(endpoint: string, body: unknown): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      
      return {
        data: response.ok ? data : null,
        error: response.ok ? null : data.error || 'Request failed',
        status: response.status
      };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 0
      };
    }
  }
  
  async healthCheck(): Promise<boolean> {
    const response = await this.get<{ status: string }>('/health');
    return response.data?.status === 'healthy';
  }
}
```

### Task 0.7.2: HTTP Infrastructure Index

**File:** `extension/src/infrastructure/http/index.ts`

```
Export HTTP infrastructure:

export { ApiClient } from './api-client';
export type { ApiResponse } from './api-client';
```

### Verification
- [ ] ApiClient compiles without errors
- [ ] Exports correctly

---

## Task 0.8: Create Basic WebView

### Task 0.8.1: WebView Provider

**File:** `extension/src/ui/panels/webview-provider.ts`

```
Create the WebView provider:

import * as vscode from 'vscode';

export class LocalPilotViewProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'localpilot.mainView';
  
  private _view?: vscode.WebviewView;
  
  constructor(private readonly _extensionUri: vscode.Uri) {}
  
  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    _context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ): void {
    this._view = webviewView;
    
    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri]
    };
    
    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
    
    // Handle messages from webview
    webviewView.webview.onDidReceiveMessage(
      message => {
        switch (message.type) {
          case 'ready':
            console.log('WebView is ready');
            break;
        }
      }
    );
  }
  
  private _getHtmlForWebview(webview: vscode.Webview): string {
    return `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LocalPilot</title>
        <style>
          body {
            padding: 20px;
            color: var(--vscode-foreground);
            font-family: var(--vscode-font-family);
          }
          h1 {
            font-size: 1.5em;
            margin-bottom: 10px;
          }
          .status {
            padding: 10px;
            background: var(--vscode-editor-background);
            border-radius: 4px;
            margin-top: 10px;
          }
          .status-item {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
          }
        </style>
      </head>
      <body>
        <h1>🧭 LocalPilot</h1>
        <p>Privacy-First AI Pair Programming</p>
        
        <div class="status">
          <div class="status-item">
            <span>Extension Status:</span>
            <span>✅ Active</span>
          </div>
          <div class="status-item">
            <span>Server Status:</span>
            <span id="server-status">Checking...</span>
          </div>
          <div class="status-item">
            <span>Ollama Status:</span>
            <span id="ollama-status">Checking...</span>
          </div>
        </div>
        
        <script>
          const vscode = acquireVsCodeApi();
          vscode.postMessage({ type: 'ready' });
        </script>
      </body>
      </html>
    `;
  }
  
  public postMessage(message: unknown): void {
    this._view?.webview.postMessage(message);
  }
}
```

### Task 0.8.2: Panels Index

**File:** `extension/src/ui/panels/index.ts`

```
Export panels:

export { LocalPilotViewProvider } from './webview-provider';
```

### Verification
- [ ] WebView provider compiles
- [ ] Exports correctly

---

## Task 0.9: Wire Extension Activation

### Task 0.9.1: Update Extension Entry Point

**File:** `extension/src/extension.ts`

```
Update the main extension file:

import * as vscode from 'vscode';
import { LocalPilotViewProvider } from './ui/panels';
import { OllamaService } from './features/ollama';
import { ApiClient } from './infrastructure/http';

let ollamaService: OllamaService;
let apiClient: ApiClient;

export async function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot is activating...');
  
  // Initialize services
  ollamaService = new OllamaService();
  apiClient = new ApiClient();
  
  // Register WebView provider
  const provider = new LocalPilotViewProvider(context.extensionUri);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      LocalPilotViewProvider.viewType,
      provider
    )
  );
  
  // Check connections
  const ollamaAvailable = await ollamaService.isAvailable();
  const serverAvailable = await apiClient.healthCheck();
  
  console.log(`Ollama available: ${ollamaAvailable}`);
  console.log(`Server available: ${serverAvailable}`);
  
  // Show status
  if (!ollamaAvailable) {
    vscode.window.showWarningMessage(
      'LocalPilot: Ollama is not running. Please start Ollama.'
    );
  }
  
  if (!serverAvailable) {
    vscode.window.showWarningMessage(
      'LocalPilot: Python server is not running.'
    );
  }
  
  // Register commands
  const startIndexing = vscode.commands.registerCommand(
    'localpilot.startIndexing',
    () => {
      vscode.window.showInformationMessage('Indexing will start here!');
    }
  );
  
  context.subscriptions.push(startIndexing);
  
  console.log('LocalPilot activated successfully!');
}

export function deactivate() {
  console.log('LocalPilot deactivated');
}
```

### Verification
- [ ] Build succeeds: `pnpm run build`
- [ ] Extension activates in VS Code (F5)
- [ ] Sidebar panel shows "LocalPilot"
- [ ] Console shows connection status

---

## Task 0.10: End-to-End Verification

### Verification Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│                 PHASE 0 COMPLETION CHECKLIST                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STRUCTURE                                                       │
│  □ All folders exist per PROJECT_STRUCTURE.md                  │
│  □ All index.ts files export correctly                          │
│                                                                  │
│  CORE                                                            │
│  □ All entities compile and export                              │
│  □ All interfaces compile and export                            │
│  □ All errors compile and export                                │
│                                                                  │
│  EXTENSION                                                       │
│  □ pnpm run build succeeds                                      │
│  □ pnpm test passes                                             │
│  □ F5 opens new VS Code window                                  │
│  □ LocalPilot appears in sidebar                                │
│  □ WebView shows status panel                                   │
│                                                                  │
│  SERVER                                                          │
│  □ python main.py starts server                                 │
│  □ /health returns healthy                                      │
│  □ /api/models returns model list                               │
│                                                                  │
│  INTEGRATION                                                     │
│  □ Extension detects Ollama running                             │
│  □ Extension detects Python server running                      │
│  □ No errors in console                                         │
│                                                                  │
│  GIT                                                             │
│  □ All files committed                                          │
│  □ Tag created: v0.1.0-alpha                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Final Commit

```powershell
git add .
git commit -m "feat: complete Phase 0 foundation setup

- Created project structure
- Added core entities, interfaces, errors
- Implemented OllamaService with tests
- Created Python server skeleton
- Added API client for server communication
- Implemented basic WebView panel
- Wired extension activation"

git tag v0.1.0-alpha
```

---

## Next Phase Preview

After completing Phase 0, you're ready for **Phase 1: Ollama Integration**:

- Complete Ollama service with all methods
- Model selection UI
- Connection management
- Settings integration

---

*Document Version: 1.0.0*
```