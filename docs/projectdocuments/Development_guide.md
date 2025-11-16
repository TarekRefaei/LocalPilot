# 📄 DOCUMENT #8: DEVELOPMENT_GUIDE.md
# LocalPilot - Development Guide

**Version:** 1.0  
**Date:** January 2025  
**Status:** Foundation  
**Author:** LocalPilot Development Team

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Bootstrapping a New Repo](#bootstrapping-a-new-repo)
3. [Project Setup](#project-setup)
4. [Development Environment](#development-environment)
5. [TDD Workflow](#tdd-workflow)
6. [Git Workflow](#git-workflow)
7. [Code Style & Conventions](#code-style--conventions)
8. [AI-Assisted Development](#ai-assisted-development)
9. [Debugging & Troubleshooting](#debugging--troubleshooting)
10. [Performance Profiling](#performance-profiling)
11. [Release Process](#release-process)

---

## 🚀 Getting Started

### Prerequisites

```yaml
Required Software:
  Node.js: >= 18.0.0
  Python: >= 3.10
  Git: >= 2.30
  VS Code: >= 1.88
  Ollama: >= 0.1.20

Required Models (Ollama):
  - qwen2.5-coder:7b-instruct-q4_K_M
  - qwen2.5-coder:14b-instruct-q4_K_M
  - bge-m3

Hardware Requirements:
  RAM: >= 16GB
  GPU: NVIDIA GPU with 8GB+ VRAM (recommended)
  Disk: >= 10GB free space
  CPU: 4+ cores recommended
```

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/localpilot.git
cd localpilot

# 2. Run setup script
./scripts/setup.sh

# 3. Start development
./scripts/dev.sh
```

## 🏗️ Bootstrapping a New Repo

Follow these steps if you are starting LocalPilot from scratch in this folder.

### 1) Initialize repository structure

```powershell
# From the repo root
git init -b main
mkdir extension, backend, docs, scripts, .vscode, .github
mkdir docs\agents\_templates
echo "# LocalPilot" > README.md
echo "MIT" > LICENSE
ni .gitignore -ItemType File
ni .editorconfig -ItemType File
ni .gitattributes -ItemType File
```

Recommended .gitignore baseline:

```gitignore
node_modules/
dist/
.venv/
venv/
.pytest_cache/
__pycache__/
.DS_Store
```

### 2) Scaffold VS Code extension (TypeScript)

- Set engines.vscode to ">=1.88.0" to use the Chat API and native Views.
- Enable strict TypeScript, ESLint, Prettier, and Jest.

```powershell
cd extension
npm init -y
npm i -D typescript eslint prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm i -D jest ts-jest @types/jest
npm i vscode @types/vscode
npx tsc --init
cd ..
```

### 3) Scaffold Python backend (FastAPI)

```powershell
cd backend
py -3.10 -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install fastapi uvicorn pydantic chromadb
pip install pytest ruff mypy
cd ..
```

### 4) VS Code workspace configs

- Create `.vscode/settings.json`, `launch.json`, and `tasks.json` as in this guide.
- Verify the Extension + Backend compound launch works on Windows.

### 5) Seed issues and milestones (optional)

Requires GitHub CLI installed and authenticated (`gh auth login`).

```powershell
# Create a GitHub repo from the current folder (adjust visibility and name)
gh repo create <owner/name> --source . --public --push

# Seed labels, milestones (W1–W10), week epics, and agent issues
powershell -File .\scripts\gh-seed-issues.ps1 -Repo <owner/name>
```

> Note: Use docs/agents/_templates for agent contracts and handoffs.

---

## 🛠️ Project Setup

### Detailed Setup Instructions

#### Step 1: Install Dependencies

```bash
# Install Node.js dependencies (Extension)
cd extension
npm install

# Return to root
cd ..

# Install Python dependencies (Backend)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Return to root
cd ..
```

#### Step 2: Install Tree-sitter Grammars

```bash
# Backend tree-sitter setup
cd backend

# Create build directory
mkdir -p build

# Clone and build language grammars
git clone https://github.com/tree-sitter/tree-sitter-typescript
git clone https://github.com/tree-sitter/tree-sitter-javascript
git clone https://github.com/tree-sitter/tree-sitter-python

# Build shared library (requires C compiler)
# On macOS/Linux:
gcc -shared -o build/languages.so \
  -I tree-sitter-typescript/typescript/src \
  -I tree-sitter-javascript/src \
  -I tree-sitter-python/src \
  tree-sitter-typescript/typescript/src/parser.c \
  tree-sitter-typescript/typescript/src/scanner.c \
  tree-sitter-javascript/src/parser.c \
  tree-sitter-javascript/src/scanner.c \
  tree-sitter-python/src/parser.c \
  tree-sitter-python/src/scanner.c

# On Windows (with MinGW):
# gcc -shared -o build/languages.dll ...

cd ..
```

#### Step 3: Configure Ollama

```bash
# Verify Ollama is running
ollama list

# Pull required models (if not already downloaded)
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
ollama pull qwen2.5-coder:14b-instruct-q4_K_M
ollama pull bge-m3

# Test models
ollama run qwen2.5-coder:7b-instruct-q4_K_M "Hello, world!"
```

#### Step 4: Environment Configuration

```bash
# Backend environment
cd backend
cp .env.example .env

# Edit .env with your settings
nano .env
```

`.env` file:
```bash
# Ollama configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_TIMEOUT_SECONDS=120

# Vector DB
VECTOR_DB_PATH=.localpilot/vectordb

# Logging
LOG_LEVEL=INFO
DEBUG=false

# Model configuration
EMBEDDING_MODEL=bge-m3
CHAT_MODEL=qwen2.5-coder:7b-instruct-q4_K_M
PLANNING_MODEL=qwen2.5-coder:14b-instruct-q4_K_M
CODING_MODEL=qwen2.5-coder:14b-instruct-q4_K_M

# Performance
MAX_CONCURRENT_EMBEDDINGS=5
BATCH_SIZE_INDEXING=32
```

#### Step 5: Initialize Databases

```bash
# Backend database initialization
cd backend
python -m src.db.init_db

# This creates:
# - SQLite database schema
# - ChromaDB collections
# - Cache directories
```

#### Step 6: Verify Setup

```bash
# Run verification script
./scripts/verify-setup.sh

# Expected output:
# ✓ Node.js version: 18.x.x
# ✓ Python version: 3.10.x
# ✓ Git version: 2.x.x
# ✓ VS Code installed
# ✓ Ollama running
# ✓ Models available: 3/3
# ✓ Extension dependencies: OK
# ✓ Backend dependencies: OK
# ✓ Tree-sitter grammars: OK
# ✓ Database initialized: OK
# 
# Setup complete! Ready to develop.
```

---

## 💻 Development Environment

### VS Code Setup

#### Required Extensions

```json
// .vscode/extensions.json
{
  "recommendations": [
    // TypeScript/JavaScript
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    
    // Python
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    
    // Testing
    "hbenl.vscode-test-explorer",
    "ms-vscode.test-adapter-converter",
    
    // Git
    "eamodio.gitlens",
    
    // Utilities
    "streetsidesoftware.code-spell-checker",
    "editorconfig.editorconfig"
  ]
}
```

#### VS Code Settings

```json
// .vscode/settings.json
{
  // TypeScript
  "typescript.tsdk": "extension/node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  
  // ESLint
  "eslint.validate": ["javascript", "typescript", "typescriptreact"],
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  
  // Prettier
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  
  // Python
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "backend/tests"
  ],
  
  // Files
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/*.pyc": true,
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true
  },
  
  // Editor
  "editor.rulers": [100],
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  
  // Python specific
  "[python]": {
    "editor.tabSize": 4,
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

#### Launch Configurations

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "runtimeExecutable": "${execPath}",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}/extension"
      ],
      "outFiles": [
        "${workspaceFolder}/extension/out/**/*.js"
      ],
      "preLaunchTask": "npm: watch"
    },
    {
      "name": "Extension Tests",
      "type": "extensionHost",
      "request": "launch",
      "runtimeExecutable": "${execPath}",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}/extension",
        "--extensionTestsPath=${workspaceFolder}/extension/out/test/suite/index"
      ],
      "outFiles": [
        "${workspaceFolder}/extension/out/test/**/*.js"
      ],
      "preLaunchTask": "npm: test-compile"
    },
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.main:app",
        "--reload",
        "--port",
        "8765"
      ],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/backend"
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "-v",
        "-s",
        "${file}"
      ],
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/backend"
    }
  ],
  "compounds": [
    {
      "name": "Extension + Backend",
      "configurations": ["Run Extension", "Python: FastAPI"],
      "presentation": {
        "hidden": false,
        "group": "development",
        "order": 1
      }
    }
  ]
}
```

#### Tasks Configuration

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "npm",
      "script": "watch",
      "path": "extension/",
      "problemMatcher": "$tsc-watch",
      "isBackground": true,
      "presentation": {
        "reveal": "never"
      },
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "type": "npm",
      "script": "test-compile",
      "path": "extension/",
      "problemMatcher": "$tsc",
      "presentation": {
        "reveal": "never"
      }
    },
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "python -m uvicorn src.main:app --reload --port 8765",
      "options": {
        "cwd": "${workspaceFolder}/backend"
      },
      "problemMatcher": [],
      "isBackground": true
    },
    {
      "label": "Run All Tests",
      "dependsOn": [
        "Test Extension",
        "Test Backend"
      ],
      "problemMatcher": []
    },
    {
      "label": "Test Extension",
      "type": "npm",
      "script": "test",
      "path": "extension/",
      "problemMatcher": []
    },
    {
      "label": "Test Backend",
      "type": "shell",
      "command": "pytest -v",
      "options": {
        "cwd": "${workspaceFolder}/backend"
      },
      "problemMatcher": []
    }
  ]
}
```

### Development Scripts

#### Main Development Script

```bash
#!/bin/bash
# scripts/dev.sh

set -e

echo "🚀 Starting LocalPilot Development Environment"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Ollama is not running. Please start Ollama first."
    exit 1
fi

# Start backend in background
echo "📦 Starting backend..."
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --reload --port 8765 &
BACKEND_PID=$!
cd ..

# Wait for backend to be ready
echo "⏳ Waiting for backend..."
for i in {1..30}; do
    if curl -s http://localhost:8765/health > /dev/null; then
        echo "✓ Backend ready"
        break
    fi
    sleep 1
done

# Start extension watch
echo "👁️  Starting extension watch..."
cd extension
npm run watch &
WATCH_PID=$!
cd ..

echo ""
echo "✅ Development environment started!"
echo ""
echo "Next steps:"
echo "  1. Press F5 in VS Code to launch extension"
echo "  2. Open a workspace in the Extension Development Host"
echo "  3. Activate LocalPilot"
echo ""
echo "To stop: Ctrl+C or run ./scripts/stop-dev.sh"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $WATCH_PID 2>/dev/null" EXIT

wait
```

#### Setup Script

```bash
#!/bin/bash
# scripts/setup.sh

set -e

echo "🔧 Setting up LocalPilot Development Environment"

# Check prerequisites
echo "Checking prerequisites..."

# Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js >= 18"
    exit 1
fi
echo "✓ Node.js $(node --version)"

# Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python >= 3.10"
    exit 1
fi
echo "✓ Python $(python3 --version)"

# Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git"
    exit 1
fi
echo "✓ Git $(git --version)"

# Ollama
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama"
    exit 1
fi
echo "✓ Ollama installed"

echo ""
echo "📦 Installing dependencies..."

# Extension dependencies
echo "Installing extension dependencies..."
cd extension
npm install
cd ..

# Backend dependencies
echo "Installing backend dependencies..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
cd ..

echo ""
echo "🌲 Setting up Tree-sitter..."
cd backend
mkdir -p build

# Check if grammars already exist
if [ ! -d "tree-sitter-typescript" ]; then
    git clone https://github.com/tree-sitter/tree-sitter-typescript
fi
if [ ! -d "tree-sitter-javascript" ]; then
    git clone https://github.com/tree-sitter/tree-sitter-javascript
fi
if [ ! -d "tree-sitter-python" ]; then
    git clone https://github.com/tree-sitter/tree-sitter-python
fi

# Build (if C compiler available)
if command -v gcc &> /dev/null; then
    echo "Building Tree-sitter grammars..."
    gcc -shared -o build/languages.so \
      -I tree-sitter-typescript/typescript/src \
      -I tree-sitter-javascript/src \
      -I tree-sitter-python/src \
      tree-sitter-typescript/typescript/src/parser.c \
      tree-sitter-typescript/typescript/src/scanner.c \
      tree-sitter-javascript/src/parser.c \
      tree-sitter-javascript/src/scanner.c \
      tree-sitter-python/src/parser.c \
      tree-sitter-python/src/scanner.c
    echo "✓ Tree-sitter grammars built"
else
    echo "⚠️  GCC not found. Tree-sitter grammars not built."
    echo "   You'll need to build them manually or install GCC."
fi

cd ..

echo ""
echo "🗄️  Initializing databases..."
cd backend
source venv/bin/activate
python -m src.db.init_db
cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Ensure Ollama is running: ollama serve"
echo "  2. Pull required models (if not already done):"
echo "     ollama pull qwen2.5-coder:7b-instruct-q4_K_M"
echo "     ollama pull qwen2.5-coder:14b-instruct-q4_K_M"
echo "     ollama pull bge-m3"
echo "  3. Start development: ./scripts/dev.sh"
echo "  4. Open VS Code and press F5 to launch extension"
```

---

## 🧪 TDD Workflow

### Test-Driven Development Cycle

```
TDD Cycle (Red-Green-Refactor):

1. RED: Write a failing test
   ├── Define the expected behavior
   ├── Write a test that fails
   └── Run test to confirm it fails

2. GREEN: Write minimal code to pass
   ├── Implement just enough to pass the test
   ├── Don't worry about perfection
   └── Run test to confirm it passes

3. REFACTOR: Improve the code
   ├── Clean up implementation
   ├── Remove duplication
   ├── Improve naming
   └── Ensure tests still pass

4. REPEAT: Move to next feature
```

### TypeScript/Extension TDD

#### Example: Testing a Service

```typescript
// extension/test/unit/services/WebSocketService.test.ts

import * as assert from 'assert';
import { WebSocketService } from '../../../src/services/WebSocketService';
import { EventEmitter } from 'events';

describe('WebSocketService', () => {
  let service: WebSocketService;
  
  beforeEach(() => {
    service = new WebSocketService();
  });
  
  afterEach(() => {
    service.disconnect();
  });
  
  describe('connect', () => {
    it('should establish connection successfully', async () => {
      // RED: Test fails (method not implemented yet)
      const result = await service.connect('ws://localhost:8765');
      
      assert.strictEqual(result, true);
      assert.strictEqual(service.isConnected(), true);
    });
    
    it('should emit connected event', async () => {
      // Arrange
      let eventEmitted = false;
      service.on('connected', () => {
        eventEmitted = true;
      });
      
      // Act
      await service.connect('ws://localhost:8765');
      
      // Assert
      assert.strictEqual(eventEmitted, true);
    });
    
    it('should handle connection failure gracefully', async () => {
      // Test error handling
      await assert.rejects(
        async () => {
          await service.connect('ws://invalid-url');
        },
        /Connection failed/
      );
    });
  });
  
  describe('send', () => {
    it('should send message when connected', async () => {
      // Arrange
      await service.connect('ws://localhost:8765');
      
      // Act
      const result = service.send('test.event', { data: 'test' });
      
      // Assert
      assert.strictEqual(result, true);
    });
    
    it('should throw error when not connected', () => {
      // Not connected yet
      assert.throws(
        () => {
          service.send('test.event', {});
        },
        /Not connected/
      );
    });
  });
});
```

#### Running TypeScript Tests

```bash
# Run all tests
cd extension
npm test

# Run specific test file
npm test -- --grep "WebSocketService"

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### Python/Backend TDD

#### Example: Testing Indexing Service

```python
# backend/tests/unit/test_indexing_service.py

import pytest
from pathlib import Path
from src.services.indexing.indexing_service import IndexingService
from src.services.indexing.discovery import DiscoveryExecutor

class TestDiscoveryExecutor:
    """Test suite for DiscoveryExecutor"""
    
    @pytest.fixture
    def executor(self):
        """Create executor instance"""
        return DiscoveryExecutor()
    
    @pytest.fixture
    def sample_workspace(self, tmp_path):
        """Create a sample workspace for testing"""
        # Create directory structure
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "index.ts").write_text("console.log('hello');")
        (tmp_path / "src" / "utils.ts").write_text("export function test() {}")
        (tmp_path / "README.md").write_text("# Test Project")
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "package").write_text("ignored")
        
        return tmp_path
    
    @pytest.mark.asyncio
    async def test_scan_workspace(self, executor, sample_workspace):
        """Test workspace scanning"""
        # RED: Write test first
        result = await executor.execute(str(sample_workspace))
        
        # Assert
        assert result.total_files == 3  # src/index.ts, src/utils.ts, README.md
        assert result.files_by_type['typescript'] == 2
        assert result.files_by_type['markdown'] == 1
    
    @pytest.mark.asyncio
    async def test_exclude_patterns(self, executor, sample_workspace):
        """Test that exclude patterns work"""
        # node_modules should be excluded
        result = await executor.execute(str(sample_workspace))
        
        # No files from node_modules
        assert all('node_modules' not in str(f) for f in result.files)
    
    @pytest.mark.asyncio
    async def test_detect_project_type(self, executor, tmp_path):
        """Test project type detection"""
        # Create package.json
        (tmp_path / "package.json").write_text('{"dependencies": {"react": "^18.0.0"}}')
        
        result = await executor.execute(str(tmp_path))
        
        assert result.project_type == 'react'
    
    @pytest.mark.asyncio
    async def test_estimate_duration(self, executor, sample_workspace):
        """Test indexing duration estimation"""
        result = await executor.execute(str(sample_workspace))
        
        # Should estimate some duration
        assert result.estimated_duration_seconds > 0
        # For 3 files, should be quick
        assert result.estimated_duration_seconds < 10


