# 📄 PROJECT_STRUCTURE.md (Complete Updated Version)

```markdown
# 📄 PROJECT_STRUCTURE.md

# LocalPilot - Project Structure

> Complete folder structure and file organization for the LocalPilot project

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Project Structure Specification |
| **Related To** | PROJECT_OVERVIEW.md, ARCHITECTURE.md |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |
| **Version** | 1.1.0 |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Repository Root Structure](#2-repository-root-structure)
3. [VS Code Extension Structure](#3-vs-code-extension-structure)
4. [Python RAG Server Structure](#4-python-rag-server-structure)
5. [Scripts Folder](#5-scripts-folder)
6. [Storage Locations](#6-storage-locations)
7. [Configuration Files](#7-configuration-files)
8. [File Naming Conventions](#8-file-naming-conventions)
9. [Import Rules](#9-import-rules)
10. [AI Agent Instructions](#10-ai-agent-instructions)

---

## 1. Overview

### Project Type: Monorepo

LocalPilot uses a **monorepo** structure containing two main packages:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONOREPO STRUCTURE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LocalPilot/                                                     │
│  ├── extension/          ← VS Code Extension (TypeScript)       │
│  ├── server/             ← Python RAG Server                    │
│  ├── docs/               ← Documentation                        │
│  ├── scripts/            ← Build & utility scripts              │
│  └── [config files]      ← Root configuration                   │
│                                                                  │
│  WHY MONOREPO?                                                   │
│  • Single repository for all code                               │
│  • Easier to keep extension and server in sync                  │
│  • Shared documentation                                          │
│  • Single git history                                            │
│  • Simpler for solo developer                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Directories Summary

| Directory | Purpose | Language |
|-----------|---------|----------|
| `extension/` | VS Code extension with React WebView | TypeScript |
| `server/` | RAG server with indexing pipeline | Python |
| `docs/` | All project documentation | Markdown |
| `scripts/` | Build, setup, and utility scripts | PowerShell/Bash |
| `.vscode/` | VS Code workspace settings | JSON |
| `.github/` | GitHub Actions and templates | YAML |

---

## 2. Repository Root Structure

```
LocalPilot/
│
├── 📁 extension/                    # VS Code Extension (TypeScript/React)
│   └── [See Section 3 for details]
│
├── 📁 server/                       # Python RAG Server
│   └── [See Section 4 for details]
│
├── 📁 scripts/                      # Build and utility scripts
│   └── [See Section 5 for details]
│
├── 📁 docs/                         # Documentation
│   ├── 📁 ProjectDocuments/         # Main project documentation
│   │   ├── 📄 overview.md           # Master project document
│   │   ├── 📄 architecture.md       # System architecture
│   │   ├── 📄 structure.md          # This document
│   │   ├── 📄 development-setup.md  # Environment setup guide
│   │   ├── 📄 indexing-spec.md      # Indexing quality contract
│   │   ├── 📄 security-model.md     # Security boundaries
│   │   ├── 📄 state-model.md        # State management spec
│   │   ├── 📄 prompt-engineer.md    # Prompt templates
│   │   ├── 📄 task0-phase.md        # Phase 0 tasks
│   │   ├── 📄 webview-protocol.md   # WebView message protocol
│   │   ├── 📄 testing-strategy.md   # Testing approach
│   │   └── 📄 troubleshooting.md    # Common issues & solutions
│   │
│   ├── 📁 decisions/                # Architecture Decision Records
│   │   ├── 📄 000-template.md       # ADR template
│   │   ├── 📄 001-monorepo-structure.md
│   │   ├── 📄 002-llamaindex-over-langchain.md
│   │   └── 📄 003-chromadb-for-vectors.md
│   │
│   └── 📁 images/                   # Documentation images
│       ├── 📷 architecture-diagram.png
│       ├── 📷 workflow-diagram.png
│       └── 📁 ui-mockups/
│
├── 📁 .github/                      # GitHub configuration
│   ├── 📁 workflows/                # GitHub Actions
│   │   ├── 📄 ci.yml                # Continuous Integration
│   │   ├── 📄 extension-build.yml   # Extension build/test
│   │   └── 📄 server-build.yml      # Server build/test
│   ├── 📄 ISSUE_TEMPLATE.md
│   └── 📄 PULL_REQUEST_TEMPLATE.md
│
├── 📁 .vscode/                      # VS Code workspace settings
│   ├── 📄 settings.json             # Editor settings
│   ├── 📄 launch.json               # Debug configurations
│   ├── 📄 tasks.json                # Build tasks
│   └── 📄 extensions.json           # Recommended extensions
│
├── 📄 .gitignore                    # Git ignore rules
├── 📄 .editorconfig                 # Editor configuration
├── 📄 README.md                     # Repository README
├── 📄 LICENSE                       # License file (MIT)
├── 📄 CHANGELOG.md                  # Version changelog
└── 📄 CONTRIBUTING.md               # Contribution guidelines
```

---

## 3. VS Code Extension Structure

### Complete Extension Folder Structure

```
extension/
│
├── 📁 src/                          # Source code
│   │
│   ├── 📁 core/                     # Core domain layer (no external dependencies)
│   │   │
│   │   ├── 📁 entities/             # Business entities
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 project.entity.ts           # Project representation
│   │   │   ├── 📄 message.entity.ts           # Chat message
│   │   │   ├── 📄 plan.entity.ts              # Plan with tasks
│   │   │   ├── 📄 task.entity.ts              # Individual task
│   │   │   ├── 📄 chunk.entity.ts             # Retrieved code chunk
│   │   │   └── 📄 file-change.entity.ts       # File modification
│   │   │
│   │   ├── 📁 interfaces/           # Contracts/Ports (abstract)
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 llm-provider.interface.ts      # LLM operations
│   │   │   ├── 📄 rag-provider.interface.ts      # RAG operations
│   │   │   ├── 📄 file-system.interface.ts       # File operations
│   │   │   ├── 📄 indexer.interface.ts           # Indexing operations
│   │   │   └── 📄 settings.interface.ts          # Settings operations
│   │   │
│   │   ├── 📁 errors/               # Custom error types
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 base.error.ts                 # Base error class
│   │   │   ├── 📄 ollama.error.ts               # Ollama-specific errors
│   │   │   ├── 📄 indexing.error.ts             # Indexing errors
│   │   │   ├── 📄 server.error.ts               # Python server errors
│   │   │   └── 📄 file-operation.error.ts       # File operation errors
│   │   │
│   │   └── 📁 types/                # Shared type definitions
│   │       ├── 📄 index.ts          # Public exports
│   │       ├── 📄 mode.types.ts                 # Chat/Plan/Act modes
│   │       ├── 📄 ollama.types.ts               # Ollama API types
│   │       └── 📄 events.types.ts               # Event types
│   │
│   ├── 📁 features/                 # Feature modules (use cases)
│   │   │
│   │   ├── 📁 indexing/             # Indexing feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 indexing.service.ts           # Main indexing logic
│   │   │   ├── 📄 sync.service.ts               # Smart sync logic
│   │   │   ├── 📄 progress-reporter.ts          # Progress updates
│   │   │   └── 📁 __tests__/        # Feature tests
│   │   │       ├── 📄 indexing.service.test.ts
│   │   │       └── 📄 sync.service.test.ts
│   │   │
│   │   ├── 📁 chat/                 # Chat mode feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 chat.service.ts               # Chat logic
│   │   │   ├── 📄 context-builder.ts            # RAG context assembly
│   │   │   ├── 📄 message-handler.ts            # Message processing
│   │   │   ├── 📄 summary-generator.ts          # Project summary
│   │   │   └── 📁 __tests__/
│   │   │       ├── 📄 chat.service.test.ts
│   │   │       └── 📄 context-builder.test.ts
│   │   │
│   │   ├── 📁 plan/                 # Plan mode feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 plan.service.ts               # Plan generation
│   │   │   ├── 📄 plan-parser.ts                # Parse LLM output to Plan
│   │   │   ├── 📄 task-extractor.ts             # Extract tasks from plan
│   │   │   └── 📁 __tests__/
│   │   │       ├── 📄 plan.service.test.ts
│   │   │       └── 📄 plan-parser.test.ts
│   │   │
│   │   ├── 📁 act/                  # Act mode feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 act.service.ts                # Act orchestration
│   │   │   ├── 📄 task-executor.ts              # Execute single task
│   │   │   ├── 📄 code-generator.ts             # Generate code for task
│   │   │   ├── 📄 diff-generator.ts             # Generate file diffs
│   │   │   ├── 📄 file-writer.ts                # Write files safely
│   │   │   ├── 📄 backup-manager.ts             # Manage file backups
│   │   │   └── 📁 __tests__/
│   │   │       ├── 📄 act.service.test.ts
│   │   │       └── 📄 task-executor.test.ts
│   │   │
│   │   ├── 📁 ollama/               # Ollama integration feature
│   │   │   ├── 📄 README.md         # Feature documentation
│   │   │   ├── 📄 index.ts          # Public exports
│   │   │   ├── 📄 ollama.service.ts             # Main Ollama service
│   │   │   ├── 📄 connection-manager.ts         # Health checks
│   │   │   ├── 📄 model-manager.ts              # Model listing/selection
│   │   │   ├── 📄 stream-handler.ts             # Handle streaming responses
│   │   │   └── 📁 __tests__/
│   │   │       ├── 📄 ollama.service.test.ts
│   │   │       └── 📄 connection-manager.test.ts
│   │   │
│   │   └── 📁 settings/             # Settings feature
│   │       ├── 📄 README.md
│   │       ├── 📄 index.ts
│   │       ├── 📄 settings.service.ts           # Settings management
│   │       ├── 📄 default-settings.ts           # Default values
│   │       └── 📁 __tests__/
│   │           └── 📄 settings.service.test.ts
│   │
│   ├── 📁 infrastructure/           # External adapters (implementations)
│   │   │
│   │   ├── 📁 vscode/               # VS Code API adapters
│   │   │   ├── 📄 index.ts
│   │   │   ├── 📄 file-system.adapter.ts        # Implements IFileSystem
│   │   │   ├── 📄 settings.adapter.ts           # Implements ISettings
│   │   │   ├── 📄 output-channel.ts             # Logging
│   │   │   └── 📄 status-bar.ts                 # Status bar management
│   │   │
│   │   ├── 📁 http/                 # HTTP client for Python server
│   │   │   ├── 📄 index.ts
│   │   │   ├── 📄 api-client.ts                 # HTTP client wrapper
│   │   │   ├── 📄 endpoints.ts                  # API endpoint definitions
│   │   │   └── 📄 request-builder.ts            # Request construction
│   │   │
│   │   └── 📁 websocket/            # WebSocket for streaming
│   │       ├── 📄 index.ts
│   │       ├── 📄 ws-client.ts                  # WebSocket client
│   │       └── 📄 stream-processor.ts           # Process incoming streams
│   │
│   ├── 📁 ui/                       # Presentation layer
│   │   │
│   │   ├── 📁 webview/              # React WebView application
│   │   │   ├── 📄 index.tsx         # React entry point
│   │   │   ├── 📄 App.tsx           # Main App component
│   │   │   │
│   │   │   ├── 📁 components/       # Reusable UI components
│   │   │   │   ├── 📁 common/       # Shared components
│   │   │   │   │   ├── 📄 Button.tsx
│   │   │   │   │   ├── 📄 Input.tsx
│   │   │   │   │   ├── 📄 Card.tsx
│   │   │   │   │   ├── 📄 Progress.tsx
│   │   │   │   │   ├── 📄 Spinner.tsx
│   │   │   │   │   ├── 📄 Badge.tsx
│   │   │   │   │   ├── 📄 Tabs.tsx
│   │   │   │   │   ├── 📄 CodeBlock.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   ├── 📁 chat/         # Chat-specific components
│   │   │   │   │   ├── 📄 ChatContainer.tsx
│   │   │   │   │   ├── 📄 MessageList.tsx
│   │   │   │   │   ├── 📄 MessageItem.tsx
│   │   │   │   │   ├── 📄 ChatInput.tsx
│   │   │   │   │   ├── 📄 TransferButton.tsx
│   │   │   │   │   ├── 📄 RagContextPanel.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   ├── 📁 plan/         # Plan-specific components
│   │   │   │   │   ├── 📄 PlanContainer.tsx
│   │   │   │   │   ├── 📄 PlanHeader.tsx
│   │   │   │   │   ├── 📄 TaskList.tsx
│   │   │   │   │   ├── 📄 TaskItem.tsx
│   │   │   │   │   ├── 📄 PlanActions.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   ├── 📁 act/          # Act-specific components
│   │   │   │   │   ├── 📄 ActContainer.tsx
│   │   │   │   │   ├── 📄 ProgressTracker.tsx
│   │   │   │   │   ├── 📄 CurrentTask.tsx
│   │   │   │   │   ├── 📄 CodePreview.tsx
│   │   │   │   │   ├── 📄 DiffView.tsx
│   │   │   │   │   ├── 📄 TaskControls.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   ├── 📁 onboarding/   # Onboarding components
│   │   │   │   │   ├── 📄 OnboardingScreen.tsx
│   │   │   │   │   ├── 📄 OllamaStatus.tsx
│   │   │   │   │   ├── 📄 ServerStatus.tsx
│   │   │   │   │   ├── 📄 IndexingProgress.tsx
│   │   │   │   │   ├── 📄 WelcomeMessage.tsx
│   │   │   │   │   └── 📄 index.ts
│   │   │   │   │
│   │   │   │   └── 📁 layout/       # Layout components
│   │   │   │       ├── 📄 Header.tsx
│   │   │   │       ├── 📄 TabBar.tsx
│   │   │   │       ├── 📄 StatusFooter.tsx
│   │   │   │       └── 📄 index.ts
│   │   │   │
│   │   │   ├── 📁 hooks/            # Custom React hooks
│   │   │   │   ├── 📄 useChat.ts
│   │   │   │   ├── 📄 usePlan.ts
│   │   │   │   ├── 📄 useAct.ts
│   │   │   │   ├── 📄 useIndexing.ts
│   │   │   │   ├── 📄 useOllama.ts
│   │   │   │   ├── 📄 useVSCode.ts              # VS Code API hook
│   │   │   │   └── 📄 index.ts
│   │   │   │
│   │   │   ├── 📁 store/            # Zustand state management
│   │   │   │   ├── 📄 index.ts
│   │   │   │   ├── 📄 app.store.ts              # Main app state
│   │   │   │   ├── 📄 chat.store.ts             # Chat state
│   │   │   │   ├── 📄 plan.store.ts             # Plan state
│   │   │   │   ├── 📄 act.store.ts              # Act state
│   │   │   │   └── 📄 settings.store.ts         # Settings state
│   │   │   │
│   │   │   ├── 📁 styles/           # Styling
│   │   │   │   ├── 📄 globals.css               # Global styles
│   │   │   │   ├── 📄 variables.css             # CSS variables
│   │   │   │   └── 📄 tailwind.css              # Tailwind entry
│   │   │   │
│   │   │   ├── 📁 utils/            # UI utilities
│   │   │   │   ├── 📄 vscode-api.ts             # VS Code WebView API
│   │   │   │   ├── 📄 message-handler.ts        # Handle messages from extension
│   │   │   │   └── 📄 formatters.ts             # Text/code formatters
│   │   │   │
│   │   │   └── 📁 types/            # UI-specific types
│   │   │       ├── 📄 props.types.ts
│   │   │       ├── 📄 messages.types.ts         # WebView message protocol
│   │   │       └── 📄 vscode.d.ts               # VS Code WebView types
│   │   │
│   │   ├── 📁 panels/               # WebView panel management
│   │   │   ├── 📄 index.ts
│   │   │   ├── 📄 main-panel.ts                 # Main sidebar panel
│   │   │   └── 📄 webview-provider.ts           # WebView content provider
│   │   │
│   │   └── 📁 commands/             # VS Code commands
│   │       ├── 📄 index.ts
│   │       ├── 📄 register-commands.ts          # Command registration
│   │       ├── 📄 indexing.commands.ts          # Indexing commands
│   │       ├── 📄 chat.commands.ts              # Chat commands
│   │       └── 📄 settings.commands.ts          # Settings commands
│   │
│   ├── 📁 prompts/                  # LLM prompt templates
│   │   ├── 📄 index.ts              # Prompt registry
│   │   ├── 📄 types.ts              # Prompt types
│   │   ├── 📁 system/               # System prompts
│   │   │   ├── 📄 chat.system.ts
│   │   │   ├── 📄 plan.system.ts
│   │   │   └── 📄 act.system.ts
│   │   └── 📁 templates/            # User prompts
│   │       ├── 📄 summary.prompt.ts
│   │       ├── 📄 plan-generate.prompt.ts
│   │       ├── 📄 code-create.prompt.ts
│   │       └── 📄 code-modify.prompt.ts
│   │
│   ├── 📁 utils/                    # Shared utilities
│   │   ├── 📄 index.ts
│   │   ├── 📄 logger.ts                         # Logging utility
│   │   ├── 📄 debounce.ts                       # Debounce helper
│   │   ├── 📄 retry.ts                          # Retry logic
│   │   ├── 📄 hash.ts                           # Hashing utilities
│   │   └── 📄 validators.ts                     # Input validation
│   │
│   ├── 📄 extension.ts              # Extension entry point
│   └── 📄 constants.ts              # Global constants
│
├── 📁 test/                         # Test configuration and utilities
│   ├── 📄 setup.ts                  # Test setup
│   ├── 📄 mocks.ts                  # Shared mocks
│   └── 📁 fixtures/                 # Test fixtures
│       ├── 📁 sample-ts-project/    # Sample TypeScript project
│       ├── 📁 sample-py-project/    # Sample Python project
│       └── 📄 sample-responses.ts   # Sample LLM responses
│
├── 📁 resources/                    # Static resources
│   ├── 📁 icons/                    # Extension icons
│   │   ├── 📷 icon.png              # Main icon (128x128)
│   │   ├── 📷 icon-dark.svg         # Dark theme icon
│   │   └── 📷 icon-light.svg        # Light theme icon
│   └── 📁 media/                    # WebView media
│       └── 📄 reset.css             # CSS reset for WebView
│
├── 📄 package.json                  # Extension manifest
├── 📄 tsconfig.json                 # TypeScript configuration
├── 📄 tsconfig.webview.json         # WebView TypeScript config
├── 📄 tailwind.config.js            # Tailwind configuration
├── 📄 postcss.config.js             # PostCSS configuration
├── 📄 esbuild.js                    # esbuild configuration
├── 📄 vitest.config.ts              # Vitest configuration
├── 📄 .eslintrc.json                # ESLint configuration
├── 📄 .prettierrc                   # Prettier configuration
└── 📄 README.md                     # Extension README
```

---

## 4. Python RAG Server Structure

### Complete Server Folder Structure

```
server/
│
├── 📁 src/                          # Source code
│   │
│   ├── 📁 api/                      # API layer (FastAPI routes)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py               # FastAPI app entry
│   │   ├── 📄 dependencies.py       # Dependency injection
│   │   │
│   │   ├── 📁 routes/               # API routes
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 health.py         # Health check endpoints
│   │   │   ├── 📄 index.py          # Indexing endpoints
│   │   │   ├── 📄 query.py          # RAG query endpoints
│   │   │   ├── 📄 chat.py           # Chat endpoints
│   │   │   └── 📄 models.py         # Model management endpoints
│   │   │
│   │   ├── 📁 schemas/              # Pydantic models (request/response)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 index.py          # Indexing schemas
│   │   │   ├── 📄 query.py          # Query schemas
│   │   │   ├── 📄 chat.py           # Chat schemas
│   │   │   └── 📄 common.py         # Common schemas
│   │   │
│   │   └── 📁 websocket/            # WebSocket handlers
│   │       ├── 📄 __init__.py
│   │       ├── 📄 chat_ws.py        # Chat streaming
│   │       └── 📄 progress_ws.py    # Indexing progress
│   │
│   ├── 📁 core/                     # Core domain layer
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 entities/             # Domain entities
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 document.py       # Document representation
│   │   │   ├── 📄 chunk.py          # Code chunk
│   │   │   ├── 📄 embedding.py      # Embedding with metadata
│   │   │   └── 📄 query_result.py   # Query result
│   │   │
│   │   ├── 📁 interfaces/           # Abstract interfaces
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 embedder.py       # Embedding interface
│   │   │   ├── 📄 vector_store.py   # Vector store interface
│   │   │   ├── 📄 llm.py            # LLM interface
│   │   │   └── 📄 parser.py         # Code parser interface
│   │   │
│   │   └── 📁 errors/               # Custom exceptions
│   │       ├── 📄 __init__.py
│   │       ├── 📄 base.py           # Base exception
│   │       ├── 📄 indexing.py       # Indexing errors
│   │       └── 📄 ollama.py         # Ollama errors
│   │
│   ├── 📁 services/                 # Business logic services
│   │   ├── 📄 __init__.py
│   │   ├── 📄 indexing_service.py   # Main indexing orchestration
│   │   ├── 📄 rag_service.py        # RAG query service
│   │   ├── 📄 chat_service.py       # Chat with RAG context
│   │   ├── 📄 sync_service.py       # Smart sync service
│   │   └── 📄 summary_service.py    # Project summary generation
│   │
│   ├── 📁 indexing/                 # Indexing subsystem
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 parsers/              # Language-specific parsers
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 base_parser.py    # Base parser class
│   │   │   ├── 📄 typescript_parser.py
│   │   │   ├── 📄 javascript_parser.py
│   │   │   ├── 📄 python_parser.py
│   │   │   ├── 📄 dart_parser.py
│   │   │   └── 📄 parser_factory.py # Parser selection
│   │   │
│   │   ├── 📄 chunker.py            # Code chunking logic
│   │   ├── 📄 file_scanner.py       # File discovery
│   │   ├── 📄 hash_tracker.py       # File hash tracking
│   │   └── 📄 progress_tracker.py   # Progress reporting
│   │
│   ├── 📁 infrastructure/           # External implementations
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 ollama/               # Ollama integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 client.py         # Ollama API client
│   │   │   ├── 📄 embedder.py       # Ollama embedder (implements interface)
│   │   │   └── 📄 llm.py            # Ollama LLM (implements interface)
│   │   │
│   │   ├── 📁 chromadb/             # ChromaDB integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 client.py         # ChromaDB client
│   │   │   └── 📄 vector_store.py   # ChromaDB store (implements interface)
│   │   │
│   │   ├── 📁 llamaindex/           # LlamaIndex integration
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 index_builder.py  # Build LlamaIndex index
│   │   │   └── 📄 query_engine.py   # Query with LlamaIndex
│   │   │
│   │   └── 📁 treesitter/           # Tree-sitter integration
│   │       ├── 📄 __init__.py
│   │       ├── 📄 parser.py         # Tree-sitter parser wrapper
│   │       └── 📁 queries/          # Tree-sitter query files
│   │           ├── 📄 typescript.scm
│   │           ├── 📄 javascript.scm
│   │           ├── 📄 python.scm
│   │           └── 📄 dart.scm
│   │
│   ├── 📁 utils/                    # Utilities
│   │   ├── 📄 __init__.py
│   │   ├── 📄 logger.py             # Logging setup
│   │   ├── 📄 file_utils.py         # File helpers
│   │   └── 📄 hash_utils.py         # Hashing helpers
│   │
│   └── 📄 config.py                 # Configuration management
│
├── 📁 tests/                        # Test suite
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py               # Pytest fixtures
│   │
│   ├── 📁 unit/                     # Unit tests
│   │   ├── 📄 __init__.py
│   │   ├── 📁 parsers/
│   │   │   ├── 📄 test_typescript_parser.py
│   │   │   ├── 📄 test_python_parser.py
│   │   │   └── 📄 test_dart_parser.py
│   │   ├── 📄 test_chunker.py
│   │   └── 📄 test_hash_tracker.py
│   │
│   ├── 📁 integration/              # Integration tests
│   │   ├── 📄 __init__.py
│   │   ├── 📄 test_ollama_client.py
│   │   ├── 📄 test_chromadb.py
│   │   └── 📄 test_indexing_pipeline.py
│   │
│   └── 📁 fixtures/                 # Test fixtures
│       ├── 📁 sample_code/
│       │   ├── 📄 sample.ts
│       │   ├── 📄 sample.py
│       │   └── 📄 sample.dart
│       └── 📄 expected_chunks.json
│
├── 📄 pyproject.toml                # Project configuration (uv/poetry)
├── 📄 requirements.txt              # Dependencies (fallback)
├── 📄 requirements-dev.txt          # Dev dependencies
├── 📄 pytest.ini                    # Pytest configuration
├── 📄 ruff.toml                     # Ruff linter configuration
├── 📄 mypy.ini                      # MyPy type checking
├── 📄 Dockerfile                    # Container definition (future)
└── 📄 README.md                     # Server README
```

---

## 5. Scripts Folder

### Script Files

```
scripts/
│
├── 📄 start-server.ps1              # Start Python server (Windows)
│   └── Usage: .\scripts\start-server.ps1 [-Dev] [-Port 52741]
│
├── 📄 start-server.sh               # Start Python server (Unix, future)
│   └── Usage: ./scripts/start-server.sh [--dev] [--port 52741]
│
├── 📄 setup.ps1                     # Full environment setup (Windows)
│   └── Installs: Node.js, pnpm, Python, uv, Ollama
│   └── Pulls: Default models
│   └── Creates: Virtual environments
│
├── 📄 build-all.ps1                 # Build both packages
│   └── Runs: Extension build + Server checks
│   └── Output: extension/dist/, type checks
│
├── 📄 package-extension.ps1         # Create .vsix file
│   └── Runs: vsce package
│   └── Output: localpilot-{version}.vsix
│
├── 📄 clean.ps1                     # Clean build artifacts
│   └── Removes: dist/, node_modules/, .venv/, __pycache__/
│
├── 📄 test-all.ps1                  # Run all tests
│   └── Runs: Extension tests + Server tests
│   └── Coverage: Reports combined coverage
│
└── 📄 dev.ps1                       # Start development environment
    └── Starts: Server (background) + Extension watch mode
    └── Opens: VS Code in debug mode
