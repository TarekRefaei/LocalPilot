# LocalPilot Master Implementation Plan (MVP v0.1)

## Executive Summary
LocalPilot is a privacy‑first, local AI coding assistant delivered as a VS Code extension with a Python backend. MVP v0.1 targets a robust Chat → Plan → Act workflow powered by a high‑quality indexing and RAG system. UI is implemented with native VS Code Side Panel views and a built‑in Chat participant (no webviews). Quality is prioritized over speed with strong TDD discipline and clean architecture.

## Confirmed MVP Decisions
- **UI**
  - Native VS Code Views API + Chat API (≥ 1.88).
  - View container id: `localpilot.views`, title: “LocalPilot”.
  - Root views: `Chat` (built‑in Chat participant), `Plans`, `Act`, `Indexing`, `Status`.
  - Chat participant id: `localpilot`, display name: “LocalPilot”.
- **Repo bootstrap**
  - Initialize Git repository and scaffold top-level structure: `extension/` (TS) and `backend/` (Python), plus base `README.md`, `LICENSE`, `.gitignore`, `.editorconfig`, `.gitattributes`, and `.github/` templates.
- **Indexing & RAG**
  - Embeddings via Ollama `bge-m3` (1024d).
  - Vector DB: Chroma for MVP (keep interfaces for future Qdrant swap).
  - Quality over latency; cache recent results; diversify re‑rank; top‑K 8–10.
- **Models & VRAM**
  - 8GB VRAM / 16GB RAM target. Mark embeddings + 7B as “permanent”; LRU for others.
  - Swap events via WebSocket (`model.swap.*`).
- **Safety**
  - Act mode requires repo presence; dry‑run preview outside repo; block writes without Git unless explicitly overridden.
- **Testing**
  - Jest for TS logic. Mocha + `@vscode/test-electron` for Views/Chat integration.
  - Gate merges on unit + integration; E2E nightly; folders with critical logic ≥ 85% coverage.
- **Windows onboarding**
  - Prebuilt Tree‑sitter binaries or fallback to lexical chunking with clear warning.

## Guiding Principles
- **SOLID** interfaces across extension services and backend layers.
- **TDD**: Red → Green → Refactor. Tests define behavior; coverage gates enforced.
- **Clean Architecture**: UI/Use‑cases/Adapters separated. Stable interfaces; replaceable infra.

## Architecture Overview
- **VS Code Extension (TypeScript)**
  - Views container: TreeDataProviders for `Plans`, `Act`, `Indexing`, `Status`.
  - Chat participant `localpilot`: streams tokens; commands for “Transfer to Plan”, “Show LocalPilot views”, “Focus Chat input (LocalPilot)”.
  - Services: WebSocket client, command router, model manager bridge, telemetry‑free logging.
- **Python Backend (FastAPI)**
  - API gateway + WebSocket server.
  - Services: indexing (five phases), embeddings, RAG pipeline, plan synthesis, act executor (dry‑run + apply).
  - Stores: Chroma (vectors), SQLite (metadata), file cache.
- **Protocols**
  - WebSocket real‑time (indexing.*, chat.*, plan.*, act.*, vram.*). REST for health/config.

## Reference Docs
- IDs and constants: [contracts/IDs_and_Constants.md](./contracts/IDs_and_Constants.md)
- Contracts index: [contracts/Contracts_Index.md](./contracts/Contracts_Index.md)
- Agents overview: [../agents/README.md](../agents/README.md)
- Agent contracts index: [../agents/contracts/README.md](../agents/contracts/README.md)

## Timeline, Milestones, and Acceptance Gates (10 Weeks)
- **Week 1 — Foundations & Bootstrap**
  - Deliverables: Initialize repo; scaffold VS Code extension (engines.vscode ≥ 1.88, strict TS, ESLint, Jest); scaffold FastAPI backend (pyproject/poetry or requirements, flake8/ruff, pytest); register Chat participant and scaffold `localpilot.views` container; baseline shared message contracts; CI (lint/type/test) on Windows runner; CODEOWNERS and contribution templates.
  - Gates: Extension loads; `localpilot.views` visible; Chat participant registered; CI green on Windows; contracts compile.
- **Week 2 — Contracts & Messaging**
  - Deliverables: Shared TS/Pydantic models; WS envelope; health + config REST; stub services.
  - Gates: Round‑trip WS ping; health endpoint; types compiled; unit test ≥ 70% for contracts.
