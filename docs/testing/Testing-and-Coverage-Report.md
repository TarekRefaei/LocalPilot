# Testing and Coverage Report

This document describes how to run tests locally and what to expect from CI. It also summarizes coverage gates and report locations.

## Backends (FastAPI)

- Run tests with coverage:
  ```bash
  pytest -q --maxfail=1 --disable-warnings \
    --cov=app --cov-report=term-missing \
    --cov-report=xml:coverage.xml --cov-report=html:htmlcov
  ```
- Reports:
  - XML: `backend/coverage.xml`
  - HTML: `backend/htmlcov/index.html`
- CI:
  - Runs on Ubuntu and Windows
  - Artifacts: coverage XML + HTML uploaded per OS
  - Static analysis: ruff (lint) and mypy (type-check)
- Current gates:
  - Effective fail if tests fail (coverage gate can be added explicitly; current overall lines ~84%).

## Extension (VS Code + Jest)

- Install and test:
  ```bash
  npm ci --no-audit --no-fund
  npm run test -- --coverage
  ```
- Reports:
  - LCOV HTML: `extension/coverage/lcov-report/index.html`
- CI:
  - Runs on Ubuntu and Windows
  - Artifacts: coverage folder uploaded per OS
  - Static analysis: ESLint and `tsc --noEmit`
- Coverage thresholds (Jest):
  - Global: lines 80, branches 70, functions 80, statements 80

## Performance tests

- Excluded by default via pytest marks.
- Run manually:
  ```bash
  pytest -q -m performance
  ```
- Nightly perf CI runs on a schedule and uploads `backend/perf-output.txt` with durations summary.

## Notes

- Windows-specific issues around file locks are avoided in tests using a fake Chroma client.
- WebSocket reconnection tests in the extension are deterministic (stubbed backoff) and unskipped.
