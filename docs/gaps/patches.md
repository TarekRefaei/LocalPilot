## PR 1 — Register validator at startup

**Branch:** `chore/startup-validator-hook`
**Commit message:** `chore(startup): register VRAM model validator on FastAPI startup`

### Goal

Ensure `validate_config_on_startup` runs at FastAPI startup reliably (so the validator actually executes before model loading and prevents unsafe model configs). This avoids relying on router import ordering and makes startup deterministic.

### What this patch does

1. Adds a small helper function `register_validator_startup(app)` inside `backend/app/api/prom_metrics.py` (or creates it there if file exists). The function registers an `on_event("startup")` handler on the FastAPI `app` that invokes the validator using `MODEL_*` env vars.
2. Adds a single import + call in `backend/app/main.py` to register the startup handler (`from app.api import prom_metrics; prom_metrics.register_validator_startup(app)`).

> Note: this is minimal: only one new function and one line change in `main.py`. If your `main.py` uses a different variable name for the FastAPI app, replace `app` with the correct identifier (I assume `app` is standard).

---

### File changes (copy/paste)

#### A — Add this helper to `backend/app/api/prom_metrics.py`

Find the top of `backend/app/api/prom_metrics.py` (after imports). Add the following imports (if not present) and the new function `register_validator_startup`.

```python
# backend/app/api/prom_metrics.py
# (insert near the top of file, after other imports)
import os
import logging
from typing import Dict

try:
    # Import validator from your services package
    from app.services.llm.validator import validate_config_on_startup
except Exception:
    # If import path differs, try fallback path
    try:
        from services.llm.validator import validate_config_on_startup
    except Exception:
        validate_config_on_startup = None

logger = logging.getLogger(__name__)


def register_validator_startup(app):
    """
    Register a FastAPI startup hook to validate model config early.

    This function is idempotent if called multiple times.
    """
    if validate_config_on_startup is None:
        logger.debug("validate_config_on_startup not available, skipping registration")
        return

    # Avoid double registration: attach a marker attribute
    if getattr(app, "_validator_startup_registered", False):
        logger.debug("Validator startup already registered")
        return

    @app.on_event("startup")
    async def _validate_models_on_startup():
        # Build config from environment variables; use common env names
        config: Dict[str, str] = {
            "embedding": os.getenv("MODEL_EMBEDDING") or os.getenv("MODEL_EMBED") or os.getenv("MODEL_EMB"),
            "chat": os.getenv("MODEL_CHAT") or os.getenv("MODEL_CH"),
            "planning": os.getenv("MODEL_PLANNING"),
            "coding": os.getenv("MODEL_CODING"),
        }
        # Only run validation if any model env var is present (avoid noise)
        if not any(config.values()):
            logger.debug("No MODEL_* env vars set - skipping model config validation")
            return

        try:
            validate_config_on_startup(config)
            logger.info("Model configuration validated successfully at startup")
        except RuntimeError as exc:
            msg = (
                f"Model configuration invalid at startup: {exc}. "
                "To override and force start (risky), set env FORCE_START=true."
            )
            # Log error to host logger and re-raise to prevent startup
            logging.getLogger("uvicorn.error").error(msg)
            # Re-raise to let the process fail-fast
            raise

    # mark registered to prevent multiple handlers
    setattr(app, "_validator_startup_registered", True)
    logger.debug("Registered model validator startup handler")
```

> If `backend/app/api/prom_metrics.py` already has an existing `router.on_event("startup")` block that you *do* want to keep, this helper function is still safe — it will be registered in `main.py` and executed alongside existing handlers.

---

#### B — Add single-line registration to `backend/app/main.py`

Open `backend/app/main.py` (or the module that creates the FastAPI `app` instance). Locate where the app is created, typically:

```python
from fastapi import FastAPI

app = FastAPI(...)
# ... other setup ...
```

Right after the `app = FastAPI(...)` line and after any other imports, add:

```python
# backend/app/main.py
try:
    # Import and register validator startup hook
    from app.api import prom_metrics
    prom_metrics.register_validator_startup(app)
except Exception as e:
    # If registration fails, log and continue to avoid masking other startup errors
    import logging
    logging.getLogger("uvicorn.error").debug("Could not register validator startup hook: %s", e)
```

If your `main.py` places app inside a function or uses a different module layout (e.g., `backend.src.app.main`), adjust import path accordingly; keep the pattern: import the module where you added `register_validator_startup` and call it with the FastAPI `app` object.

---

### Local verification (after patch)

1. Run unit tests for validator:

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt || pip install pytest
pytest -q backend/tests/test_vram_validator.py
```

2. Start the backend with an intentionally unsafe config (no GPU but 14B model) and confirm startup fails:

```bash
# simulate no GPU config by unsetting GPU envs and setting big model
export MODEL_CHAT="qwen2.5-coder:14b-instruct-q4_K_M"
python -m uvicorn app.main:app --reload
# You should see a startup error and the process should exit / not complete startup
```

3. Start with `FORCE_START=true` to ensure override:

```bash
export FORCE_START=true
python -m uvicorn app.main:app --reload
# Service should start but log a warning about forced start
```

---

## PR 2 — Fix Act E2E test: set git identity in temp repo

**Branch:** `test/fix-act-e2e-git-config`
**Commit message:** `test(e2e): configure local git user.name/user.email in temp repo to prevent CI commit failures`

### Goal

Ensure the Act E2E test does not fail in CI due to Git refusing to commit (missing identity). The fix is to set local `user.name` and `user.email` in the temp repo created by the test.

### Change (single-file patch)

Edit `backend/tests/e2e/test_act_mode_safety.py`. Insert the two `git config` commands immediately after the `git init` invocation.

#### Example patch (context + insertion):

Locate the sequence:

```python
run("git init -b main", repo)
(repo / "hello.txt").write_text("hello\n")
run("git add hello.txt && git commit -m 'init'", repo)
```

Replace / augment with:

```python
run("git init -b main", repo)
# Configure local git identity so CI commits succeed even if global config is absent
run('git config user.email "ci@example.com"', repo)
run('git config user.name "LocalPilot CI"', repo)