```

### Script Descriptions

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `start-server.ps1` | Start the Python RAG server | Before using extension |
| `setup.ps1` | One-time environment setup | New developer onboarding |
| `build-all.ps1` | Build extension for production | Before packaging |
| `package-extension.ps1` | Create installable .vsix | For distribution |
| `clean.ps1` | Remove all generated files | When things are broken |
| `test-all.ps1` | Run complete test suite | Before commits |
| `dev.ps1` | Quick development startup | Daily development |

---

## 6. Storage Locations

### 6.1 Storage Location Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    STORAGE LOCATIONS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  There are THREE types of storage:                              │
│                                                                  │
│  1. GLOBAL (~/.localpilot/)                                     │
│     Cross-project data that persists across workspaces          │
│                                                                  │
│  2. WORKSPACE ({workspace}/.localpilot/)                        │
│     Project-specific data stored within the workspace           │
│                                                                  │
│  3. EXTENSION (VS Code managed)                                 │
│     Session and workspace state managed by VS Code             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Global Storage (~/.localpilot/)

```
~/.localpilot/                       # User home directory
│
├── 📁 indexes/                      # All project indexes
│   │
│   ├── 📁 {project-id-1}/           # Index for project 1
│   │   ├── 📁 chroma/               # ChromaDB database files
│   │   │   ├── chroma.sqlite3       # SQLite database
│   │   │   └── ...                  # Other ChromaDB files
│   │   ├── 📄 metadata.json         # Index metadata
│   │   │   └── Contains: project_id, workspace_path, 
│   │   │       indexed_at, files_count, chunks_count, languages
│   │   └── 📄 hashes.json           # File hash tracking
│   │       └── Contains: { "path": { hash, indexed_at, chunk_ids } }
│   │
│   └── 📁 {project-id-2}/           # Index for project 2
│       └── ...
│
├── 📁 logs/                         # Application logs
│   ├── 📄 server.log                # Python server logs
│   └── 📄 extension.log             # Extension logs (if file logging enabled)
│
└── 📄 settings.json                 # Global settings (optional override)
    └── Only if not using VS Code settings API
