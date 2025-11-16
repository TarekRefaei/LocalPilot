# Agent Prompts (Kickstart)

Use these prompts to kick off each agent's work. See each agent doc for scope and acceptance gates.

- **Agent 01 — Repo Architecture & Tooling**
  Prompt: "Set up monorepo structure for VS Code extension (TS) and FastAPI backend (Python). Enforce strict typing, linting, test runners, and CI."

- **Agent 02 — Extension Views & Commands**
  Prompt: "Implement `localpilot.views` container with `Plans/Act/Indexing/Status` TreeViews and register commands."

- **Agent 03 — Chat Participant**
  Prompt: "Create `localpilot` Chat participant with streaming, markdown, and ‘Transfer to Plan’ action."

- **Agent 04 — WebSocket Client & Contract**
  Prompt: "Implement robust WS client with reconnect, backoff, heartbeat; shared message types."

- **Agent 05 — Backend API Gateway**
  Prompt: "Expose WS + REST; schema-validated endpoints; logging; config."

- **Agent 06 — Indexing: Discovery & Docs**
  Prompt: "Implement discovery, ignore rules, doc extraction, file hash cache, progress events."

- **Agent 07 — Indexing: Structure & Chunking**
  Prompt: "AST‑first chunking with Tree‑sitter; fallback lexical; symbol/import maps."

- **Agent 08 — Embeddings & Vector Store**
  Prompt: "Integrate Ollama `bge‑m3`; Chroma upsert/query; ef settings; caching."

- **Agent 09 — Retrieval & Ranking**
  Prompt: "Implement multi‑level retrieval (summary/symbol/semantic/lexical) and fusion with diversity re‑rank."

- **Agent 10 — Plan Mode**
  Prompt: "Plan CRUD in TreeView; persistent storage; from‑Chat conversion; acceptance criteria model."

- **Agent 11 — Act Mode (Safe Execution)**
  Prompt: "Dry‑run diffs; approval workflow; Git safety; apply/rollback."

- **Agent 12 — Integration & E2E**
  Prompt: "Orchestrate cross‑component tests, fixtures, and nightly scenario."

- **Agent 13 — Testing & Coverage**
  Prompt: "Fill coverage gaps, edge cases, performance and regression; enforce gates."

- **Agent 14 — Docs & DX**
  Prompt: "Maintain docs, changelogs, contribution guide, onboarding; ensure Windows flow polished."
