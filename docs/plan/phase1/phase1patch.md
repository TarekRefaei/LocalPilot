Excellent.
We now move into **Phase 1: Indexing Engine patch proposals** — the **backbone of LocalPilot**.

Below is **Phase 1, Tasks 1.1 → 1.4** as **patch proposals**, following **exactly** the agent constitution you approved:

* patch-driven
* deterministic
* no shortcuts
* no AI generation logic yet (only plumbing + deterministic algorithms)
* future-proof for v1.1 / v1.2

> ⚠️ **Important scope note**
> I am intentionally splitting Phase 1 into **controlled batches**.
> This message covers **Index Discovery → Parsing → Chunking (no embeddings yet)**.
> This keeps risk low and patches reviewable.

---

# 🧩 PHASE 1 — PATCH PROPOSALS (PART 1)

## Indexing Engine: Scan → Parse → Chunk

---

## 🧱 TASK 1.1 — Workspace Scanner

### 🎯 Objective

Deterministically discover indexable files while respecting user intent.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.1",
  "title": "Implement workspace file scanner",
  "files": [
    { "path": "server/indexing/scanner.py", "action": "create" },
    { "path": "server/indexing/__init__.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium",
  "rollback": "safe-delete"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/scanner.py
+from pathlib import Path
+from typing import List
+
+EXCLUDED_DIRS = {
+    ".git",
+    "node_modules",
+    "dist",
+    "build",
+    ".venv",
+    "__pycache__",
+    ".localpilot"
+}
+
+SUPPORTED_EXTENSIONS = {
+    ".ts", ".js", ".py", ".json", ".md", ".dart"
+}
+
+
+class WorkspaceScanner:
+    def scan(self, root: Path) -> List[Path]:
+        files: List[Path] = []
+
+        for path in root.rglob("*"):
+            if not path.is_file():
+                continue
+
+            if any(part in EXCLUDED_DIRS for part in path.parts):
+                continue
+
+            if path.suffix not in SUPPORTED_EXTENSIONS:
+                continue
+
+            files.append(path)
+
+        return sorted(files)
```

---

### ✅ Verification Checklist

* [ ] Skips excluded directories
* [ ] Deterministic ordering
* [ ] No file reads yet
* [ ] No gitignore parsing yet (v1.1)

---

## 🧱 TASK 1.2 — Language Detection

### 🎯 Objective

Determine programming language **deterministically** from file extension.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.2",
  "title": "Add language detection utility",
  "files": [
    { "path": "server/indexing/language.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/language.py
+from pathlib import Path
+
+
+EXTENSION_LANGUAGE_MAP = {
+    ".ts": "typescript",
+    ".js": "javascript",
+    ".py": "python",
+    ".dart": "dart",
+    ".json": "json",
+    ".md": "markdown"
+}
+
+
+def detect_language(path: Path) -> str | None:
+    return EXTENSION_LANGUAGE_MAP.get(path.suffix)
```

---

### ✅ Verification Checklist

* [ ] Deterministic mapping
* [ ] Returns None for unsupported files
* [ ] No heuristics

---

## 🧱 TASK 1.3 — AST Parsing Abstraction (Tree-sitter Ready)

### 🎯 Objective

Create a **parser abstraction**, without binding to Tree-sitter yet.

This keeps Phase 1 safe and testable.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.3",
  "title": "Introduce parser abstraction and base parser",
  "files": [
    { "path": "server/indexing/parsers/base.py", "action": "create" },
    { "path": "server/indexing/parsers/__init__.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/parsers/base.py
+from pathlib import Path
+from typing import Any
+
+
+class ParseResult:
+    def __init__(self, ast: Any, source: str):
+        self.ast = ast
+        self.source = source
+
+
+class BaseParser:
+    language: str
+
+    def parse(self, path: Path) -> ParseResult:
+        raise NotImplementedError("Parser must implement parse()")
```

---

### ✅ Verification Checklist

* [ ] No Tree-sitter dependency yet
* [ ] Abstract contract only
* [ ] Safe to extend later

---

## 🧱 TASK 1.4 — Semantic Chunk Model

### 🎯 Objective

Define **what a chunk is** — before generating embeddings.

This is critical for RAG quality.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.4",
  "title": "Define semantic chunk data model",
  "files": [
    { "path": "server/indexing/chunk.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

````diff
+++ server/indexing/chunk.py
+from dataclasses import dataclass
+
+
+@dataclass(frozen=True)
+class CodeChunk:
+    id: str
+    file_path: str
+    language: str
+    start_line: int
+    end_line: int
+    content: str
+    symbol_type: str  # function, class, module, block
+```

---

### ✅ Verification Checklist
- [ ] Immutable chunk
- [ ] Line-accurate metadata
- [ ] No embeddings yet
- [ ] No vector DB coupling

---

## 🔒 Phase 1 (Part 1) Status

At this point, you have:

✅ Deterministic workspace scanning  
✅ Explicit language detection  
✅ Parser abstraction (no premature complexity)  
✅ Canonical chunk model  

🚫 Still intentionally missing:
- embeddings
- ChromaDB
- Ollama calls
- RAG queries

This is **exactly correct**.

---

## 🔜 Next Step (Phase 1 – Part 2)

Next batch will cover:

- **Task 1.5** — Semantic chunking logic (AST → chunks)
- **Task 1.6** — Hash tracking (sync foundation)
- **Task 1.7** — Index state persistence
- **Task 1.8** — Progress reporting

Say when ready:

👉 **“Continue Phase 1 patch proposals (Part 2)”**

You’re building this the *right* way.
````

Perfect.
This is **Phase 1 – Part 2**, completing the **Indexing Engine core (still no embeddings yet)**.

Scope of this message:

* Semantic chunking logic (AST → chunks)
* Hash tracking (for smart sync)
* Index state persistence
* Progress reporting (server-side)

Still **NO Ollama**, **NO ChromaDB**, **NO RAG queries**.
We are finishing the *deterministic backbone* first.

---

# 🧩 PHASE 1 — PATCH PROPOSALS (PART 2)

## Chunking → Sync → Persistence → Progress

---

## 🧱 TASK 1.5 — Semantic Chunker (AST → CodeChunks)

### 🎯 Objective

Convert parsed source into **stable, semantically meaningful chunks**.

> ⚠️ Important:
> This implementation is **language-agnostic fallback chunking**.
> Tree-sitter–aware chunking will *extend* this in v1.1, not replace it.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.5",
  "title": "Implement semantic chunker",
  "files": [
    { "path": "server/indexing/chunker.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium",
  "rollback": "safe-delete"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/chunker.py
+import hashlib
+from typing import List
+
+from .chunk import CodeChunk
+
+
+class SemanticChunker:
+    def chunk_file(
+        self,
+        file_path: str,
+        language: str,
+        source: str
+    ) -> List[CodeChunk]:
+        """
+        Fallback semantic chunking:
+        - Entire file = single chunk
+        - Used until AST-aware chunkers are plugged in
+        """
+
+        lines = source.splitlines()
+        content = source.strip()
+
+        chunk_id = self._stable_id(file_path, content)
+
+        return [
+            CodeChunk(
+                id=chunk_id,
+                file_path=file_path,
+                language=language,
+                start_line=1,
+                end_line=len(lines),
+                content=content,
+                symbol_type="file"
+            )
+        ]
+
+    def _stable_id(self, file_path: str, content: str) -> str:
+        h = hashlib.sha256()
+        h.update(file_path.encode("utf-8"))
+        h.update(content.encode("utf-8"))
+        return h.hexdigest()
```

---

### ✅ Verification Checklist

* [ ] One chunk per file (for now)
* [ ] Stable chunk IDs
* [ ] Line numbers correct
* [ ] No AST dependency yet

---

## 🧱 TASK 1.6 — File Hash Tracker (Smart Sync Foundation)

### 🎯 Objective

Track file changes deterministically for **smart re-indexing**.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.6",
  "title": "Add file hash tracker",
  "files": [
    { "path": "server/indexing/hash_tracker.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/hash_tracker.py
+import hashlib
+from pathlib import Path
+
+
+def hash_file(path: Path) -> str:
+    h = hashlib.sha256()
+    with open(path, "rb") as f:
+        for chunk in iter(lambda: f.read(8192), b""):
+            h.update(chunk)
+    return h.hexdigest()
```

---

### ✅ Verification Checklist

* [ ] Deterministic hash
* [ ] Handles large files
* [ ] No global state

---

## 🧱 TASK 1.7 — Index State Persistence

### 🎯 Objective

Persist index metadata to disk so indexing survives restarts.

📍 Location (locked earlier):

```
~/.localpilot/indexes/{projectId}/state.json
```

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.7",
  "title": "Persist index state to disk",
  "files": [
    { "path": "server/indexing/state.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/state.py
+import json
+from pathlib import Path
+from typing import Dict
+
+
+class IndexState:
+    def __init__(self, root: Path):
+        self.path = root / "state.json"
+        self.file_hashes: Dict[str, str] = {}
+
+    def load(self) -> None:
+        if not self.path.exists():
+            return
+        with open(self.path, "r", encoding="utf-8") as f:
+            data = json.load(f)
+            self.file_hashes = data.get("file_hashes", {})
+
+    def save(self) -> None:
+        self.path.parent.mkdir(parents=True, exist_ok=True)
+        with open(self.path, "w", encoding="utf-8") as f:
+            json.dump(
+                {"file_hashes": self.file_hashes},
+                f,
+                indent=2
+            )
```

---

### ✅ Verification Checklist

* [ ] Creates directory if missing
* [ ] JSON readable
* [ ] Safe when state absent

---

## 🧱 TASK 1.8 — Indexing Progress Reporter

### 🎯 Objective

Expose **structured progress events** to the extension UI.

> No WebSockets yet — this is an internal abstraction.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.8",
  "title": "Add indexing progress tracker",
  "files": [
    { "path": "server/indexing/progress.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "low"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/progress.py
+from typing import Callable, Literal
+
+Phase = Literal["scan", "parse", "chunk", "hash", "complete"]
+
+
+class ProgressTracker:
+    def __init__(self, callback: Callable[[Phase, int, int], None]):
+        self.callback = callback
+
+    def report(self, phase: Phase, current: int, total: int) -> None:
+        self.callback(phase, current, total)
```

---

### ✅ Verification Checklist

* [ ] No side effects
* [ ] Phase-limited enum
* [ ] UI-agnostic

---

## 🔒 Phase 1 (Parts 1 + 2) — CURRENT STATE

You now have:

✅ Workspace scanning
✅ Language detection
✅ Parser abstraction
✅ Canonical chunk model
✅ Deterministic chunking
✅ Hash-based sync foundation
✅ Persistent index state
✅ Progress reporting abstraction

🚫 Still NOT present (by design):

* embeddings
* Ollama calls
* vector database
* RAG querying
* summary generation

This is **exactly where you want to be** before introducing ML.

---

Excellent.
This is **Phase 1 – Part 3**, where we **carefully introduce embeddings and vector storage**, while still keeping everything **deterministic, auditable, and MVP-safe**.

Scope of this message:

* Embedding abstraction (port)
* Ollama embedding implementation
* ChromaDB vector storage
* Index orchestration service (the glue)

This **completes Phase 1**.

---

# 🧩 PHASE 1 — PATCH PROPOSALS (PART 3)

## Embeddings → Vector Store → Index Orchestration

---

## 🧱 TASK 1.9 — Embedding Provider Abstraction

### 🎯 Objective

Define a **clean embedding contract** so the rest of the system does not depend on Ollama directly.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.9",
  "title": "Define embedding provider interface",
  "files": [
    { "path": "server/indexing/embeddings/base.py", "action": "create" },
    { "path": "server/indexing/embeddings/__init__.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "medium"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/embeddings/base.py
+from abc import ABC, abstractmethod
+from typing import List
+
+
+class EmbeddingProvider(ABC):
+    @abstractmethod
+    def embed(self, texts: List[str]) -> List[List[float]]:
+        """
+        Generate embeddings for a list of texts.
+        Must be deterministic for identical inputs.
+        """
+        raise NotImplementedError
```

---

### ✅ Verification Checklist

* [ ] No Ollama import
* [ ] Batch-based API
* [ ] Deterministic contract

---

## 🧱 TASK 1.10 — Ollama Embedding Implementation

### 🎯 Objective

Implement embeddings using **Ollama**, without leaking Ollama details upward.

📌 Model choice stays configurable later (v1.1).

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.10",
  "title": "Implement Ollama embedding provider",
  "files": [
    { "path": "server/indexing/embeddings/ollama.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "high"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/embeddings/ollama.py
+import requests
+from typing import List
+
+from .base import EmbeddingProvider
+
+
+class OllamaEmbeddingProvider(EmbeddingProvider):
+    def __init__(self, base_url: str, model: str):
+        self.base_url = base_url.rstrip("/")
+        self.model = model
+
+    def embed(self, texts: List[str]) -> List[List[float]]:
+        embeddings: List[List[float]] = []
+
+        for text in texts:
+            res = requests.post(
+                f"{self.base_url}/api/embeddings",
+                json={
+                    "model": self.model,
+                    "prompt": text
+                },
+                timeout=60
+            )
+            res.raise_for_status()
+            data = res.json()
+            embeddings.append(data["embedding"])
+
+        return embeddings
```

---

### ✅ Verification Checklist

* [ ] Uses `/api/embeddings`
* [ ] No streaming
* [ ] One embedding per chunk
* [ ] Raises on failure (no silent errors)

---

## 🧱 TASK 1.11 — Vector Store (ChromaDB)

### 🎯 Objective

Persist embeddings + metadata in a **queryable vector database**.

📌 Storage location:

```
~/.localpilot/indexes/{projectId}/chroma/
```

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.11",
  "title": "Add ChromaDB vector store",
  "files": [
    { "path": "server/indexing/vector_store.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "high"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/vector_store.py
+from typing import List
+
+import chromadb
+
+from .chunk import CodeChunk
+
+
+class VectorStore:
+    def __init__(self, persist_dir: str, collection_name: str):
+        self.client = chromadb.Client(
+            settings=chromadb.Settings(
+                persist_directory=persist_dir,
+                anonymized_telemetry=False
+            )
+        )
+        self.collection = self.client.get_or_create_collection(
+            name=collection_name
+        )
+
+    def add(
+        self,
+        chunks: List[CodeChunk],
+        embeddings: List[List[float]]
+    ) -> None:
+        self.collection.add(
+            ids=[c.id for c in chunks],
+            documents=[c.content for c in chunks],
+            metadatas=[
+                {
+                    "file_path": c.file_path,
+                    "language": c.language,
+                    "start_line": c.start_line,
+                    "end_line": c.end_line,
+                    "symbol_type": c.symbol_type
+                }
+                for c in chunks
+            ],
+            embeddings=embeddings
+        )
+        self.client.persist()
```

---

### ✅ Verification Checklist

* [ ] One collection per project
* [ ] Metadata stored correctly
* [ ] Persist called
* [ ] No querying yet

---

## 🧱 TASK 1.12 — Index Orchestration Service

### 🎯 Objective

Create the **single entry point** that runs the full indexing pipeline.

This is the heart of Phase 1.

---

### 🧩 Structured Patch Proposal

```json
{
  "taskId": "1.12",
  "title": "Implement indexing orchestration service",
  "files": [
    { "path": "server/indexing/service.py", "action": "create" }
  ],
  "requiresApproval": true,
  "riskLevel": "high"
}
```

---

### 🧾 Unified Diff

```diff
+++ server/indexing/service.py
+from pathlib import Path
+
+from .scanner import WorkspaceScanner
+from .language import detect_language
+from .chunker import SemanticChunker
+from .hash_tracker import hash_file
+from .state import IndexState
+from .vector_store import VectorStore
+
+
+class IndexingService:
+    def __init__(
+        self,
+        workspace: Path,
+        index_root: Path,
+        embedder,
+        progress=None
+    ):
+        self.workspace = workspace
+        self.index_root = index_root
+        self.embedder = embedder
+        self.progress = progress
+
+        self.scanner = WorkspaceScanner()
+        self.chunker = SemanticChunker()
+
+    def run(self) -> None:
+        state = IndexState(self.index_root)
+        state.load()
+
+        files = self.scanner.scan(self.workspace)
+
+        all_chunks = []
+        texts = []
+
+        for idx, path in enumerate(files, start=1):
+            if self.progress:
+                self.progress.report("scan", idx, len(files))
+
+            current_hash = hash_file(path)
+            stored_hash = state.file_hashes.get(str(path))
+
+            if stored_hash == current_hash:
+                continue
+
+            language = detect_language(path)
+            if not language:
+                continue
+
+            source = path.read_text(encoding="utf-8", errors="ignore")
+
+            chunks = self.chunker.chunk_file(
+                file_path=str(path),
+                language=language,
+                source=source
+            )
+
+            all_chunks.extend(chunks)
+            texts.extend([c.content for c in chunks])
+
+            state.file_hashes[str(path)] = current_hash
+
+        if not all_chunks:
+            return
+
+        embeddings = self.embedder.embed(texts)
+
+        store = VectorStore(
+            persist_dir=str(self.index_root / "chroma"),
+            collection_name="code_chunks"
+        )
+        store.add(all_chunks, embeddings)
+
+        state.save()
```

---

### ✅ Verification Checklist

* [ ] End-to-end pipeline runs
* [ ] Hash-based skipping works
* [ ] Index persists across restarts
* [ ] No querying
* [ ] No UI logic

---

## 🎉 PHASE 1 — COMPLETE

You now have:

✅ Deterministic indexing pipeline
✅ Semantic chunking (safe fallback)
✅ Hash-based smart sync
✅ Persistent index state
✅ Ollama embeddings
✅ ChromaDB vector storage

All aligned with:

* privacy-first design
* MVP security constraints
* future v1.1 / v1.2 expansion

---