class TestIndexingService:
    """Test suite for IndexingService"""
    
    @pytest.fixture
    async def service(self, vector_store_mock, embedding_service_mock):
        """Create service with mocked dependencies"""
        return IndexingService(
            vector_store=vector_store_mock,
            embedding_service=embedding_service_mock
        )
    
    @pytest.mark.asyncio
    async def test_index_workspace_success(self, service, sample_workspace):
        """Test successful workspace indexing"""
        # RED: Write test
        result = await service.index_workspace(str(sample_workspace))
        
        # Assert
        assert result.status == 'completed'
        assert result.statistics.indexed_files > 0
        assert result.project_summary is not None
    
    @pytest.mark.asyncio
    async def test_index_workspace_emits_progress(self, service, sample_workspace):
        """Test that progress events are emitted"""
        progress_events = []
        
        async for progress in service.index_workspace(str(sample_workspace)):
            progress_events.append(progress)
        
        # Should have events for all 5 phases
        phases = [e.phase for e in progress_events]
        assert 'discovery' in phases
        assert 'documentation' in phases
        assert 'structure' in phases
        assert 'chunking' in phases
        assert 'summarization' in phases
    
    @pytest.mark.asyncio
    async def test_handles_parsing_errors_gracefully(self, service, tmp_path):
        """Test error handling for unparseable files"""
        # Create file with syntax error
        (tmp_path / "broken.ts").write_text("const x = {{{")
        
        result = await service.index_workspace(str(tmp_path))
        
        # Should complete with some failures
        assert result.status == 'completed'
        assert result.statistics.failed_files > 0
