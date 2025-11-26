# Nightly Workflows and E2E Summary

This repository runs nightly validation across Windows and Ubuntu to catch regressions early.

## Workflows

- Nightly E2E (Chat-Plan-Act)
  - File: .github/workflows/nightly-e2e.yml
  - Runs Python E2E harness on Windows and Ubuntu
  - Artifacts: artifacts/e2e/** (backend.log, e2e-result.json, ws-trace.jsonl, tree.txt)
  - Job summary includes the JSON result and parsed timings

- Nightly Extension Integration (with Backend)
  - File: .github/workflows/nightly-extension-e2e.yml
  - Starts backend, runs VS Code extension integration tests on Windows and Ubuntu
  - Artifacts: backend/backend.log, extension/.vscode-test/**

## On-demand PR E2E

- File: .github/workflows/pr-e2e.yml
- Trigger conditions:
  - Label the PR with `e2e:run`, or use the "Run workflow" button (workflow_dispatch)
- Runs the same Python E2E harness on both OS runners and uploads artifacts
- Job summary includes `e2e-result.json` and parsed timings

## Flake Quarantine & Telemetry

- Flake quarantine file: scripts/e2e/.flaky.json (list of scenarios to skip)
- E2E result JSON (artifacts/e2e/e2e-result.json) includes:
  - ok, scenario, retry, flaky, error, error_type (on failure)
  - timings_ms for key steps (health, indexing broadcast, chat echo, apply times)

## Manual dispatch

- From the Actions tab, select either workflow and click "Run workflow"
- Default branch: main

## Troubleshooting

- Backend did not become healthy: check artifacts/e2e/backend.log
- ACT_SAFETY_BLOCKED: working tree had uncommitted changes; harness now pre-commits before apply
- Windows file lock on Chroma DB: harness uses a temp per-run vector DB path to avoid locks