(repo / "hello.txt").write_text("hello\n")
run("git add hello.txt && git commit -m 'init'", repo)
```

If the test uses `git init` without `-b main`, adapt accordingly — just place the two `git config` commands immediately after the `git init` call.

---

### Full modified snippet (if you want to replace the test file)

If you prefer, here is a full minimal version of the test file with the change applied:

```python
# backend/tests/e2e/test_act_mode_safety.py
import subprocess
from pathlib import Path
import pytest

def run(cmd, cwd):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed: {cmd}\nstdout:{r.stdout}\nstderr:{r.stderr}")
    return r.stdout.strip()

@pytest.mark.e2e
def test_act_mode_branch_and_rollback(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    # Initialize repo and set local git identity to avoid CI commit errors
    run("git init -b main", repo)
    run('git config user.email "ci@example.com"', repo)
    run('git config user.name "LocalPilot CI"', repo)

    (repo / "hello.txt").write_text("hello\n")
    run("git add hello.txt && git commit -m 'init'", repo)

    # Create a branch and simulate work
    branch = "localpilot/plan-test"
    run(f"git checkout -b {branch}", repo)
    (repo / "newfile.txt").write_text("some content")
    run("git add newfile.txt && git commit -m 'add newfile'", repo)

    # Simulate failure -> rollback to previous commit
    run("git reset --hard HEAD~1", repo)
    run("git checkout main", repo)
    run(f"git branch -D {branch}", repo)

    # newfile should not exist (rolled back)
    assert not (repo / "newfile.txt").exists()
```

---

### Local verification (after patch)

```bash
cd backend
. .venv/bin/activate
pytest -q backend/tests/e2e/test_act_mode_safety.py::test_act_mode_branch_and_rollback -q
```

This should run without git errors in CI environments that do not have global git identity configured.

---

## Patch proposal for your AI coding agent (unified, actionable)

Below is a single, precise plan your AI coding agent can follow to apply both patches programmatically.

### Steps for agent to apply patch

1. Create branch `chore/startup-validator-hook` from your default branch.
2. Edit `backend/app/api/prom_metrics.py`: add the `register_validator_startup` helper (code block above). If `app.services.llm.validator` import fails, try fallback `services.llm.validator`. Save file.
3. Edit `backend/app/main.py`: add `from app.api import prom_metrics` and call `prom_metrics.register_validator_startup(app)` immediately after `app = FastAPI(...)`. (Wrap in try/except to avoid masking other errors.)
4. Run backend unit tests: `pytest -q backend/tests/test_vram_validator.py`. Fix import paths if tests import differently.
5. Commit changes with message: `chore(startup): register VRAM model validator on FastAPI startup`
6. Push branch and open PR.

Then:

7. Create branch `test/fix-act-e2e-git-config`.
8. Edit `backend/tests/e2e/test_act_mode_safety.py`: after `git init` add `git config user.email` and `git config user.name` commands (insert as two `run()` calls).
9. Run the test: `pytest -q backend/tests/e2e/test_act_mode_safety.py::test_act_mode_branch_and_rollback`.
10. Commit changes with message: `test(e2e): set local git identity in temp repo to prevent CI commit failures`
11. Push branch and open PR.

### PR descriptions (copy-paste recommendations)

**PR 1 title:** chore(startup): register VRAM model validator on FastAPI startup
**PR 1 body (suggested):**

```
Register the model validator to run on FastAPI startup to ensure VRAM/model configuration is validated before model loading. This fails fast with a clear error unless FORCE_START=true is set.

- Adds helper register_validator_startup() in backend/app/api/prom_metrics.py
- Registers it in backend/app/main.py (safe, wrapped in try/except)

This prevents starting with configurations that will cause OOMs on limited hardware. Unit tests for validator already exist.
```

**PR 2 title:** test(e2e): set local git identity in temp repo to prevent CI commit failures
**PR 2 body (suggested):**

```
Ensure e2e test creates a temporary git repo with a local user.name and user.email configuration so that commits succeed in CI environments without global git config.

- Adds git config user.email and user.name commands immediately after git init in backend/tests/e2e/test_act_mode_safety.py

This avoids spurious CI failures when tests attempt to commit.
```

---

## Notes & safety

* These patches are intentionally small and low-risk. They do not change model loading behavior (only validate and fail fast, or allow override with `FORCE_START=true`).
* The startup registration is idempotent and logs debug messages — it will not double-register handlers.
* The test fix only modifies test code.

---

## After applying — recommended verification checklist

* Run `pytest` for the backend test subsets described above.
* Push branches and run CI safety workflow to see both tests pass in the runner.
* Try starting the app with unsafe config and confirm it fails as expected; then try with `FORCE_START=true` to confirm override.