```

#### Running Python Tests

```bash
# Activate virtual environment
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_indexing_service.py

# Run specific test
pytest tests/unit/test_indexing_service.py::TestDiscoveryExecutor::test_scan_workspace

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v -s

# Watch mode (requires pytest-watch)
ptw
```

### Test Coverage Goals

```yaml
Coverage Targets:
  Overall: >= 70%
  Critical Components: >= 85%
    - Indexing Service
    - RAG Service
    - File Operations (Act Mode)
    - WebSocket Communication
  
  UI Components: >= 60%
    - Focus on logic, not rendering details
  
  Utilities: >= 80%
    - Pure functions should be well-tested
```

---

## 🌿 Git Workflow

### Branch Strategy (Git Flow)

```
Branch Structure:

main (protected)
├── Production releases only
├── Tagged with version numbers (v0.1.0, v0.2.0, etc.)
└── Never commit directly

develop
├── Integration branch
├── Merge point for all features
└── Should always be stable

feature/* (short-lived)
├── feature/foundation-setup
├── feature/indexing-system
├── feature/chat-mode
├── feature/plan-mode
├── feature/act-mode
└── feature/ui-polish

bugfix/* (short-lived)
├── bugfix/fix-indexing-timeout
└── bugfix/websocket-reconnect

hotfix/* (emergency fixes)
├── Branch from main
└── Merge to main and develop
```

### Commit Conventions

```
Conventional Commits Format:

<type>(<scope>): <subject>

<body>

<footer>

Types:
  feat:     New feature
  fix:      Bug fix
  docs:     Documentation only
  style:    Code style (formatting, no logic change)
  refactor: Code refactoring
  test:     Adding or updating tests
  chore:    Build process, dependencies, etc.
  perf:     Performance improvement

Examples:

feat(indexing): implement tree-sitter code parser

- Add Tree-sitter integration for TypeScript
- Extract functions and classes from AST
- Store symbols in metadata database

Closes #12

---

fix(chat): resolve streaming response timeout

The WebSocket was timing out for long responses.
Increased timeout from 30s to 120s and added
heartbeat mechanism.

Fixes #45

---

test(rag): add unit tests for context retrieval

- Test embedding generation
- Test vector search
- Test relevance scoring
- Achieve 85% coverage for RAG service

---

refactor(ui): extract Message component

Split large ChatView component into smaller,
reusable components for better maintainability.

---

chore(deps): upgrade react to 18.2.0
```

### Git Workflow Commands

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/chat-mode

# Work on feature (TDD cycle)
# 1. Write test
git add tests/unit/test_chat_service.py
git commit -m "test(chat): add test for message sending"

# 2. Implement feature
git add src/services/chat/
git commit -m "feat(chat): implement message sending service"

# 3. Refactor
git add src/services/chat/
git commit -m "refactor(chat): extract message validation logic"

# Push feature branch
git push origin feature/chat-mode

# Create pull request (via GitHub/GitLab)
# After review and approval, merge to develop

# Update develop
git checkout develop
git pull origin develop

# Delete feature branch
git branch -d feature/chat-mode
git push origin --delete feature/chat-mode
```

### Pre-commit Hooks

```bash
# .husky/pre-commit

#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "🔍 Running pre-commit checks..."

# 1. Run linters
echo "Running ESLint..."
cd extension && npm run lint
if [ $? -ne 0 ]; then
    echo "❌ ESLint failed"
    exit 1
fi

echo "Running Flake8..."
cd backend && source venv/bin/activate && flake8 src/
if [ $? -ne 0 ]; then
    echo "❌ Flake8 failed"
    exit 1
fi

# 2. Run type checking
echo "Running TypeScript type check..."
cd extension && npm run type-check
if [ $? -ne 0 ]; then
    echo "❌ Type check failed"
    exit 1
fi

echo "Running mypy..."
cd backend && mypy src/
if [ $? -ne 0 ]; then
    echo "❌ MyPy failed"
    exit 1
fi

# 3. Run tests
echo "Running tests..."
cd extension && npm test
if [ $? -ne 0 ]; then
    echo "❌ Extension tests failed"
    exit 1
fi

cd backend && pytest tests/unit/
if [ $? -ne 0 ]; then
    echo "❌ Backend tests failed"
    exit 1
fi

echo "✅ All checks passed!"
```

---

## 📝 Code Style & Conventions

### TypeScript/JavaScript Style

```typescript
// extension/src/example.ts

/**
 * Use JSDoc for all public APIs
 * 
 * @param param1 - Description of param1
 * @param param2 - Description of param2
 * @returns Description of return value
 */
