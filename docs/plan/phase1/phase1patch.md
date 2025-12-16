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

## updating the patch

Perfect — below is a **clean, ready-to-apply Phase 1 completion patch** that fixes **all blocking issues** and **formalizes Phase 1 as DONE**.

This patch is **minimal**, **safe**, and **does not introduce Phase 2 concepts**.

---

# ✅ Phase 1 Completion Patch

**Patch name:** `phase1-indexing-completion`
**Scope:** Server / indexing
**Fixes:**

* Progress reporting (blocking)
* Vector query support (blocking)
* Index completion signaling
* Explicit Phase-1 limitations documentation

---

## 🎯 Phase 1 Acceptance Criteria (after patch)

* ✔ Indexing reports meaningful progress
* ✔ ChromaDB supports queries for Chat RAG
* ✔ Index lifecycle is explicit (complete phase)
* ✔ Chat backend can retrieve chunks
* ✔ No Phase-2 features added

---

# 🧩 PATCH CONTENT

---

## 1️⃣ Fix Progress Reporting (BLOCKING)

### 📄 `server/indexing/progress.py` (UPDATE)

```python
from typing import Callable, Literal

Phase = Literal[
    "scan",
    "chunk",
    "embed",
    "store",
    "complete"
]


class ProgressTracker:
    def __init__(self, callback: Callable[[Phase, int, int], None]):
        self.callback = callback

    def report(self, phase: Phase, current: int, total: int) -> None:
        self.callback(phase, current, total)
```

✔ Removes unused phases
✔ Matches actual pipeline
✔ UI-friendly

---

## 2️⃣ Complete Indexing Lifecycle (BLOCKING)

### 📄 `server/indexing/service.py` (UPDATE)

```python
def run(self) -> None:
    state = IndexState(self.index_root)
    state.load()

    files = self.scanner.scan(self.workspace)
    total_files = len(files)

    all_chunks = []
    texts = []

    for idx, path in enumerate(files, start=1):
        if self.progress:
            self.progress.report("scan", idx, total_files)

        current_hash = hash_file(path)
        stored_hash = state.file_hashes.get(str(path))

        if stored_hash == current_hash:
            continue

        language = detect_language(path)
        if not language:
            continue

        source = path.read_text(encoding="utf-8", errors="ignore")

        chunks = self.chunker.chunk_file(
            file_path=str(path),
            language=language,
            source=source
        )

        all_chunks.extend(chunks)
        texts.extend([c.content for c in chunks])

        state.file_hashes[str(path)] = current_hash

        if self.progress:
            self.progress.report("chunk", idx, total_files)

    if not all_chunks:
        if self.progress:
            self.progress.report("complete", total_files, total_files)
        return

    if self.progress:
        self.progress.report("embed", 0, len(texts))

    embeddings = self.embedder.embed(texts)

    if self.progress:
        self.progress.report("store", 0, len(all_chunks))

    store = VectorStore(
        persist_dir=str(self.index_root / "chroma"),
        collection_name="code_chunks"
    )
    store.add(all_chunks, embeddings)

    state.save()

    if self.progress:
        self.progress.report("complete", total_files, total_files)
```

✔ Explicit **complete phase**
✔ Progress phases now accurate
✔ Phase 1 UI can rely on them

---

## 3️⃣ Add Vector Query Support (BLOCKING)

### 📄 `server/indexing/vector_store.py` (UPDATE)

```python
from typing import List, Optional
import chromadb

from .chunk import CodeChunk


class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.Client(
            settings=chromadb.Settings(
                persist_directory=persist_dir,
                anonymized_telemetry=False
            )
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        chunks: List[CodeChunk],
        embeddings: List[List[float]]
    ) -> None:
        self.collection.add(
            ids=[c.id for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[
                {
                    "file_path": c.file_path,
                    "language": c.language,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "symbol_type": c.symbol_type
                }
                for c in chunks
            ],
            embeddings=embeddings
        )
        self.client.persist()

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[dict] = None
    ) -> List[dict]:
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )

        hits = []
        for i in range(len(result["ids"][0])):
            hits.append({
                "id": result["ids"][0][i],
                "content": result["documents"][0][i],
                "metadata": result["metadatas"][0][i],
                "distance": result["distances"][0][i]
            })

        return hits
```