```

**Project ID Generation:**

```typescript
function generateProjectId(workspacePath: string): string {
  // Hash the absolute path for uniqueness
  const hash = crypto
    .createHash('sha256')
    .update(workspacePath)
    .digest('hex')
    .substring(0, 16);
  
  // Include folder name for readability
  const folderName = path.basename(workspacePath)
    .replace(/[^a-zA-Z0-9]/g, '_')
    .substring(0, 20);
  
  return `${folderName}_${hash}`;
  // Example: "my_project_a1b2c3d4e5f6g7h8"
}
```

### 6.3 Workspace Storage ({workspace}/.localpilot/)

```
{workspace}/                         # User's project folder
│
├── 📁 .localpilot/                  # LocalPilot workspace data
│   │
│   ├── 📁 backups/                  # File backups from Act mode
│   │   ├── 📁 2024-01-15T10-30-00/  # Timestamped backup folder
│   │   │   ├── 📄 src_auth_auth.service.ts  # Backed up file
│   │   │   └── 📄 src_utils_helpers.ts      # Another backup
│   │   └── 📁 2024-01-15T14-22-00/  # Another backup session
│   │       └── ...
│   │
│   └── 📄 audit.log                 # Operations audit trail
│       └── JSON lines: { timestamp, operation, file, result }
│
├── 📄 TODO.md                       # Generated by Act mode (in workspace root)
│   └── Contains: Current plan tasks with checkboxes
│
└── ... (other project files)
```

**Important:** Add to your project's `.gitignore`:

```gitignore
# LocalPilot workspace data
.localpilot/
```

### 6.4 Extension Storage (VS Code Managed)

```
┌─────────────────────────────────────────────────────────────────┐
│                  VS CODE EXTENSION STORAGE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  context.workspaceState (per-workspace session data)            │
│  ─────────────────────────────────────────────────────────────  │
│  • Chat message history                                          │
│  • Current plan draft                                            │
│  • Act mode progress                                             │
│  • Current mode (chat/plan/act)                                 │
│  • Execution checkpoint (for recovery)                          │
│                                                                  │
│  Cleared: When VS Code closes (session scope)                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  context.globalState (cross-workspace settings)                 │
│  ─────────────────────────────────────────────────────────────  │
│  • Onboarding completion flag                                    │
│  • User preferences                                              │
│  • Recent projects list                                          │
│                                                                  │
│  Cleared: Never (global scope)                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.5 Storage Decision Matrix

