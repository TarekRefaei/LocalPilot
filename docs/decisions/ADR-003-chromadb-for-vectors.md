# ADR-003: ChromaDB for Vector Storage

## Status
Accepted

## Context
Need a vector database for storing and querying code embeddings.

## Decision
Use ChromaDB as the vector database.

## Consequences
### Positive
- Simple setup (embedded, no separate server)
- Python native
- Sufficient performance for MVP
- Easy persistence

### Negative
- May need to switch for larger codebases
- Less feature-rich than alternatives

## Alternatives Considered
- Qdrant: Better performance but more complex setup
- FAISS: No metadata filtering, not persistent by default
- Pinecone: Cloud-based, violates privacy requirement