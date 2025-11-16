# IDs and Constants (Single Source of Truth)

Authoritative IDs, command names, and topics used across extension and backend. Update here first; reference in agent docs and code.

## Views and Participants
- View container id: `localpilot.views`
- Views (proposed ids):
  - Plans: `localpilot.views.plans`
  - Act: `localpilot.views.act`
  - Indexing: `localpilot.views.indexing`
  - Status: `localpilot.views.status`
- Chat participant id: `localpilot`
- Chat display name: `LocalPilot`

## Commands (proposed)
- Core
  - Show views: `localpilot.showViews`
  - Focus Chat input: `localpilot.focusChatInput`
- Chat/Plan
  - Transfer to Plan: `localpilot.chat.transferToPlan`
- Plans
  - Create Plan: `localpilot.plan.create`
  - Update Plan: `localpilot.plan.update`
  - Delete Plan: `localpilot.plan.delete`
- Act
  - Dry-run: `localpilot.act.dryRun`
  - Approve: `localpilot.act.approve`
  - Apply: `localpilot.act.apply`
  - Rollback: `localpilot.act.rollback`
- Indexing
  - Start: `localpilot.index.start`
  - Stop: `localpilot.index.stop`
- Models
  - Swap: `localpilot.model.swap`

## WebSocket Topics
- indexing.start | indexing.progress | indexing.partial_ready | indexing.complete | indexing.error | indexing.cancelled
- chat.request | chat.stream.start | chat.stream.chunk | chat.stream.complete | chat.stream.error
- plan.suggest | plan.create | plan.update | plan.delete
- act.request_approval | act.apply_result | act.progress | act.error
- vram.warning | vram.info
- system.health

## Storage and Paths (MVP)
- Vector DB (Chroma) path: `.localpilot/vectordb`
- SQLite metadata path: `.localpilot/meta.db`

## Config Keys (Backend .env)
- OLLAMA_HOST, OLLAMA_TIMEOUT_SECONDS
- VECTOR_DB_PATH
- LOG_LEVEL, DEBUG
- EMBEDDING_MODEL, CHAT_MODEL, PLANNING_MODEL, CODING_MODEL
- MAX_CONCURRENT_EMBEDDINGS, BATCH_SIZE_INDEXING

## Notes
- Prefer kebab-case in filenames; dot-separated namespaces for WS topics; camelCase for TS properties; snake_case for Python fields.
- Keep this file synchronized with: Contracts_Index.md, API_Specifications.md, Data_Models.md, and package.json contributions.