| Data Type | Location | Reason |
|-----------|----------|--------|
| Vector embeddings | `~/.localpilot/indexes/` | Large, reusable across sessions |
| File hashes | `~/.localpilot/indexes/` | Needed for sync even after restart |
| Index metadata | `~/.localpilot/indexes/` | Persists with index |
| File backups | `{workspace}/.localpilot/` | Project-specific, user might want access |
| Audit log | `{workspace}/.localpilot/` | Project-specific history |
| Chat history | VS Code workspaceState | Session-only (MVP) |
| Current plan | VS Code workspaceState | Session-only |
| User settings | VS Code settings API | Standard VS Code pattern |
| Server logs | `~/.localpilot/logs/` | Cross-project, for debugging |

---

## 7. Configuration Files

### 7.1 Root Configuration Files

```
┌─────────────────────────────────────────────────────────────────┐
│                    ROOT CONFIGURATION FILES                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  .gitignore                                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  # Node                                                          │
│  node_modules/                                                   │
│  *.vsix                                                          │
│  dist/                                                           │
│  out/                                                            │
│                                                                  │
│  # Python                                                        │
│  __pycache__/                                                    │
│  *.py[cod]                                                       │
│  *$py.class                                                      │
│  .venv/                                                          │
│  venv/                                                           │
│  *.egg-info/                                                     │
│                                                                  │
│  # IDE                                                           │
│  .idea/                                                          │
│  *.swp                                                           │
│  *.swo                                                           │
│                                                                  │
│  # OS                                                            │
│  .DS_Store                                                       │
│  Thumbs.db                                                       │
│                                                                  │
│  # Project specific                                              │
│  server/data/                                                    │
│  .localpilot/                                                    │
│  *.log                                                           │
│                                                                  │
│  # Environment                                                   │
│  .env                                                            │
│  .env.local                                                      │
│                                                                  │
│  # Build                                                         │
│  *.tsbuildinfo                                                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  .editorconfig                                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  root = true                                                     │
│                                                                  │
│  [*]                                                             │
│  indent_style = space                                            │
│  end_of_line = lf                                                │
│  charset = utf-8                                                 │
│  trim_trailing_whitespace = true                                │
│  insert_final_newline = true                                    │
│                                                                  │
│  [*.{ts,tsx,js,jsx,json}]                                       │
│  indent_size = 2                                                 │
│                                                                  │
│  [*.py]                                                          │
│  indent_size = 4                                                 │
│                                                                  │
│  [*.md]                                                          │
│  trim_trailing_whitespace = false                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Extension Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | Extension manifest + npm dependencies |
| `tsconfig.json` | TypeScript compiler options (extension) |
| `tsconfig.webview.json` | TypeScript options (React WebView) |
| `.eslintrc.json` | ESLint rules |
| `.prettierrc` | Prettier formatting |
| `tailwind.config.js` | Tailwind CSS config |
| `postcss.config.js` | PostCSS plugins |
| `esbuild.js` | Build configuration |
| `vitest.config.ts` | Test configuration |

### 7.3 Server Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project config + Python dependencies |
| `ruff.toml` | Ruff linter configuration |
| `mypy.ini` | Type checking configuration |
| `pytest.ini` | Test configuration |

---

## 8. File Naming Conventions

### 8.1 TypeScript/JavaScript Files

```
┌─────────────────────────────────────────────────────────────────┐
│               TYPESCRIPT FILE NAMING CONVENTIONS                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PATTERN: kebab-case.type.ts                                    │
│                                                                  │
│  FILE TYPES:                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Services (business logic):                                      │
│  ├── chat.service.ts                                             │
│  ├── indexing.service.ts                                         │
│  └── ollama.service.ts                                           │
│                                                                  │
│  Entities (data structures):                                     │
│  ├── message.entity.ts                                           │
│  ├── plan.entity.ts                                              │
│  └── project.entity.ts                                           │
│                                                                  │
│  Interfaces (contracts):                                         │
│  ├── llm-provider.interface.ts                                   │
│  ├── rag-provider.interface.ts                                   │
│  └── file-system.interface.ts                                    │
│                                                                  │
│  Types (type definitions):                                       │
│  ├── mode.types.ts                                               │
│  ├── ollama.types.ts                                             │
│  └── messages.types.ts                                           │
│                                                                  │
│  Errors (custom errors):                                         │
│  ├── base.error.ts                                               │
│  ├── ollama.error.ts                                             │
│  └── indexing.error.ts                                           │
│                                                                  │
│  Adapters (implementations):                                     │
│  ├── file-system.adapter.ts                                      │
│  └── settings.adapter.ts                                         │
│                                                                  │
│  Prompts:                                                        │
│  ├── chat.system.ts                                              │
│  └── plan-generate.prompt.ts                                     │
│                                                                  │
│  Tests:                                                          │
│  ├── chat.service.test.ts                                        │
│  └── plan-parser.test.ts                                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  REACT COMPONENTS: PascalCase.tsx                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ├── ChatContainer.tsx                                           │
│  ├── MessageList.tsx                                             │
│  ├── MessageItem.tsx                                             │
│  ├── Button.tsx                                                  │
│  └── DiffView.tsx                                                │
│                                                                  │
│  HOOKS: useCamelCase.ts                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ├── useChat.ts                                                  │
│  ├── usePlan.ts                                                  │
│  └── useVSCode.ts                                                │
│                                                                  │
│  STORES: camelCase.store.ts                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ├── app.store.ts                                                │
│  ├── chat.store.ts                                               │
│  └── settings.store.ts                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Python Files

