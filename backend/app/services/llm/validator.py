# backend/app/services/llm/validator.py
import logging
import os

from .hardware_profile import detect_hardware_profile

logger = logging.getLogger(__name__)

# Keep minimal default vram numbers (sync with your ModelRegistry if present)
DEFAULT_MODEL_VRAM = {
    "bge-m3": 1.5,
    "qwen2.5-coder:7b-instruct-q4_K_M": 4.5,
    "qwen2.5-coder:14b-instruct-q4_K_M": 9.0,
}


def compute_vram_requirements(
    config: dict[str, str], model_vram_map: dict[str, float] | None = None
):
    if model_vram_map is None:
        model_vram_map = DEFAULT_MODEL_VRAM
    concurrent_models = [
        ("embedding", config.get("embedding")),
        ("chat", config.get("chat")),
    ]
    swappable_models = [config.get("planning"), config.get("coding")]

    concurrent_vram = sum(model_vram_map.get(m, 0) for _, m in concurrent_models if m)
    peak_swappable = max(
        (model_vram_map.get(m, 0) for m in swappable_models if m), default=0
    )
    peak_vram = max(concurrent_vram, peak_swappable)
    return concurrent_vram, peak_vram


def validate_config_on_startup(config: dict[str, str]):
    profile = detect_hardware_profile()
    concurrent_vram, peak_vram = compute_vram_requirements(config)
    max_safe = profile.max_safe_vram_gb

    logger.info("HardwareProfile: %s", profile)
    logger.info(
        "Config concurrent_vram=%s GB, peak_vram=%s GB (max_safe=%s GB)",
        concurrent_vram,
        peak_vram,
        max_safe,
    )

    force = os.getenv("FORCE_START", "false").lower() == "true"

    if profile.total_vram_gb <= 0 and peak_vram > 0:
        msg = f"No GPU detected, but config peak_vram={peak_vram}GB requires GPU."
        if not force:
            raise RuntimeError(msg)
        logger.warning("FORCE_START=true; continuing despite: %s", msg)

    if concurrent_vram > max_safe:
        msg = f"Concurrent VRAM ({concurrent_vram:.1f}GB) exceeds safe limit ({max_safe:.1f}GB)."
        if not force:
            raise RuntimeError(msg)
        logger.warning("FORCE_START=true; continuing despite: %s", msg)

    if profile.total_vram_gb > 0 and peak_vram > profile.total_vram_gb:
        msg = f"Peak VRAM ({peak_vram:.1f}GB) exceeds total VRAM ({profile.total_vram_gb:.1f}GB)."
        if not force:
            raise RuntimeError(msg)
        logger.warning("FORCE_START=true; continuing despite: %s", msg)

    return True
