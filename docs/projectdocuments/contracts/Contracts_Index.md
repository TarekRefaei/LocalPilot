# Contracts Index

This document catalogs the core contracts used by the LocalPilot extension and backend.
It is the single source of truth for message topics, payloads, and REST endpoints.

- Contract version: 0.1.0
- Transport: WebSocket (primary), REST (auxiliary)
- Envelope (WebSocket):

```json
{
  "event": "<category.name>",
  "data": { /* payload */ },
  "timestamp": "<ISO8601>",
  "correlationId": "<uuid>",
  "contractVersion": "0.1.0"
}
```

## Topics and Payloads (WebSocket)

- indexing.start
- indexing.progress
- indexing.partial_ready
- indexing.complete
- indexing.error
- indexing.cancelled

- chat.request
- chat.stream.start
- chat.stream.chunk
- chat.stream.complete
- chat.stream.error

- plan.suggest
- plan.create
- plan.update
- plan.delete

- act.request_approval
- act.apply_result
- act.error
- act.progress

- vram.warning
- vram.info

- system.health

Refer to Data_Models.md for types:
- Indexing: IndexingPhase, IndexingProgress, IndexingResult, CodeChunk, Symbol
- Chat: ChatMessage, RAGContext, ChatSession, PlanSuggestion
- Plan: Plan, TodoItem, PlanStatus
- Act: ApprovalRequest, ExecutionStatus, ActSession, FileOperation
- System: ModelInfo, SystemResources, HealthStatus

## REST Endpoints (FastAPI)

- GET /health
  - 200 OK with HealthStatus
- GET /models
  - List ModelInfo
- GET /config
  - Effective backend configuration
- PUT /config/validate
  - Validate proposed configuration; returns errors/warnings

## Versioning and Compatibility
- Additive changes only within 0.x; breaking changes bump contractVersion and are documented here.
- Consumers must check `contractVersion` and be forward-compatible where possible.

## Error Envelope

```json
{
  "event": "<category.error>",
  "data": { "message": "<error>", "code": "<string>", "details": {} },
  "timestamp": "<ISO8601>",
  "correlationId": "<uuid>",
  "contractVersion": "0.1.0"
}
```

## References
- API_Specifications.md
- Data_Models.md
- ws-contract.md
- Technical_Architecture.md
