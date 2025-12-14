# 📄 INDEXING_SPEC.md

# LocalPilot - Indexing Specification

> Quality contract and technical specification for the indexing system

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | LocalPilot |
| **Author** | TarekRefaei |
| **Document Type** | Technical Specification |
| **Last Updated** | [Current Date] |
| **Status** | Planning Phase |

---

## Table of Contents

1. [Indexing Goals](#1-indexing-goals)
2. [Indexing Guarantees](#2-indexing-guarantees)
3. [Indexing Non-Goals](#3-indexing-non-goals)
4. [Chunking Strategy](#4-chunking-strategy)
5. [Quality Metrics](#5-quality-metrics)
6. [Language Support](#6-language-support)
7. [Performance Targets](#7-performance-targets)
8. [Testing & Validation](#8-testing--validation)

---

## 1. Indexing Goals

```
┌─────────────────────────────────────────────────────────────────┐
│                     INDEXING GOALS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRIMARY GOAL:                                                   │
│  Enable the LLM to retrieve relevant code context for any      │
│  user query about the codebase.                                 │
│                                                                  │
│  SUCCESS DEFINITION:                                             │
│  When user asks "How does X work?", the RAG system retrieves   │
│  the actual code that implements X, not unrelated code.         │
│                                                                  │
│  CORE REQUIREMENTS:                                              │
│  1. Every function/class is retrievable by its purpose         │
│  2. Retrieved code includes enough context to understand        │
│  3. Retrieval is fast enough for interactive use (<2s)         │
│  4. Index survives VS Code restart                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Indexing Guarantees

### What We WILL Do

```
┌─────────────────────────────────────────────────────────────────┐
│                   INDEXING GUARANTEES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GUARANTEE 1: AST-Aware Chunking                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  We chunk code by semantic units, NOT by character count.       │
│                                                                  │
│  ✓ Functions are never split in half                            │
│  ✓ Classes stay together (unless very large)                    │
│  ✓ Methods are individual chunks                                │
│  ✓ Imports are preserved with their file                        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GUARANTEE 2: Line-Accurate Metadata                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Every chunk includes:                                           │
│                                                                  │
│  ✓ Exact file path (relative to workspace)                     │
│  ✓ Start line number                                             │
│  ✓ End line number                                               │
│  ✓ Chunk type (function/class/method/etc.)                      │
│  ✓ Symbol name (function name, class name)                      │
│  ✓ Language identifier                                           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GUARANTEE 3: Complete Coverage                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Every supported file is indexed. No silent skipping.           │
│                                                                  │
│  ✓ All .ts, .js, .py, .dart files indexed                      │
│  ✓ Failed files reported (not silently skipped)                │
│  ✓ Index statistics show coverage                              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GUARANTEE 4: Persistence                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Index survives:                                                 │
│                                                                  │
│  ✓ VS Code restart                                               │
│  ✓ Computer restart                                              │
│  ✓ Extension update (same project ID)                           │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  GUARANTEE 5: Determinism                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Same code → Same chunks → Same embeddings                      │
│                                                                  │
│  ✓ Parsing is deterministic                                      │
│  ✓ Chunk IDs are hash-based (reproducible)                      │
│  ✓ Re-indexing same file produces same result                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Indexing Non-Goals

### What We Will NOT Do (v0.1)

```
┌─────────────────────────────────────────────────────────────────┐
│                   INDEXING NON-GOALS (MVP)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✗ Runtime Execution Analysis                                   │
│    We don't run code to understand it.                          │
│    Static analysis only.                                         │
│                                                                  │
│  ✗ Dynamic Type Inference                                        │
│    We don't infer types beyond what's in source.               │
│    No runtime type tracking.                                     │
│                                                                  │
│  ✗ Cross-Package Dependency Graph                               │
│    We index files, not npm/pip dependency trees.                │
│    (May add in v1.2+)                                           │
│                                                                  │
│  ✗ Semantic Understanding                                        │
│    We don't "understand" what code does.                        │
│    We chunk and embed, LLM does understanding.                  │
│                                                                  │
│  ✗ Binary/Compiled File Indexing                                │
│    No .pyc, .class, .dll, .exe files.                          │
│    Source code only.                                             │
│                                                                  │
│  ✗ Media File Indexing                                           │
│    No images, videos, audio.                                     │
│    Text/code files only.                                         │
│                                                                  │
│  ✗ Minified Code Handling                                        │
│    We don't de-minify JavaScript.                               │
│    Minified files indexed as-is (poor quality).                 │
│                                                                  │
│  ✗ Git History Analysis                                          │
│    Current state only.                                           │
│    No blame, no history, no diffs.                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Chunking Strategy

### 4.1 Chunk Types

| Type | Description | Example |
|------|-------------|---------|
| `function` | Standalone function | `function add(a, b)` |
| `class` | Class definition (without methods) | `class User { }` |
| `method` | Method inside a class | `User.save()` |
| `interface` | TypeScript interface | `interface Props` |
| `type` | Type alias | `type ID = string` |
| `variable` | Top-level const/let/var | `const API_URL = ...` |
| `import` | Import block (grouped) | All imports in file |
| `module` | Module-level code | File-level statements |
| `file` | Entire file (fallback) | When AST parsing fails |

### 4.2 Chunking Rules

```
┌─────────────────────────────────────────────────────────────────┐
│                     CHUNKING RULES                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  RULE 1: Maximum Chunk Size                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Max tokens per chunk: 500 tokens (~2000 chars)                 │
│                                                                  │
│  If a function exceeds this:                                     │
│  • Keep first 400 tokens                                         │
│  • Add "[...truncated...]"                                       │
│  • Store full content in metadata for retrieval                 │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  RULE 2: Minimum Chunk Size                                      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Min tokens per chunk: 20 tokens                                 │
│                                                                  │
│  Tiny functions/variables: Group with neighbors                 │
│  • Group consecutive small items                                 │
│  • Label as "module" chunk type                                 │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  RULE 3: Context Inclusion                                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Each chunk includes:                                            │
│  • Docstring/JSDoc (if present)                                 │
│  • Decorators (Python) / Annotations (TS)                       │
│  • Type annotations                                              │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  RULE 4: Class Handling                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Classes with < 5 methods: One chunk (whole class)              │
│  Classes with ≥ 5 methods: Split into method chunks            │
│  Each method chunk includes: Class name + method                │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  RULE 5: Import Handling                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  All imports in a file: One chunk (type: "import")              │
│  Helps LLM understand file dependencies                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Chunk Metadata Schema

```typescript
interface ChunkMetadata {
  // Identity
  chunk_id: string;        // Hash of file_path + content
  file_path: string;       // Relative to workspace
  
  // Location
  line_start: number;
  line_end: number;
  
  // Classification
  chunk_type: ChunkType;
  symbol_name: string | null;
  language: string;
  
  // Context
  docstring: string | null;
  parent_class: string | null;  // For methods
  
  // Quality
  token_count: number;
  is_truncated: boolean;
}
```

---

## 5. Quality Metrics

### 5.1 Retrieval Quality Targets

```
┌─────────────────────────────────────────────────────────────────┐
│                   QUALITY METRICS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  METRIC 1: Precision@5                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Target: ≥ 60%                                                  │
│                                                                  │
│  Definition: Of top 5 retrieved chunks, how many are           │
│  actually relevant to the query?                                │
│                                                                  │
│  Test: 10 sample queries, manually evaluate results             │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  METRIC 2: Recall@10                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Target: ≥ 80%                                                  │
│                                                                  │
│  Definition: When searching for a known function,              │
│  is it in the top 10 results?                                   │
│                                                                  │
│  Test: Search for 20 known functions by description            │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  METRIC 3: Coverage                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Target: 100% of supported files indexed                        │
│                                                                  │
│  Definition: All .ts, .js, .py, .dart files have chunks        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│  METRIC 4: Chunk Completeness                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Target: ≤ 5% truncated chunks                                  │
│                                                                  │
│  Definition: How many chunks had to be truncated?              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 How to Measure

```python
# Quality test script (manual for MVP)
def test_retrieval_quality():
    queries = [
        ("How does user authentication work?", ["auth.service.ts"]),
        ("Where is the login function?", ["login.ts"]),
        # ... more test queries
    ]
    
    precision_scores = []
    for query, expected_files in queries:
        results = rag_query(query, top_k=5)
        relevant = sum(1 for r in results if r.file_path in expected_files)
        precision_scores.append(relevant / 5)
    
    avg_precision = sum(precision_scores) / len(precision_scores)
    print(f"Precision@5: {avg_precision:.2%}")
    assert avg_precision >= 0.60, "Quality below threshold!"
```

---

## 6. Language Support

### 6.1 MVP Languages

| Language | Parser | Chunk Types Extracted |
|----------|--------|----------------------|
| **TypeScript** | Tree-sitter | function, class, method, interface, type, variable |
| **JavaScript** | Tree-sitter | function, class, method, variable |
| **Python** | Tree-sitter | function, class, method, variable |
| **Dart** | Tree-sitter | function, class, method, variable |

### 6.2 File Extensions

```python
SUPPORTED_EXTENSIONS = {
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.py': 'python',
    '.dart': 'dart',
}

EXCLUDED_PATTERNS = [
    '**/node_modules/**',
    '**/.git/**',
    '**/dist/**',
    '**/build/**',
    '**/__pycache__/**',
    '**/.venv/**',
    '**/venv/**',
    '**/*.min.js',
    '**/*.bundle.js',
]
```

---

## 7. Performance Targets

```
┌─────────────────────────────────────────────────────────────────┐
│                  PERFORMANCE TARGETS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INDEXING SPEED:                                                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Small project (<100 files): < 2 minutes                      │
│  • Medium project (100-500 files): < 10 minutes                 │
│  • Target: ~100ms per file average                              │
│                                                                  │
│  QUERY SPEED:                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • RAG query (top-5): < 500ms                                   │
│  • Embedding generation: < 200ms                                │
│  • Vector search: < 100ms                                        │
│                                                                  │
│  MEMORY USAGE:                                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • Indexing: < 500MB RAM                                        │
│  • Query: < 200MB RAM                                            │
│  • Idle: < 50MB RAM                                              │
│                                                                  │
│  STORAGE:                                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  • ~10KB per file indexed (chunks + embeddings)                 │
│  • 100 files ≈ 1MB storage                                      │
│  • 1000 files ≈ 10MB storage                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Testing & Validation

### 8.1 Unit Tests Required

```
□ Parser correctly extracts functions from TypeScript
□ Parser correctly extracts classes from Python
□ Parser correctly extracts methods from Dart
□ Chunker respects max token limit
□ Chunker groups small items correctly
□ Metadata includes accurate line numbers
□ Hash-based IDs are deterministic
□ Excluded patterns are respected
```

### 8.2 Integration Tests Required

```
□ Full index of sample project completes
□ Index persists to disk and reloads
□ Sync correctly detects changed files
□ Query returns relevant results
□ Performance meets targets
```

### 8.3 Sample Test Project

```
test-project/
├── src/
│   ├── auth/
│   │   ├── auth.service.ts    (5 functions)
│   │   └── auth.types.ts      (3 interfaces)
│   ├── users/
│   │   ├── user.model.ts      (1 class, 4 methods)
│   │   └── user.service.ts    (6 functions)
│   └── utils/
│       └── helpers.ts         (10 small functions)
├── lib/
│   └── api.py                 (3 classes)
└── app/
    └── main.dart              (2 classes, 8 methods)

Total: ~50 files, ~200 code units
Expected index time: < 1 minute
Expected chunks: ~150-200
```

---

## 9. Chunk ID Specification

### 9.1 ID Generation

Chunk IDs must be deterministic to enable sync detection.

**Algorithm:**
```python
import hashlib

def generate_chunk_id(
    file_path: str,      # Relative to workspace
    content: str,        # Full chunk content
    chunk_type: str,     # function, class, method, etc.
    line_start: int      # Starting line number
) -> str:
    """
    Generate deterministic 16-character chunk ID.
    
    Same inputs always produce same output.
    """
    data = f"{file_path}|{content}|{chunk_type}|{line_start}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]
```

### 9.2 ID Properties

- **Deterministic:** Same code = same ID
- **Unique:** Collision probability < 1 in 2^64
- **Compact:** 16 hex characters
- **Stable:** Only changes if content, type, or location changes


---

*Document Version: 1.0.0*