```
┌─────────────────────────────────────────────────────────────────┐
│                 PYTHON FILE NAMING CONVENTIONS                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PATTERN: snake_case.py                                          │
│                                                                  │
│  FILE TYPES:                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Services:                                                       │
│  ├── indexing_service.py                                         │
│  ├── rag_service.py                                              │
│  └── chat_service.py                                             │
│                                                                  │
│  Entities:                                                       │
│  ├── document.py                                                 │
│  ├── chunk.py                                                    │
│  └── embedding.py                                                │
│                                                                  │
│  Interfaces:                                                     │
│  ├── embedder.py                                                 │
│  ├── vector_store.py                                             │
│  └── parser.py                                                   │
│                                                                  │
│  Parsers:                                                        │
│  ├── base_parser.py                                              │
│  ├── typescript_parser.py                                        │
│  └── python_parser.py                                            │
│                                                                  │
│  Routes:                                                         │
│  ├── health.py                                                   │
│  ├── index.py                                                    │
│  └── query.py                                                    │
│                                                                  │
│  Tests:                                                          │
│  ├── test_indexing_service.py                                    │
│  ├── test_typescript_parser.py                                   │
│  └── test_chromadb.py                                            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  CLASS NAMING: PascalCase                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  class IndexingService:                                          │
│  class TypeScriptParser:                                         │
│  class OllamaClient:                                             │
│                                                                  │
│  FUNCTION/METHOD NAMING: snake_case                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  def index_document(self, doc: Document) -> None:               │
│  def get_embeddings(self, text: str) -> List[float]:            │
│  async def query_similar(self, query: str) -> List[Chunk]:      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.3 Tree-sitter Query Files

```
PATTERN: {language}.scm

