# ADR 0001: Adopt Native VS Code Side Panel Views and Chat Participant

- Status: Accepted
- Date: January 2025

## Context
Initial UI concept used a React webview. We revised to use the native VS Code Views API and Chat participant to reduce complexity, align with platform conventions, and improve testability.

## Decision
- Use Views API for side panel container `localpilot.views` with views: Plans, Act, Indexing, Status.
- Use Chat API (VS Code ≥ 1.88) to register participant `localpilot` with streaming responses and commands (e.g., Transfer to Plan).
- Remove webview UI from scope for MVP.
- Testing: Jest for TS logic; Mocha + @vscode/test-electron for Views/Chat integration.

## Consequences
- Pros: Native UX, lower maintenance, better accessibility and performance, simpler security posture.
- Cons: Less fine-grained custom styling vs webview; some features depend on VS Code version cadence.

## Alternatives Considered
- Continue with React webview (rejected due to scope and complexity).

## Links
- Technical_Architecture.md (updated diagrams and responsibilities)
- Testing_Strategy.md (Views/Chat testing)
- UI_Design_System.md (strategy update note)