- **Week 3 — Indexing I (Discovery, Documentation)**
  - Deliverables: Discovery executor; ignore rules; doc extraction; metadata store with file hash cache.
  - Gates: Index small repo; progress events in `Indexing` view; unit tests ≥ 75%.
- **Week 4 — Indexing II (Structure, Chunking)**
  - Deliverables: Tree‑sitter structure; symbol/import map; AST‑first chunking with lexical fallback.
  - Gates: Deterministic chunks; partial‑ready events; precision checks on chunk boundaries.
- **Week 5 — Embeddings & Vector Search**
  - Deliverables: Ollama `bge‑m3` embedding service; Chroma integration; upsert/index maintenance; filters.
  - Gates: Vector search returns coherent neighbors; retrieval harness metrics logged; unit+integration ≥ 80% for RAG infra.
- **Week 6 — Retrieval Pipeline & Chat Integration**
  - Deliverables: Multi‑level retrieval (summary/symbol/semantic/lexical) + fusion/ranking; Chat participant streaming; “Transfer to Plan”.
  - Gates: Chat returns grounded answers; plan suggestions appear; integration tests for Chat + RAG.
- **Week 7 — Plans View**
  - Deliverables: Plan model; CRUD; tree rendering; file refs; acceptance criteria; persistence.
  - Gates: Create/edit/reorder/complete steps; keyboard command to navigate; tests ≥ 80% for Plan components.
- **Week 8 — Act Mode (Safe Execution)**
  - Deliverables: Dry‑run diff preview; Git safety checks; approval workflow; apply + rollback.
  - Gates: Cannot apply without approval; blocked outside Git repo unless override; integration tests pass.
- **Week 9 — Hardening & Coverage**
  - Deliverables: Edge cases; perf checks; regression suite; VRAM monitor + model swapper.
  - Gates: Coverage overall ≥ 85% (critical ≥ 85%); type coverage 100%; no cyclic deps; perf smoke passes.
- **Week 10 — Release Readiness**
  - Deliverables: Docs finalized; onboarding; examples; VSIX packaging; issue templates.
  - Gates: E2E nightly green for 5 consecutive days; smoke on Windows; acceptance sign‑off.

## Quality Gates and Metrics
- **Coverage**: Overall ≥ 85%; critical folders (indexing, RAG, act) ≥ 85%.
- **Type Safety**: `strict` TS config; 0 implicit any; no TS compile warnings.
- **Static Analysis**: ESLint/flake8; no high‑severity issues.
- **Integration**: Views + Chat integration tests must pass on CI.
- **E2E**: Nightly Chat→Plan→Act scenario must pass on a sample repo.

## AI Coding Agent Team
- **Agent 01 — Repo Architecture & Tooling**
  - Prompt: “Set up monorepo structure for VS Code extension (TS) and FastAPI backend (Python). Enforce strict typing, linting, test runners, and CI.”
  - Success: CI green; scripts for lint/type/test; strict configs.
  - TODOs: Configure ESLint/Prettier/tsconfig; flake8/ruff/pyproject; CI workflows; VS Code tasks/launch.
- **Agent 02 — Extension Views & Commands**
  - Prompt: “Implement `localpilot.views` container with `Plans/Act/Indexing/Status` TreeViews and register commands.”
  - Success: Views render; commands visible; tests for providers.
  - TODOs: Providers, context keys, icons, keybindings, `Show LocalPilot views` command.
- **Agent 03 — Chat Participant**
  - Prompt: “Create `localpilot` Chat participant with streaming, markdown, and ‘Transfer to Plan’ action.”
  - Success: Chat responses stream; action inserts plan draft; integration tests.
  - TODOs: Participant registration; stream handler; RAG request/response; command wiring.
- **Agent 04 — WebSocket Client (TS) & Contract**
  - Prompt: “Implement robust WS client with reconnect, backoff, heartbeat; shared message types.”
  - Success: Reconnect works; messages routed; unit tests.
  - TODOs: Envelope, router, subscriptions, error states.
- **Agent 05 — Backend API Gateway (Python)**
  - Prompt: “Expose WS + REST; schema‑validated endpoints; logging; config.”
  - Success: Health, config; WS topics; tests.
  - TODOs: Pydantic models; routers; error handling.
- **Agent 06 — Indexing: Discovery & Docs**
  - Prompt: “Implement discovery, ignore rules, doc extraction, file hash cache, progress events.”
  - Success: Index small repo reliably; events emitted; unit tests.
  - TODOs: Walkers; detectors; doc parsers; metadata store.
