# Agent Prompts (Kickstart)

Use these prompts to kick off each agent's work. See each agent doc for scope and acceptance gates.

## Index
- [Agent 01 — Repo Architecture & Tooling](#agent-01)
- [Agent 02 — Extension Views & Commands](#agent-02)
- [Agent 03 — Chat Participant](#agent-03)
- [Agent 04 — WebSocket Client & Contract](#agent-04)
- [Agent 05 — Backend API Gateway](#agent-05)
- [Agent 06 — Indexing: Discovery & Docs](#agent-06)
- [Agent 07 — Indexing: Structure & Chunking](#agent-07)
- [Agent 08 — Embeddings & Vector Store](#agent-08)
- [Agent 09 — Retrieval & Ranking](#agent-09)
- [Agent 10 — Plan Mode](#agent-10)
- [Agent 11 — Act Mode (Safe Execution)](#agent-11)
- [Agent 12 — Integration & E2E](#agent-12)
- [Agent 13 — Testing & Coverage](#agent-13)
- [Agent 14 — Docs & DX](#agent-14)

## Shared Context

- Repo layout
  - extension/ (VS Code TypeScript; ESLint; Jest)
  - backend/ (FastAPI; pytest; ruff; black)
  - .vscode/ (tasks.json, launch.json)
  - .github/workflows/ (ci-extension.yml, ci-backend.yml)
  - docs/ (Master Plan, Contracts Index, IDs & Constants, Agent Prompts, ADRs)
- Versions & constraints
  - VS Code ≥ 1.88
  - Node 20.x; TypeScript ~5.5.x
  - Python 3.11
  - Windows-friendly scripts; local-first
- Definition of Done (DoD)
  - CI green on Windows and Ubuntu
  - extension/: typecheck, lint, tests, compile green
  - backend/: ruff, pytest green
  - Tasks/launch usable on Windows

---

<a id="agent-01"></a>
## Agent 01 — Repo Architecture & Tooling

- Mission
  - Finalize repo architecture, strict quality gates, and dev ergonomics.
- Deliverables
  - Strict TS config; ESLint; Jest baseline. Ruff/Black; pytest baseline.
  - Improve CI reliability and caching for npm/pip across OSes.
  - .editorconfig; CODEOWNERS; PR/Issue templates; optional pre-commit hooks.
  - Validate README Quickstart and .vscode tasks/launch on Windows.
- Acceptance
  - extension: npm typecheck/lint/compile pass.
  - backend: ruff check and pytest pass.
  - Both CI workflows green on Windows+Ubuntu.
- References
  - docs/projectdocuments/Master_Implementation_Plan.md
  - docs/projectdocuments/contracts/Contracts_Index.md
  - docs/projectdocuments/contracts/IDs_and_Constants.md
  - docs/adr/0001-UI-Native-Views.md, README.md
- Output
  - Summary of changes with exact commands/files; follow-up TODOs.

<a id="agent-02"></a>
## Agent 02 — Extension Views & Commands

- Mission
  - Implement `localpilot.views` with `Plans/Act/Indexing/Status` TreeViews and commands.
- Deliverables
  - TreeDataProviders; command registrations; context keys; icons; (optional) keybindings.
  - Unit tests for providers and commands; type-safe APIs.
- Acceptance
  - Views visible; commands functional; typecheck/lint/tests pass.
- References
  - docs/projectdocuments/contracts/IDs_and_Constants.md
  - docs/projectdocuments/Technical_Architecture.md
  - docs/projectdocuments/UI_Design_System.md
  - docs/projectdocuments/Master_Implementation_Plan.md
- Output
  - Summary of changes, commands added, and tests.

<a id="agent-03"></a>
## Agent 03 — Chat Participant

- Mission
  - Register `localpilot` Chat participant with streaming markdown and “Transfer to Plan”.
- Deliverables
  - Chat participant activation; streaming responses; action to create/append a plan.
  - Integration tests covering streaming and action dispatch.
- Acceptance
  - Chat works with streaming; Transfer-to-Plan creates/updates plan; tests pass.
- References
  - docs/projectdocuments/Master_Implementation_Plan.md
  - docs/projectdocuments/Technical_Architecture.md
  - docs/adr/0001-UI-Native-Views.md
- Output
  - Summary of changes; demo steps and tests.

<a id="agent-04"></a>
## Agent 04 — WebSocket Client & Contract

- Mission
  - Robust WS client in the extension with reconnect, backoff, heartbeat; typed envelope.
- Deliverables
  - Message router; error states; offline handling; typed shared models.
- Acceptance
  - Ping/pong and reconnect verified; typecheck/lint/tests pass.
- References
  - docs/projectdocuments/contracts/Contracts_Index.md
  - docs/projectdocuments/API_Specifications.md
- Output
  - Summary of APIs, message types, and tests.

<a id="agent-05"></a>
## Agent 05 — Backend API Gateway

- Mission
  - Expose WebSocket + REST gateway with schema validation, logging, config.
- Deliverables
  - Health + config endpoints; WS handshake; Pydantic models; structured logs.
- Acceptance
  - OpenAPI schema valid; health 200; WS integration smoke passes; pytest green.
- References
  - docs/projectdocuments/API_Specifications.md
  - docs/projectdocuments/Technical_Architecture.md
- Output
  - Summary of endpoints, models, and tests.

<a id="agent-06"></a>
## Agent 06 — Indexing: Discovery & Docs

- Mission
  - Discovery walker, ignore rules, doc extraction, metadata store, progress events.
- Deliverables
  - File hashing cache; progress events surfaced to Indexing view.
- Acceptance
  - Index a small repo; progress visible; pytest >= baseline coverage.
- References
  - docs/projectdocuments/Indexing_System_Spec.md
- Output
  - Summary of extractors, store design, and tests.

<a id="agent-07"></a>
## Agent 07 — Indexing: Structure & Chunking

- Mission
  - AST-first chunking with Tree-sitter; lexical fallback; symbol/import maps.
- Deliverables
  - Deterministic chunk boundaries; partial-ready events.
- Acceptance
  - Boundary precision checks; unit tests for chunkers.
- References
  - docs/projectdocuments/Indexing_System_Spec.md
- Output
  - Summary of chunking strategy and tests.

<a id="agent-08"></a>
## Agent 08 — Embeddings & Vector Store

- Mission
  - Integrate Ollama `bge-m3`; Chroma upsert/query; filters; caching.
- Deliverables
  - Index maintenance; configurable ef/collection settings.
- Acceptance
  - Coherent nearest neighbors; metrics logged; tests pass.
- References
  - docs/projectdocuments/RAG_System_Spec.md
- Output
  - Summary of embedding pipeline and tests.

<a id="agent-09"></a>
## Agent 09 — Retrieval & Ranking

- Mission
  - Multi-level retrieval (summary/symbol/semantic/lexical) and fusion with diversity re-rank.
- Deliverables
  - Ranking metrics harness; ablations; logging.
- Acceptance
  - Grounded results on benchmarks; integration tests pass.
- References
  - docs/projectdocuments/RAG_System_Spec.md
- Output
  - Summary of retrieval stages, fusion, and metrics.

<a id="agent-10"></a>
## Agent 10 — Plan Mode

- Mission
  - Plan model and storage; CRUD; tree rendering; from-Chat conversion.
- Deliverables
  - Acceptance criteria model; keyboard navigation.
- Acceptance
  - Editing operations work; tests >= baseline.
- References
  - docs/projectdocuments/Master_Implementation_Plan.md
  - docs/projectdocuments/Technical_Architecture.md
- Output
  - Summary of data model, commands, and tests.

<a id="agent-11"></a>
## Agent 11 — Act Mode (Safe Execution)

- Mission
  - Dry-run diffs; approval workflow; Git safety; apply/rollback.
- Deliverables
  - Guardrails: block outside Git repo (unless override); approval gates.
- Acceptance
  - Cannot apply without approval; integration tests pass.
- References
  - docs/projectdocuments/Master_Implementation_Plan.md
  - docs/projectdocuments/Technical_Architecture.md
- Output
  - Summary of safety checks and tests.

<a id="agent-12"></a>
## Agent 12 — Integration & E2E

- Mission
  - Cross-component tests, fixtures, nightly scenario.
- Deliverables
  - Stable E2E scenario with deterministic seeds.
- Acceptance
  - Nightly E2E green; failure diagnostics collected.
- References
  - docs/projectdocuments/Testing_Strategy.md
- Output
  - Summary of scenarios, fixtures, and results.

<a id="agent-13"></a>
## Agent 13 — Testing & Coverage

- Mission
  - Fill coverage gaps, edge cases, performance, regression packs; enforce gates.
- Deliverables
  - Coverage thresholds; regression suites; perf smoke tests.
- Acceptance
  - Overall coverage meets gates; fast feedback.
- References
  - docs/projectdocuments/Testing_Strategy.md
- Output
  - Summary of tests added and coverage deltas.

<a id="agent-14"></a>
## Agent 14 — Docs & DX

- Mission
  - Maintain docs, changelogs, contribution guide, onboarding; Windows polish.
- Deliverables
  - Docs consistency; glossary; release checklist alignment.
- Acceptance
  - Docs up-to-date; onboarding under 15 minutes; release checklist passes.
- References
  - docs/Glossary.md, docs/Release_Checklist.md, README.md
- Output
  - Summary of docs changes and links.
