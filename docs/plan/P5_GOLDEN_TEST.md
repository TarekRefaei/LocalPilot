# P5 Golden Test — Semantic Awareness

## Scenario
A plan attempts to add a function that already exists.

### Given
- `utils.py` contains `def subtract(a, b)`
- Plan task:
  - `actionType`: `create`
  - `description`: "Add subtract function"

### When
Execution starts

### Then
- ❌ Execution is blocked
- ❌ No diff is generated
- ❌ No file is modified
- ✅ Error shown:
  "Function 'subtract' already exists"

## This behavior is mandatory and must never regress.

## Invariants (Must Never Change)

- Semantic failures are terminal
- No resume after semantic failure
- No diff generation after semantic failure
- No partial execution after semantic failure
- User must regenerate or repair plan