export function exampleFunction(param1: string, param2: number): boolean {
  // Use descriptive variable names
  const isValid = validateInput(param1);
  
  // Early returns for error cases
  if (!isValid) {
    return false;
  }
  
  // Prefer const over let
  const result = processData(param2);
  
  // Use template literals
  console.log(`Processing ${param1} with value ${param2}`);
  
  return result > 0;
}

// Interfaces in PascalCase
export interface UserData {
  id: string;
  name: string;
  email: string;
}

// Enums in PascalCase
export enum Status {
  PENDING = 'pending',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

// Constants in UPPER_SNAKE_CASE
export const MAX_RETRY_ATTEMPTS = 3;
export const DEFAULT_TIMEOUT_MS = 5000;

// Private functions prefixed with underscore
function _privateHelper(data: string): string {
  return data.trim();
}

// Async functions clearly named
async function fetchUserData(userId: string): Promise<UserData> {
  // Use try-catch for async operations
  try {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch user ${userId}:`, error);
    throw new Error('User fetch failed');
  }
}
```

#### ESLint Configuration

```json
// extension/.eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json",
    "tsconfigRootDir": "."
  },
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/naming-convention": [
      "warn",
      {
        "selector": "interface",
        "format": ["PascalCase"]
      },
      {
        "selector": "typeAlias",
        "format": ["PascalCase"]
      },
      {
        "selector": "enum",
        "format": ["PascalCase"]
      },
      {
        "selector": "variable",
        "modifiers": ["const"],
        "format": ["camelCase", "UPPER_CASE", "PascalCase"]
      }
    ],
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/no-explicit-any": "error",
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "prefer-const": "error",
    "no-var": "error"
  }
}
```

#### Prettier Configuration

```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

### Python Style

```python
# backend/src/example.py

"""
Module docstring explaining what this module does.

This module provides example functions demonstrating
LocalPilot's Python coding standards.
"""

from typing import List, Optional, Dict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Constants in UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT_SECONDS = 30


@dataclass
class UserData:
    """Data class for user information."""
    id: str
    name: str
    email: str
    age: Optional[int] = None


def process_user_data(
    user_id: str,
    options: Optional[Dict] = None
) -> UserData:
    """
    Process user data with optional configuration.
    
    Args:
        user_id: Unique identifier for the user
        options: Optional configuration dictionary
    
    Returns:
        UserData object with processed information
    
    Raises:
        ValueError: If user_id is empty
        RuntimeError: If processing fails
    
    Example:
        >>> data = process_user_data("user-123")
        >>> print(data.name)
    """
    # Early validation
    if not user_id:
        raise ValueError("user_id cannot be empty")
    
    # Use options.get() for optional parameters
    timeout = options.get('timeout', DEFAULT_TIMEOUT_SECONDS) if options else DEFAULT_TIMEOUT_SECONDS
    
    # Type hints for local variables (when helpful)
    result: UserData
    
    try:
        result = _fetch_user(user_id, timeout)
    except Exception as e:
        logger.error(f"Failed to process user {user_id}: {e}")
        raise RuntimeError(f"User processing failed") from e
    
    return result


def _fetch_user(user_id: str, timeout: int) -> UserData:
    """
    Private helper function (prefixed with underscore).
    
    Args:
        user_id: User identifier
        timeout: Request timeout in seconds
    
    Returns:
        UserData object
    """
    # Implementation
    pass


async def async_process_data(data: List[str]) -> List[str]:
    """
    Async functions clearly marked with 'async' prefix in name when helpful.
    
    Args:
        data: List of data to process
    
    Returns:
        Processed data list
    """
    processed = []
    
    for item in data:
        result = await _async_helper(item)
        processed.append(result)
    
    return processed


async def _async_helper(item: str) -> str:
    """Private async helper."""
    # Async implementation
    pass


# Class naming in PascalCase
class DataProcessor:
    """
    Class for processing data.
    
    Attributes:
        max_retries: Maximum number of retry attempts
        timeout: Timeout in seconds
    """
    
    def __init__(self, max_retries: int = MAX_RETRIES):
        """
        Initialize processor.
        
        Args:
            max_retries: Maximum retry attempts
        """
        self.max_retries = max_retries
        self._cache: Dict[str, str] = {}  # Private attribute
    
    def process(self, data: str) -> str:
        """
        Process data.
        
        Args:
            data: Input data
        
        Returns:
            Processed data
        """
        # Method implementation
        return data.upper()
    
    def _private_method(self) -> None:
        """Private method (prefixed with underscore)."""
        pass
```

#### Python Tools Configuration

```toml
# backend/pyproject.toml

[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_calls = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --strict-markers --cov=src --cov-report=term-missing"
testpaths = ["tests"]
pythonpath = ["."]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "**/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

### Naming Conventions Summary

```yaml
TypeScript/JavaScript:
  Variables: camelCase (userName, isValid)
  Functions: camelCase (fetchData, processUser)
  Classes: PascalCase (UserService, DataProcessor)
  Interfaces: PascalCase (UserData, ChatMessage)
  Types: PascalCase (UserId, MessageType)
  Enums: PascalCase (Status, ErrorCode)
  Constants: UPPER_SNAKE_CASE (MAX_RETRIES, API_URL)
  Private: _prefixed (_privateHelper, _internalState)

Python:
  Variables: snake_case (user_name, is_valid)
  Functions: snake_case (fetch_data, process_user)
  Classes: PascalCase (UserService, DataProcessor)
  Constants: UPPER_SNAKE_CASE (MAX_RETRIES, API_URL)
  Private: _prefixed (_private_method, _internal_cache)
  
Files:
  TypeScript: PascalCase for components (Button.tsx, ChatView.tsx)
  TypeScript: camelCase for utilities (validators.ts, helpers.ts)
  Python: snake_case (indexing_service.py, rag_service.py)
```

---

## 🤖 AI-Assisted Development

### Using AI Coding Assistants Effectively

#### Prompt Engineering for Code Generation

```markdown
Good Prompt Structure:

1. Context
   - What you're building
   - Technology stack
   - Architecture constraints

2. Specific Task
   - Clear, focused requirement
   - Expected inputs/outputs
   - Edge cases to handle

3. Constraints
   - Code style to follow
   - Performance requirements
   - Testing requirements

Example Good Prompt:

"""
I'm building a LocalPilot VS Code extension (TypeScript + Python backend).

Task: Implement a WebSocket reconnection mechanism for the extension's 
backend communication layer.

Requirements:
- Exponential backoff (2^n seconds, max 30s)
- Max 5 reconnection attempts
- Emit events for connection state changes
- Handle graceful shutdown

Constraints:
- Follow our TypeScript style guide (ESLint config)
- Write comprehensive unit tests (Jest)
- Use existing WebSocket library (ws)
- Include JSDoc comments

Technology:
- TypeScript 5.0
- Node.js 18
- ws library

Please implement:
1. ReconnectionManager class
2. Unit tests
3. Integration with existing WebSocketService
"""
```

#### Code Review with AI

```markdown
Code Review Prompt Template:

"""
Review this code for:
1. Potential bugs
2. Performance issues
3. Security vulnerabilities
4. Code style violations
5. Test coverage gaps
6. Documentation completeness

Code:
[paste code here]

Our standards:
- TypeScript with strict mode
- TDD methodology
- Maximum function complexity: 10
- Minimum test coverage: 70%
- All public APIs must have JSDoc
"""
```

#### Debugging with AI

```markdown
Debugging Prompt:

"""
I'm encountering an issue in LocalPilot's indexing system.

Error:
[paste error message and stack trace]

Context:
- Function: IndexingService.index_workspace()
- Input: 500-file TypeScript project
- Expected: Complete indexing in <5 minutes
- Actual: Hangs at 80% (chunking phase)

Environment:
- Python 3.10
- ChromaDB 0.4.15
- bge-m3 embeddings
- RTX 4060 8GB VRAM

Code:
[paste relevant code]

Please help:
1. Identify root cause
2. Suggest fix
3. Recommend preventive measures
"""
```

### AI Pair Programming Workflow

```yaml
Session Structure:

1. Planning Phase (with AI)
   - Discuss feature requirements
   - Design API/interfaces
   - Identify edge cases
   - Plan test cases

2. TDD Cycle (with AI assistance)
   - AI helps write test cases
   - You write failing tests
   - AI suggests implementation
   - You review and refine
   - You refactor together

3. Review Phase (with AI)
   - AI reviews code
   - You address feedback
   - AI suggests improvements
   - Iterate until satisfied

4. Documentation (with AI)
   - AI generates initial docs
   - You review and enhance
   - AI suggests examples
   - Finalize together
```

### Effective Use of GitHub Copilot/Claude/etc.

```typescript
// Example: Using Copilot for boilerplate

// 1. Write comment describing what you need
// Create a service for handling chat messages with the following methods:
// - sendMessage(message: string): Promise<void>
// - streamMessage(message: string): AsyncGenerator<string>
// - getHistory(limit: number): Promise<ChatMessage[]>

// 2. Copilot suggests implementation (review carefully!)

// 3. Add tests first (TDD)
describe('ChatService', () => {
  it('should send message successfully', async () => {
    // Copilot can help generate test structure
  });
});

// 4. Refine generated code
// - Add error handling
// - Improve naming
// - Add type safety
// - Add documentation
```

---

## 🐛 Debugging & Troubleshooting

### Debug Configuration

#### Extension Debugging

```json
// Debug extension with detailed logging
{
  "name": "Extension Debug (Verbose)",
  "type": "extensionHost",
  "request": "launch",
  "runtimeExecutable": "${execPath}",
  "args": [
    "--extensionDevelopmentPath=${workspaceFolder}/extension",
    "--log=debug"
  ],
  "env": {
    "VSCODE_DEBUG_MODE": "true",
    "LOG_LEVEL": "debug"
  }
}
```

#### Backend Debugging

```python
# backend/src/main.py

import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to INFO in production
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('.localpilot/debug.log')
    ]
)

logger = logging.getLogger(__name__)

# Add debug endpoints
@app.get("/debug/state")
async def get_debug_state():
    """Debug endpoint to inspect system state"""
    return {
        "active_connections": len(connection_manager.active_connections),
        "loaded_models": model_manager.get_loaded_models(),
        "vram_usage": vram_monitor.get_usage(),
        "cache_size": cache_manager.get_size(),
    }
```

### Common Issues & Solutions

```yaml
Issue: Extension not activating
Solutions:
  - Check activation events in package.json
  - Verify extension ID is correct
  - Check VS Code version compatibility
  - Look for errors in Output > Extension Host

Issue: WebSocket connection fails
Solutions:
  - Verify backend is running (curl http://localhost:8765/health)
  - Check firewall settings
  - Verify port 8765 is not in use
  - Check WebSocket URL is correct

Issue: Indexing fails for large projects
Solutions:
  - Increase memory limits in backend/.env
  - Check Tree-sitter grammar is built correctly
  - Verify VRAM is not exhausted
  - Check file permissions

Issue: Slow embedding generation
Solutions:
  - Verify GPU is being used (nvidia-smi)
  - Check batch size (reduce if OOM)
  - Ensure Ollama has GPU access
  - Monitor VRAM usage

Issue: Tests failing intermittently
Solutions:
  - Check for race conditions
  - Add proper async/await handling
  - Increase timeouts for slow operations
  - Mock external dependencies properly
```

### Logging Best Practices

```typescript
// TypeScript logging
import * as vscode from 'vscode';

export class Logger {
  private output: vscode.OutputChannel;
  
  constructor(name: string) {
    this.output = vscode.window.createOutputChannel(name);
  }
  
  debug(message: string, ...args: any[]) {
    this.output.appendLine(`[DEBUG] ${message} ${JSON.stringify(args)}`);
  }
  
  info(message: string) {
    this.output.appendLine(`[INFO] ${message}`);
  }
  
  error(message: string, error?: Error) {
    this.output.appendLine(`[ERROR] ${message}`);
    if (error) {
      this.output.appendLine(error.stack || error.message);
    }
  }
  
  show() {
    this.output.show();
  }
}

// Usage
const logger = new Logger('LocalPilot');
logger.info('Indexing started');
logger.debug('Processing file', { path: 'src/index.ts', size: 1024 });
logger.error('Indexing failed', error);
```

```python
# Python logging
import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)

def log_execution_time(func):
    """Decorator to log function execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start
            logger.info(f"{func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(f"{func.__name__} failed after {duration:.2f}s: {e}")
            raise
    return wrapper

# Usage
@log_execution_time
async def index_workspace(workspace_path: str):
    logger.debug(f"Starting indexing for {workspace_path}")
    # ... implementation
```

---

## 📊 Performance Profiling

### Frontend Profiling

```typescript
// React DevTools Profiler
import { Profiler } from 'react';

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}

<Profiler id="ChatView" onRender={onRenderCallback}>
  <ChatView />
</Profiler>
```

### Backend Profiling

```python
# backend/src/utils/profiling.py

import cProfile
import pstats
from functools import wraps

def profile(func):
    """Profile function execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20
        
        return result
    return wrapper

# Usage
@profile
def index_large_project(path: str):
    # ... implementation
```

---

## 🚀 Release Process

### Version Bumping

```bash
# Update version
npm version patch  # 0.1.0 -> 0.1.1
npm version minor  # 0.1.1 -> 0.2.0
npm version major  # 0.2.0 -> 1.0.0

# Tag release
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

### Build & Package

```bash
# Build extension
cd extension
npm run build

# Package extension
vsce package

# Generates: localpilot-0.1.0.vsix
```

---

## 📚 Related Documents

- `PROJECT_CHARTER.md` - Vision and timeline
- `TECHNICAL_ARCHITECTURE.md` - System architecture
- `INDEXING_SYSTEM_SPEC.md` - Indexing deep dive
- `UI_DESIGN_SYSTEM.md` - UI components (PREVIOUS)
- `TESTING_STRATEGY.md` - Test specifications (NEXT)
- `DATA_MODELS.md` - Data schemas
- `API_SPECIFICATION.md` - API documentation

---

**END OF DOCUMENT**