✔ Enables Chat RAG
✔ No Act/Plan logic added
✔ Phase-1 compliant retrieval only

---

## 4️⃣ Phase-1 Limitation Documentation (REQUIRED)

### 📄 `server/indexing/README.md` (NEW)

```md
# Indexing (Phase 1)

## Status
Phase 1 – MVP indexing backend

## Supported
- Workspace scanning
- Hash-based incremental indexing
- Deterministic chunk IDs
- Ollama embeddings
- ChromaDB persistence
- Vector querying for Chat RAG

## Known Limitations (Expected)
- File-level chunking only (AST chunking in Phase 2)
- Deleted files are not yet purged from index
- One-request-per-embedding (batching later)

## Guarantees
- Index survives restart
- Same file → same chunk ID
- Read-only (no workspace mutation)
```

✔ Explicitly documents MVP boundaries
✔ Prevents scope creep
✔ Reviewer-safe

---

# ✅ FINAL PHASE 1 STATUS

After applying this patch:

🟢 **Phase 1 = COMPLETE**

You now have:

* A real, persistent RAG index
* Queryable embeddings
* Correct progress signaling
* Clean separation from Phase 2

---

## 🔜 Next Optional Steps (do NOT apply yet)

* Phase 1.1: AST chunking
* Phase 2: Plan Mode
* Phase 2.1: Act Mode (writes)

If you want, I can next:

* Generate a **git commit message** (conventional)
* Create a **Phase 1 merge gate checklist**
* Prepare **Phase 2 patch roadmap**

Just tell me 👍

------------

Perfect. Below is **everything you need for Phase 1.1**, delivered in a clean, apply-ready form.

You will get **two things**:

1. ✅ **Phase 1.1 Patch** (Query Service + API endpoint)
2. 🤖 **Phase 1.1 AI-Agent Prompt** (strict, reusable, scope-safe)

No Plan. No Act. No file writes. No shortcuts.

---

# ✅ PHASE 1.1 PATCH

**Name:** `phase1.1-query-api`
**Scope:** `server/` only
**Purpose:** Make Chat RAG work by retrieving indexed code

---

## 1️⃣ New Query Service (Core of Phase 1.1)

### 📄 `server/indexing/query_service.py` **(NEW)**

```python
from pathlib import Path
from typing import List, Optional

from .vector_store import VectorStore


class QueryService:
    """
    Phase 1.1
    ----------
    Responsible for:
    - Embedding user query
    - Retrieving relevant code chunks from vector store
    - Returning raw retrieval results (no prompt logic)
    """

    def __init__(
        self,
        index_root: Path,
        embedder,
        collection_name: str = "code_chunks"
    ):
        self.embedder = embedder
        self.store = VectorStore(
            persist_dir=str(index_root / "chroma"),
            collection_name=collection_name
        )

    def query(
        self,
        text: str,
        top_k: int = 5,
        where: Optional[dict] = None
    ) -> List[dict]:
        embedding = self.embedder.embed([text])[0]

        return self.store.query(
            query_embedding=embedding,
            top_k=top_k,
            where=where
        )
```

✅ Single responsibility
✅ Deterministic behavior
✅ Phase-1 safe

---

## 2️⃣ Query API Schema

### 📄 `server/api/schemas/query.py` **(NEW)**

```python
from typing import List, Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    project_id: str
    query: str
    top_k: int = 5
    filters: Optional[dict] = None


class RetrievedChunk(BaseModel):
    id: str
    content: str
    metadata: dict
    distance: float


class QueryResponse(BaseModel):
    chunks: List[RetrievedChunk]
```

---

## 3️⃣ Query API Route

