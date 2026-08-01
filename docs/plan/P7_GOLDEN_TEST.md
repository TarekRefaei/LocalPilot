# P7 Golden Test — Intelligent Plan Repair

## Scenario
Execution fails due to a semantic error (duplicate function).

## Expected

- Execution is terminal
- No retry or resume allowed
- No diff is generated
- Repair proposals are returned by the server
- Repair proposals are visible in the UI
- Applying a repair creates a NEW draft plan
- Original plan remains unchanged

## Regression Guard

If execution ever:
- Auto-applies a repair
- Modifies files after semantic failure
- Resumes execution

❌ Phase 7 is broken.
