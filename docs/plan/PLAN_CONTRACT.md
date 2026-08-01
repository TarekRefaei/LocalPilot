# LocalPilot — Plan Contract (P0)

## Definition
A Plan is a deterministic, ordered description of file-level changes
that MAY be executed by Act Mode after approval.

## Guarantees
- Plans are JSON-structured and schema-validated.
- Tasks are atomic and target exactly one file.
- Execution order is defined explicitly by `orderIndex`.
- No plan can be executed without approval.

## Status Semantics
- `draft`:
  - Plan may be invalid.
  - Plan may be regenerated or repaired.
- `approved`:
  - Plan is trusted.
  - Plan MUST NOT change.
  - Plan may be executed by Act Mode.

## Non-Goals (by design)
- Workspace awareness (introduced in P2)
- Automatic plan repair (introduced in P3)
- Semantic reasoning (introduced in P5)

## Stability Rule
This contract MUST NOT be broken.
Future versions may extend the Plan,
but MUST NOT invalidate this contract.
