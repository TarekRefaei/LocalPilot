# 📄 DEVELOPMENT_SETUP.md

# LocalPilot - Development Environment Setup

> Step-by-step guide to set up your LocalPilot development environment

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Development Setup Guide |
| **Platform** | Windows (MVP) |
| **Last Updated** | [Current Date] |

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install Required Software](#2-install-required-software)
3. [Repository Setup](#3-repository-setup)
4. [Extension Setup (TypeScript)](#4-extension-setup-typescript)
5. [Server Setup (Python)](#5-server-setup-python)
6. [Ollama Configuration](#6-ollama-configuration)
7. [VS Code Development Setup](#7-vs-code-development-setup)
8. [Running the Project](#8-running-the-project)
9. [Verification Checklist](#9-verification-checklist)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Software Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    REQUIRED SOFTWARE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Software          Version        Purpose                        │
│  ─────────────────────────────────────────────────────────────  │
│  Node.js           18.x or 20.x   Extension runtime             │
│  pnpm              8.x+           Package manager               │
│  Python            3.11+          RAG server                    │
│  uv                Latest         Python package manager         │
│  Git               Latest         Version control               │
│  VS Code           1.85+          IDE & extension host          │
│  Ollama            Latest         Local LLM provider            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Your System

Based on your specs:
- **OS:** Windows 11
- **RAM:** 16GB ✓ (sufficient)
- **GPU:** RTX 4060 ✓ (excellent for Ollama)
- **CPU:** AMD Ryzen 7 8845HS ✓

---

## 2. Install Required Software

### 2.1 Install Node.js

```powershell
# Option A: Download installer from nodejs.org
# https://nodejs.org/en/download/ (LTS version 20.x)

# Option B: Using winget
winget install OpenJS.NodeJS.LTS

# Verify installation
node --version   # Should show v20.x.x
npm --version    # Should show 10.x.x
```

### 2.2 Install pnpm

```powershell
# Install pnpm globally
npm install -g pnpm

# Verify installation
pnpm --version   # Should show 8.x.x or 9.x.x
```

### 2.3 Install Python 3.11+

```powershell
# Option A: Download from python.org
# https://www.python.org/downloads/ (3.11 or 3.12)
# ⚠️ CHECK "Add Python to PATH" during installation!

# Option B: Using winget
winget install Python.Python.3.11

# Verify installation
python --version   # Should show Python 3.11.x or 3.12.x
pip --version      # Should show pip 23.x or 24.x
```

### 2.4 Install uv (Python Package Manager)

```powershell
# Install uv
pip install uv

# Verify installation
uv --version   # Should show uv 0.x.x
```

### 2.5 Install Git

```powershell
# Using winget
winget install Git.Git

# Verify installation
git --version   # Should show git version 2.x.x

# Configure Git (if not already done)
git config --global user.name "TarekRefaei"
git config --global user.email "your-email@example.com"
```

### 2.6 Install VS Code

```powershell
# Using winget
winget install Microsoft.VisualStudioCode

# Or download from: https://code.visualstudio.com/
```

### 2.7 Install Ollama

```powershell
# Download from: https://ollama.com/download/windows

# After installation, Ollama runs as a service
# Verify it's running:
curl http://localhost:11434/api/version

# Or in browser: http://localhost:11434
```

---

## 3. Repository Setup

### 3.1 Create Repository

```powershell
# Navigate to your projects directory
cd C:\Projects  # or your preferred location

# Create project directory
mkdir LocalPilot
cd LocalPilot

# Initialize Git repository
git init

# Create initial structure
mkdir extension
mkdir server
mkdir docs
mkdir scripts
mkdir .vscode
```

### 3.2 Create Root Configuration Files

#### .gitignore

```powershell
# Create .gitignore
New-Item -Path ".gitignore" -ItemType File
```

Add this content to `.gitignore`:

```gitignore
# Node
node_modules/
*.vsix
dist/
out/

# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
*.egg-info/

# IDE
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
server/data/
.localpilot/
*.log

# Environment
.env
.env.local

# Build
*.tsbuildinfo
```

#### .editorconfig

```editorconfig
# .editorconfig
root = true

[*]
indent_style = space
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{ts,tsx,js,jsx,json}]
indent_size = 2

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
```

### 3.3 Initial Commit

```powershell
git add .
git commit -m "chore: initial project structure"
```

---

## 4. Extension Setup (TypeScript)

### 4.1 Initialize Extension Package

```powershell
cd extension

# Initialize package.json
pnpm init
```

### 4.2 Create package.json

Replace the generated `package.json` with:

```json
{
  "name": "localpilot",
  "displayName": "LocalPilot",
  "description": "Privacy-First AI Pair Programming",
  "version": "0.1.0",
  "publisher": "TarekRefaei",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Other"],
  "activationEvents": [],
  "main": "./dist/extension.js",
  "contributes": {
    "viewsContainers": {
      "activitybar": [
        {
          "id": "localpilot",
          "title": "LocalPilot",
          "icon": "resources/icons/icon.svg"
        }
      ]
    },
    "views": {
      "localpilot": [
        {
          "type": "webview",
          "id": "localpilot.mainView",
          "name": "LocalPilot"
        }
      ]
    },
    "commands": [
      {
        "command": "localpilot.startIndexing",
        "title": "LocalPilot: Start Indexing"
      },
      {
        "command": "localpilot.syncIndex",
        "title": "LocalPilot: Sync Index"
      }
    ],
    "configuration": {
      "title": "LocalPilot",
      "properties": {
        "localpilot.ollamaUrl": {
          "type": "string",
          "default": "http://localhost:11434",
          "description": "Ollama server URL"
        },
        "localpilot.chatModel": {
          "type": "string",
          "default": "qwen2.5-coder:7b-instruct-q4_K_M",
          "description": "Model for chat"
        },
        "localpilot.embeddingModel": {
          "type": "string",
          "default": "mxbai-embed-large:latest",
          "description": "Model for embeddings"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "pnpm run build",
    "build": "node esbuild.js --production",
    "watch": "node esbuild.js --watch",
    "lint": "eslint src --ext ts,tsx",
    "format": "prettier --write \"src/**/*.{ts,tsx}\"",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@types/vscode": "^1.85.0",
    "@typescript-eslint/eslint-plugin": "^6.13.0",
    "@typescript-eslint/parser": "^6.13.0",
    "esbuild": "^0.19.8",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0",
    "typescript": "^5.3.2",
    "vitest": "^1.0.0"
  },
  "dependencies": {
    "ws": "^8.14.2"
  }
}
```

### 4.3 Install Extension Dependencies

```powershell
# Install all dependencies
pnpm install

# Install React and related packages
pnpm add react react-dom zustand
pnpm add -D @types/react @types/react-dom

# Install Tailwind CSS
pnpm add -D tailwindcss postcss autoprefixer
```

### 4.4 Create TypeScript Configuration

Create `extension/tsconfig.json`:

```json
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2022",
    "lib": ["ES2022", "DOM"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "baseUrl": "./src",
    "paths": {
      "@core/*": ["core/*"],
      "@features/*": ["features/*"],
      "@infrastructure/*": ["infrastructure/*"],
      "@ui/*": ["ui/*"],
      "@utils/*": ["utils/*"]
    },
    "jsx": "react-jsx"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 4.5 Create esbuild Configuration

Create `extension/esbuild.js`:

```javascript
const esbuild = require('esbuild');

const production = process.argv.includes('--production');
const watch = process.argv.includes('--watch');

async function main() {
  const ctx = await esbuild.context({
    entryPoints: ['src/extension.ts'],
    bundle: true,
    format: 'cjs',
    minify: production,
    sourcemap: !production,
    sourcesContent: false,
    platform: 'node',
    outfile: 'dist/extension.js',
    external: ['vscode'],
    logLevel: 'info',
  });

  if (watch) {
    await ctx.watch();
    console.log('Watching for changes...');
  } else {
    await ctx.rebuild();
    await ctx.dispose();
  }
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
```

### 4.6 Create Entry Point

Create `extension/src/extension.ts`:

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  console.log('LocalPilot is now active!');

  // Register a simple command to verify extension works
  const disposable = vscode.commands.registerCommand(
    'localpilot.helloWorld',
    () => {
      vscode.window.showInformationMessage('Hello from LocalPilot!');
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {
  console.log('LocalPilot deactivated');
}
```

### 4.7 Verify Extension Setup

```powershell
# Build the extension
pnpm run build

# Should create dist/extension.js without errors
```

---

## 5. Server Setup (Python)

### 5.1 Navigate to Server Directory

```powershell
cd ../server  # From extension directory
# Or: cd C:\Projects\LocalPilot\server
```

### 5.2 Create Virtual Environment

```powershell
# Create virtual environment using uv
uv venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Your prompt should now show (.venv)
```

### 5.3 Create pyproject.toml

Create `server/pyproject.toml`:

```toml
[project]
name = "localpilot-server"
version = "0.1.0"
description = "LocalPilot RAG Server"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "websockets>=12.0",
    "chromadb>=0.4.18",
    "llama-index>=0.9.0",
    "tree-sitter>=0.20.4",
    "httpx>=0.25.2",
    "pydantic>=2.5.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "ruff>=0.1.6",
    "mypy>=1.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### 5.4 Install Python Dependencies

```powershell
# Install dependencies using uv
uv pip install -e ".[dev]"

# This installs:
# - FastAPI (web framework)
# - ChromaDB (vector database)
# - LlamaIndex (RAG framework)
# - Tree-sitter (code parsing)
# - And dev tools (pytest, ruff, mypy)
```

### 5.5 Install Tree-sitter Language Parsers

```powershell
# Install language parsers
uv pip install tree-sitter-python tree-sitter-javascript tree-sitter-typescript
```

**Note:** Dart parser may need to be built from source. For MVP, we'll add it later.

### 5.6 Create Server Entry Point

Create `server/src/__init__.py`:

```python
"""LocalPilot RAG Server"""
```

Create `server/src/main.py`:

```python
"""
LocalPilot RAG Server - Main Entry Point

This is the FastAPI application that handles:
- Workspace indexing
- RAG queries
- Chat with streaming
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="LocalPilot RAG Server",
    description="Local RAG server for LocalPilot VS Code extension",
    version="0.1.0"
)

# Allow connections from VS Code extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # VS Code extension
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }


@app.get("/api/models")
async def list_models():
    """List available Ollama models (placeholder)"""
    return {
        "models": []
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=52741,
        reload=True
    )
```

### 5.7 Verify Server Setup

```powershell
# Make sure virtual environment is activated
# (.venv) should show in prompt

# Run the server
cd src
python main.py

# Should show:
# INFO:     Uvicorn running on http://127.0.0.1:52741
# INFO:     Started reloader process

# Test in another terminal:
curl http://localhost:52741/health

# Should return: {"status":"healthy","version":"0.1.0"}

# Press Ctrl+C to stop server
```

---

## 6. Ollama Configuration

### 6.1 Verify Ollama is Running

```powershell
# Check Ollama status
curl http://localhost:11434/api/version

# Should return something like:
# {"version":"0.1.x"}
```

### 6.2 Pull Required Models

```powershell
# Pull embedding model (required for RAG)
ollama pull mxbai-embed-large

# Pull chat model (for conversations)
# You already have these based on your earlier message:
# - qwen2.5-coder:7b-instruct-q4_K_M
# - qwen2.5-coder:14b-instruct-q4_K_M

# If not, pull them:
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
```

### 6.3 Verify Models

```powershell
# List installed models
ollama list

# Expected output (your models):
# NAME                                    SIZE
# qwen2.5-coder:7b-instruct-q4_K_M       4.7 GB
# qwen2.5-coder:14b-instruct-q4_K_M      9.0 GB
# mxbai-embed-large:latest               670 MB
# bge-m3:latest                          1.2 GB
# jina/jina-embeddings-v2-base-en        547 MB
```

### 6.4 Test Ollama

```powershell
# Test chat completion
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:7b-instruct-q4_K_M",
  "prompt": "Write hello world in Python",
  "stream": false
}'

# Test embedding
curl http://localhost:11434/api/embeddings -d '{
  "model": "mxbai-embed-large",
  "prompt": "Hello world"
}'
```

---

## 7. VS Code Development Setup

### 7.1 Install Recommended Extensions

Create `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "eamodio.gitlens"
  ]
}
```

### 7.2 Create VS Code Settings

Create `.vscode/settings.json`:

```json
{
  // Editor settings
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },

  // TypeScript
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },

  // Python
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "python.defaultInterpreterPath": "${workspaceFolder}/server/.venv/Scripts/python.exe",

  // Files
  "files.exclude": {
    "**/__pycache__": true,
    "**/node_modules": true,
    "**/.git": true
  },

  // Search
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.venv": true
  }
}
```

### 7.3 Create Launch Configurations

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}/extension"
      ],
      "outFiles": [
        "${workspaceFolder}/extension/dist/**/*.js"
      ],
      "preLaunchTask": "npm: watch"
    },
    {
      "name": "Run Python Server",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/server/src/main.py",
      "cwd": "${workspaceFolder}/server/src",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/server/src"
      }
    }
  ],
  "compounds": [
    {
      "name": "Full Stack",
      "configurations": ["Run Python Server", "Run Extension"]
    }
  ]
}
```

### 7.4 Create Tasks

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "npm",
      "script": "watch",
      "path": "extension",
      "problemMatcher": "$esbuild-watch",
      "isBackground": true,
      "presentation": {
        "reveal": "silent"
      },
      "label": "npm: watch"
    },
    {
      "type": "npm",
      "script": "build",
      "path": "extension",
      "group": "build",
      "label": "npm: build extension"
    },
    {
      "label": "Start Python Server",
      "type": "shell",
      "command": "${workspaceFolder}/server/.venv/Scripts/python.exe",
      "args": ["${workspaceFolder}/server/src/main.py"],
      "isBackground": true,
      "problemMatcher": []
    }
  ]
}
```

---

## 8. Running the Project

### 8.1 Development Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT WORKFLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TERMINAL 1: Python Server                                       │
│  ─────────────────────────────────────────────────────────────  │
│  cd server                                                       │
│  .venv\Scripts\activate                                          │
│  cd src                                                          │
│  python main.py                                                  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  TERMINAL 2: Extension Watch Mode                                │
│  ─────────────────────────────────────────────────────────────  │
│  cd extension                                                    │
│  pnpm run watch                                                  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  VS CODE: Debug Extension                                        │
│  ─────────────────────────────────────────────────────────────  │
│  Press F5 (with "Run Extension" selected)                       │
│  A new VS Code window opens with extension loaded                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Quick Start Commands

```powershell
# From project root (C:\Projects\LocalPilot)

# Terminal 1: Start Python server
cd server
.venv\Scripts\activate
cd src
python main.py

# Terminal 2: Watch extension (new terminal)
cd extension
pnpm run watch

# Terminal 3: Test extension (or press F5 in VS Code)
# Opens new VS Code window with extension
```
---

### 8.3 Starting the Python Server

Use the provided script to start the server:

```powershell
# From project root
.\scripts\start-server.ps1

# Or with auto-reload for development
.\scripts\start-server.ps1 -Dev
```

The script will:
1. Check virtual environment exists
2. Verify port 52741 is available
3. Check Ollama connection (warning if not running)
4. Start the FastAPI server

**Manual Start (Alternative):**
```powershell
cd server
.venv\Scripts\activate
cd src
python -m uvicorn api.main:app --host 127.0.0.1 --port 52741 --reload
```

---

## 9. Verification Checklist

Run through this checklist to ensure everything is set up correctly:

```
┌─────────────────────────────────────────────────────────────────┐
│                   VERIFICATION CHECKLIST                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SOFTWARE VERSIONS                                               │
│  ─────────────────────────────────────────────────────────────  │
│  □ node --version          → v20.x.x                            │
│  □ pnpm --version          → 8.x.x or 9.x.x                     │
│  □ python --version        → 3.11.x or 3.12.x                   │
│  □ uv --version            → 0.x.x                              │
│  □ git --version           → 2.x.x                              │
│  □ code --version          → 1.85.x+                            │
│                                                                  │
│  OLLAMA                                                          │
│  ─────────────────────────────────────────────────────────────  │
│  □ Ollama running          → http://localhost:11434 responds    │
│  □ Embedding model         → mxbai-embed-large installed        │
│  □ Chat model              → qwen2.5-coder:7b installed         │
│                                                                  │
│  EXTENSION                                                       │
│  ─────────────────────────────────────────────────────────────  │
│  □ Dependencies installed  → pnpm install succeeds              │
│  □ Build works             → pnpm run build creates dist/       │
│  □ No TypeScript errors    → No red squiggles in VS Code        │
│                                                                  │
│  SERVER                                                          │
│  ─────────────────────────────────────────────────────────────  │
│  □ Virtual env created     → .venv folder exists                │
│  □ Dependencies installed  → uv pip install succeeds            │
│  □ Server starts           → python main.py runs                │
│  □ Health check works      → /health returns healthy            │
│                                                                  │
│  DEVELOPMENT                                                     │
│  ─────────────────────────────────────────────────────────────  │
│  □ VS Code opens project   → No errors in terminal              │
│  □ Extensions installed    → ESLint, Prettier, Python working   │
│  □ F5 launches extension   → New VS Code window opens           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Troubleshooting

### Common Issues

```
┌─────────────────────────────────────────────────────────────────┐
│                    TROUBLESHOOTING                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ISSUE: "pnpm not found"                                         │
│  ─────────────────────────────────────────────────────────────  │
│  Solution: Restart terminal after npm install -g pnpm           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: "python not found" after installation                   │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Ensure "Add to PATH" was checked during install             │
│  2. Restart terminal/VS Code                                     │
│  3. Or manually add to PATH:                                     │
│     C:\Users\{you}\AppData\Local\Programs\Python\Python311\     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: Ollama connection refused                                │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Check Ollama is running (system tray icon)                  │
│  2. Restart Ollama from Start Menu                              │
│  3. Check port 11434 is not blocked                             │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: Extension not loading in debug                           │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Run pnpm run build first                                     │
│  2. Check dist/extension.js exists                               │
│  3. Check Output panel for errors                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: Python import errors                                     │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Ensure virtual environment is activated                     │
│  2. Check (.venv) appears in terminal prompt                    │
│  3. Re-run: uv pip install -e ".[dev]"                          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ISSUE: Tree-sitter build errors                                 │
│  ─────────────────────────────────────────────────────────────  │
│  Solution:                                                       │
│  1. Install Visual Studio Build Tools                           │
│  2. Or use pre-built wheels:                                     │
│     pip install tree-sitter-python --only-binary :all:          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

After completing this setup:

1. **Verify everything works** using the checklist above

---

*Document Version: 1.0.0*
*Created: Planning Phase*