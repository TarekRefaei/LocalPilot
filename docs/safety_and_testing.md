# Safety and Testing

This repo includes a VRAM/model configuration validator and quick safety tests to reduce runtime risks.

- VRAM validator runs at backend startup and fails fast if configured models exceed safe VRAM limits.
  - Override with FORCE_START=true to continue at your own risk.
  - Env vars read: MODEL_EMBEDDING, MODEL_CHAT, MODEL_PLANNING, MODEL_CODING.
- Act-mode E2E test simulates a git branch, change, and rollback.
- WebSocket contract presence test guards against accidental event name changes.
- Retrieval regression is covered by existing tests with precision@5 ≥ 0.80.

## How to run locally

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Unix/macOS: . .venv/bin/activate
pip install -r requirements-dev.txt || pip install pytest psutil GPUtil
pytest -q backend/tests/test_vram_validator.py
pytest -q backend/tests/e2e/test_act_mode_safety.py::test_act_mode_branch_and_rollback -q
pytest -q backend/tests/test_retrieval_integration.py::TestRetrievalFixtures::test_all_fixtures_precision -q
```

## CI

A PR workflow `.github/workflows/ci-safety.yml` runs the VRAM validator test, the Act-mode quick e2e, and a retrieval precision check. You can trigger it manually via "Run workflow".