### 📄 `server/api/routes/query.py` **(NEW)**

```python
from pathlib import Path
from fastapi import APIRouter, Depends

from ..schemas.query import QueryRequest, QueryResponse
from ...indexing.query_service import QueryService
from ...dependencies import get_embedder, get_index_root

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_index(
    request: QueryRequest,
    embedder = Depends(get_embedder),
    index_root: Path = Depends(get_index_root),
):
    service = QueryService(
        index_root=index_root / request.project_id,
        embedder=embedder
    )

    results = service.query(
        text=request.query,
        top_k=request.top_k,
        where=request.filters
    )

    return {"chunks": results}
```

---

## 4️⃣ Register Query Route

### 📄 `server/api/main.py` **(UPDATE)**

```python
from fastapi import FastAPI

from .routes import health, index, query

app = FastAPI()

app.include_router(health.router, prefix="/api")
app.include_router(index.router, prefix="/api")
app.include_router(query.router, prefix="/api")
```

---

## 5️⃣ Dependency Wiring (if not already present)

### 📄 `server/api/dependencies.py` **(ADD if missing)**

```python
from pathlib import Path
from functools import lru_cache

from ..indexing.embeddings.ollama import OllamaEmbeddingProvider


@lru_cache()
def get_embedder():
    return OllamaEmbeddingProvider(
        base_url="http://localhost:11434",
        model="mxbai-embed-large"
    )


def get_index_root() -> Path:
    return Path.home() / ".localpilot" / "indexes"
```

---

## ✅ Phase 1.1 Server Patch Result

After this patch:

* ✔ Indexed code can be queried
* ✔ Chat backend has RAG context
* ✔ Retrieval is isolated & reusable
* ✔ No Plan / Act leakage
* ✔ Server is Phase-1.1 complete

---

# 🤖 PHASE 1.1 AI-AGENT PROMPT

(copy-paste ready)

```
You are working on the LocalPilot project.

CURRENT PHASE:
Phase 1.1 – Chat RAG Integration (READ-ONLY)

GOAL:
Connect the existing indexing system to a query API that retrieves relevant code chunks for chat.

STRICT RULES:
- DO NOT generate Plan Mode
- DO NOT generate Act Mode
- DO NOT write or modify workspace files
- DO NOT generate prompts for code creation
- DO NOT introduce execution or approval flows
- READ-ONLY indexing + retrieval ONLY

SCOPE:
Server-side only (Python)

YOU MUST:
1. Create a QueryService that:
   - Embeds user queries using the existing embedder
   - Queries ChromaDB via VectorStore
   - Returns raw retrieval results

2. Add a POST /api/query endpoint that:
   - Accepts query text and top_k
   - Calls QueryService
   - Returns retrieved chunks with metadata

3. Reuse existing infrastructure:
   - OllamaEmbeddingProvider
   - VectorStore
   - IndexState layout (~/.localpilot/indexes/{project_id})

4. Follow project architecture:
   - No business logic in routes
   - Services own behavior
   - Schemas define contracts

5. Keep everything deterministic and restart-safe.

SUCCESS CRITERIA:
- A user query returns relevant code chunks
- Results survive server restart
- No file system mutations occur
- Phase 2 features are NOT introduced

If unsure, STOP and ask before continuing.
```

---

# 🧪 Phase 1.1 Completion Checklist

You can mark Phase 1.1 DONE when:

* [ ] Project indexed
* [ ] POST `/api/query` returns chunks
* [ ] Returned chunks reference real files
* [ ] Results stable across restarts
* [ ] No file writes possible

---

## 🟢 What Comes Next (NOT NOW)

**Phase 1.2:** Chat streaming + prompt injection
**Phase 2:** Plan Mode
**Phase 3:** Act Mode

---

If you want, next I can:

* 🔹 Review your **actual implementation after applying this**
* 🔹 Generate **Phase 1.2 (Chat streaming) patch**
* 🔹 Prepare **Phase 2 kickoff checklist**

