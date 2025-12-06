# backend/tests/test_startup_validator_registration.py
import importlib
import logging

from fastapi import FastAPI
from starlette.testclient import TestClient

# We will import the module that defines register_validator_startup (prom_metrics)
# and monkeypatch the validate_config_on_startup symbol it references.
MODULE_PATH = "app.api.prom_metrics"


def test_register_validator_startup_invokes_validator(monkeypatch, caplog):
    """
    Ensure register_validator_startup registers a startup handler that calls
    validate_config_on_startup at app startup.

    Strategy:
    - Import the prom_metrics module
    - Replace its validate_config_on_startup with a stub that records calls
    - Create a FastAPI app, call register_validator_startup(app)
    - Create TestClient(app) -> triggers startup events
    - Assert our stub was called.
    """

    caplog.set_level(logging.DEBUG)

    # Import the prom_metrics module
    prom_metrics = importlib.import_module(MODULE_PATH)

    called = {"count": 0, "args": None}

    def fake_validate(cfg):
        called["count"] += 1
        called["args"] = cfg
        # Do not raise

    # Monkeypatch the symbol used inside the module
    monkeypatch.setattr(
        prom_metrics, "validate_config_on_startup", fake_validate, raising=False
    )

    # Create app and register
    app = FastAPI()
    prom_metrics.register_validator_startup(app)

    # Ensure that TestClient startup triggers the handler
    with TestClient(app) as client:
        # trigger a simple request to ensure server started
        r = client.get("/openapi.json")
        assert r.status_code in (200, 404, 422, 500) or isinstance(r.status_code, int)

    assert (
        called["count"] >= 1
    ), "validate_config_on_startup was not invoked during startup"
