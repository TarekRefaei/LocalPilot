# backend/tests/test_validator_force_start.py
import importlib
import logging

import pytest

# validator module import path
VALIDATOR_MOD = "app.services.llm.validator"


def test_force_start_overrides_runtime_error(monkeypatch, caplog):
    """
    Ensure validate_config_on_startup does not raise when FORCE_START=true.
    We monkeypatch detect_hardware_profile to simulate a no-GPU host and set a big model
    in the config so validation would normally raise.
    """
    caplog.set_level(logging.WARNING)
    validator = importlib.import_module(VALIDATOR_MOD)

    class FakeProfile:
        total_vram_gb = 0.0
        available_vram_gb = 0.0

        def __repr__(self):
            return "<FakeProfile no GPU>"

        @property
        def max_safe_vram_gb(self):
            return 0.0

    # Force detect_hardware_profile to return no-GPU profile
    monkeypatch.setattr(validator, "detect_hardware_profile", lambda: FakeProfile())

    cfg = {
        "embedding": "bge-m3",
        "chat": "qwen2.5-coder:14b-instruct-q4_K_M",
        "planning": None,
        "coding": None,
    }

    # Ensure default behavior raises
    monkeypatch.delenv("FORCE_START", raising=False)
    with pytest.raises(RuntimeError):
        validator.validate_config_on_startup(cfg)

    # Now set FORCE_START and verify it does not raise and logs a warning
    monkeypatch.setenv("FORCE_START", "true")
    try:
        assert validator.validate_config_on_startup(cfg) is True
        # Check a WARNING or higher about forced start is present
        found = any(
            "FORCE_START" in rec.getMessage() or "force" in rec.getMessage().lower()
            for rec in caplog.records
        )
        assert found, "Expected a warning or log entry indicating FORCE_START override"
    finally:
        monkeypatch.delenv("FORCE_START", raising=False)
