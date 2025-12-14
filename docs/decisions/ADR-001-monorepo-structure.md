# ADR-001: Monorepo Structure

## Status
Accepted

## Context
We need to decide how to organize the codebase containing:
- VS Code extension (TypeScript)
- Python RAG server
- Shared documentation

## Decision
Use a monorepo structure with both packages in one repository.

## Consequences
### Positive
- Single source of truth
- Easier to keep extension and server in sync
- Unified versioning
- Simpler for solo developer

### Negative
- Larger repository size
- Need to manage two package managers (pnpm + uv)

## Alternatives Considered
- Multi-repo: Rejected due to coordination overhead
- Workspace package (npm/yarn): Not suitable for Python