# PR E2E Quarantine Toggle v2

- Canonical workflow: `.github/workflows/pr-e2e-quarantine-v2.yml`
- Wrapper redirect: `.github/workflows/pr-e2e-quarantine.yml` (calls v2 via reusable workflow)

## What it does
- Toggles entries in `scripts/e2e/.flaky.json` under the `skip` array using `jq`.
- Push guard: only commits back when the PR originates from the same repo; otherwise uploads the modified `.flaky.json` as an artifact.
- Supports manual dispatch and PR label events.

## How to trigger
- Manual: Actions → "PR E2E Quarantine Toggle v2" → Run workflow with inputs `action` (add/remove) and `scenario` (e.g. `chat-plan-act`).
- PR labels: add or remove label `e2e:quarantine` to run with action add/remove respectively.

## Reusable workflow usage
You can invoke v2 from another workflow:

```yaml
jobs:
  toggle:
    uses: ./.github/workflows/pr-e2e-quarantine-v2.yml
    with:
      action: add # or remove
      scenario: chat-plan-act
```
