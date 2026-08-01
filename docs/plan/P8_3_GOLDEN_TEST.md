# P8.3 Golden Tests — Structural Enforcement Gate

## Purpose
Ensure that structurally invalid plans can NEVER enter execution.

Structural validation is authoritative and blocks execution
*before* semantic analysis, LLM invocation, or file mutation.

---

## Scenario 1 — Dependency Cycle Blocks Execution

### Given
A plan with a dependency cycle:
- t1 depends on t2
- t2 depends on t1

### When
Execution is started

### Then
- ❌ Execution is rejected
- ❌ No ExecutionState is created
- ❌ No semantic analysis runs
- ❌ No LLM calls occur
- ✅ Error includes `dependency_cycle`

---

## Scenario 2 — Duplicate orderIndex Blocks Execution

### Given
Two tasks share the same orderIndex

### When
Execution is started

### Then
- ❌ Execution is rejected
- ✅ Error includes `duplicate_order_index`

---

## Scenario 3 — Non-contiguous orderIndex Blocks Execution

### Given
Tasks have orderIndex [0, 2]

### Then
- ❌ Execution is rejected
- ✅ Error includes `non_contiguous_order_index`

---

## Scenario 4 — Self-Dependency Blocks Execution

### Given
A task depends on itself

### Then
- ❌ Execution is rejected
- ✅ Error includes `self_dependency`

---

## Scenario 5 — Unknown Dependency Blocks Execution

### Given
A task depends on a non-existent task id

### Then
- ❌ Execution is rejected
- ✅ Error includes `unknown_dependency`

---

## Invariants (Must Never Change)

- Structural validation happens **before**:
  - semantic validation
  - execution proof
  - task scheduling
- Execution MUST NOT partially initialize
- Structural errors are **terminal**
- User must regenerate or repair the plan
