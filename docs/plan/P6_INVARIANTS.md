# Phase 6 Invariants — Execution Correctness

These invariants must never regress.

## Semantic Failures
- Semantic failures are terminal
- No resume after semantic failure
- No retry after semantic failure
- No diff generation after semantic failure
- User must regenerate or repair the plan

## Execution Proof
- Every execution must carry a proof
- Proof must match plan_id
- Task count must match plan task count
- Task order must match order_index

## Diff Safety
- One task modifies exactly one file
- No path escape
- No forbidden files
- Idempotent diffs are rejected

## Anchors
- Unverified anchors block execution
- Verified anchors guarantee insertion location

## Replay Safety
- No task may mutate the workspace twice
- Failed executions cannot be resumed
