# ADR-002: LlamaIndex over LangChain

## Status
Accepted

## Context
Need a framework for RAG (Retrieval-Augmented Generation) operations.

## Decision
Use LlamaIndex instead of LangChain.

## Consequences
### Positive
- Better designed for indexing/retrieval use cases
- Simpler API for our needs
- Good Ollama integration
- Less abstraction overhead

### Negative
- Smaller community than LangChain
- Fewer tutorials available

## Alternatives Considered
- LangChain: More complex, designed for chains/agents
- Custom implementation: Too much work for MVP