Files:
├── typescript.scm    # TypeScript queries
├── javascript.scm    # JavaScript queries (often same as TS)
├── python.scm        # Python queries
└── dart.scm          # Dart queries
```

---

## 9. Import Rules

### 9.1 TypeScript Import Order

```typescript
/**
 * Import Order for TypeScript files
 * 
 * 1. Node.js built-in modules
 * 2. External dependencies (npm packages)
 * 3. VS Code API
 * 4. Internal - Core layer (entities, interfaces, errors)
 * 5. Internal - Features
 * 6. Internal - Infrastructure
 * 7. Internal - UI (if applicable)
 * 8. Relative imports (same feature)
 * 
 * Each group separated by a blank line
 */

// 1. Node.js built-in
import * as path from 'path';
import * as fs from 'fs';
import * as crypto from 'crypto';

// 2. External dependencies
import { create } from 'zustand';
import React from 'react';

// 3. VS Code API
import * as vscode from 'vscode';

// 4. Core layer
import { Message, Plan, Task } from '@core/entities';
import { ILLMProvider, IRAGProvider } from '@core/interfaces';
import { OllamaError } from '@core/errors';

// 5. Features
import { ChatService } from '@features/chat';
import { IndexingService } from '@features/indexing';

// 6. Infrastructure
import { OllamaService } from '@infrastructure/ollama';
import { ApiClient } from '@infrastructure/http';