- **Agent 07 — Indexing: Structure & Chunking**
  - Prompt: “AST‑first chunking with Tree‑sitter; fallback lexical; symbol/import maps.”
  - Success: Deterministic chunk boundaries; tests.
  - TODOs: Language drivers; chunk rules; metadata.
- **Agent 08 — Embeddings & Vector Store**
  - Prompt: “Integrate Ollama `bge‑m3`; Chroma upsert/query; ef settings; caching.”
  - Success: Stable embeddings; vector search returns sane neighbors.
  - TODOs: Pooling; batching; index maintenance; filters.
- **Agent 09 — Multi‑Level Retrieval & Ranking**
  - Prompt: “Implement multi‑level retrieval (summary/symbol/semantic/lexical) and fusion with diversity re‑rank.”
  - Success: Precision@5 ≥ 0.80 against fixture; integration tests.
  - TODOs: Query decorators; fusion; scoring; evaluators.
- **Agent 10 — Plan Mode**
  - Prompt: “Plan CRUD in TreeView; persistent storage; from‑Chat conversion; acceptance criteria model.”
  - Success: Create/edit/reorder; persisted; tests.
  - TODOs: Data model; commands; storage; UI states.
- **Agent 11 — Act Mode (Safe Execution)**
  - Prompt: “Dry‑run diffs; approval workflow; Git safety; apply/rollback.”
  - Success: Block unsafe operations; approvals logged; tests.
  - TODOs: Diff engine; previews; checkers; command execution.
- **Agent 12 — Integration & E2E**
  - Prompt: “Orchestrate cross‑component tests, fixtures, and nightly scenario.”
  - Success: E2E green; fixtures reproducible.
  - TODOs: Harness; sample repos; environment setup.
- **Agent 13 — Testing & Coverage**
  - Prompt: “Fill coverage gaps, edge cases, performance and regression; enforce gates.”
  - Success: Coverage > 90% where feasible; gates enforced; CI stable.
  - TODOs: Mutation tests (opt), load tests (opt), regression packs.
- **Agent 14 — Docs & DX**
  - Prompt: “Maintain docs, changelogs, contribution guide, onboarding; ensure Windows flow polished.”
  - Success: Up‑to‑date docs; onboarding smooth on Windows.
  - TODOs: Guides; templates; issue forms; READMEs.

## Test Strategy Alignment
- **Jest (TS)**: Services, routers, utilities, model adapters.
- **Mocha + @vscode/test-electron**: TreeViews, commands, Chat participant.
- **Pytest (Python)**: Indexing executors, embeddings, RAG, act.
- **E2E**: Chat→Plan→Act; nightly on Windows runner.

## Junior Dev Manager Guide
- **Daily Rhythm**
  - Standup: blockers, risks, today’s tests; keep WIP low.
  - Review yesterday’s failing tests first; then new work.
- **PR Checklist**
  - Tests added and pass locally; coverage meets gate.
  - No TODOs/console logs; types strict; contracts stable.
  - User‑visible changes documented; commands and views registered.
- **Branching & Commits**
  - Git Flow; conventional commits; small PRs (<400 lines diff when possible).
- **Task Review**
  - Verify acceptance criteria; run integration test locally; validate UX in VS Code Insiders (for Chat API when needed).
- **AI Agent Supervision**
  - Provide precise prompts, inputs, outputs. Require tests first. Compare diffs against plan.

## Risk Register (Top)
- **Tree‑sitter build issues (Windows)** → Prebuilt binaries; lexical fallback with warning.
- **VRAM exhaustion** → VRAM monitor; hard caps; LRU swap.
- **Index quality drift** → Golden repos; evaluation harness; nightly checks.
- **Chat API churn** → Pin VS Code engine; test against Insiders weekly.
- **Large repos (10k+)** → Early discovery estimates; docs‑first mode; chunk budget caps.

## MVP Exit Criteria
- Side panel views operational; Chat participant functional with RAG.
- Plan and Act workflows work end‑to‑end with approvals and Git safety.
- Coverage and quality gates met; E2E nightly stable.
- Docs current; onboarding reproducible on Windows.

## Post‑MVP Backlog (Brief)
- Qdrant adapter; multi‑model ensembles; advanced planning; fine‑grained code actions; richer UI affordances.