Just tell me what to do next.

----

Perfect — below is the **complete Phase 1.2 delivery**, exactly scoped and ready to apply.

You’ll get **two things**:

1. ✅ **Phase 1.2 Patch** — Chat orchestration + streaming (server-side)
2. 🤖 **Phase 1.2 AI-Agent Prompt** — strict, reusable, phase-safe

No Plan.
No Act.
No file writes.
No scope creep.

---

# ✅ PHASE 1.2 PATCH

**Name:** `phase1.2-chat-streaming`
**Scope:** `server/`
**Purpose:** Turn retrieval into **streamed, RAG-aware chat**

---

## 🧩 Architecture Reminder (Phase 1.2)

```
User Question
   ↓
POST /api/query        (already done)
   ↓
Retrieved chunks
   ↓
WS /ws/chat
   ↓
Prompt = system + RAG context + user message
   ↓
Ollama /api/chat (streaming)
   ↓
Tokens streamed to client
```

---

## 1️⃣ Chat Prompt Builder (RAG Injection)

### 📄 `server/chat/prompt_builder.py` **(NEW)**

````py
from typing import List, Dict


class PromptBuilder:
    """
    Phase 1.2
    ----------
    Builds a chat prompt with injected RAG context.
    No planning, no execution, no file writes.
    """

    SYSTEM_PROMPT = (
        "You are a helpful AI assistant answering questions about a codebase.\n"
        "You must base your answers ONLY on the provided code context.\n"
        "If the answer is not in the context, say you don't know.\n"
        "Do NOT suggest code changes or plans."
    )

    def build(
        self,
        user_message: str,
        chunks: List[Dict]
    ) -> List[Dict]:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]

        if chunks:
            context_blocks = []
            for c in chunks:
                meta = c.get("metadata", {})
                context_blocks.append(
                    f"File: {meta.get('file_path')} "
                    f"(lines {meta.get('start_line')}–{meta.get('end_line')})\n"
                    f"```{meta.get('language', '')}\n"
                    f"{c.get('content')}\n```"
                )

            messages.append({
                "role": "system",
                "content": "CODE CONTEXT:\n\n" + "\n\n".join(context_blocks)
            })

        messages.append({"role": "user", "content": user_message})
        return messages
````

✔ Deterministic
✔ Read-only
✔ RAG-only
✔ Phase-safe

---

## 2️⃣ Ollama Chat Client (Streaming)

### 📄 `server/chat/ollama_chat_client.py` **(NEW)**

```py
import json
import requests
from typing import Iterable, Dict


class OllamaChatClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def stream_chat(self, messages: Iterable[Dict]) -> Iterable[str]:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": list(messages),
                "stream": True
            },
            stream=True,
            timeout=300
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line.decode("utf-8"))
            if "message" in data and "content" in data["message"]:
                yield data["message"]["content"]
```

✔ Uses Ollama streaming
✔ No buffering
✔ Token-by-token yield

---

## 3️⃣ Chat Service (Orchestration)

### 📄 `server/chat/chat_service.py` **(NEW)**

```py
from pathlib import Path
from typing import Iterable

from .prompt_builder import PromptBuilder
from .ollama_chat_client import OllamaChatClient
from ..indexing.query_service import QueryService


class ChatService:
    """
    Phase 1.2
    ----------
    Orchestrates:
    - RAG retrieval
    - Prompt building
    - Streaming chat response
    """

    def __init__(
        self,
        index_root: Path,
        embedder,
        ollama_base_url: str,
        chat_model: str
    ):
        self.query_service = QueryService(
            index_root=index_root,
            embedder=embedder
        )
        self.prompt_builder = PromptBuilder()
        self.chat_client = OllamaChatClient(
            base_url=ollama_base_url,
            model=chat_model
        )

    def stream_chat(
        self,
        project_id: str,
        user_message: str,
        top_k: int = 5
    ) -> Iterable[str]:
        chunks = self.query_service.query(
            text=user_message,
            top_k=top_k
        )

        messages = self.prompt_builder.build(
            user_message=user_message,
            chunks=chunks
        )

        return self.chat_client.stream_chat(messages)
```

