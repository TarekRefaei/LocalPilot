# P3 Golden Integration Test (Manual)

## Golden Path (Success)

1. Generate a plan that contains a blocking workspace warning
   - Example: a task with `actionType: "create"` targeting a file that already exists

2. Open Plan view

3. Validate
   - Expected: warning list includes at least one blocking warning
   - Expected: the ⚙ button is in **Fix** mode (enabled)

4. Click ⚙ (Fix)
   - Expected: a unified diff preview opens
   - Expected: plan is not auto-approved

5. Validate again
   - Expected: no blocking warnings

6. Approve
   - Expected: plan becomes approved

7. Act
   - Expected: ⚙ button is now in **Act** mode (enabled)


## Failure Path (Repair Loop Prevention)

1. Generate a plan with a blocking warning

2. Click ⚙ (Fix) and force the repair to fail
   - Example: backend returns invalid plan or plan that still contains blocking issues

3. Expected:
   - Error is shown
   - Plan is not replaced
   - Repair attempt count increments

4. Repeat step 2

5. Expected:
   - After 2 failed attempts, further repair attempts are blocked
   - UI suggests regeneration
