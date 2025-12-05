# 📄 DOCUMENT #4: API_SPECIFICATION.md
# LocalPilot - API Specification

**Version:** 1.0
**Date:** January 2025
**Status:** Foundation
**Author:** LocalPilot Backend Team

---

## 📋 Table of Contents

1. [API Overview](#api-overview)
2. [Connection & Authentication](#connection--authentication)
3. [WebSocket API](#websocket-api)
4. [REST API](#rest-api)
5. [Data Schemas](#data-schemas)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Code Examples](#code-examples)

---

## 🌐 API Overview

### Architecture

LocalPilot uses a **dual-protocol approach**:

```
┌─────────────────────────────────────────────────────────┐
│                  Extension (TypeScript)                 │
└────────┬──────────────────────────────────┬─────────────┘
         │                                  │
         │ WebSocket (Primary)              │ REST (Fallback)
         │ ws://localhost:8765/ws           │ http://localhost:8765/api
         │                                  │
┌────────▼──────────────────────────────────▼─────────────┐
│              Backend (Python/FastAPI)                   │
│  ┌──────────────────┐      ┌──────────────────┐         │
│  │ WebSocket Hub    │      │  REST Router     │         │
│  │ (Real-time)      │      │  (Request/Reply) │         │
│  └──────────────────┘      └──────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### Protocol Selection Guide

| Use Case | Protocol | Reason |
|----------|----------|--------|
| **LLM Streaming** | WebSocket | Real-time token streaming |
| **Indexing Progress** | WebSocket | Live progress updates |
| **Chat Messages** | WebSocket | Bidirectional conversation |
| **Plan Execution** | WebSocket | Real-time status updates |
| **Health Check** | REST | Simple request/response |
| **Model List** | REST | One-time fetch |
| **Configuration** | REST | CRUD operations |

### Base URLs

```yaml
Development:
  WebSocket: ws://localhost:8765/ws
  REST: http://localhost:8765/api
  Health: http://localhost:8765/health

Production (Future):
  WebSocket: ws://127.0.0.1:8765/ws
  REST: http://127.0.0.1:8765/api
  Health: http://127.0.0.1:8765/health
```

### Versioning

```yaml
Current Version: v1
Strategy: URL path versioning (future)

Example (v2 in future):
  REST: http://localhost:8765/api/v2/...
  WebSocket: ws://localhost:8765/ws/v2

MVP: No versioning (single version)
```

---

## 🔐 Connection & Authentication

### WebSocket Connection

**Endpoint:** `ws://localhost:8765/ws`

**Query Parameters:**
```typescript
interface ConnectionParams {
  client_id: string;      // Unique client identifier (UUID)
  workspace_id?: string;  // Workspace identifier (optional for MVP)
}
```

**Connection Flow:**

```typescript
// Extension side (TypeScript)
const clientId = generateUUID();
const ws = new WebSocket(`ws://localhost:8765/ws?client_id=${clientId}`);

ws.onopen = () => {
  console.log('Connected to LocalPilot backend');
  // Send handshake
  ws.send(JSON.stringify({
    type: 'handshake',
    payload: {
      version: '0.1.0',
      workspace: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath
    }
  }));
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  handleWebSocketMessage(message);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
  attemptReconnect();
};

ws.onclose = () => {
  console.log('WebSocket closed');
  attemptReconnect();
};
```

**Handshake Response:**

```json
{
  "type": "handshake_ack",
  "payload": {
    "server_version": "0.1.0",
    "client_id": "550e8400-e29b-41d4-a716-446655440000",
    "capabilities": [
      "streaming",
      "indexing",
      "chat",
      "plan",
      "act"
    ],
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

### Authentication (MVP: Local Only)

```yaml
MVP Authentication: NONE
Reason: Backend runs on localhost, single-user

Security Measures:
  - Only bind to 127.0.0.1 (not 0.0.0.0)
  - No external network access
  - No sensitive data transmission
  - Workspace isolation via file paths

Future (v0.2+):
  - API key for multi-client scenarios
  - JWT tokens for team features
  - OAuth for cloud sync
```

---

## 🔌 WebSocket API

### Message Format

All WebSocket messages follow this structure:

```typescript
interface WebSocketMessage {
  type: string;           // Event type
  payload: any;           // Event-specific data
  request_id?: string;    // Optional request correlation ID
  timestamp?: string;     // ISO 8601 timestamp
}
```

### Event Categories

```
├── Connection Events
│   ├── handshake
│   └── handshake_ack
│
├── Indexing Events
│   ├── indexing.start
│   ├── indexing.progress
│   ├── indexing.complete
│   └── indexing.error
│
├── Chat Events
│   ├── chat.message
│   ├── chat.stream.start
│   ├── chat.stream.chunk
│   ├── chat.stream.complete
│   └── chat.error
│
├── Plan Events
│   ├── plan.generate
│   ├── plan.save
│   ├── plan.update
│   └── plan.error
│
├── Act Events
│   ├── act.start
│   ├── act.progress
│   ├── act.request_approval
│   ├── act.approval_response
│   ├── act.complete
│   └── act.error
│
└── System Events
    ├── vram.warning
    ├── model.swap.start
    ├── model.swap.complete
    └── error
```

---

### Indexing Events

#### 1. Start Indexing

**Client → Server**

```typescript
{
  "type": "indexing.start",
  "payload": {
    "workspace_path": "/Users/dev/my-project",
    "options": {
      "exclude_patterns": ["node_modules", ".git", "dist"],
      "max_file_size_mb": 10,
      "languages": ["typescript", "javascript", "python"],
      "force_reindex": false  // Skip cached files if false
    }
  },
  "request_id": "idx-001"
}
```

**Server → Client (Acknowledgment)**

```json
{
  "type": "indexing.started",
  "payload": {
    "indexing_id": "idx-20250115-103045",
    "estimated_files": 623,
    "estimated_duration_seconds": 180
  },
  "request_id": "idx-001",
  "timestamp": "2025-01-15T10:30:45Z"
}
```

#### 2. Indexing Progress

**Server → Client (Streaming)**

```json
{
  "type": "indexing.progress",
  "payload": {
    "indexing_id": "idx-20250115-103045",
    "phase": "chunking",
    "phase_number": 4,
    "total_phases": 5,
    "current_file": 547,
    "total_files": 623,
    "current_file_path": "src/components/Dashboard.tsx",
    "percentage": 87.8,
    "estimated_time_remaining_seconds": 135,
    "message": "Creating semantic chunks and generating embeddings..."
  },
  "timestamp": "2025-01-15T10:33:12Z"
}
```

**Phases:**
```typescript
enum IndexingPhase {
  DISCOVERY = 'discovery',           // Phase 1
  DOCUMENTATION = 'documentation',   // Phase 2
  STRUCTURE = 'structure',           // Phase 3
  CHUNKING = 'chunking',             // Phase 4
  SUMMARIZATION = 'summarization'    // Phase 5
}
```

#### 3. Indexing Complete

**Server → Client**

```json
{
  "type": "indexing.complete",
  "payload": {
    "indexing_id": "idx-20250115-103045",
    "duration_seconds": 187,
    "statistics": {
      "total_files": 623,
      "indexed_files": 618,
      "failed_files": 5,
      "total_chunks": 4521,
      "total_embeddings": 4521,
      "total_symbols": 1847,
      "index_size_mb": 125.3
    },
    "project_summary": "This is a React + TypeScript e-commerce application...",
    "failed_files": [
      {
        "path": "src/legacy/old.js",
        "error": "Syntax error at line 142"
      }
    ]
  },
  "timestamp": "2025-01-15T10:33:52Z"
}
```

#### 4. Indexing Error

**Server → Client**

```json
{
  "type": "indexing.error",
  "payload": {
    "indexing_id": "idx-20250115-103045",
    "error_code": "PARSING_FAILED",
    "error_message": "Failed to parse multiple files",
    "details": {
      "failed_count": 12,
      "total_files": 623,
      "can_continue": true
    },
    "recovery_options": [
      "continue_with_partial",
      "skip_failed_and_retry",
      "abort"
    ]
  },
  "timestamp": "2025-01-15T10:32:15Z"
}
```

---

### Chat Events

#### 1. Send Message

**Client → Server**

```typescript
{
  "type": "chat.message",
  "payload": {
    "session_id": "chat-550e8400",
    "message": "How does authentication work in this app?",
    "context": {
      "current_file": "src/auth/AuthService.ts",  // Optional: file user is viewing
      "selected_code": "...",                     // Optional: highlighted code
      "workspace_path": "/Users/dev/my-project"
    },
    "options": {
      "stream": true,          // Enable streaming response
      "max_tokens": 2048,
      "temperature": 0.7,
      "retrieve_context": true  // Enable RAG
    }
  },
  "request_id": "msg-001"
}
```

#### 2. Stream Start

**Server → Client**

```json
{
  "type": "chat.stream.start",
  "payload": {
    "message_id": "msg-20250115-103100",
    "session_id": "chat-550e8400",
    "rag_context": {
      "chunks_retrieved": 5,
      "total_tokens": 1847,
      "relevance_scores": [0.92, 0.89, 0.87, 0.82, 0.78],
      "files": [
        {
          "path": "src/auth/AuthService.ts",
          "lines": "45-67",
          "relevance": 0.92
        },
        {
          "path": "src/middleware/auth.ts",
          "lines": "12-34",
          "relevance": 0.89
        }
      ]
    }
  },
  "request_id": "msg-001",
  "timestamp": "2025-01-15T10:31:00Z"
}
```

#### 3. Stream Chunk

**Server → Client (Multiple Messages)**

```json
{
  "type": "chat.stream.chunk",
  "payload": {
    "message_id": "msg-20250115-103100",
    "chunk": "The authentication system uses ",
    "index": 0
  },
  "timestamp": "2025-01-15T10:31:01Z"
}

{
  "type": "chat.stream.chunk",
  "payload": {
    "message_id": "msg-20250115-103100",
    "chunk": "JWT tokens stored in HTTP-only cookies. ",
    "index": 1
  },
  "timestamp": "2025-01-15T10:31:01.050Z"
}

// ... more chunks ...
```

#### 4. Stream Complete

**Server → Client**

```json
{
  "type": "chat.stream.complete",
  "payload": {
    "message_id": "msg-20250115-103100",
    "session_id": "chat-550e8400",
    "full_response": "The authentication system uses JWT tokens...",
    "metadata": {
      "tokens_generated": 245,
      "generation_time_seconds": 3.2,
      "model_used": "qwen2.5-coder:7b-instruct-q4_K_M",
      "rag_context_tokens": 1847
    },
    "plan_suggestion": {
      "detected": true,
      "title": "Add Two-Factor Authentication",
      "confidence": 0.87,
      "preview": "To add 2FA, we'll need to..."
    }
  },
  "request_id": "msg-001",
  "timestamp": "2025-01-15T10:31:04Z"
}
```

#### 5. Chat Error

**Server → Client**

```json
{
  "type": "chat.error",
  "payload": {
    "message_id": "msg-20250115-103100",
    "error_code": "LLM_TIMEOUT",
    "error_message": "LLM did not respond within 120 seconds",
    "details": {
      "model": "qwen2.5-coder:7b-instruct-q4_K_M",
      "elapsed_time": 120.5
    },
    "recovery_options": [
      "retry",
      "switch_to_smaller_model"
    ]
  },
  "request_id": "msg-001",
  "timestamp": "2025-01-15T10:33:00Z"
}
```

---

### Plan Events

#### 1. Generate Plan

**Client → Server**

```typescript
{
  "type": "plan.generate",
  "payload": {
    "source": "chat",
    "chat_session_id": "chat-550e8400",
    "plan_suggestion": {
      "title": "Add Refund Functionality",
      "description": "Implement refund processing with admin approval",
      "goals": [
        "Add refund method to PaymentService",
        "Create refund API endpoints",
        "Update payment status tracking",
        "Add UI for refund requests",
        "Implement admin approval workflow"
      ]
    },
    "workspace_path": "/Users/dev/my-project"
  },
  "request_id": "plan-001"
}
```

**Server → Client**

```json
{
  "type": "plan.generated",
  "payload": {
    "plan_id": "plan-20250115-103200",
    "title": "Add Refund Functionality",
    "description": "Implement refund processing with admin approval workflow",
    "complexity": "medium",
    "estimated_duration_minutes": 45,
    "todos": [
      {
        "id": "todo-001",
        "title": "Add refund method to PaymentService",
        "description": "Create a new method in PaymentService to handle refund logic...",
        "type": "create",
        "files": [
          {
            "path": "src/services/PaymentService.ts",
            "operation": "modify",
            "estimated_changes": "+45 lines"
          }
        ],
        "dependencies": [],
        "status": "pending",
        "ai_instructions": "Add a method called processRefund() that accepts paymentId..."
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
            "estimated_changes": "+120 lines"
          },
          {
            "path": "src/routes/payment.ts",
            "operation": "modify",
            "estimated_changes": "+15 lines"
          }
        ],
        "dependencies": ["todo-001"],
        "status": "pending",
        "ai_instructions": "Create a new Express router for /api/refund with POST and GET endpoints..."
      }
      // ... more TODOs
    ],
    "metadata": {
      "total_todos": 5,
      "new_files": 3,
      "modified_files": 4,
      "estimated_total_lines": 350
    }
  },
  "request_id": "plan-001",
  "timestamp": "2025-01-15T10:32:05Z"
}
```

#### 2. Save Plan

**Client → Server**

```typescript
{
  "type": "plan.save",
  "payload": {
    "plan_id": "plan-20250115-103200",
    "status": "draft",
    "todos": [/* updated TODOs if user edited */]
  },
  "request_id": "plan-002"
}
```

**Server → Client**

```json
{
  "type": "plan.saved",
  "payload": {
    "plan_id": "plan-20250115-103200",
    "status": "draft",
    "saved_at": "2025-01-15T10:35:00Z"
  },
  "request_id": "plan-002",
  "timestamp": "2025-01-15T10:35:00Z"
}
```

---

### Act Events

#### 1. Start Execution

**Client → Server**

```typescript
{
  "type": "act.start",
  "payload": {
    "plan_id": "plan-20250115-103200",
    "workspace_path": "/Users/dev/my-project",
    "options": {
      "auto_approve": false,       // Manual approval required
      "create_git_branch": true,
      "git_branch_name": "localpilot/plan-42",
      "model": "qwen2.5-coder:14b-instruct-q4_K_M"
    }
  },
  "request_id": "act-001"
}
```

**Server → Client (Acknowledgment)**

```json
{
  "type": "act.started",
  "payload": {
    "execution_id": "exec-20250115-103500",
    "plan_id": "plan-20250115-103200",
    "git_branch": "localpilot/plan-42",
    "safety_checks": {
      "git_repo_exists": true,
      "no_uncommitted_changes": true,
      "branch_created": true
    },
    "total_todos": 5
  },
  "request_id": "act-001",
  "timestamp": "2025-01-15T10:35:00Z"
}
```

#### 2. Execution Progress

**Server → Client**

```json
{
  "type": "act.progress",
  "payload": {
    "execution_id": "exec-20250115-103500",
    "current_todo": {
      "id": "todo-001",
      "title": "Add refund method to PaymentService",
      "index": 1,
      "total": 5
    },
    "status": "generating_code",
    "message": "Generating code for PaymentService refund method..."
  },
  "timestamp": "2025-01-15T10:35:15Z"
}
```

#### 3. Request Approval

**Server → Client**

```json
{
  "type": "act.request_approval",
  "payload": {
    "execution_id": "exec-20250115-103500",
    "todo_id": "todo-001",
    "file_operations": [
      {
        "operation_id": "op-001",
        "type": "modify",
        "path": "src/services/PaymentService.ts",
        "diff": "--- a/src/services/PaymentService.ts\n+++ b/src/services/PaymentService.ts\n@@ -45,6 +45,20 @@\n   async processPayment(amount: number): Promise<Payment> {\n     // existing code\n   }\n+\n+  async processRefund(\n+    paymentId: string,\n+    amount: number,\n+    reason: string\n+  ): Promise<Refund> {\n+    // Validate payment exists\n+    const payment = await this.getPayment(paymentId);\n+    \n+    // Process refund via Stripe\n+    const refund = await stripe.refunds.create({\n+      payment_intent: payment.stripePaymentIntentId,\n+      amount: amount * 100, // Convert to cents\n+      reason: reason\n+    });\n+    \n+    return this.saveRefund(refund);\n+  }\n }",
        "preview": "async processRefund(\n  paymentId: string,\n  amount: number,\n  reason: string\n): Promise<Refund> {\n  // ... (see diff for details)\n}",
        "requires_approval": true,
        "metadata": {
          "additions": 20,
          "deletions": 0,
          "language": "typescript"
        }
      }
    ],
    "approval_timeout_seconds": 300
  },
  "timestamp": "2025-01-15T10:35:30Z"
}
```

#### 4. Approval Response

**Client → Server**

```typescript
{
  "type": "act.approval_response",
  "payload": {
    "execution_id": "exec-20250115-103500",
    "todo_id": "todo-001",
    "decision": "approve",  // "approve" | "reject" | "edit" | "skip"
    "edited_operations": [  // Only if decision === "edit"
      {
        "operation_id": "op-001",
        "content": "/* user-edited code */"
      }
    ]
  },
  "request_id": "act-002"
}
```

**Server → Client**

```json
{
  "type": "act.approval_processed",
  "payload": {
    "execution_id": "exec-20250115-103500",
    "todo_id": "todo-001",
    "result": "applied",
    "git_commit": {
      "hash": "a3f892c",
      "message": "[LocalPilot] TODO #1: Add refund method to PaymentService"
    },
    "files_changed": [
      "src/services/PaymentService.ts"
    ]
  },
  "request_id": "act-002",
  "timestamp": "2025-01-15T10:36:00Z"
}
```

#### 5. Execution Complete

**Server → Client**

```json
{
  "type": "act.complete",
  "payload": {
    "execution_id": "exec-20250115-103500",
    "plan_id": "plan-20250115-103200",
    "status": "completed",
    "summary": {
      "total_todos": 5,
      "completed": 5,
      "skipped": 0,
      "failed": 0,
      "duration_seconds": 487,
      "files_created": 3,
      "files_modified": 4,
      "total_commits": 5
    },
    "git_info": {
      "branch": "localpilot/plan-42",
      "commits": [
        { "hash": "a3f892c", "message": "TODO #1: Add refund method..." },
        { "hash": "b7e234d", "message": "TODO #2: Create refund API..." },
        { "hash": "c8d123e", "message": "TODO #3: Update payment status..." },
        { "hash": "d9f456a", "message": "TODO #4: Add refund request UI..." },
        { "hash": "e0a789b", "message": "TODO #5: Implement admin approval..." }
      ],
      "merge_instructions": "git checkout main && git merge localpilot/plan-42"
    }
  },
  "timestamp": "2025-01-15T10:43:07Z"
}
```

#### 6. Execution Error

**Server → Client**

```json
{
  "type": "act.error",
  "payload": {
    "execution_id": "exec-20250115-103500",
    "todo_id": "todo-003",
    "error_code": "COMPILATION_ERROR",
    "error_message": "TypeScript compilation failed",
    "details": {
      "file": "src/middleware/auth.ts",
      "line": 23,
      "message": "Cannot find name 'UserModel'",
      "suggestion": "This TODO depends on TODO #1 which was skipped"
    },
    "recovery_options": [
      {
        "action": "retry",
        "description": "Ask AI to fix the error"
      },
      {
        "action": "edit_manually",
        "description": "Open file for manual editing"
      },
      {
        "action": "skip",
        "description": "Skip this TODO and continue"
      },
      {
        "action": "abort",
        "description": "Stop execution entirely"
      }
    ]
  },
  "timestamp": "2025-01-15T10:38:45Z"
}
```

---

### System Events

#### 1. VRAM Warning

**Server → Client**

```json
{
  "type": "vram.warning",
  "payload": {
    "level": "warning",  // "warning" | "critical"
    "current_usage_gb": 7.2,
    "total_vram_gb": 8.0,
    "usage_percentage": 90,
    "loaded_models": [
      {
        "name": "qwen2.5-coder:14b-instruct-q4_K_M",
        "vram_gb": 5.5
      },
      {
        "name": "bge-m3",
        "vram_gb": 1.7
      }
    ],
    "recommendation": "Consider switching to a smaller model or closing other GPU applications"
  },
  "timestamp": "2025-01-15T10:40:00Z"
}
```

#### 2. Model Swap

**Server → Client (Start)**

```json
{
  "type": "model.swap.start",
  "payload": {
    "unloading": "qwen2.5-coder:7b-instruct-q4_K_M",
    "loading": "qwen2.5-coder:14b-instruct-q4_K_M",
    "reason": "Planning mode requires larger model",
    "estimated_duration_seconds": 3
  },
  "timestamp": "2025-01-15T10:40:30Z"
}
```

**Server → Client (Complete)**

```json
{
  "type": "model.swap.complete",
  "payload": {
    "loaded_model": "qwen2.5-coder:14b-instruct-q4_K_M",
    "duration_seconds": 2.8,
    "vram_usage_gb": 6.2
  },
  "timestamp": "2025-01-15T10:40:33Z"
}
```

---

## 🌐 REST API

### Base Path: `/api`

### Health & Status

#### GET `/health`

**Description:** Check if backend is running and healthy

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "uptime_seconds": 3847,
  "services": {
    "ollama": {
      "status": "connected",
      "host": "http://localhost:11434"
    },
    "vector_db": {
      "status": "ready",
      "collections": 1,
      "total_vectors": 4521
    }
  },
  "resources": {
    "vram_usage_gb": 6.2,
    "vram_total_gb": 8.0,
    "ram_usage_gb": 8.5,
    "ram_total_gb": 16.0
  },
  "timestamp": "2025-01-15T10:45:00Z"
}
```

#### GET `/health/ollama`

**Description:** Check Ollama connection specifically

**Response:**
```json
{
  "status": "connected",
  "host": "http://localhost:11434",
  "version": "0.1.20",
  "models": [
    {
      "name": "qwen2.5-coder:7b-instruct-q4_K_M",
      "size_gb": 4.5,
      "loaded": true
    },
    {
      "name": "qwen2.5-coder:14b-instruct-q4_K_M",
      "size_gb": 9.0,
      "loaded": false
    },
    {
      "name": "bge-m3",
      "size_gb": 1.5,
      "loaded": true
    }
  ]
}
```

---

### Models

#### GET `/api/models`

**Description:** List available LLM models

**Response:**
```json
{
  "models": [
    {
      "id": "qwen2.5-coder:7b-instruct-q4_K_M",
      "name": "Qwen2.5-Coder 7B Instruct",
      "type": "chat",
      "size_gb": 4.5,
      "context_window": 32768,
      "capabilities": ["chat", "code_generation", "summarization"],
      "loaded": true,
      "recommended_for": ["chat", "summarization"]
    },
    {
      "id": "qwen2.5-coder:14b-instruct-q4_K_M",
      "name": "Qwen2.5-Coder 14B Instruct",
      "type": "chat",
      "size_gb": 9.0,
      "context_window": 32768,
      "capabilities": ["chat", "code_generation", "planning", "complex_reasoning"],
      "loaded": false,
      "recommended_for": ["planning", "coding"]
    },
    {
      "id": "bge-m3",
      "name": "BGE-M3 Embeddings",
      "type": "embedding",
      "size_gb": 1.5,
      "dimensions": 1024,
      "max_sequence": 8192,
      "loaded": true,
      "recommended_for": ["embeddings"]
    }
  ],
  "system_info": {
    "vram_available_gb": 8.0,
    "recommended_config": {
      "embedding": "bge-m3",
      "chat": "qwen2.5-coder:7b-instruct-q4_K_M",
      "planning": "qwen2.5-coder:14b-instruct-q4_K_M",
      "coding": "qwen2.5-coder:14b-instruct-q4_K_M"
    }
  }
}
```

#### POST `/api/models/validate`

**Description:** Validate model configuration for hardware

**Request:**
```json
{
  "configuration": {
    "embedding": "bge-m3",
    "chat": "qwen2.5-coder:7b-instruct-q4_K_M",
    "planning": "qwen2.5-coder:14b-instruct-q4_K_M",
    "coding": "qwen2.5-coder:14b-instruct-q4_K_M"
  },
  "hardware": {
    "vram_gb": 8.0,
    "ram_gb": 16.0
  }
}
```

**Response:**
```json
{
  "valid": true,
  "level": "warning",
  "message": "Configuration is valid but requires model swapping",
  "details": {
    "concurrent_vram_gb": 6.0,
    "peak_vram_gb": 10.5,
    "requires_swapping": true,
    "swap_pairs": [
      {
        "models": ["qwen2.5-coder:7b-instruct-q4_K_M", "qwen2.5-coder:14b-instruct-q4_K_M"],
        "reason": "Planning/coding model too large for concurrent loading"
      }
    ]
  },
  "recommendations": [
    "Planning and coding will require model swapping (~2-3s delay)",
    "Consider using 7b model for all tasks if speed is critical"
  ]
}
```

---

### Indexing

#### GET `/api/indexing/status`

**Description:** Get current indexing status

**Query Parameters:**
- `workspace_id` (optional): Specific workspace

**Response:**
```json
{
  "status": "in_progress",
  "indexing_id": "idx-20250115-103045",
  "workspace_path": "/Users/dev/my-project",
  "current_phase": "chunking",
  "progress_percentage": 87.8,
  "current_file": "src/components/Dashboard.tsx",
  "files_processed": 547,
  "files_total": 623,
  "estimated_time_remaining_seconds": 135,
  "started_at": "2025-01-15T10:30:45Z"
}
```

#### POST `/api/indexing/cancel`

**Description:** Cancel ongoing indexing

**Request:**
```json
{
  "indexing_id": "idx-20250115-103045"
}
```

**Response:**
```json
{
  "success": true,
  "indexing_id": "idx-20250115-103045",
  "status": "cancelled",
  "files_indexed": 547,
  "partial_index_available": true
}
```

---

### Chat

#### GET `/api/chat/sessions`

**Description:** List chat sessions

**Response:**
```json
{
  "sessions": [
    {
      "id": "chat-550e8400",
      "created_at": "2025-01-15T10:31:00Z",
      "updated_at": "2025-01-15T10:45:00Z",
      "message_count": 12,
      "title": "Authentication Discussion",
      "workspace_path": "/Users/dev/my-project"
    }
  ]
}
```

#### GET `/api/chat/sessions/{session_id}`

**Description:** Get chat session details

**Response:**
```json
{
  "id": "chat-550e8400",
  "created_at": "2025-01-15T10:31:00Z",
  "messages": [
    {
      "id": "msg-001",
      "role": "user",
      "content": "How does authentication work?",
      "timestamp": "2025-01-15T10:31:00Z"
    },
    {
      "id": "msg-002",
      "role": "assistant",
      "content": "The authentication system uses JWT tokens...",
      "timestamp": "2025-01-15T10:31:04Z",
      "metadata": {
        "model": "qwen2.5-coder:7b-instruct-q4_K_M",
        "tokens": 245,
        "rag_context_used": true
      }
    }
  ]
}
```

#### DELETE `/api/chat/sessions/{session_id}`

**Description:** Delete chat session

**Response:**
```json
{
  "success": true,
  "deleted_session_id": "chat-550e8400"
}
```

---

### Plans

#### GET `/api/plans`

**Description:** List all plans

**Response:**
```json
{
  "plans": [
    {
      "id": "plan-20250115-103200",
      "title": "Add Refund Functionality",
      "status": "completed",
      "created_at": "2025-01-15T10:32:00Z",
      "updated_at": "2025-01-15T10:43:07Z",
      "total_todos": 5,
      "completed_todos": 5,
      "workspace_path": "/Users/dev/my-project"
    }
  ]
}
```

#### GET `/api/plans/{plan_id}`

**Description:** Get plan details

**Response:**
```json
{
  "id": "plan-20250115-103200",
  "title": "Add Refund Functionality",
  "description": "Implement refund processing with admin approval workflow",
  "status": "completed",
  "complexity": "medium",
  "todos": [
    /* Full TODO list */
  ],
  "created_at": "2025-01-15T10:32:00Z",
  "execution_history": [
    {
      "execution_id": "exec-20250115-103500",
      "started_at": "2025-01-15T10:35:00Z",
      "completed_at": "2025-01-15T10:43:07Z",
      "status": "completed"
    }
  ]
}
```

#### DELETE `/api/plans/{plan_id}`

**Description:** Delete plan

**Response:**
```json
{
  "success": true,
  "deleted_plan_id": "plan-20250115-103200"
}
```

---

### Configuration

#### GET `/api/config`

**Description:** Get current configuration

**Response:**
```json
{
  "ollama": {
    "host": "http://localhost:11434",
    "timeout_seconds": 120
  },
  "models": {
    "embedding": "bge-m3",
    "chat": "qwen2.5-coder:7b-instruct-q4_K_M",
    "planning": "qwen2.5-coder:14b-instruct-q4_K_M",
    "coding": "qwen2.5-coder:14b-instruct-q4_K_M"
  },
  "indexing": {
    "exclude_patterns": ["node_modules", ".git", "dist"],
    "max_file_size_mb": 10,
    "chunk_size": 1000,
    "chunk_overlap": 200
  },
  "safety": {
    "require_git_repo": true,
    "check_uncommitted_changes": true,
    "auto_approve_new_files": false
  }
}
```

#### PUT `/api/config`

**Description:** Update configuration

**Request:**
```json
{
  "models": {
    "chat": "qwen2.5-coder:14b-instruct-q4_K_M"
  }
}
```

**Response:**
```json
{
  "success": true,
  "updated_fields": ["models.chat"],
  "new_config": {
    /* full config */
  }
}
```

---

## 📐 Data Schemas

### Common Types

```typescript
// Timestamp (ISO 8601)
type Timestamp = string;  // "2025-01-15T10:30:00Z"

// File Path (absolute or relative to workspace)
type FilePath = string;

// UUID v4
type UUID = string;

// Status enums
enum IndexingStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

enum PlanStatus {
  DRAFT = 'draft',
  READY = 'ready',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

enum TodoStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed',
  SKIPPED = 'skipped'
}

enum FileOperationType {
  CREATE = 'create',
  MODIFY = 'modify',
  DELETE = 'delete'
}
```

### Request/Response Schemas

See TypeScript interfaces in earlier event descriptions for detailed schemas.

---

## ⚠️ Error Handling

### Error Response Format

All errors follow this structure:

```typescript
interface ErrorResponse {
  error: {
    code: string;           // Machine-readable error code
    message: string;        // Human-readable message
    details?: any;          // Additional context
    timestamp: string;      // When error occurred
    request_id?: string;    // Original request ID
    recovery_options?: RecoveryOption[];
  }
}

interface RecoveryOption {
  action: string;
  description: string;
  parameters?: Record<string, any>;
}
```

### Error Codes

```typescript
// Connection Errors (1xxx)
WEBSOCKET_CONNECTION_FAILED = '1001'
WEBSOCKET_TIMEOUT = '1002'
HANDSHAKE_FAILED = '1003'

// LLM Errors (2xxx)
LLM_CONNECTION_FAILED = '2001'
LLM_TIMEOUT = '2002'
LLM_MODEL_NOT_FOUND = '2003'
LLM_GENERATION_FAILED = '2004'
LLM_CONTEXT_TOO_LARGE = '2005'

// Indexing Errors (3xxx)
INDEXING_FAILED = '3001'
PARSING_FAILED = '3002'
EMBEDDING_FAILED = '3003'
VECTOR_DB_ERROR = '3004'

// Plan Errors (4xxx)
PLAN_GENERATION_FAILED = '4001'
PLAN_NOT_FOUND = '4002'
INVALID_PLAN = '4003'

// Act Errors (5xxx)
EXECUTION_FAILED = '5001'
GIT_ERROR = '5002'
FILE_OPERATION_FAILED = '5003'
COMPILATION_ERROR = '5004'
APPROVAL_TIMEOUT = '5005'

// Resource Errors (6xxx)
VRAM_OVERFLOW = '6001'
RAM_OVERFLOW = '6002'
DISK_FULL = '6003'

// System Errors (9xxx)
INTERNAL_ERROR = '9001'
INVALID_REQUEST = '9002'
NOT_IMPLEMENTED = '9003'
```

### Example Error Response

**WebSocket:**
```json
{
  "type": "error",
  "payload": {
    "error": {
      "code": "LLM_TIMEOUT",
      "message": "LLM did not respond within 120 seconds",
      "details": {
        "model": "qwen2.5-coder:14b-instruct-q4_K_M",
        "elapsed_time": 120.5
      },
      "timestamp": "2025-01-15T10:45:00Z",
      "request_id": "msg-001",
      "recovery_options": [
        {
          "action": "retry",
          "description": "Retry with same parameters"
        },
        {
          "action": "switch_model",
          "description": "Switch to faster 7b model",
          "parameters": {
            "suggested_model": "qwen2.5-coder:7b-instruct-q4_K_M"
          }
        }
      ]
    }
  }
}
```

**REST:**
```json
{
  "error": {
    "code": "PLAN_NOT_FOUND",
    "message": "Plan with ID 'plan-12345' does not exist",
    "details": {
      "plan_id": "plan-12345"
    },
    "timestamp": "2025-01-15T10:45:00Z"
  }
}
```

---

## 🚦 Rate Limiting

### MVP: No Rate Limiting

```yaml
Reason: Single-user, local-only application

Future Considerations (v0.2+):
  - Prevent accidental DDOS of Ollama
  - Protect backend from runaway processes
  - Fair resource allocation in multi-client scenarios

Proposed Limits (future):
  - Chat messages: 60 per minute per client
  - Indexing: 1 concurrent per workspace
  - Plan generation: 10 per hour per workspace
  - Act execution: 1 concurrent per workspace
```

---

## 💻 Code Examples

### TypeScript (Extension)

#### WebSocket Client Setup

```typescript
import WebSocket from 'ws';
import { v4 as uuidv4 } from 'uuid';

export class LocalPilotBackendClient {
  private ws: WebSocket | null = null;
  private clientId: string;
  private eventHandlers: Map<string, Function[]> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor() {
    this.clientId = uuidv4();
  }

  async connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(`ws://localhost:8765/ws?client_id=${this.clientId}`);

      this.ws.on('open', () => {
        console.log('Connected to LocalPilot backend');
        this.reconnectAttempts = 0;
        this.sendHandshake();
        resolve();
      });

      this.ws.on('message', (data: string) => {
        const message = JSON.parse(data);
        this.handleMessage(message);
      });

      this.ws.on('error', (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      });

      this.ws.on('close', () => {
        console.log('WebSocket closed');
        this.attemptReconnect();
      });
    });
  }

  private sendHandshake(): void {
    this.send('handshake', {
      version: '0.1.0',
      workspace: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath
    });
  }

  send(type: string, payload: any, requestId?: string): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket is not connected');
    }

    const message = {
      type,
      payload,
      request_id: requestId || uuidv4(),
      timestamp: new Date().toISOString()
    };

    this.ws.send(JSON.stringify(message));
  }

  on(eventType: string, handler: Function): void {
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, []);
    }
    this.eventHandlers.get(eventType)!.push(handler);
  }

  private handleMessage(message: any): void {
    const handlers = this.eventHandlers.get(message.type);
    if (handlers) {
      handlers.forEach(handler => handler(message.payload));
    }
  }

  private async attemptReconnect(): Promise<void> {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

    console.log(`Reconnecting in ${delay}ms... (attempt ${this.reconnectAttempts})`);

    await new Promise(resolve => setTimeout(resolve, delay));
    await this.connect();
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
```

#### Usage Example

```typescript
// Initialize client
const client = new LocalPilotBackendClient();
await client.connect();

// Listen for indexing progress
client.on('indexing.progress', (progress) => {
  updateProgressBar(progress.percentage);
  updateStatusMessage(progress.message);
});

// Listen for chat responses
client.on('chat.stream.chunk', (chunk) => {
  appendToChat(chunk.chunk);
});

// Send chat message
client.send('chat.message', {
  session_id: 'chat-550e8400',
  message: 'How does authentication work?',
  options: {
    stream: true,
    retrieve_context: true
  }
});

// Start indexing
client.send('indexing.start', {
  workspace_path: '/Users/dev/my-project',
  options: {
    exclude_patterns: ['node_modules', '.git'],
    max_file_size_mb: 10
  }
});
```

### Python (Backend)

#### WebSocket Handler

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import json
from datetime import datetime

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"Client {client_id} connected")

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        print(f"Client {client_id} disconnected")

    async def send_personal(self, client_id: str, event: str, data: dict):
        if client_id in self.active_connections:
            message = {
                "type": event,
                "payload": data,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            await self.active_connections[client_id].send_text(json.dumps(message))

    async def broadcast(self, event: str, data: dict):
        message = {
            "type": event,
            "payload": data,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        for connection in self.active_connections.values():
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await handle_message(client_id, message)
    except WebSocketDisconnect:
        manager.disconnect(client_id)

async def handle_message(client_id: str, message: dict):
    event_type = message.get("type")
    payload = message.get("payload")

    if event_type == "handshake":
        await handle_handshake(client_id, payload)
    elif event_type == "chat.message":
        await handle_chat_message(client_id, payload)
    elif event_type == "indexing.start":
        await handle_indexing_start(client_id, payload)
    # ... more handlers

async def handle_chat_message(client_id: str, payload: dict):
    # Get RAG context
    context = await rag_service.retrieve_context(payload["message"])

    # Send stream start
    await manager.send_personal(client_id, "chat.stream.start", {
        "message_id": generate_id(),
        "rag_context": context
    })

    # Stream LLM response
    async for chunk in llm_service.stream_chat(payload["message"], context):
        await manager.send_personal(client_id, "chat.stream.chunk", {
            "chunk": chunk
        })

    # Send stream complete
    await manager.send_personal(client_id, "chat.stream.complete", {
        "message_id": generate_id(),
        "full_response": "..."
    })
```

---

## 📚 Related Documents

- `PROJECT_CHARTER.md` - Vision and success criteria
- `TECHNICAL_ARCHITECTURE.md` - System design
- `USER_JOURNEY.md` - User flows and UX (PREVIOUS)
- `DATA_MODELS.md` - Detailed data schemas (NEXT)
- `INDEXING_SYSTEM_SPEC.md` - Indexing algorithm
- `DEVELOPMENT_GUIDE.md` - Setup and workflow

---

**END OF DOCUMENT**
