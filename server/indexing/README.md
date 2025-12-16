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
