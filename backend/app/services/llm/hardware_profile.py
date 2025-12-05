# backend/app/services/llm/hardware_profile.py
import logging
from dataclasses import dataclass

try:
    import GPUtil  # type: ignore
except Exception:
    GPUtil = None  # type: ignore

try:
    import psutil  # type: ignore
except Exception:
    psutil = None  # type: ignore

logger = logging.getLogger(__name__)


@dataclass
class HardwareProfile:
    gpu_name: str
    total_vram_gb: float
    available_vram_gb: float
    gpu_utilization_percent: float
    total_ram_gb: float
    available_ram_gb: float

    @property
    def max_safe_vram_gb(self) -> float:
        # 90% safety threshold
        return round(self.total_vram_gb * 0.9, 2)


def detect_hardware_profile() -> HardwareProfile:
    total_ram_gb = 0.0
    available_ram_gb = 0.0
    try:
        if psutil:
            vm = psutil.virtual_memory()  # type: ignore[attr-defined]
            total_ram_gb = round(vm.total / (1024**3), 2)
            available_ram_gb = round(vm.available / (1024**3), 2)
    except Exception:
        logger.debug("psutil unavailable or failed to detect RAM")

    if GPUtil:
        try:
            gpus = GPUtil.getGPUs()  # type: ignore[attr-defined]
            if gpus:
                gpu = gpus[0]
                total_vram_gb = round(gpu.memoryTotal / 1024, 2)
                available_vram_gb = round(gpu.memoryFree / 1024, 2)
                gpu_util = round(gpu.load * 100, 1)
                return HardwareProfile(
                    gpu_name=getattr(gpu, "name", "GPU"),
                    total_vram_gb=total_vram_gb,
                    available_vram_gb=available_vram_gb,
                    gpu_utilization_percent=gpu_util,
                    total_ram_gb=total_ram_gb,
                    available_ram_gb=available_ram_gb,
                )
        except Exception as e:
            logger.warning("GPUtil detection failed: %s", e)

    # CPU fallback (no GPU)
    return HardwareProfile(
        gpu_name="CPU (no GPU)",
        total_vram_gb=0.0,
        available_vram_gb=0.0,
        gpu_utilization_percent=0.0,
        total_ram_gb=total_ram_gb,
        available_ram_gb=available_ram_gb,
    )
