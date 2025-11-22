# Agent 10 — Plan Mode: Summary

## Data Model
- **Plan**: id, title, createdAt, updatedAt, status ('draft'|'active'|'completed'), steps[], acceptance[], version=2
- **PlanStep**: id, title, done, order, children?
- **AcceptanceCriterion**: id, text, refs? (path, startLine?, endLine?), done?

## Storage & Migration
- **State**: `InMemoryState`, `MementoState` (persisted via VS Code Memento)
- **Migration**: Legacy `{ id, title }` → `Plan v2` via `createPlan`

## Commands
- Plans:
  - `localpilot.plan.create` (payload: { id?, title?, steps? })
  - `localpilot.plan.update` (payload: { id, title?, status? })
  - `localpilot.plan.delete` (payload: { id })
- Steps:
  - `localpilot.plan.step.add` (payload: { planId, title?, index? })
  - `localpilot.plan.step.toggle` (payload: { planId, stepId })
  - `localpilot.plan.step.moveUp` (payload: { planId, stepId })
  - `localpilot.plan.step.moveDown` (payload: { planId, stepId })
  - `localpilot.plan.step.delete` (payload: { planId, stepId })
- Chat → Plan:
  - `localpilot.chat.transferToPlan` (payload: { id?, title?, prompt? })

## UI (TreeView)
- `Plans` view renders plans (root) and steps (children)
- Step items have Enter-bound toggle via `planStepToggle`
- Context menus for step ops and plan add

## Parser
- `parsePlanDraft(prompt)` → { steps[], acceptance[] }
- Recognizes numbered or dashed lists; acceptance section starting with `Acceptance:`
- File refs: `[file: path#start-end]`

## Tests
- `__tests__/plan.test.ts`: Plan CRUD + nested rendering + chat transfer payload
- `__tests__/state_migration.test.ts`: Legacy migration → Plan v2
- Existing: commands, views, chat

## Handoff to Agent 11 — Act Mode
- Provide: Plan schema, step states (done), acceptance criterion with file refs
- Expect: Use selected plan to drive dry-run/apply with Git safety; request approvals per step

## Notes
- Keyboard and context menus added in `package.json`
- Indexing commands still toggle `localpilot.indexing.running` and state
