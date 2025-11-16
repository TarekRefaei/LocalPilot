# 📄 DOCUMENT #5: DATA_MODELS.md
# LocalPilot - Data Models & Schemas

**Version:** 1.0  
**Date:** January 2025  
**Status:** Foundation  
**Author:** LocalPilot Data Team

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [TypeScript Models (Extension)](#typescript-models-extension)
3. [Python Models (Backend)](#python-models-backend)
4. [Shared Types](#shared-types)
5. [Database Schemas](#database-schemas)
6. [Validation Rules](#validation-rules)
7. [Example Data](#example-data)
8. [Migration Strategy](#migration-strategy)

---

## 🎯 Overview

### Model Organization

```
Data Models Architecture:

┌─────────────────────────────────────────────────────────────┐
│                    Extension (TypeScript)                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  TypeScript Interfaces                                 │ │
│  │  - UI state models                                     │ │
│  │  - WebSocket message types                             │ │
│  │  - VS Code API integration types                       │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    JSON over WebSocket
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Backend (Python)                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Pydantic Models                                       │ │
│  │  - Request/Response validation                         │ │
│  │  - Business logic models                               │ │
│  │  - Database models                                     │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    Storage Layer                            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐ │
│  │   ChromaDB       │  │   SQLite         │  │   Files   │ │
│  │   (Vectors)      │  │   (Metadata)     │  │   (Cache) │ │
│  └──────────────────┘  └──────────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Naming Conventions

```yaml
TypeScript:
  Interfaces: PascalCase (e.g., ChatMessage)
  Enums: PascalCase (e.g., IndexingPhase)
  Properties: camelCase (e.g., messageId)
  
Python:
  Classes: PascalCase (e.g., ChatMessage)
  Enums: PascalCase (e.g., IndexingPhase)
  Fields: snake_case (e.g., message_id)
  
Shared Identifiers:
  IDs: {entity}-{timestamp}-{random} (e.g., chat-20250115-103045)
  Timestamps: ISO 8601 UTC (e.g., 2025-01-15T10:30:45Z)
```

---

## 🔷 TypeScript Models (Extension)

### Location: `/extension/src/models/` and `/shared/types/`

### Core Types

```typescript
// shared/types/common.ts

/**
 * Unique identifier type
 */
export type UUID = string;

/**
 * ISO 8601 timestamp
 */
export type Timestamp = string;

/**
 * File path (absolute or workspace-relative)
 */
export type FilePath = string;

/**
 * Percentage (0-100)
 */
export type Percentage = number;
```

---

### Indexing Models

```typescript
// shared/types/indexing.ts

/**
 * Indexing phases
 */
export enum IndexingPhase {
  DISCOVERY = 'discovery',
  DOCUMENTATION = 'documentation',
  STRUCTURE = 'structure',
  CHUNKING = 'chunking',
  SUMMARIZATION = 'summarization',
  COMPLETE = 'complete'
}

/**
 * Indexing status
 */
export enum IndexingStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

/**
 * Indexing options for starting indexing process
 */
export interface IndexingOptions {
  /** Patterns to exclude from indexing (glob patterns) */
  excludePatterns: string[];
  
  /** Maximum file size in MB */
  maxFileSizeMb: number;
  
  /** Programming languages to index (empty = all) */
  languages: string[];
  
  /** Force re-indexing even if cache exists */
  forceReindex: boolean;
}

/**
 * Indexing progress update
 */
export interface IndexingProgress {
  /** Unique indexing operation ID */
  indexingId: string;
  
  /** Current phase */
  phase: IndexingPhase;
  
  /** Phase number (1-5) */
  phaseNumber: number;
  
  /** Total phases (always 5) */
  totalPhases: number;
  
  /** Current file being processed */
  currentFile: number;
  
  /** Total files to process */
  totalFiles: number;
  
  /** Current file path */
  currentFilePath?: string;
  
  /** Overall percentage (0-100) */
  percentage: Percentage;
  
  /** Estimated time remaining in seconds */
  estimatedTimeRemainingSeconds: number;
  
  /** Human-readable status message */
  message: string;
}

/**
 * Indexing statistics after completion
 */
export interface IndexingStatistics {
  /** Total files discovered */
  totalFiles: number;
  
  /** Files successfully indexed */
  indexedFiles: number;
  
  /** Files that failed to index */
  failedFiles: number;
  
  /** Total semantic chunks created */
  totalChunks: number;
  
  /** Total embeddings generated */
  totalEmbeddings: number;
  
  /** Total symbols extracted (functions, classes, etc.) */
  totalSymbols: number;
  
  /** Index size in megabytes */
  indexSizeMb: number;
}

/**
 * Failed file information
 */
export interface FailedFile {
  /** File path */
  path: FilePath;
  
  /** Error message */
  error: string;
  
  /** Error code (optional) */
  errorCode?: string;
}

/**
 * Complete indexing result
 */
export interface IndexingResult {
  /** Unique indexing operation ID */
  indexingId: string;
  
  /** Duration in seconds */
  durationSeconds: number;
  
  /** Statistics */
  statistics: IndexingStatistics;
  
  /** AI-generated project summary */
  projectSummary: string;
  
  /** List of failed files */
  failedFiles: FailedFile[];
  
  /** Timestamp when indexing started */
  startedAt: Timestamp;
  
  /** Timestamp when indexing completed */
  completedAt: Timestamp;
}
```

---

### Chat Models

```typescript
// shared/types/chat.ts

/**
 * Message role
 */
export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system'
}

/**
 * Chat message
 */
export interface ChatMessage {
  /** Unique message ID */
  id: string;
  
  /** Message role */
  role: MessageRole;
  
  /** Message content */
  content: string;
  
  /** Timestamp */
  timestamp: Timestamp;
  
  /** Metadata (optional) */
  metadata?: ChatMessageMetadata;
}

/**
 * Chat message metadata
 */
export interface ChatMessageMetadata {
  /** Model used for generation */
  model?: string;
  
  /** Tokens generated */
  tokens?: number;
  
  /** Generation time in seconds */
  generationTimeSeconds?: number;
  
  /** Whether RAG context was used */
  ragContextUsed?: boolean;
  
  /** Number of context chunks retrieved */
  contextChunksRetrieved?: number;
}

/**
 * RAG context chunk
 */
export interface RAGContextChunk {
  /** File path */
  filePath: FilePath;
  
  /** Start line */
  startLine: number;
  
  /** End line */
  endLine: number;
  
  /** Code content */
  content: string;
  
  /** Relevance score (0-1) */
  relevanceScore: number;
}

/**
 * RAG context
 */
export interface RAGContext {
  /** Retrieved chunks */
  chunks: RAGContextChunk[];
  
  /** Total tokens in context */
  totalTokens: number;
  
  /** Relevance scores */
  relevanceScores: number[];
  
  /** Query used for retrieval */
  query: string;
}

/**
 * Chat session
 */
export interface ChatSession {
  /** Unique session ID */
  id: string;
  
  /** Session title (auto-generated or user-defined) */
  title: string;
  
  /** Messages in session */
  messages: ChatMessage[];
  
  /** Current RAG context (if any) */
  context?: RAGContext;
  
  /** Suggested plan (if any) */
  suggestedPlan?: PlanSuggestion;
  
  /** Workspace path */
  workspacePath: string;
  
  /** Created timestamp */
  createdAt: Timestamp;
  
  /** Last updated timestamp */
  updatedAt: Timestamp;
}

/**
 * Plan suggestion from chat
 */
export interface PlanSuggestion {
  /** Suggested title */
  title: string;
  
  /** Description */
  description: string;
  
  /** Goals/objectives */
  goals: string[];
  
  /** Estimated complexity */
  estimatedComplexity: 'low' | 'medium' | 'high';
  
  /** Confidence score (0-1) */
  confidence: number;
}

/**
 * Chat options
 */
export interface ChatOptions {
  /** Enable streaming response */
  stream: boolean;
  
  /** Maximum tokens to generate */
  maxTokens: number;
  
  /** Temperature (0-1) */
  temperature: number;
  
  /** Enable RAG context retrieval */
  retrieveContext: boolean;
  
  /** Model to use (optional, uses default if not specified) */
  model?: string;
}

/**
 * Chat context (current user environment)
 */
export interface ChatContext {
  /** File user is currently viewing */
  currentFile?: FilePath;
  
  /** Selected/highlighted code */
  selectedCode?: string;
  
  /** Workspace path */
  workspacePath: string;
  
  /** Active tab/mode */
  activeMode?: 'chat' | 'plan' | 'act';
}
```

---

### Plan Models

```typescript
// shared/types/plan.ts

/**
 * Plan status
 */
export enum PlanStatus {
  DRAFT = 'draft',
  READY = 'ready',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

/**
 * TODO item status
 */
export enum TodoStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  SKIPPED = 'skipped'
}

/**
 * File operation type
 */
export enum FileOperationType {
  CREATE = 'create',
  MODIFY = 'modify',
  DELETE = 'delete',
  RESEARCH = 'research'  // For TODO items that don't modify files
}

/**
 * File to be affected by TODO
 */
export interface TodoFile {
  /** File path */
  path: FilePath;
  
  /** Operation type */
  operation: FileOperationType;
  
  /** Estimated changes */
  estimatedChanges?: string;  // e.g., "+45 lines"
}

/**
 * TODO item
 */
export interface TodoItem {
  /** Unique TODO ID */
  id: string;
  
  /** Title */
  title: string;
  
  /** Detailed description */
  description: string;
  
  /** Primary operation type */
  type: FileOperationType;
  
  /** Files affected */
  files: TodoFile[];
  
  /** IDs of prerequisite TODOs */
  dependencies: string[];
  
  /** Current status */
  status: TodoStatus;
  
  /** Detailed instructions for AI (Act mode) */
  aiInstructions: string;
  
  /** Order/index in plan */
  order: number;
  
  /** Error message (if failed) */
  error?: string;
}

/**
 * Plan
 */
export interface Plan {
  /** Unique plan ID */
  id: string;
  
  /** Source chat session (if created from chat) */
  fromChatSession?: string;
  
  /** Plan title */
  title: string;
  
  /** Overview/description */
  overview: string;
  
  /** TODO items */
  todos: TodoItem[];
  
  /** Current status */
  status: PlanStatus;
  
  /** Estimated complexity */
  complexity: 'low' | 'medium' | 'high';
  
  /** Estimated duration in minutes */
  estimatedDurationMinutes?: number;
  
  /** Workspace path */
  workspacePath: string;
  
  /** Created timestamp */
  createdAt: Timestamp;
  
  /** Last updated timestamp */
  updatedAt: Timestamp;
  
  /** Execution history */
  executionHistory: ExecutionSummary[];
}

/**
 * Execution summary (for plan history)
 */
export interface ExecutionSummary {
  /** Execution ID */
  executionId: string;
  
  /** Started timestamp */
  startedAt: Timestamp;
  
  /** Completed timestamp */
  completedAt?: Timestamp;
  
  /** Status */
  status: 'in_progress' | 'completed' | 'failed' | 'cancelled';
  
  /** TODOs completed */
  todosCompleted: number;
  
  /** TODOs failed */
  todosFailed: number;
  
  /** TODOs skipped */
  todosSkipped: number;
}
```

---

### Act Mode Models

```typescript
// shared/types/act.ts

/**
 * Execution status
 */
export enum ExecutionStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

/**
 * File operation
 */
export interface FileOperation {
  /** Unique operation ID */
  operationId: string;
  
  /** Operation type */
  type: FileOperationType;
  
  /** File path */
  path: FilePath;
  
  /** New content (for create/modify) */
  content?: string;
  
  /** Diff (unified diff format) */
  diff?: string;
  
  /** Preview (shortened version) */
  preview?: string;
  
  /** Requires user approval */
  requiresApproval: boolean;
  
  /** Metadata */
  metadata?: FileOperationMetadata;
}

/**
 * File operation metadata
 */
export interface FileOperationMetadata {
  /** Lines added */
  additions: number;
  
  /** Lines deleted */
  deletions: number;
  
  /** Programming language */
  language: string;
  
  /** File size (bytes) */
  fileSize?: number;
}

/**
 * Approval decision
 */
export enum ApprovalDecision {
  APPROVE = 'approve',
  REJECT = 'reject',
  EDIT = 'edit',
  SKIP = 'skip'
}

/**
 * Approval request
 */
export interface ApprovalRequest {
  /** Execution ID */
  executionId: string;
  
  /** TODO ID */
  todoId: string;
  
  /** File operations to approve */
  fileOperations: FileOperation[];
  
  /** Timeout in seconds */
  approvalTimeoutSeconds: number;
  
  /** Requested timestamp */
  requestedAt: Timestamp;
}

/**
 * Approval response
 */
export interface ApprovalResponse {
  /** Execution ID */
  executionId: string;
  
  /** TODO ID */
  todoId: string;
  
  /** Decision */
  decision: ApprovalDecision;
  
  /** Edited operations (if decision = edit) */
  editedOperations?: FileOperation[];
  
  /** Timestamp */
  respondedAt: Timestamp;
}

/**
 * Execution log entry
 */
export interface ExecutionLogEntry {
  /** Entry ID */
  id: string;
  
  /** TODO ID */
  todoId: string;
  
  /** Entry type */
  type: 'info' | 'success' | 'warning' | 'error';
  
  /** Message */
  message: string;
  
  /** Timestamp */
  timestamp: Timestamp;
  
  /** Additional data */
  data?: any;
}

/**
 * Git commit info
 */
export interface GitCommitInfo {
  /** Commit hash */
  hash: string;
  
  /** Commit message */
  message: string;
  
  /** Author */
  author?: string;
  
  /** Timestamp */
  timestamp?: Timestamp;
}

/**
 * File change (for summary)
 */
export interface FileChange {
  /** File path */
  path: FilePath;
  
  /** Change type */
  type: FileOperationType;
  
  /** Lines added */
  additions: number;
  
  /** Lines deleted */
  deletions: number;
}

/**
 * Act session (execution state)
 */
export interface ActSession {
  /** Unique execution ID */
  executionId: string;
  
  /** Plan ID */
  planId: string;
  
  /** Current TODO ID */
  currentTodoId?: string;
  
  /** Execution status */
  status: ExecutionStatus;
  
  /** Git branch */
  gitBranch?: string;
  
  /** Base Git commit */
  baseCommit?: string;
  
  /** Execution log */
  executionLog: ExecutionLogEntry[];
  
  /** Generated file changes */
  generatedFiles: FileChange[];
  
  /** Git commits made */
  commits: GitCommitInfo[];
  
  /** Started timestamp */
  startedAt: Timestamp;
  
  /** Completed timestamp */
  completedAt?: Timestamp;
  
  /** Error (if failed) */
  error?: string;
}

/**
 * Execution options
 */
export interface ExecutionOptions {
  /** Auto-approve all changes (dangerous!) */
  autoApprove: boolean;
  
  /** Create Git branch */
  createGitBranch: boolean;
  
  /** Custom Git branch name */
  gitBranchName?: string;
  
  /** Model to use for code generation */
  model?: string;
  
  /** Timeout per TODO in seconds */
  timeoutPerTodoSeconds: number;
}
```

---

### System Models

```typescript
// shared/types/system.ts

/**
 * Model type
 */
export enum ModelType {
  CHAT = 'chat',
  EMBEDDING = 'embedding',
  CODE_GENERATION = 'code_generation'
}

/**
 * Model info
 */
export interface ModelInfo {
  /** Model ID/name */
  id: string;
  
  /** Display name */
  name: string;
  
  /** Model type */
  type: ModelType;
  
  /** Size in GB */
  sizeGb: number;
  
  /** Context window (tokens) */
  contextWindow?: number;
  
  /** Embedding dimensions (for embedding models) */
  dimensions?: number;
  
  /** Capabilities */
  capabilities: string[];
  
  /** Currently loaded in memory */
  loaded: boolean;
  
  /** Recommended use cases */
  recommendedFor: string[];
}

/**
 * System resources
 */
export interface SystemResources {
  /** VRAM usage in GB */
  vramUsageGb: number;
  
  /** Total VRAM in GB */
  vramTotalGb: number;
  
  /** RAM usage in GB */
  ramUsageGb: number;
  
  /** Total RAM in GB */
  ramTotalGb: number;
  
  /** CPU usage percentage */
  cpuUsagePercent?: number;
  
  /** Disk usage in GB */
  diskUsageGb?: number;
}

/**
 * Health status
 */
export interface HealthStatus {
  /** Overall status */
  status: 'healthy' | 'degraded' | 'unhealthy';
  
  /** Backend version */
  version: string;
  
  /** Uptime in seconds */
  uptimeSeconds: number;
  
  /** Service statuses */
  services: {
    ollama: ServiceStatus;
    vectorDb: ServiceStatus;
  };
  
  /** Resource usage */
  resources: SystemResources;
  
  /** Timestamp */
  timestamp: Timestamp;
}

/**
 * Service status
 */
export interface ServiceStatus {
  /** Status */
  status: 'connected' | 'disconnected' | 'error';
  
  /** Additional info */
  info?: any;
  
  /** Error message (if error) */
  error?: string;
}

/**
 * VRAM warning
 */
export interface VRAMWarning {
  /** Warning level */
  level: 'warning' | 'critical';
  
  /** Current usage in GB */
  currentUsageGb: number;
  
  /** Total VRAM in GB */
  totalVramGb: number;
  
  /** Usage percentage */
  usagePercentage: number;
  
  /** Loaded models */
  loadedModels: Array<{
    name: string;
    vramGb: number;
  }>;
  
  /** Recommendation */
  recommendation: string;
}

/**
 * Model swap event
 */
export interface ModelSwapEvent {
  /** Model being unloaded */
  unloading?: string;
  
  /** Model being loaded */
  loading: string;
  
  /** Reason for swap */
  reason: string;
  
  /** Estimated duration in seconds */
  estimatedDurationSeconds: number;
  
  /** Timestamp */
  timestamp: Timestamp;
}
```

---

### Configuration Models

```typescript
// shared/types/config.ts

/**
 * Model configuration
 */
export interface ModelConfiguration {
  /** Embedding model */
  embedding: string;
  
  /** Chat model */
  chat: string;
  
  /** Planning model */
  planning: string;
  
  /** Coding model */
  coding: string;
}

/**
 * Indexing configuration
 */
export interface IndexingConfiguration {
  /** Exclude patterns */
  excludePatterns: string[];
  
  /** Max file size in MB */
  maxFileSizeMb: number;
  
  /** Chunk size (tokens) */
  chunkSize: number;
  
  /** Chunk overlap (tokens) */
  chunkOverlap: number;
}

/**
 * Safety configuration
 */
export interface SafetyConfiguration {
  /** Require Git repository for Act mode */
  requireGitRepo: boolean;
  
  /** Check for uncommitted changes */
  checkUncommittedChanges: boolean;
  
  /** Auto-approve new files */
  autoApproveNewFiles: boolean;
  
  /** Auto-approve config file changes */
  autoApproveConfigChanges: boolean;
}

/**
 * Ollama configuration
 */
export interface OllamaConfiguration {
  /** Ollama host URL */
  host: string;
  
  /** Request timeout in seconds */
  timeoutSeconds: number;
}

/**
 * Full configuration
 */
export interface Configuration {
  /** Ollama config */
  ollama: OllamaConfiguration;
  
  /** Model config */
  models: ModelConfiguration;
  
  /** Indexing config */
  indexing: IndexingConfiguration;
  
  /** Safety config */
  safety: SafetyConfiguration;
}
```

---

### Error Models

```typescript
// shared/types/error.ts

/**
 * Error codes
 */
export enum ErrorCode {
  // Connection errors (1xxx)
  WEBSOCKET_CONNECTION_FAILED = '1001',
  WEBSOCKET_TIMEOUT = '1002',
  HANDSHAKE_FAILED = '1003',
  
  // LLM errors (2xxx)
  LLM_CONNECTION_FAILED = '2001',
  LLM_TIMEOUT = '2002',
  LLM_MODEL_NOT_FOUND = '2003',
  LLM_GENERATION_FAILED = '2004',
  LLM_CONTEXT_TOO_LARGE = '2005',
  
  // Indexing errors (3xxx)
  INDEXING_FAILED = '3001',
  PARSING_FAILED = '3002',
  EMBEDDING_FAILED = '3003',
  VECTOR_DB_ERROR = '3004',
  
  // Plan errors (4xxx)
  PLAN_GENERATION_FAILED = '4001',
  PLAN_NOT_FOUND = '4002',
  INVALID_PLAN = '4003',
  
  // Act errors (5xxx)
  EXECUTION_FAILED = '5001',
  GIT_ERROR = '5002',
  FILE_OPERATION_FAILED = '5003',
  COMPILATION_ERROR = '5004',
  APPROVAL_TIMEOUT = '5005',
  
  // Resource errors (6xxx)
  VRAM_OVERFLOW = '6001',
  RAM_OVERFLOW = '6002',
  DISK_FULL = '6003',
  
  // System errors (9xxx)
  INTERNAL_ERROR = '9001',
  INVALID_REQUEST = '9002',
  NOT_IMPLEMENTED = '9003'
}

/**
 * Recovery option
 */
export interface RecoveryOption {
  /** Action identifier */
  action: string;
  
  /** Human-readable description */
  description: string;
  
  /** Parameters for action */
  parameters?: Record<string, any>;
}

/**
 * Error response
 */
export interface ErrorResponse {
  /** Error code */
  code: ErrorCode | string;
  
  /** Human-readable message */
  message: string;
  
  /** Additional details */
  details?: any;
  
  /** Timestamp */
  timestamp: Timestamp;
  
  /** Request ID (if applicable) */
  requestId?: string;
  
  /** Recovery options */
  recoveryOptions?: RecoveryOption[];
}
```

---

## 🐍 Python Models (Backend)

### Location: `/backend/src/models/`

### Base Models

```python
# backend/src/models/base.py

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum

class TimestampedModel(BaseModel):
    """Base model with timestamp fields"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + 'Z'
        }

class IdentifiedModel(TimestampedModel):
    """Base model with ID and timestamps"""
    id: str = Field(..., description="Unique identifier")
```

---

### Indexing Models

```python
# backend/src/models/indexing.py

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from enum import Enum
from .base import IdentifiedModel

class IndexingPhase(str, Enum):
    """Indexing phases"""
    DISCOVERY = 'discovery'
    DOCUMENTATION = 'documentation'
    STRUCTURE = 'structure'
    CHUNKING = 'chunking'
    SUMMARIZATION = 'summarization'
    COMPLETE = 'complete'

class IndexingStatus(str, Enum):
    """Indexing status"""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class IndexingOptions(BaseModel):
    """Options for indexing"""
    exclude_patterns: List[str] = Field(
        default=['node_modules', '.git', 'dist', 'build'],
        description="Patterns to exclude"
    )
    max_file_size_mb: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum file size in MB"
    )
    languages: List[str] = Field(
        default=[],
        description="Languages to index (empty = all)"
    )
    force_reindex: bool = Field(
        default=False,
        description="Force re-indexing"
    )

class IndexingProgress(BaseModel):
    """Indexing progress update"""
    indexing_id: str
    phase: IndexingPhase
    phase_number: int = Field(ge=1, le=5)
    total_phases: int = Field(default=5)
    current_file: int = Field(ge=0)
    total_files: int = Field(ge=0)
    current_file_path: Optional[str] = None
    percentage: float = Field(ge=0, le=100)
    estimated_time_remaining_seconds: int = Field(ge=0)
    message: str
    
    @validator('percentage')
    def round_percentage(cls, v):
        return round(v, 1)

class IndexingStatistics(BaseModel):
    """Indexing statistics"""
    total_files: int
    indexed_files: int
    failed_files: int
    total_chunks: int
    total_embeddings: int
    total_symbols: int
    index_size_mb: float

class FailedFile(BaseModel):
    """Failed file information"""
    path: str
    error: str
    error_code: Optional[str] = None

class IndexingResult(IdentifiedModel):
    """Complete indexing result"""
    indexing_id: str
    duration_seconds: float
    statistics: IndexingStatistics
    project_summary: str
    failed_files: List[FailedFile] = []
    workspace_path: str
    status: IndexingStatus

class CodeChunk(BaseModel):
    """Semantic code chunk"""
    id: str
    content: str
    file_path: str
    start_line: int
    end_line: int
    language: str
    chunk_type: str  # 'function', 'class', 'block', etc.
    tokens: int
    embedding: Optional[List[float]] = None
    metadata: Dict = {}

class Symbol(BaseModel):
    """Code symbol (function, class, variable, etc.)"""
    name: str
    type: str  # 'function', 'class', 'interface', 'variable'
    file_path: str
    line: int
    definition: str
    docstring: Optional[str] = None
    signature: Optional[str] = None
```

---

### Chat Models

```python
# backend/src/models/chat.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from .base import IdentifiedModel

class MessageRole(str, Enum):
    """Message role"""
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'

class ChatMessageMetadata(BaseModel):
    """Chat message metadata"""
    model: Optional[str] = None
    tokens: Optional[int] = None
    generation_time_seconds: Optional[float] = None
    rag_context_used: bool = False
    context_chunks_retrieved: Optional[int] = None

class ChatMessage(BaseModel):
    """Chat message"""
    id: str
    role: MessageRole
    content: str
    timestamp: str
    metadata: Optional[ChatMessageMetadata] = None

class RAGContextChunk(BaseModel):
    """RAG context chunk"""
    file_path: str
    start_line: int
    end_line: int
    content: str
    relevance_score: float = Field(ge=0, le=1)

class RAGContext(BaseModel):
    """RAG context"""
    chunks: List[RAGContextChunk]
    total_tokens: int
    relevance_scores: List[float]
    query: str

class PlanSuggestion(BaseModel):
    """Plan suggestion from chat"""
    title: str
    description: str
    goals: List[str]
    estimated_complexity: str = Field(pattern='^(low|medium|high)$')
    confidence: float = Field(ge=0, le=1)

class ChatSession(IdentifiedModel):
    """Chat session"""
    title: str
    messages: List[ChatMessage] = []
    context: Optional[RAGContext] = None
    suggested_plan: Optional[PlanSuggestion] = None
    workspace_path: str

class ChatOptions(BaseModel):
    """Chat options"""
    stream: bool = True
    max_tokens: int = Field(default=2048, ge=100, le=8192)
    temperature: float = Field(default=0.7, ge=0, le=2)
    retrieve_context: bool = True
    model: Optional[str] = None

class ChatContext(BaseModel):
    """Chat context (user environment)"""
    current_file: Optional[str] = None
    selected_code: Optional[str] = None
    workspace_path: str
    active_mode: Optional[str] = Field(None, pattern='^(chat|plan|act)$')
```

---

### Plan Models

```python
# backend/src/models/plan.py

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from .base import IdentifiedModel

class PlanStatus(str, Enum):
    """Plan status"""
    DRAFT = 'draft'
    READY = 'ready'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'

class TodoStatus(str, Enum):
    """TODO status"""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    SKIPPED = 'skipped'

class FileOperationType(str, Enum):
    """File operation type"""
    CREATE = 'create'
    MODIFY = 'modify'
    DELETE = 'delete'
    RESEARCH = 'research'

class TodoFile(BaseModel):
    """File affected by TODO"""
    path: str
    operation: FileOperationType
    estimated_changes: Optional[str] = None

class TodoItem(BaseModel):
    """TODO item"""
    id: str
    title: str
    description: str
    type: FileOperationType
    files: List[TodoFile]
    dependencies: List[str] = []
    status: TodoStatus = TodoStatus.PENDING
    ai_instructions: str
    order: int
    error: Optional[str] = None

class ExecutionSummary(BaseModel):
    """Execution summary"""
    execution_id: str
    started_at: str
    completed_at: Optional[str] = None
    status: str = Field(pattern='^(in_progress|completed|failed|cancelled)$')
    todos_completed: int = 0
    todos_failed: int = 0
    todos_skipped: int = 0

class Plan(IdentifiedModel):
    """Plan"""
    from_chat_session: Optional[str] = None
    title: str
    overview: str
    todos: List[TodoItem]
    status: PlanStatus = PlanStatus.DRAFT
    complexity: str = Field(pattern='^(low|medium|high)$')
    estimated_duration_minutes: Optional[int] = None
    workspace_path: str
    execution_history: List[ExecutionSummary] = []
```

---

### Act Mode Models

```python
# backend/src/models/act.py

from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from enum import Enum
from .base import IdentifiedModel
from .plan import FileOperationType

class ExecutionStatus(str, Enum):
    """Execution status"""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class FileOperationMetadata(BaseModel):
    """File operation metadata"""
    additions: int = 0
    deletions: int = 0
    language: str
    file_size: Optional[int] = None

class FileOperation(BaseModel):
    """File operation"""
    operation_id: str
    type: FileOperationType
    path: str
    content: Optional[str] = None
    diff: Optional[str] = None
    preview: Optional[str] = None
    requires_approval: bool = True
    metadata: Optional[FileOperationMetadata] = None

class ApprovalDecision(str, Enum):
    """Approval decision"""
    APPROVE = 'approve'
    REJECT = 'reject'
    EDIT = 'edit'
    SKIP = 'skip'

class ApprovalRequest(BaseModel):
    """Approval request"""
    execution_id: str
    todo_id: str
    file_operations: List[FileOperation]
    approval_timeout_seconds: int = 300
    requested_at: str

class ApprovalResponse(BaseModel):
    """Approval response"""
    execution_id: str
    todo_id: str
    decision: ApprovalDecision
    edited_operations: Optional[List[FileOperation]] = None
    responded_at: str

class ExecutionLogEntry(BaseModel):
    """Execution log entry"""
    id: str
    todo_id: str
    type: str = Field(pattern='^(info|success|warning|error)$')
    message: str
    timestamp: str
    data: Optional[Any] = None

class GitCommitInfo(BaseModel):
    """Git commit info"""
    hash: str
    message: str
    author: Optional[str] = None
    timestamp: Optional[str] = None

class FileChange(BaseModel):
    """File change summary"""
    path: str
    type: FileOperationType
    additions: int = 0
    deletions: int = 0

class ActSession(IdentifiedModel):
    """Act session (execution state)"""
    execution_id: str
    plan_id: str
    current_todo_id: Optional[str] = None
    status: ExecutionStatus
    git_branch: Optional[str] = None
    base_commit: Optional[str] = None
    execution_log: List[ExecutionLogEntry] = []
    generated_files: List[FileChange] = []
    commits: List[GitCommitInfo] = []
    started_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None

class ExecutionOptions(BaseModel):
    """Execution options"""
    auto_approve: bool = False
    create_git_branch: bool = True
    git_branch_name: Optional[str] = None
    model: Optional[str] = None
    timeout_per_todo_seconds: int = Field(default=300, ge=60, le=3600)
```

---

### System Models

```python
# backend/src/models/system.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class ModelType(str, Enum):
    """Model type"""
    CHAT = 'chat'
    EMBEDDING = 'embedding'
    CODE_GENERATION = 'code_generation'

class ModelInfo(BaseModel):
    """Model information"""
    id: str
    name: str
    type: ModelType
    size_gb: float
    context_window: Optional[int] = None
    dimensions: Optional[int] = None
    capabilities: List[str]
    loaded: bool
    recommended_for: List[str]

class SystemResources(BaseModel):
    """System resources"""
    vram_usage_gb: float
    vram_total_gb: float
    ram_usage_gb: float
    ram_total_gb: float
    cpu_usage_percent: Optional[float] = None
    disk_usage_gb: Optional[float] = None

class ServiceStatus(BaseModel):
    """Service status"""
    status: str = Field(pattern='^(connected|disconnected|error)$')
    info: Optional[Any] = None
    error: Optional[str] = None

class HealthStatus(BaseModel):
    """Health status"""
    status: str = Field(pattern='^(healthy|degraded|unhealthy)$')
    version: str
    uptime_seconds: int
    services: Dict[str, ServiceStatus]
    resources: SystemResources
    timestamp: str

class VRAMWarning(BaseModel):
    """VRAM warning"""
    level: str = Field(pattern='^(warning|critical)$')
    current_usage_gb: float
    total_vram_gb: float
    usage_percentage: float
    loaded_models: List[Dict[str, Any]]
    recommendation: str

class ModelSwapEvent(BaseModel):
    """Model swap event"""
    unloading: Optional[str] = None
    loading: str
    reason: str
    estimated_duration_seconds: int
    timestamp: str
```

---

### Configuration Models

```python
# backend/src/models/config.py

from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List

class ModelConfiguration(BaseModel):
    """Model configuration"""
    embedding: str = Field(default="bge-m3")
    chat: str = Field(default="qwen2.5-coder:7b-instruct-q4_K_M")
    planning: str = Field(default="qwen2.5-coder:14b-instruct-q4_K_M")
    coding: str = Field(default="qwen2.5-coder:14b-instruct-q4_K_M")

class IndexingConfiguration(BaseModel):
    """Indexing configuration"""
    exclude_patterns: List[str] = Field(
        default=['node_modules', '.git', 'dist', 'build']
    )
    max_file_size_mb: int = Field(default=10, ge=1, le=100)
    chunk_size: int = Field(default=1000, ge=100, le=2000)
    chunk_overlap: int = Field(default=200, ge=0, le=500)

class SafetyConfiguration(BaseModel):
    """Safety configuration"""
    require_git_repo: bool = True
    check_uncommitted_changes: bool = True
    auto_approve_new_files: bool = False
    auto_approve_config_changes: bool = False

class OllamaConfiguration(BaseModel):
    """Ollama configuration"""
    host: str = Field(default="http://localhost:11434")
    timeout_seconds: int = Field(default=120, ge=30, le=600)
    
    @validator('host')
    def validate_host(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Host must start with http:// or https://')
        return v

class Configuration(BaseModel):
    """Full configuration"""
    ollama: OllamaConfiguration = OllamaConfiguration()
    models: ModelConfiguration = ModelConfiguration()
    indexing: IndexingConfiguration = IndexingConfiguration()
    safety: SafetyConfiguration = SafetyConfiguration()
```

---

## 🔄 Shared Types

### Constants File

```typescript
// shared/types/constants.ts

/**
 * Default values and limits
 */
export const CONSTANTS = {
  // Indexing
  DEFAULT_CHUNK_SIZE: 1000,
  DEFAULT_CHUNK_OVERLAP: 200,
  DEFAULT_MAX_FILE_SIZE_MB: 10,
  DEFAULT_EXCLUDE_PATTERNS: ['node_modules', '.git', 'dist', 'build', '.next'],
  
  // Chat
  DEFAULT_MAX_TOKENS: 2048,
  DEFAULT_TEMPERATURE: 0.7,
  MAX_CONTEXT_TOKENS: 4096,
  
  // WebSocket
  WEBSOCKET_RECONNECT_DELAY_MS: 2000,
  MAX_WEBSOCKET_RECONNECT_ATTEMPTS: 5,
  WEBSOCKET_TIMEOUT_MS: 30000,
  
  // Act Mode
  DEFAULT_APPROVAL_TIMEOUT_SECONDS: 300,
  DEFAULT_TODO_TIMEOUT_SECONDS: 300,
  GIT_BRANCH_PREFIX: 'localpilot',
  
  // Resources
  VRAM_WARNING_THRESHOLD: 0.9,
  VRAM_CRITICAL_THRESHOLD: 0.95,
  
  // Models
  DEFAULT_EMBEDDING_MODEL: 'bge-m3',
  DEFAULT_CHAT_MODEL: 'qwen2.5-coder:7b-instruct-q4_K_M',
  DEFAULT_PLANNING_MODEL: 'qwen2.5-coder:14b-instruct-q4_K_M',
  DEFAULT_CODING_MODEL: 'qwen2.5-coder:14b-instruct-q4_K_M',
} as const;

/**
 * Supported programming languages
 */
export const SUPPORTED_LANGUAGES = [
  'typescript',
  'javascript',
  'python',
  'kotlin',
  'dart',
  'swift',
  'java',
  'go',
  'rust',
  'cpp',
  'c',
] as const;

export type SupportedLanguage = typeof SUPPORTED_LANGUAGES[number];
```

---

## 💾 Database Schemas

### ChromaDB Collections

```python
# backend/src/db/schemas.py

"""
ChromaDB collection schemas
"""

# Collection: localpilot_codebase
CODEBASE_COLLECTION_SCHEMA = {
    "name": "localpilot_codebase",
    "metadata": {
        "hnsw:space": "cosine",  # Use cosine similarity
        "description": "Code chunks and documentation embeddings"
    },
    "embedding_function": "bge-m3",  # Model used for embeddings
}

# Document metadata structure
DOCUMENT_METADATA_SCHEMA = {
    "file_path": str,          # Path to source file
    "chunk_id": str,           # Unique chunk identifier
    "chunk_type": str,         # 'function', 'class', 'block', 'doc'
    "language": str,           # Programming language
    "start_line": int,         # Starting line number
    "end_line": int,           # Ending line number
    "tokens": int,             # Token count
    "symbols": list,           # Extracted symbols (function names, etc.)
    "imports": list,           # Import statements
    "workspace_id": str,       # Workspace identifier
    "indexed_at": str,         # ISO timestamp
}
```

### SQLite Schema

```sql
-- backend/src/db/schema.sql

-- Metadata database for LocalPilot

CREATE TABLE IF NOT EXISTS workspaces (
    id TEXT PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    name TEXT,
    created_at TEXT NOT NULL,
    last_indexed_at TEXT,
    index_version TEXT
);

CREATE TABLE IF NOT EXISTS indexing_sessions (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    status TEXT NOT NULL,
    phase TEXT,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    duration_seconds REAL,
    files_indexed INTEGER,
    files_failed INTEGER,
    error TEXT,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
);

CREATE TABLE IF NOT EXISTS chat_sessions (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    message_count INTEGER DEFAULT 0,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    metadata_json TEXT,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS plans (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    chat_session_id TEXT,
    title TEXT NOT NULL,
    overview TEXT NOT NULL,
    status TEXT NOT NULL,
    complexity TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    todos_json TEXT NOT NULL,  -- Serialized TODO list
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id),
    FOREIGN KEY (chat_session_id) REFERENCES chat_sessions(id)
);

CREATE TABLE IF NOT EXISTS executions (
    id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL,
    status TEXT NOT NULL,
    git_branch TEXT,
    base_commit TEXT,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    duration_seconds REAL,
    todos_completed INTEGER DEFAULT 0,
    todos_failed INTEGER DEFAULT 0,
    todos_skipped INTEGER DEFAULT 0,
    error TEXT,
    FOREIGN KEY (plan_id) REFERENCES plans(id)
);

CREATE TABLE IF NOT EXISTS execution_logs (
    id TEXT PRIMARY KEY,
    execution_id TEXT NOT NULL,
    todo_id TEXT,
    type TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    data_json TEXT,
    FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS file_hashes (
    file_path TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    hash TEXT NOT NULL,
    last_indexed TEXT NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_plans_workspace ON plans(workspace_id);
CREATE INDEX IF NOT EXISTS idx_executions_plan ON executions(plan_id);
CREATE INDEX IF NOT EXISTS idx_file_hashes_workspace ON file_hashes(workspace_id);
```

---

## ✅ Validation Rules

### TypeScript Validators

```typescript
// extension/src/utils/validators.ts

import { z } from 'zod';

/**
 * UUID v4 validator
 */
export const uuidSchema = z.string().uuid();

/**
 * File path validator
 */
export const filePathSchema = z.string().min(1).refine(
  (path) => !path.includes('..'),
  { message: 'File path cannot contain ..' }
);

/**
 * Percentage validator
 */
export const percentageSchema = z.number().min(0).max(100);

/**
 * Timestamp validator (ISO 8601)
 */
export const timestampSchema = z.string().datetime();

/**
 * Plan complexity validator
 */
export const complexitySchema = z.enum(['low', 'medium', 'high']);

/**
 * Chat message validator
 */
export const chatMessageSchema = z.object({
  id: uuidSchema,
  role: z.enum(['user', 'assistant', 'system']),
  content: z.string().min(1).max(10000),
  timestamp: timestampSchema,
  metadata: z.object({
    model: z.string().optional(),
    tokens: z.number().optional(),
    generationTimeSeconds: z.number().optional(),
    ragContextUsed: z.boolean().optional(),
  }).optional(),
});

/**
 * Validate chat message
 */
export function validateChatMessage(data: unknown) {
  return chatMessageSchema.parse(data);
}
```

### Python Validators

```python
# backend/src/utils/validators.py

import re
from typing import Any
from pydantic import validator

class Validators:
    """Common validators"""
    
    @staticmethod
    def validate_file_path(v: str) -> str:
        """Validate file path"""
        if '..' in v:
            raise ValueError('File path cannot contain ..')
        if not v.strip():
            raise ValueError('File path cannot be empty')
        return v
    
    @staticmethod
    def validate_percentage(v: float) -> float:
        """Validate percentage (0-100)"""
        if not 0 <= v <= 100:
            raise ValueError('Percentage must be between 0 and 100')
        return round(v, 1)
    
    @staticmethod
    def validate_complexity(v: str) -> str:
        """Validate complexity level"""
        if v not in ('low', 'medium', 'high'):
            raise ValueError('Complexity must be low, medium, or high')
        return v
    
    @staticmethod
    def validate_model_name(v: str) -> str:
        """Validate model name"""
        # Must be alphanumeric with optional hyphens, colons, dots
        if not re.match(r'^[a-zA-Z0-9\-.:_]+$', v):
            raise ValueError('Invalid model name format')
        return v
```

---

## 📝 Example Data

### Example 1: Complete Indexing Flow

```json
{
  "indexingId": "idx-20250115-103045",
  "workspacePath": "/Users/dev/my-project",
  "status": "completed",
  "startedAt": "2025-01-15T10:30:45Z",
  "completedAt": "2025-01-15T10:33:52Z",
  "durationSeconds": 187,
  "statistics": {
    "totalFiles": 623,
    "indexedFiles": 618,
    "failedFiles": 5,
    "totalChunks": 4521,
    "totalEmbeddings": 4521,
    "totalSymbols": 1847,
    "indexSizeMb": 125.3
  },
  "projectSummary": "This is a React + TypeScript e-commerce application with user authentication, product management, and payment processing. The backend is built with Express and uses MongoDB for data storage. Key features include JWT authentication, Stripe payment integration, and a responsive UI built with Tailwind CSS.",
  "failedFiles": [
    {
      "path": "src/legacy/old-parser.js",
      "error": "Syntax error at line 142: Unexpected token",
      "errorCode": "PARSING_FAILED"
    }
  ]
}
```

### Example 2: Chat Session

```json
{
  "id": "chat-550e8400",
  "title": "Authentication Discussion",
  "workspacePath": "/Users/dev/my-project",
  "createdAt": "2025-01-15T10:31:00Z",
  "updatedAt": "2025-01-15T10:45:00Z",
  "messages": [
    {
      "id": "msg-001",
      "role": "user",
      "content": "How does authentication work in this app?",
      "timestamp": "2025-01-15T10:31:00Z"
    },
    {
      "id": "msg-002",
      "role": "assistant",
      "content": "The authentication system uses JWT tokens stored in HTTP-only cookies...",
      "timestamp": "2025-01-15T10:31:04Z",
      "metadata": {
        "model": "qwen2.5-coder:7b-instruct-q4_K_M",
        "tokens": 245,
        "generationTimeSeconds": 3.2,
        "ragContextUsed": true,
        "contextChunksRetrieved": 5
      }
    }
  ],
  "context": {
    "query": "How does authentication work in this app?",
    "chunks": [
      {
        "filePath": "src/auth/AuthService.ts",
        "startLine": 45,
        "endLine": 67,
        "content": "export class AuthService {\n  async login(email: string, password: string) {\n    ...\n  }\n}",
        "relevanceScore": 0.92
      }
    ],
    "totalTokens": 1847,
    "relevanceScores": [0.92, 0.89, 0.87, 0.82, 0.78]
  },
  "suggestedPlan": {
    "title": "Add Two-Factor Authentication",
    "description": "Implement 2FA using TOTP",
    "goals": [
      "Add TOTP library",
      "Update user model",
      "Create 2FA setup flow",
      "Add verification step to login"
    ],
    "estimatedComplexity": "medium",
    "confidence": 0.87
  }
}
```

### Example 3: Plan with TODOs

```json
{
  "id": "plan-20250115-103200",
  "fromChatSession": "chat-550e8400",
  "title": "Add Refund Functionality",
  "overview": "Implement refund processing with admin approval workflow",
  "status": "ready",
  "complexity": "medium",
  "estimatedDurationMinutes": 45,
  "workspacePath": "/Users/dev/my-project",
  "createdAt": "2025-01-15T10:32:00Z",
  "updatedAt": "2025-01-15T10:34:00Z",
  "todos": [
    {
      "id": "todo-001",
      "title": "Add refund method to PaymentService",
      "description": "Create a new method in PaymentService to handle refund logic via Stripe API",
      "type": "modify",
      "files": [
        {
          "path": "src/services/PaymentService.ts",
          "operation": "modify",
          "estimatedChanges": "+45 lines"
        }
      ],
      "dependencies": [],
      "status": "pending",
      "aiInstructions": "Add a method called processRefund() that accepts paymentId, amount, and reason. Use Stripe's refunds.create() API. Include error handling and validation.",
      "order": 1
    },
    {
      "id": "todo-002",
      "title": "Create refund API endpoints",
      "description": "Add REST API endpoints for initiating and checking refund status",
      "type": "create",
      "files": [
        {
          "path": "src/api/refund.ts",
          "operation": "create",
          "estimatedChanges": "+120 lines"
        },
        {
          "path": "src/routes/payment.ts",
          "operation": "modify",
          "estimatedChanges": "+15 lines"
        }
      ],
      "dependencies": ["todo-001"],
      "status": "pending",
      "aiInstructions": "Create Express router with POST /api/refund and GET /api/refund/:id endpoints. Include authentication middleware.",
      "order": 2
    }
  ],
  "executionHistory": []
}
```

### Example 4: Act Session

```json
{
  "id": "act-001",
  "executionId": "exec-20250115-103500",
  "planId": "plan-20250115-103200",
  "currentTodoId": "todo-002",
  "status": "in_progress",
  "gitBranch": "localpilot/plan-42",
  "baseCommit": "a1b2c3d",
  "executionLog": [
    {
      "id": "log-001",
      "todoId": "todo-001",
      "type": "success",
      "message": "Successfully completed TODO #1: Add refund method to PaymentService",
      "timestamp": "2025-01-15T10:36:00Z",
      "data": {
        "filesModified": ["src/services/PaymentService.ts"],
        "linesAdded": 48,
        "commitHash": "a3f892c"
      }
    },
    {
      "id": "log-002",
      "todoId": "todo-002",
      "type": "info",
      "message": "Starting TODO #2: Create refund API endpoints",
      "timestamp": "2025-01-15T10:36:15Z"
    }
  ],
  "generatedFiles": [
    {
      "path": "src/services/PaymentService.ts",
      "type": "modify",
      "additions": 48,
      "deletions": 0
    }
  ],
  "commits": [
    {
      "hash": "a3f892c",
      "message": "[LocalPilot] TODO #1: Add refund method to PaymentService",
      "timestamp": "2025-01-15T10:36:00Z"
    }
  ],
  "startedAt": "2025-01-15T10:35:00Z",
  "createdAt": "2025-01-15T10:35:00Z",
  "updatedAt": "2025-01-15T10:36:15Z"
}
```

---

## 🔄 Migration Strategy

### Version Compatibility

```typescript
// extension/src/utils/migration.ts

/**
 * Schema version for data models
 */
export const SCHEMA_VERSION = '1.0.0';

/**
 * Migration functions for future schema changes
 */
export const migrations = {
  '0.1.0_to_1.0.0': (data: any) => {
    // Example migration
    return data;
  },
};

/**
 * Check if data needs migration
 */
export function needsMigration(dataVersion: string): boolean {
  return dataVersion !== SCHEMA_VERSION;
}

/**
 * Migrate data to current schema version
 */
export function migrateData(data: any, fromVersion: string): any {
  // Apply migrations sequentially
  let migrated = data;
  // ... migration logic
  return migrated;
}
```

### Backwards Compatibility

```yaml
Strategy:
  - Maintain schema version in all persisted data
  - Support reading previous schema versions
  - Migrate on load (lazy migration)
  - Never auto-migrate user data without consent
  
Future Considerations:
  - Export/import functionality
  - Schema validation on load
  - Migration rollback capability
  - Data backup before migration
```

---

## 📚 Related Documents

- `PROJECT_CHARTER.md` - Vision and success criteria
- `TECHNICAL_ARCHITECTURE.md` - System design
- `USER_JOURNEY.md` - User flows and UX
- `API_SPECIFICATION.md` - API documentation (PREVIOUS)
- `INDEXING_SYSTEM_SPEC.md` - Indexing algorithm (NEXT in Batch 2)
- `DEVELOPMENT_GUIDE.md` - Setup and workflow

---

**END OF DOCUMENT**