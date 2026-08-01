# Plan Repair Contract (P7)

## Core Rules

- Repair proposals are plan-level only
- No diffs are generated
- No execution state is modified
- Applying a repair always creates a NEW draft plan
- Original plans are immutable

## Allowed Repair Kinds

- change_action_type
- rename_symbol
- remove_task
- split_task
- reorder_tasks

## Forbidden Actions

- Auto-applying repairs
- Modifying workspace files
- Resuming execution
- Retrying semantic failures
