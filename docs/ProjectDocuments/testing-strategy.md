### Document 2: TESTING_STRATEGY.md

**Location:** `docs/ProjectDocuments/testing-strategy.md`

**Purpose:** Define testing approach for both extension and server

**Content Required:**

# LocalPilot - Testing Strategy

## Overview
- Extension: Vitest + @vscode/test-electron
- Server: pytest + pytest-asyncio
- Coverage Target: 70% minimum

## Test Categories

### Unit Tests
| Component | Framework | Mock Strategy |
|-----------|-----------|---------------|
| Core entities | Vitest | None needed |
| Services | Vitest | Mock interfaces |
| Parsers | pytest | Sample code fixtures |
| Chunker | pytest | Pre-parsed AST fixtures |

### Integration Tests
| Test | Components | Setup |
|------|------------|-------|
| Ollama connection | OllamaService ↔ Ollama | Requires running Ollama |
| Server API | Extension ↔ Python Server | Both running |
| Full indexing | All indexing components | Sample project |

### E2E Tests (Post-MVP)
- Full workflow: Index → Chat → Plan → Act
- Requires test workspace

## Test Fixtures

### Sample TypeScript Project
```
test/fixtures/sample-ts-project/
├── src/
│   ├── index.ts          # Entry point
│   ├── auth/
│   │   ├── auth.service.ts
│   │   └── auth.types.ts
│   └── utils/
│       └── helpers.ts
├── package.json
└── tsconfig.json
```

### Sample Python Project
```
test/fixtures/sample-py-project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── services/
│       └── auth_service.py
└── requirements.txt
```

### Mock Ollama Responses
[Include sample responses for testing without Ollama]

## Running Tests

### Extension
```bash
cd extension
pnpm test           # Run all tests
pnpm test:watch     # Watch mode
pnpm test:coverage  # With coverage
```

### Server
```bash
cd server
pytest                    # Run all tests
pytest --cov=src         # With coverage
pytest -k "test_parser"  # Specific tests
```