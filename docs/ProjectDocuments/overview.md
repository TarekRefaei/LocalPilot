# 📄 PROJECT_OVERVIEW.md

# LocalPilot - Project Overview

> **Privacy-First AI Pair Programming**

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Version** | 0.1.0-planning |
| **Author** | TarekRefaei |
| **Repository** | github.com/TarekRefaei/LocalPilot |
| **Document Type** | Master Project Overview |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Vision](#2-project-vision)
3. [Problem Statement](#3-problem-statement)
4. [Solution Overview](#4-solution-overview)
5. [Target Users](#5-target-users)
6. [Core Features](#6-core-features)
7. [System Architecture](#7-system-architecture)
8. [Technology Stack](#8-technology-stack)
9. [Project Scope](#9-project-scope)
10. [Success Criteria](#10-success-criteria)
11. [Constraints & Assumptions](#11-constraints--assumptions)
12. [Glossary](#12-glossary)
13. [Document References](#13-document-references)

---

## 1. Executive Summary

### What is LocalPilot?

LocalPilot is a Visual Studio Code extension that brings AI-powered coding assistance 
to developers who want to keep their code **private and offline**. Unlike cloud-based 
AI coding assistants (GitHub Copilot, Cursor, Augment), LocalPilot runs entirely on 
your local machine using Ollama as the LLM provider.

### Key Differentiator

LocalPilot introduces a **structured three-mode workflow**:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│    💬 CHAT          📋 PLAN           ⚡ ACT                   │
│    ─────────────    ─────────────    ─────────────              │
│    Discuss &        Create           Execute &                  │
│    Understand       TODO List        Implement                  │
│    Project          with Steps       Changes                    │
│                                                                 │
│         │                │                 │                    │
│         └───────────────►└────────────────►│                    │
│                                                                 │
│    "I want to add     "Here's the        "Creating              │
│     authentication"    step-by-step       auth.service.ts..."   │
│                        plan..."                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

This workflow ensures that AI assistance is **deliberate and controlled**, not just 
autocomplete-style suggestions. Users understand what will happen before any code 
is written.

### One-Line Description

> A VS Code extension that provides privacy-first AI coding assistance using local 
> LLMs (Ollama) with a structured Chat → Plan → Act workflow powered by advanced 
> RAG indexing.

---

## 2. Project Vision

### Vision Statement

To empower developers with intelligent AI coding assistance that:
- **Never sends code to the cloud**
- **Understands project context deeply** through advanced RAG indexing
- **Produces deliberate, planned changes** rather than unpredictable autocomplete
- **Works offline** in any environment

### Mission

Make local LLM-powered coding assistance accessible, effective, and structured, 
enabling developers to maintain complete control over their code and data while 
benefiting from AI productivity gains.

### Core Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                      CORE PRINCIPLES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔒 PRIVACY FIRST                                                │
│     All processing happens locally. No code ever leaves         │
│     your machine. Period.                                        │
│                                                                  │
│  🧠 CONTEXT-AWARE                                                │
│     The LLM understands your entire project through             │
│     intelligent RAG indexing, not just the current file.        │
│                                                                  │
│  📋 STRUCTURED WORKFLOW                                          │
│     Chat → Plan → Act ensures you understand and approve        │
│     every change before it happens.                             │
│                                                                  │
│  👁️ TRANSPARENT                                                  │
│     Every action is visible. Every change is reviewable.        │
│     No magic, no surprises.                                      │
│                                                                  │
│  🎯 PRACTICAL                                                    │
│     Built for real-world use with real-world hardware.          │
│     Works on 16GB RAM with consumer GPUs.                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Problem Statement

### The Current Landscape

AI coding assistants have transformed software development. However, current 
solutions present significant challenges:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROBLEMS WITH CURRENT SOLUTIONS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ PROBLEM 1: Privacy & Security Concerns                       │
│  ─────────────────────────────────────────────────────────────  │
│  • Code is sent to cloud servers                                │
│  • Enterprise policies may prohibit cloud AI tools              │
│  • Sensitive/proprietary code at risk                           │
│  • GDPR, HIPAA, and compliance issues                           │
│  • No control over how code is used for training                │
│                                                                  │
│  ❌ PROBLEM 2: Subscription Fatigue & Cost                       │
│  ─────────────────────────────────────────────────────────────  │
│  • GitHub Copilot: $19/month                                    │
│  • Cursor Pro: $20/month                                        │
│  • Augment: Enterprise pricing                                  │
│  • Costs add up for independent developers                      │
│                                                                  │
│  ❌ PROBLEM 3: Internet Dependency                               │
│  ─────────────────────────────────────────────────────────────  │
│  • No offline capability                                         │
│  • Unusable in restricted networks                              │
│  • Latency issues with cloud round-trips                        │
│  • Service outages affect productivity                          │
│                                                                  │
│  ❌ PROBLEM 4: Limited Project Understanding                     │
│  ─────────────────────────────────────────────────────────────  │
│  • Most tools only see current file or limited context          │
│  • Suggestions often ignore project conventions                 │
│  • No understanding of architecture or patterns                 │
│  • Repetitive explanations needed                               │
│                                                                  │
│  ❌ PROBLEM 5: Unstructured Assistance                           │
│  ─────────────────────────────────────────────────────────────  │
│  • Autocomplete is reactive, not deliberate                     │
│  • No planning phase before implementation                      │
│  • Hard to implement complex, multi-file features               │
│  • Changes can be unpredictable                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Who Feels These Problems?

1. **Enterprise Developers** - Cannot use cloud AI due to policies
2. **Security-Conscious Developers** - Don't trust code in the cloud
3. **Offline Workers** - Air-gapped environments, travel, poor connectivity
4. **Independent Developers** - Subscription costs are prohibitive
5. **Open Source Contributors** - Privacy concerns with commercial tools

---

## 4. Solution Overview

### How LocalPilot Solves These Problems

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOCALPILOT SOLUTION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ SOLUTION 1: Complete Privacy                                 │
│  ─────────────────────────────────────────────────────────────  │
│  • All LLM inference runs locally via Ollama                    │
│  • RAG index stored on your machine                             │
│  • Zero network calls for AI features                           │
│  • Your code never leaves your computer                         │
│                                                                  │
│  ✅ SOLUTION 2: Free After Hardware                              │
│  ─────────────────────────────────────────────────────────────  │
│  • Ollama is free and open source                               │
│  • LocalPilot extension is free                                  │
│  • One-time hardware investment, unlimited use                  │
│                                                                  │
│  ✅ SOLUTION 3: Works Offline                                    │
│  ─────────────────────────────────────────────────────────────  │
│  • No internet required after initial setup                     │
│  • Works in air-gapped environments                             │
│  • No latency from network round-trips                          │
│  • No service dependency                                        │
│                                                                  │
│  ✅ SOLUTION 4: Deep Project Understanding via RAG               │
│  ─────────────────────────────────────────────────────────────  │
│  • Indexes entire codebase semantically                         │
│  • Understands code structure (functions, classes, modules)     │
│  • Retrieves relevant context for every query                   │
│  • Learns your project's patterns and conventions               │
│                                                                  │
│  ✅ SOLUTION 5: Structured Chat → Plan → Act Workflow            │
│  ─────────────────────────────────────────────────────────────  │
│  • Discuss before deciding (Chat Mode)                          │
│  • Plan before implementing (Plan Mode)                         │
│  • Review before applying (Act Mode)                            │
│  • Full control at every step                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### The LocalPilot Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE LOCALPILOT WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STEP 0: INDEXING (One-time setup per project)                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  📁 Your Project                                             ││
│  │       │                                                      ││
│  │       ▼                                                      ││
│  │  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐  ││
│  │  │   Scanner   │ ───► │   Chunker   │ ───► │  Embedder   │  ││
│  │  │             │      │  (AST-aware)│      │  (Ollama)   │  ││
│  │  └─────────────┘      └─────────────┘      └─────────────┘  ││
│  │                                                   │          ││
│  │                                                   ▼          ││
│  │                                          ┌─────────────┐     ││
│  │                                          │ Vector DB   │     ││
│  │                                          │ (ChromaDB)  │     ││
│  │                                          └─────────────┘     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  STEP 1: CHAT MODE                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  User: "I want to add user authentication to my app"           │
│                                                                  │
│  LocalPilot:                                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Based on your project structure, I can see you're using     ││
│  │ Express.js with a modular architecture. Here's how I'd      ││
│  │ approach authentication:                                     ││
│  │                                                              ││
│  │ 1. Create an auth module in src/modules/auth/               ││
│  │ 2. Add JWT token handling                                   ││
│  │ 3. Create middleware for protected routes                   ││
│  │ 4. Add login/register endpoints                             ││
│  │                                                              ││
│  │ [📋 Transfer to Plan Mode]                                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  STEP 2: PLAN MODE                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ## Plan: User Authentication Implementation                  ││
│  │                                                              ││
│  │ ### Prerequisites                                            ││
│  │ - [ ] Install jsonwebtoken and bcrypt packages              ││
│  │                                                              ││
│  │ ### Tasks                                                    ││
│  │ 1. [ ] Create src/modules/auth/auth.service.ts              ││
│  │    └── JWT sign/verify, password hashing                    ││
│  │                                                              ││
│  │ 2. [ ] Create src/modules/auth/auth.controller.ts           ││
│  │    └── Login, register, refresh endpoints                   ││
│  │                                                              ││
│  │ 3. [ ] Create src/middleware/auth.middleware.ts             ││
│  │    └── Token verification middleware                        ││
│  │                                                              ││
│  │ 4. [ ] Update src/routes/index.ts                           ││
│  │    └── Add auth routes                                       ││
│  │                                                              ││
│  │ 5. [ ] Create src/modules/auth/auth.test.ts                 ││
│  │    └── Unit tests for auth service                          ││
│  │                                                              ││
│  │ [✏️ Edit] [🔄 Regenerate] [✅ Approve & Execute]             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  STEP 3: ACT MODE                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 📋 Progress: ████░░░░░░ 40% (2/5 tasks)                      ││
│  │                                                              ││
│  │ ✅ Task 1: Create auth.service.ts         DONE              ││
│  │ ✅ Task 2: Create auth.controller.ts      DONE              ││
│  │ 🔄 Task 3: Create auth.middleware.ts      IN PROGRESS       ││
│  │ ⏳ Task 4: Update routes                  PENDING           ││
│  │ ⏳ Task 5: Create tests                   PENDING           ││
│  │                                                              ││
│  │ ─────────────────────────────────────────────────────────── ││
│  │ Currently creating: src/middleware/auth.middleware.ts       ││
│  │                                                              ││
│  │ ```typescript                                                ││
│  │ import { Request, Response, NextFunction } from 'express';  ││
│  │ import { AuthService } from '../modules/auth/auth.service'; ││
│  │                                                              ││
│  │ export const authMiddleware = async (                       ││
│  │   req: Request,                                              ││
│  │   res: Response,                                             ││
│  │   next: NextFunction                                         ││
│  │ ) => {                                                       ││
│  │   // ... implementation                                      ││
│  │ };                                                           ││
│  │ ```                                                          ││
│  │                                                              ││
│  │ [👁️ View Full] [✅ Apply] [❌ Skip] [✏️ Edit]                ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Target Users

### Primary User Personas

```
┌─────────────────────────────────────────────────────────────────┐
│                      TARGET USER PERSONAS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  👤 PERSONA 1: The Privacy-Conscious Developer                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: Alex                                                      │
│  Role: Senior Developer at a security-focused startup            │
│  Pain: "I can't use Copilot because our security policy          │
│         prohibits sending code to external servers"              │
│  Need: AI coding help that stays completely local               │
│  Tech: Works with TypeScript, Python, handles sensitive data    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  👤 PERSONA 2: The Independent Developer                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: Sam                                                       │
│  Role: Freelancer working on multiple projects                   │
│  Pain: "Subscription costs for all these AI tools add up        │
│         quickly when you're independent"                        │
│  Need: Free/one-time-cost AI assistance                         │
│  Tech: Full-stack, works with React, Node, Python               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  👤 PERSONA 3: The Mobile Developer                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: Jordan                                                    │
│  Role: Flutter/React Native developer                           │
│  Pain: "Most AI tools don't understand Dart well, and I         │
│         often work offline during commutes"                     │
│  Need: Offline-capable AI that understands mobile patterns      │
│  Tech: Dart/Flutter, TypeScript, occasionally Kotlin            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  👤 PERSONA 4: The Learning Developer                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Name: Taylor                                                    │
│  Role: Junior developer, 1 year experience                      │
│  Pain: "I want to understand what AI suggests, not just         │
│         accept code blindly"                                    │
│  Need: Structured workflow that explains before doing           │
│  Tech: Learning TypeScript and Python                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### User Requirements Summary

| Requirement | Priority | Addressed By |
|-------------|----------|--------------|
| Code stays local | MUST | Ollama + local RAG |
| Works offline | MUST | No cloud dependencies |
| Free to use | SHOULD | Open source + Ollama |
| Understands whole project | MUST | RAG indexing system |
| Explains before changing | MUST | Chat → Plan → Act workflow |
| Supports multiple languages | SHOULD | Extensible parser system |
| Fast responses | SHOULD | Optimized local inference |
| Easy to set up | MUST | Guided onboarding |

---

## 6. Core Features

### Feature Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      CORE FEATURES                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔧 FEATURE 1: Intelligent Project Indexing                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Scans all project files                                       │
│  • Parses code structure (functions, classes, imports)          │
│  • Creates semantic embeddings using local LLM                  │
│  • Stores in local vector database                              │
│  • Enables intelligent code retrieval                           │
│                                                                  │
│  User sees:                                                      │
│  • One-click "Index Project" button                             │
│  • Progress indicator during indexing                           │
│  • Summary of indexed content                                    │
│                                                                  │
│  Technical details:                                              │
│  • Uses Tree-sitter for AST parsing                             │
│  • mxbai-embed-large for embeddings                             │
│  • ChromaDB for vector storage                                   │
│  • Incremental updates via file watching                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  💬 FEATURE 2: Chat Mode                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Natural conversation about your codebase                     │
│  • Retrieves relevant code context automatically                │
│  • Explains code, answers questions                             │
│  • Suggests approaches for new features                         │
│  • Provides project summary after indexing                      │
│                                                                  │
│  User sees:                                                      │
│  • Chat interface in sidebar                                     │
│  • Messages with code highlighting                              │
│  • "Transfer to Plan" button when ready                         │
│                                                                  │
│  Technical details:                                              │
│  • RAG-enhanced prompts                                          │
│  • Streaming responses via WebSocket                            │
│  • Context window management                                     │
│  • Conversation history (session-based)                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  📋 FEATURE 3: Plan Mode                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Converts chat discussion into structured plan                │
│  • Creates detailed TODO list with file paths                   │
│  • Specifies what will be created/modified                      │
│  • Allows editing before execution                              │
│                                                                  │
│  User sees:                                                      │
│  • Formatted plan with checkboxes                               │
│  • File paths for each change                                    │
│  • Edit/Regenerate/Approve buttons                              │
│                                                                  │
│  Technical details:                                              │
│  • Specialized planning prompt                                   │
│  • Structured output parsing                                     │
│  • Plan state management                                         │
│  • Transfer mechanism to Act Mode                               │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  ⚡ FEATURE 4: Act Mode                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Executes plan step by step                                   │
│  • Creates and modifies files                                    │
│  • Shows diffs before applying                                   │
│  • Tracks progress visually                                      │
│  • Allows pause/resume/skip                                      │
│                                                                  │
│  User sees:                                                      │
│  • Progress tracker with task status                            │
│  • Current task details with code preview                       │
│  • Apply/Skip/Edit controls per task                            │
│  • Terminal output (when running commands)                       │
│                                                                  │
│  Technical details:                                              │
│  • VS Code file system API integration                          │
│  • Diff generation and display                                   │
│  • Task queue management                                         │
│  • Rollback capability                                           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  🔗 FEATURE 5: Ollama Integration                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  What it does:                                                   │
│  • Detects running Ollama instance                              │
│  • Lists available models                                        │
│  • Handles chat completions                                      │
│  • Handles embedding generation                                  │
│  • Manages connection health                                     │
│                                                                  │
│  User sees:                                                      │
│  • Ollama status indicator                                       │
│  • Model selection dropdown                                      │
│  • Connection error messages                                     │
│                                                                  │
│  Technical details:                                              │
│  • REST API communication (port 11434)                          │
│  • Streaming response handling                                   │
│  • Automatic reconnection                                        │
│  • Model capability detection                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Feature Matrix by Release

| Feature | MVP (v0.1) | v1.1 | v1.2+ |
|---------|------------|------|-------|
| Ollama connection | ✅ | ✅ | ✅ |
| AST-aware indexing | ✅ | ✅ | ✅ |
| Smart Sync indexing | ✅ | ✅ | ✅ |
| Auto file watching | ❌ | ✅ | ✅ |
| Chat mode | ✅ | ✅ | ✅ |
| Plan mode | ✅ | ✅ | ✅ |
| Act mode (basic) | ✅ | ✅ | ✅ |
| Act mode (terminal) | ❌ | ✅ | ✅ |
| Conversation persistence | ❌ | ✅ | ✅ |
| TypeScript/JavaScript | ✅ | ✅ | ✅ |
| Python | ✅ | ✅ | ✅ |
| Dart/Flutter | ✅ | ✅ | ✅ |
| Kotlin | ❌ | ✅ | ✅ |
| Swift | ❌ | ❌ | ✅ |
| Settings UI | ❌ | ✅ | ✅ |
| Multiple workspaces | ❌ | ❌ | ✅ |
---

## 7. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 LOCALPILOT SYSTEM ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                        ┌─────────────────┐                      │
│                        │    VS Code      │                      │
│                        │    (Host)       │                      │
│                        └────────┬────────┘                      │
│                                 │                                │
│  ┌──────────────────────────────┼──────────────────────────────┐│
│  │                              │                               ││
│  │           LOCALPILOT EXTENSION (TypeScript)                  ││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                    PRESENTATION LAYER                    │││
│  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐              │││
│  │  │  │ Onboarding│ │  Chat UI  │ │  Plan UI  │              │││
│  │  │  │   View    │ │           │ │           │              │││
│  │  │  └───────────┘ └───────────┘ └───────────┘              │││
│  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐              │││
│  │  │  │  Act UI   │ │ Settings  │ │  Status   │              │││
│  │  │  │           │ │    UI     │ │   Bar     │              │││
│  │  │  └───────────┘ └───────────┘ └───────────┘              │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                    FEATURE LAYER                         │││
│  │  │                                                          │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │   Indexing   │ │     Chat     │ │     Plan     │     │││
│  │  │  │   Feature    │ │   Feature    │ │   Feature    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  │  ┌──────────────┐ ┌──────────────┐                      │││
│  │  │  │     Act      │ │   Settings   │                      │││
│  │  │  │   Feature    │ │   Feature    │                      │││
│  │  │  └──────────────┘ └──────────────┘                      │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                      CORE LAYER                          │││
│  │  │                                                          │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │   Entities   │ │  Interfaces  │ │    Errors    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                 INFRASTRUCTURE LAYER                     │││
│  │  │                                                          │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │    VS Code   │ │     HTTP     │ │  WebSocket   │     │││
│  │  │  │    Adapter   │ │    Client    │ │    Client    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  └──────────────────────────────┼──────────────────────────────┘│
│                                 │                                │
│                    HTTP / WebSocket                              │
│                                 │                                │
│  ┌──────────────────────────────┼──────────────────────────────┐│
│  │                              │                               ││
│  │              PYTHON RAG SERVER (FastAPI)                     ││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                       API LAYER                          │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │  /index      │ │  /query      │ │  /chat       │     │││
│  │  │  │  endpoint    │ │  endpoint    │ │  endpoint    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                    SERVICE LAYER                         │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │  Indexing    │ │     RAG      │ │     LLM      │     │││
│  │  │  │   Service    │ │   Service    │ │   Service    │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                 INFRASTRUCTURE LAYER                     │││
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │││
│  │  │  │  LlamaIndex  │ │   ChromaDB   │ │ Tree-sitter  │     │││
│  │  │  │   Adapter    │ │   Adapter    │ │   Parser     │     │││
│  │  │  └──────────────┘ └──────────────┘ └──────────────┘     │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                              │                               ││
│  └──────────────────────────────┼──────────────────────────────┘│
│                                 │                                │
│                           Ollama API                             │
│                                 │                                │
│                    ┌────────────┴───────────┐                   │
│                    │       OLLAMA           │                   │
│                    │   (Local LLM Server)   │                   │
│                    │                        │                   │
│                    │  ┌──────────────────┐  │                   │
│                    │  │ qwen2.5-coder    │  │                   │
│                    │  │ mxbai-embed      │  │                   │
│                    │  └──────────────────┘  │                   │
│                    └────────────────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA FLOW OVERVIEW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FLOW 1: INDEXING                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │ VS Code│───►│  Scan  │───►│ Parse  │───►│ Chunk  │          │
│  │  Files │    │ Files  │    │  AST   │    │  Code  │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                   │              │
│       ┌────────────────────────────────────────────┘              │
│       │                                                          │
│       ▼                                                          │
│  ┌────────┐    ┌────────┐    ┌────────┐                         │
│  │Ollama  │───►│Generate│───►│ Store  │                         │
│  │Embed   │    │Vectors │    │ChromaDB│                         │
│  └────────┘    └────────┘    └────────┘                         │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FLOW 2: CHAT QUERY                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │  User  │───►│ Embed  │───►│ Query  │───►│Retrieve│          │
│  │  Query │    │  Query │    │ChromaDB│    │ Chunks │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                   │              │
│       ┌────────────────────────────────────────────┘              │
│       │                                                          │
│       ▼                                                          │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │ Build  │───►│ Send   │───►│ Stream │───►│Display │          │
│  │ Prompt │    │ Ollama │    │Response│    │  Chat  │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  FLOW 3: PLAN TO ACT                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐          │
│  │  Plan  │───►│ Parse  │───►│Generate│───►│ Write  │          │
│  │  JSON  │    │ Tasks  │    │  Code  │    │  File  │          │
│  └────────┘    └────────┘    └────────┘    └────────┘          │
│                                                   │              │
│       ┌────────────────────────────────────────────┘              │
│       │                                                          │
│       ▼                                                          │
│  ┌────────┐    ┌────────┐    ┌────────┐                         │
│  │ Update │───►│ Re-    │───►│  Next  │                         │
│  │ Index  │    │ Index  │    │  Task  │                         │
│  └────────┘    └────────┘    └────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Communication

```
┌─────────────────────────────────────────────────────────────────┐
│                  COMMUNICATION PROTOCOLS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VS Code Extension ◄──────► Python RAG Server                    │
│                                                                  │
│  Protocol: HTTP REST + WebSocket                                │
│  Port: 8000 (configurable)                                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  REST Endpoints:                                             ││
│  │                                                              ││
│  │  POST   /api/index/start    - Start indexing                 ││
│  │  GET    /api/index/status   - Get indexing progress          ││
│  │  DELETE /api/index          - Clear index                    ││
│  │  POST   /api/query          - Query RAG                      ││
│  │  GET    /api/health         - Health check                   ││
│  │  GET    /api/models         - List Ollama models            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  WebSocket:                                                  ││
│  │                                                              ││
│  │  WS /ws/chat     - Streaming chat responses                  ││
│  │  WS /ws/progress - Real-time indexing progress               ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  Python RAG Server ◄──────► Ollama                               │
│                                                                  │
│  Protocol: HTTP REST                                             │
│  Port: 11434 (Ollama default)                                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Ollama Endpoints Used:                                      ││
│  │                                                              ││
│  │  POST   /api/generate    - Text generation (chat)           ││
│  │  POST   /api/embeddings  - Generate embeddings               ││
│  │  GET    /api/tags        - List available models             ││
│  │  POST   /api/show        - Model information                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Technology Stack

### Complete Stack Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VS CODE EXTENSION (TypeScript)                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Core:                                                           │
│  ├── Language:        TypeScript 5.x                            │
│  ├── Runtime:         Node.js 18+                               │
│  ├── VS Code API:     1.85+                                     │
│  └── Module System:   ES Modules                                │
│                                                                  │
│  UI:                                                             │
│  ├── Framework:       React 18                                  │
│  ├── Styling:         Tailwind CSS                              │
│  ├── State:           Zustand                                   │
│  ├── Rendering:       VS Code WebView                           │
│  └── Icons:           Lucide React                              │
│                                                                  │
│  Build & Dev:                                                    │
│  ├── Bundler:         esbuild                                   │
│  ├── Package Manager: pnpm                                      │
│  ├── Linting:         ESLint + Prettier                         │
│  └── Testing:         Vitest + Testing Library                  │
│                                                                  │
│  Communication:                                                  │
│  ├── HTTP Client:     fetch (native)                            │
│  └── WebSocket:       ws                                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PYTHON RAG SERVER                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Core:                                                           │
│  ├── Language:        Python 3.11+                              │
│  ├── Framework:       FastAPI                                   │
│  ├── Server:          Uvicorn                                   │
│  └── Async:           asyncio                                   │
│                                                                  │
│  RAG:                                                            │
│  ├── Framework:       LlamaIndex                                │
│  ├── Vector DB:       ChromaDB                                  │
│  ├── Embeddings:      Ollama (mxbai-embed-large)                │
│  └── LLM:             Ollama (qwen2.5-coder)                    │
│                                                                  │
│  Code Parsing:                                                   │
│  ├── AST Parser:      Tree-sitter                               │
│  └── Languages:       TS, JS, Python, Dart (MVP)                │
│                                                                  │
│  Build & Dev:                                                    │
│  ├── Package Manager: uv (or poetry)                            │
│  ├── Linting:         Ruff                                      │
│  ├── Type Checking:   mypy                                      │
│  └── Testing:         pytest + pytest-asyncio                   │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  LLM PROVIDER                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Platform:            Ollama                                     │
│  Default Chat Model:  qwen2.5-coder:7b-instruct-q4_K_M         │
│  Default Embed Model: mxbai-embed-large:latest                  │
│  Backup Chat Model:   qwen2.5-coder:14b-instruct-q4_K_M        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  DEVELOPMENT TOOLS                                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Version Control:     Git + GitHub                              │
│  CI/CD:               GitHub Actions                            │
│  Documentation:       Markdown + TypeDoc + Sphinx               │
│  Pre-commit:          Husky + lint-staged                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why These Technologies?

| Technology | Chosen Over | Reason |
|------------|-------------|--------|
| **TypeScript** | JavaScript | Type safety, better tooling, required for complex extension |
| **React** | Vue, Svelte, Vanilla | Most familiar to developer, largest ecosystem |
| **Zustand** | Redux, MobX | Lightweight, simple API, less boilerplate |
| **esbuild** | Webpack, Vite | Fastest bundler, simple config |
| **FastAPI** | Flask, Django | Modern async Python, great for APIs |
| **LlamaIndex** | LangChain | Better for indexing/RAG, simpler API |
| **ChromaDB** | Qdrant, FAISS | Easiest setup, Python native, sufficient for MVP |
| **Tree-sitter** | Regex, Custom | Industry standard, supports all needed languages |
| **pnpm** | npm, yarn | Faster, disk efficient |
| **uv** | pip, poetry | Faster, simpler than poetry |

---

## 9. Project Scope

### In Scope (MVP)

```
┌─────────────────────────────────────────────────────────────────┐
│                     MVP SCOPE (v0.1.0)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ INCLUDED IN MVP                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Extension Core:                                                 │
│  ☑ VS Code extension activation and lifecycle                   │
│  ☑ Sidebar panel with three-tab interface                       │
│  ☑ Onboarding screen with indexing button                       │
│  ☑ Basic settings (model selection)                             │
│  ☑ Status bar indicator                                          │
│                                                                  │
│  Ollama Integration:                                             │
│  ☑ Detect Ollama running status                                  │
│  ☑ List available models                                         │
│  ☑ Chat completions with streaming                              │
│  ☑ Embedding generation                                          │
│  ☑ Error handling for connection issues                         │
│                                                                  │
│  Indexing (ENHANCED):                                            │
│  ☑ Scan workspace files                                          │
│  ☑ AST-aware code chunking (functions, classes, methods)        │
│  ☑ Tree-sitter parsing for TS, JS, Python, Dart                 │
│  ☑ Generate embeddings via Ollama                               │
│  ☑ Store in ChromaDB with metadata                              │
│  ☑ Progress indicator                                            │
│  ☑ Index persistence                                             │
│  ☑ Smart "Sync Index" with hash-based change detection          │
│                                                                  │
│  Chat Mode:                                                       │
│  ☑ Chat interface with message display                          │
│  ☑ RAG-enhanced responses                                        │
│  ☑ Project summary after indexing                               │
│  ☑ Transfer to Plan button                                       │
│  ☑ Streaming response display                                    │
│                                                                  │
│  Plan Mode:                                                       │
│  ☑ Display structured plan                                       │
│  ☑ TODO list with checkboxes                                    │
│  ☑ File paths for each task                                     │
│  ☑ Edit/Regenerate capabilities                                 │
│  ☑ Approve and transfer to Act                                  │
│                                                                  │
│  Act Mode (Basic):                                                │
│  ☑ Display task list with progress                              │
│  ☑ Create new files                                              │
│  ☑ Modify existing files with diff preview                      │
│  ☑ Delete files (with confirmation)                             │
│  ☑ Create folders                                                │
│  ☑ Apply/Skip/Edit controls                                     │
│  ☑ Generate TODO markdown file                                  │
│  ☐ Terminal command execution (v1.1)                            │
│                                                                  │
│  Languages (Full AST Support):                                   │
│  ☑ TypeScript                                                    │
│  ☑ JavaScript                                                    │
│  ☑ Python                                                        │
│  ☑ Dart (Flutter)                                                │
│                                                                  │
│  Platform:                                                        │
│  ☑ Windows 10/11                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```


### Out of Scope (MVP)

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOT IN MVP (Future)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ EXCLUDED FROM MVP                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Features:                                                       │
│  ☐ Incremental indexing / file watching (v1.1)                  │
│  ☐ Terminal command execution (v1.1)                            │
│  ☐ Conversation history persistence (v1.1)                      │
│  ☐ Multiple workspace support (v1.2)                            │
│  ☐ Git integration (v1.2)                                        │
│  ☐ Voice input (Future)                                          │
│  ☐ Custom system prompts (v1.2)                                 │
│                                                                  │
│  Languages (Future):                                              │
│  ☐ Kotlin                                                        │
│  ☐ Swift                                                         │
│  ☐ Java                                                          │
│  ☐ C/C++                                                         │
│  ☐ Rust                                                          │
│  ☐ Go                                                            │
│                                                                  │
│  Platforms (Future):                                              │
│  ☐ macOS                                                         │
│  ☐ Linux                                                         │
│                                                                  │
│  Advanced:                                                        │
│  ☐ Cloud LLM providers (OpenAI, Anthropic)                      │
│  ☐ Team collaboration features                                  │
│  ☐ Model fine-tuning                                             │
│  ☐ Multi-model routing                                          │
│  ☐ LangChain alternative provider                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Success Criteria

### Definition of Done (MVP)

```
┌─────────────────────────────────────────────────────────────────┐
│                      MVP SUCCESS CRITERIA                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  The MVP is successful when a user can:                         │
│                                                                  │
│  ✅ CRITERION 1: Installation & Setup                            │
│  ─────────────────────────────────────────────────────────────  │
│  • Install the extension from .vsix file                        │
│  • See Ollama connection status                                  │
│  • Select from available Ollama models                          │
│  • Complete without reading documentation                       │
│  Time: < 5 minutes                                               │
│                                                                  │
│  ✅ CRITERION 2: Project Indexing                                │
│  ─────────────────────────────────────────────────────────────  │
│  • Click "Index Project" button                                  │
│  • See progress indicator                                        │
│  • Complete indexing for 100-file project                       │
│  • Receive project summary                                       │
│  Time: < 5 minutes for 100 files                                 │
│                                                                  │
│  ✅ CRITERION 3: Chat Understanding                              │
│  ─────────────────────────────────────────────────────────────  │
│  • Ask "What does this project do?"                             │
│  • Receive accurate, context-aware answer                       │
│  • Ask about specific file/function                             │
│  • Get relevant code in response                                 │
│  Accuracy: 80%+ relevant responses                               │
│                                                                  │
│  ✅ CRITERION 4: Plan Generation                                 │
│  ─────────────────────────────────────────────────────────────  │
│  • Request a new feature in chat                                 │
│  • Transfer to Plan mode                                         │
│  • See structured TODO list                                      │
│  • Tasks include file paths                                      │
│  Quality: Actionable, specific tasks                             │
│                                                                  │
│  ✅ CRITERION 5: Code Execution                                  │
│  ─────────────────────────────────────────────────────────────  │
│  • Approve plan and enter Act mode                              │
│  • See task progress                                             │
│  • Preview code before applying                                  │
│  • Files are created/modified correctly                         │
│  Quality: Code compiles/runs without errors                      │
│                                                                  │
│  ✅ CRITERION 6: Reliability                                     │
│  ─────────────────────────────────────────────────────────────  │
│  • No crashes during normal use                                  │
│  • Graceful error handling                                       │
│  • Clear error messages                                          │
│  Stability: 95%+ uptime during sessions                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Performance Indicators (KPIs)

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Indexing Speed** | <100ms per file | Stopwatch during indexing |
| **Query Response** | <3s for first token | Time from send to display |
| **Memory Usage** | <500MB extension | VS Code memory monitor |
| **Chat Accuracy** | 80%+ relevant | Manual review of 10 queries |
| **Code Quality** | Compiles 90%+ | Manual testing of generated code |
| **Crash Rate** | <1 per session | Crash logs |

---

## 11. Constraints & Assumptions

### Constraints

```
┌─────────────────────────────────────────────────────────────────┐
│                        CONSTRAINTS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TECHNICAL CONSTRAINTS                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Hardware Requirements:                                          │
│  • Minimum 16GB RAM                                              │
│  • GPU optional but recommended                                  │
│  • ~10GB disk space (Ollama models)                             │
│                                                                  │
│  Software Requirements:                                          │
│  • VS Code 1.85 or higher                                       │
│  • Ollama installed and running                                 │
│  • At least one chat model in Ollama                           │
│  • At least one embedding model in Ollama                       │
│                                                                  │
│  Platform:                                                       │
│  • Windows only for MVP                                          │
│                                                                  │
│  LLM Limitations:                                                │
│  • Context window limits (8K-32K tokens)                        │
│  • Local inference speed depends on hardware                    │
│  • Model quality varies                                          │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  PROJECT CONSTRAINTS                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  Team:                                                           │
│  • Solo developer                                                │
│  • Part-time availability                                        │
│  • Learning TypeScript and VS Code extensions                   │
│                                                                  │
│  Timeline:                                                       │
│  • Flexible but aiming for usable MVP                           │
│                                                                  │
│  Budget:                                                         │
│  • No paid services                                              │
│  • Open source tools only                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Assumptions

```
┌─────────────────────────────────────────────────────────────────┐
│                       ASSUMPTIONS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  USER ASSUMPTIONS                                                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  • User has Ollama installed before using LocalPilot            │
│  • User has downloaded at least one compatible model            │
│  • User is comfortable with VS Code                             │
│  • User understands basic LLM concepts                          │
│  • User has a project they want to work on                      │
│                                                                  │
│  TECHNICAL ASSUMPTIONS                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  • Ollama API remains stable (v0.1.x)                           │
│  • VS Code WebView API remains stable                           │
│  • ChromaDB can handle <10,000 document workspaces              │
│  • LlamaIndex Ollama integration works reliably                 │
│  • Tree-sitter parsers are accurate for target languages        │
│                                                                  │
│  QUALITY ASSUMPTIONS                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                  │
│  • qwen2.5-coder can generate usable code                       │
│  • mxbai-embed-large provides good code embeddings              │
│  • RAG retrieval will find relevant context                     │
│  • Semantic chunking is sufficient for MVP                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **AST** | Abstract Syntax Tree - A tree representation of code structure |
| **Chunking** | Splitting documents into smaller pieces for embedding |
| **Embedding** | A numerical vector representation of text |
| **LLM** | Large Language Model - AI model for text generation |
| **Ollama** | Local LLM runtime that runs models on your machine |
| **RAG** | Retrieval-Augmented Generation - Enhancing LLM with retrieved context |
| **Vector Database** | Database optimized for similarity search on embeddings |
| **WebView** | VS Code's way of displaying custom HTML/React UI |
| **Context Window** | Maximum tokens an LLM can process at once |
| **Tree-sitter** | Fast, incremental parsing library for code |
| **ChromaDB** | Open-source embedding database |
| **LlamaIndex** | Framework for building RAG applications |
| **FastAPI** | Modern Python web framework for APIs |
| **Token** | Basic unit of text for LLMs (roughly 4 characters) |

---


## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Owner | TarekRefaei | | |

---

*Document Version: 1.0.0*
*Created: Planning Phase*
*Last Updated: [Current Date]*