# backend/tests/test_vram_validator.py
import pytest

from app.services.llm import validator


def test_compute_vram_requirements_basic():
    cfg = {
        "embedding": "bge-m3",
        "chat": "qwen2.5-coder:7b-instruct-q4_K_M",
        "planning": "qwen2.5-coder:14b-instruct-q4_K_M",
    }
    concurrent, peak = validator.compute_vram_requirements(cfg)
    assert concurrent >= 0
    assert peak >= concurrent


def test_validate_raises_no_gpu(monkeypatch):
    # simulate no GPU profile by monkeypatching detect_hardware_profile
    class FakeProfile:
        total_vram_gb = 0.0

        def __repr__(self):
            return "<FakeProfile no GPU>"

        @property
        def max_safe_vram_gb(self):
            return 0.0

    monkeypatch.setattr(
        "app.services.llm.validator.detect_hardware_profile", lambda: FakeProfile()
    )
    cfg = {"embedding": "bge-m3", "chat": "qwen2.5-coder:14b-instruct-q4_K_M"}
    with pytest.raises(RuntimeError):
        validator.validate_config_on_startup(cfg)
    # set FORCE_START and ensure no raise
    monkeypatch.setenv("FORCE_START", "true")
    try:
        assert validator.validate_config_on_startup(cfg) is True
    finally:
        monkeypatch.delenv("FORCE_START", raising=False)