// 7. UI
import { Button, Card } from '@ui/components/common';

// 8. Relative imports
import { MessageHandler } from './message-handler';
import { ContextBuilder } from './context-builder';
```

### 9.2 Python Import Order

```python
"""
Import Order for Python files

1. Standard library imports
2. Third-party imports
3. Local application imports
   - Core layer
   - Services
   - Infrastructure

Each group separated by a blank line
"""

# 1. Standard library
import asyncio
import hashlib
from pathlib import Path
from typing import List, Optional

# 2. Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb

# 3. Local - Core
from src.core.entities import Document, Chunk
from src.core.interfaces import IEmbedder, IVectorStore
from src.core.errors import IndexingError

# 4. Local - Services
from src.services.indexing_service import IndexingService

# 5. Local - Infrastructure
from src.infrastructure.ollama import OllamaClient
from src.infrastructure.chromadb import ChromaDBStore
```

### 9.3 Import Path Aliases (TypeScript)

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@core/*": ["core/*"],
      "@features/*": ["features/*"],
      "@infrastructure/*": ["infrastructure/*"],
      "@ui/*": ["ui/*"],
      "@utils/*": ["utils/*"],
      "@prompts/*": ["prompts/*"]
    }
  }
}
```

### 9.4 Layer Dependency Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                  LAYER DEPENDENCY RULES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ALLOWED DEPENDENCIES (→ means "can import from")               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  UI Layer:                                                       │
│  ├──→ Features Layer (use services)                             │
│  ├──→ Core Layer (use entities, types)                          │
│  └──→ Infrastructure Layer (ONLY via Features)                  │
│                                                                  │
│  Features Layer:                                                 │
│  ├──→ Core Layer (use entities, interfaces, types)             │
│  └──→ Other Features (sparingly, prefer events)                │
│                                                                  │
│  Infrastructure Layer:                                          │
│  └──→ Core Layer (implement interfaces)                        │
│                                                                  │
│  Core Layer:                                                     │
│  └──→ NOTHING (innermost layer)                                 │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FORBIDDEN DEPENDENCIES (✗)                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ✗ Core → Features                                              │
│  ✗ Core → Infrastructure                                        │
│  ✗ Core → UI                                                    │
│  ✗ Features → Infrastructure (use interfaces!)                 │
│  ✗ Features → UI                                                │
│  ✗ Infrastructure → Features                                    │
│  ✗ Infrastructure → UI                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. AI Agent Instructions