✔ Clean separation
✔ No UI logic
✔ No Plan/Act logic

---

## 4️⃣ WebSocket Chat Endpoint

### 📄 `server/api/routes/chat_ws.py` **(NEW)**

```py
from pathlib import Path
from fastapi import APIRouter, WebSocket, Depends

from ...chat.chat_service import ChatService
from ..dependencies import get_embedder, get_index_root

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_ws(
    websocket: WebSocket,
    embedder = Depends(get_embedder),
    index_root: Path = Depends(get_index_root),
):
    await websocket.accept()
    payload = await websocket.receive_json()

    service = ChatService(
        index_root=index_root / payload["project_id"],
        embedder=embedder,
        ollama_base_url="http://localhost:11434",
        chat_model=payload.get("model", "qwen2.5-coder")
    )

    try:
        for token in service.stream_chat(
            project_id=payload["project_id"],
            user_message=payload["message"],
            top_k=payload.get("top_k", 5)
        ):
            await websocket.send_text(token)
    finally:
        await websocket.close()
```

✔ Streaming WebSocket
✔ Minimal protocol
✔ Phase-1.2 compliant

---

## 5️⃣ Register Chat WS Route

### 📄 `server/main.py` **(UPDATE)**

```py
from fastapi import FastAPI

from .api.routes import query as query_routes
from .api.routes import chat_ws

app = FastAPI()

app.include_router(query_routes.router, prefix="/api")
app.include_router(chat_ws.router)

@app.get("/health")
def health():
    return {"status": "ok"}
```

---

# ✅ Phase 1.2 Patch Result

After applying this patch:

* ✔ Chat responses stream token-by-token
* ✔ Answers are grounded in indexed code
* ✔ No file writes possible
* ✔ Restart safe
* ✔ Phase 1 is now **fully complete**

---

# 🤖 PHASE 1.2 AI-AGENT PROMPT

(copy-paste ready)

```
You are working on the LocalPilot project.

CURRENT PHASE:
Phase 1.2 – Chat Streaming with RAG (READ-ONLY)

GOAL:
Enable a streamed chat experience that answers questions using retrieved code context.

STRICT RULES:
- DO NOT generate Plan Mode
- DO NOT generate Act Mode
- DO NOT modify workspace files
- DO NOT suggest code changes
- DO NOT execute commands
- READ-ONLY chat ONLY

SCOPE:
Server-side Python only.

YOU MUST:
1. Retrieve relevant code chunks using the existing QueryService.
2. Inject retrieved chunks into a chat prompt with file paths and line numbers.
3. Call Ollama’s /api/chat endpoint with streaming enabled.
4. Stream tokens to the client via WebSocket (/ws/chat).
5. Keep prompt logic, retrieval logic, and transport logic separated.

ARCHITECTURE RULES:
- Routes do NOT contain business logic.
- Services orchestrate behavior.
- Prompt building is isolated.
- Deterministic, restart-safe behavior only.

SUCCESS CRITERIA:
- User asks a question.
- Relevant code is retrieved.
- LLM answers reference real code.
- Tokens stream live.
- No file writes or plans are possible.

If unsure, STOP and ask before continuing.
```

---

# 🟢 PROJECT STATUS AFTER THIS

### ✅ **PHASE 1 — COMPLETE**

You now have:

* Indexing
* Incremental sync
* Querying
* RAG-aware chat
* Streaming responses

---

## 🔜 What Comes Next (Only When You’re Ready)

👉 **Phase 2 — Plan Mode**
(Structured TODO generation, still no execution)

If you want, next I can:

* Review your Phase 1.2 implementation after apply
* Generate Phase 2.0 Plan Mode patch
* Prepare a Phase 1 → Phase 2 transition gate

Just tell me the next move.