### 10.1 For AI Coding Assistants

```
┌─────────────────────────────────────────────────────────────────┐
│              AI AGENT WORKING INSTRUCTIONS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WHEN CREATING FILES:                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  1. Always check PROJECT_STRUCTURE.md for correct location      │
│  2. Use the exact naming conventions specified                  │
│  3. Include the appropriate file header/documentation           │
│  4. Export from the folder's index.ts file                      │
│  5. Create corresponding test file                              │
│                                                                  │
│  Example - Creating a new service:                              │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Task: "Create the BackupManager service"                       │
│                                                                  │
│  Steps:                                                          │
│  1. Create: extension/src/features/act/backup-manager.ts        │
│  2. Update: extension/src/features/act/index.ts (add export)    │
│  3. Create: extension/src/features/act/__tests__/               │
│             backup-manager.test.ts                               │
│  4. If implements interface, reference from @core/interfaces   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 File Header Templates

**TypeScript File Header:**

```typescript
/**
 * @file backup-manager.ts
 * @description Manages file backups for Act mode operations
 *
 * WHY: Before modifying any user file, we create a backup
 * so changes can be reverted if something goes wrong.
 *
 * RESPONSIBILITIES:
 * - Create timestamped backup folders
 * - Copy files before modification
 * - Restore files from backup
 * - Clean up old backups
 *
 * @example
 * const backup = new BackupManager(fileSystem);
 * const backupPath = await backup.createBackup('src/auth.ts');
 * // ... if something goes wrong ...
 * await backup.restore(backupPath, 'src/auth.ts');
 */
```

**Python File Header:**

```python
"""
Indexing Service

Orchestrates the indexing pipeline for code files.

WHY: This is the main entry point for indexing operations.
It coordinates file scanning, parsing, chunking, and
embedding generation.

RESPONSIBILITIES:
- Scan workspace for supported files
- Coordinate parsing with language-specific parsers
- Generate embeddings via Ollama
- Store in ChromaDB vector database
- Track file hashes for incremental sync

Example:
    service = IndexingService(embedder, vector_store)
    result = await service.index_workspace("/path/to/project")
"""
```

### 10.3 Quick Reference: Where to Put Things

```
┌─────────────────────────────────────────────────────────────────┐
│                 QUICK REFERENCE: WHERE TO PUT THINGS             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  "I need to create a..."                  → Put it in...        │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  EXTENSION (TypeScript):                                         │
│                                                                  │
│  New entity/data structure     → extension/src/core/entities/   │
│  New interface/contract        → extension/src/core/interfaces/ │
│  New error type                → extension/src/core/errors/     │
│  New type definition           → extension/src/core/types/      │
│  New feature service           → extension/src/features/{name}/ │
│  VS Code API wrapper           → extension/src/infrastructure/vscode/ │
│  HTTP/API client code          → extension/src/infrastructure/http/ │
│  WebSocket client code         → extension/src/infrastructure/websocket/ │
│  React component               → extension/src/ui/webview/components/ │
│  React hook                    → extension/src/ui/webview/hooks/ │
│  Zustand store                 → extension/src/ui/webview/store/ │
│  VS Code command               → extension/src/ui/commands/     │
│  LLM prompt template           → extension/src/prompts/         │
│  Utility function              → extension/src/utils/           │
│  WebView message types         → extension/src/ui/webview/types/ │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SERVER (Python):                                                │
│                                                                  │
│  New API endpoint              → server/src/api/routes/         │
│  Request/Response schema       → server/src/api/schemas/        │
│  WebSocket handler             → server/src/api/websocket/      │
│  New entity                    → server/src/core/entities/      │
│  New interface                 → server/src/core/interfaces/    │
│  New error type                → server/src/core/errors/        │
│  New service                   → server/src/services/           │
│  Language parser               → server/src/indexing/parsers/   │
│  Tree-sitter query             → server/src/infrastructure/treesitter/queries/ │
│  Ollama integration            → server/src/infrastructure/ollama/ │
│  ChromaDB integration          → server/src/infrastructure/chromadb/ │
│  Utility function              → server/src/utils/              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  SCRIPTS:                                                        │
│                                                                  │
│  Build/setup script            → scripts/                       │
│                                                                  │
│  DOCUMENTATION:                                                  │
│                                                                  │
│  Project documentation         → docs/ProjectDocuments/         │
│  Architecture decision         → docs/decisions/                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 10.4 When Modifying Existing Files

```
┌─────────────────────────────────────────────────────────────────┐
│              WHEN MODIFYING EXISTING FILES                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Read the entire file first to understand context            │
│  2. Check for existing patterns and match them                  │
│  3. Update related test files                                    │
│  4. Update index.ts exports if adding new exports               │
│  5. Maintain existing documentation style                       │
│  6. Run linter after changes                                     │
│                                                                  │
│  CHECKLIST BEFORE COMMITTING:                                    │
│  □ File is in correct location per structure.md                │
│  □ Naming follows conventions                                    │
│  □ Exports added to index.ts                                    │
│  □ Tests updated or created                                      │
│  □ No circular dependencies introduced                          │
│  □ Layer boundaries respected                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Document Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | TarekRefaei | | |

---

*Document Version: 1.1.0*
*Created: Planning Phase*
*Last Updated: [Current Date]*
```

---

This is the complete, updated `structure.md` document with all the modifications including:

1. ✅ Clarified storage locations (Section 6)
2. ✅ Added scripts folder documentation (Section 5)
3. ✅ Added WebView message types file location
4. ✅ Added Tree-sitter query files location
5. ✅ Added backup-manager.ts to Act feature
6. ✅ Added server status component to onboarding
7. ✅ Added chunk.entity.ts to entities
8. ✅ Added server.error.ts to errors
9. ✅ Updated AI agent instructions
10. ✅ Added layer dependency rules visualization