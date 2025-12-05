# 📄 DOCUMENT #10: MODEL_MANAGEMENT_SPEC.md
# LocalPilot - Model Management Specification

**Version:** 1.0
**Date:** January 2025
**Status:** Advanced Specification
**Author:** LocalPilot ML Systems Team

---

## 📋 Table of Contents

- [📄 DOCUMENT #10: MODEL\_MANAGEMENT\_SPEC.md](#-document-10-model_management_specmd)
- [LocalPilot - Model Management Specification](#localpilot---model-management-specification)
  - [📋 Table of Contents](#-table-of-contents)
  - [🎯 Overview](#-overview)
    - [Purpose](#purpose)
    - [Critical Requirements](#critical-requirements)
  - [💻 Hardware Constraints](#-hardware-constraints)
    - [Target Hardware Profile](#target-hardware-profile)
    - [Hardware-Aware Configuration](#hardware-aware-configuration)
  - [📚 Model Registry](#-model-registry)
    - [Model Information Database](#model-information-database)
  - [🧠 VRAM Management](#-vram-management)
    - [VRAM Monitor](#vram-monitor)
  - [🔄 Model Swapping Strategy](#-model-swapping-strategy)
    - [Model Swapper Implementation](#model-swapper-implementation)
    - [Swap Timing Optimization](#swap-timing-optimization)
  - [✅ Model Validation System](#-model-validation-system)
    - [Configuration Validator](#configuration-validator)
  - [📊 Resource Monitoring](#-resource-monitoring)
    - [Comprehensive Resource Monitor](#comprehensive-resource-monitor)
  - [⚡ Performance Optimization](#-performance-optimization)
    - [Model Loading Optimization](#model-loading-optimization)
  - [⚠️ Error Handling](#️-error-handling)
    - [Model Management Error Handling](#model-management-error-handling)
  - [⚙️ Configuration Management](#️-configuration-management)
    - [Model Configuration Service](#model-configuration-service)
  - [📚 Related Documents](#-related-documents)

---

## 🎯 Overview

### Purpose

The Model Management System is responsible for:

1. **Resource-Aware Loading**: Load models within hardware constraints
2. **Smart Swapping**: Swap models on-demand to maximize quality while fitting in VRAM
3. **Validation**: Prevent dangerous configurations that could crash the system
4. **Monitoring**: Track resource usage in real-time
5. **Optimization**: Maximize performance given hardware limitations

### Critical Requirements

```yaml
Hardware Constraints (Reference: RTX 4060 8GB VRAM):
  Total VRAM: 8GB
  System Reserved: ~500MB
  Available: ~7.5GB

Model Sizes:
  bge-m3 (embeddings): 1.5GB
  qwen2.5-coder:7b: 4.5GB
  qwen2.5-coder:14b: 9GB (requires swapping!)

Operating Modes:
  Concurrent: Embeddings + Chat (7b) = 6GB ✓
  Swappable: Planning/Coding (14b) = 9GB (swap required)

Goals:
  - Never exceed 90% VRAM (7.2GB max concurrent)
  - Swap models in < 3 seconds
  - Maintain quality (use 14b when possible)
  - Prevent OOM crashes
```

---

## 💻 Hardware Constraints

### Target Hardware Profile

```python
# backend/src/services/llm/hardware_profile.py

from dataclasses import dataclass
from typing import Optional
import GPUtil
import psutil

@dataclass
class HardwareProfile:
    """Hardware capabilities profile"""

    # GPU
    gpu_name: str
    total_vram_gb: float
    available_vram_gb: float
    gpu_utilization_percent: float

    # CPU
    cpu_cores: int
    cpu_freq_ghz: float

    # RAM
    total_ram_gb: float
    available_ram_gb: float

    # Computed properties
    @property
    def max_safe_vram_gb(self) -> float:
        """Maximum safe VRAM usage (90% of total)"""
        return self.total_vram_gb * 0.9

    @property
    def vram_buffer_gb(self) -> float:
        """Recommended VRAM buffer"""
        return self.total_vram_gb * 0.1

    @property
    def can_run_concurrent_models(self) -> bool:
        """Check if can run embeddings + chat concurrently"""
        # bge-m3 (1.5GB) + qwen2.5-coder:7b (4.5GB) = 6GB
        return self.total_vram_gb >= 6.5


class HardwareDetector:
    """Detect hardware capabilities"""

    @staticmethod
    def detect() -> HardwareProfile:
        """Detect current hardware profile"""

        # Detect GPU
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]  # Use first GPU
            gpu_name = gpu.name
            total_vram_gb = gpu.memoryTotal / 1024  # Convert MB to GB
            available_vram_gb = gpu.memoryFree / 1024
            gpu_utilization = gpu.load * 100
        else:
            # No GPU detected - CPU fallback
            gpu_name = "CPU (No GPU)"
            total_vram_gb = 0
            available_vram_gb = 0
            gpu_utilization = 0

        # Detect CPU
        cpu_cores = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        cpu_freq_ghz = cpu_freq.current / 1000 if cpu_freq else 0

        # Detect RAM
        ram = psutil.virtual_memory()
        total_ram_gb = ram.total / (1024 ** 3)
        available_ram_gb = ram.available / (1024 ** 3)

        return HardwareProfile(
            gpu_name=gpu_name,
            total_vram_gb=round(total_vram_gb, 2),
            available_vram_gb=round(available_vram_gb, 2),
            gpu_utilization_percent=round(gpu_utilization, 1),
            cpu_cores=cpu_cores,
            cpu_freq_ghz=round(cpu_freq_ghz, 2),
            total_ram_gb=round(total_ram_gb, 2),
            available_ram_gb=round(available_ram_gb, 2),
        )

    @staticmethod
    def get_current_vram_usage() -> float:
        """Get current VRAM usage in GB"""
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            return (gpu.memoryTotal - gpu.memoryFree) / 1024
        return 0.0

    @staticmethod
    def get_available_vram() -> float:
        """Get available VRAM in GB"""
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[0].memoryFree / 1024
        return 0.0
```

### Hardware-Aware Configuration

```python
# backend/src/services/llm/hardware_config.py

from typing import Dict, List
from .hardware_profile import HardwareProfile, HardwareDetector

class HardwareAwareConfig:
    """Generate optimal configuration based on hardware"""

    # Model VRAM requirements (in GB)
    MODEL_VRAM_REQUIREMENTS = {
        'bge-m3': 1.5,
        'qwen2.5-coder:7b-instruct-q4_K_M': 4.5,
        'qwen2.5-coder:14b-instruct-q4_K_M': 9.0,
        'qwen2.5-coder:32b-instruct-q4_K_M': 18.0,
    }

    @staticmethod
    def generate_recommended_config(
        hardware: HardwareProfile
    ) -> Dict[str, str]:
        """Generate recommended model configuration"""

        vram = hardware.total_vram_gb

        # Default configuration
        config = {
            'embedding': 'bge-m3',
            'chat': 'qwen2.5-coder:7b-instruct-q4_K_M',
            'planning': 'qwen2.5-coder:7b-instruct-q4_K_M',
            'coding': 'qwen2.5-coder:7b-instruct-q4_K_M',
        }

        # High-end GPU (16GB+): Use 14b for everything
        if vram >= 16:
            config['chat'] = 'qwen2.5-coder:14b-instruct-q4_K_M'
            config['planning'] = 'qwen2.5-coder:14b-instruct-q4_K_M'
            config['coding'] = 'qwen2.5-coder:14b-instruct-q4_K_M'

        # Mid-range GPU (8-16GB): Use 14b for planning/coding (with swap)
        elif vram >= 8:
            # Keep 7b for chat (frequent use)
            # Use 14b for planning/coding (swap on-demand)
            config['planning'] = 'qwen2.5-coder:14b-instruct-q4_K_M'
            config['coding'] = 'qwen2.5-coder:14b-instruct-q4_K_M'

        # Low-end GPU (4-8GB): Use 7b for everything
        elif vram >= 4:
            # Already configured with 7b
            pass

        # Very low or CPU: Warn user
        else:
            # Use 7b but warn about performance
            pass

        return config

    @staticmethod
    def validate_config(
        config: Dict[str, str],
        hardware: HardwareProfile
    ) -> Dict:
        """Validate model configuration against hardware"""

        # Calculate VRAM requirements
        concurrent_models = []
        swappable_models = []

        # Embedding is always loaded
        concurrent_models.append(('embedding', config['embedding']))

        # Chat is loaded concurrently (frequent use)
        concurrent_models.append(('chat', config['chat']))

        # Planning/Coding are swappable (less frequent)
        swappable_models.append(('planning', config['planning']))
        swappable_models.append(('coding', config['coding']))

        # Calculate concurrent VRAM
        concurrent_vram = sum(
            HardwareAwareConfig.MODEL_VRAM_REQUIREMENTS.get(model, 0)
            for _, model in concurrent_models
        )

        # Calculate peak VRAM (max of concurrent or any swappable)
        swappable_vram = max(
            HardwareAwareConfig.MODEL_VRAM_REQUIREMENTS.get(model, 0)
            for _, model in swappable_models
        ) if swappable_models else 0

        peak_vram = max(concurrent_vram, swappable_vram)

        # Determine status
        max_safe_vram = hardware.max_safe_vram_gb

        if concurrent_vram > max_safe_vram:
            return {
                'valid': False,
                'level': 'error',
                'concurrent_vram_gb': round(concurrent_vram, 2),
                'peak_vram_gb': round(peak_vram, 2),
                'max_safe_vram_gb': round(max_safe_vram, 2),
                'message': f'Concurrent usage ({concurrent_vram:.1f}GB) exceeds safe limit ({max_safe_vram:.1f}GB)',
                'recommendations': [
                    'Reduce to smaller models',
                    f'Try using 7b models instead of 14b',
                ],
            }

        elif peak_vram > hardware.total_vram_gb:
            return {
                'valid': False,
                'level': 'error',
                'concurrent_vram_gb': round(concurrent_vram, 2),
                'peak_vram_gb': round(peak_vram, 2),
                'max_safe_vram_gb': round(max_safe_vram, 2),
                'message': f'Peak usage ({peak_vram:.1f}GB) exceeds total VRAM ({hardware.total_vram_gb:.1f}GB)',
                'recommendations': [
                    'Use smaller models',
                    'Model swapping not possible with current selection',
                ],
            }

        elif concurrent_vram > max_safe_vram * 0.7:
            return {
                'valid': True,
                'level': 'warning',
                'concurrent_vram_gb': round(concurrent_vram, 2),
                'peak_vram_gb': round(peak_vram, 2),
                'max_safe_vram_gb': round(max_safe_vram, 2),
                'message': f'High VRAM usage ({concurrent_vram:.1f}GB / {hardware.total_vram_gb:.1f}GB)',
                'recommendations': [
                    'Configuration will work but may be unstable under load',
                    'Consider using 7b for chat if experiencing issues',
                ],
            }

        else:
            # Check if swapping needed
            requires_swapping = any(
                HardwareAwareConfig.MODEL_VRAM_REQUIREMENTS.get(model, 0) + concurrent_vram > max_safe_vram
                for _, model in swappable_models
            )

            return {
                'valid': True,
                'level': 'success',
                'concurrent_vram_gb': round(concurrent_vram, 2),
                'peak_vram_gb': round(peak_vram, 2),
                'max_safe_vram_gb': round(max_safe_vram, 2),
                'requires_swapping': requires_swapping,
                'message': f'Configuration is optimal ({concurrent_vram:.1f}GB / {hardware.total_vram_gb:.1f}GB)',
                'recommendations': [
                    f'Planning/Coding will require model swapping (~2-3s delay)' if requires_swapping else 'All models can run concurrently',
                ],
            }
```

---

## 📚 Model Registry

### Model Information Database

```python
# backend/src/services/llm/model_registry.py

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class ModelType(Enum):
    """Model type classification"""
    CHAT = 'chat'
    EMBEDDING = 'embedding'
    CODE_GENERATION = 'code_generation'

class ModelCapability(Enum):
    """Model capabilities"""
    CHAT = 'chat'
    CODE_GENERATION = 'code_generation'
    SUMMARIZATION = 'summarization'
    PLANNING = 'planning'
    EMBEDDING = 'embedding'

@dataclass
class ModelInfo:
    """Complete model information"""

    # Identification
    id: str
    name: str
    provider: str  # 'ollama', 'lmstudio', 'localai'

    # Type & capabilities
    type: ModelType
    capabilities: List[ModelCapability]

    # Resource requirements
    size_gb: float
    vram_required_gb: float
    context_window: int

    # Performance characteristics
    tokens_per_second: Optional[float] = None  # Benchmark
    quality_score: Optional[float] = None  # Subjective 0-1

    # Embedding-specific
    embedding_dimensions: Optional[int] = None
    max_sequence_length: Optional[int] = None

    # Metadata
    description: str = ""
    recommended_for: List[str] = None

    def __post_init__(self):
        if self.recommended_for is None:
            self.recommended_for = []


class ModelRegistry:
    """Central registry of available models"""

    # Pre-defined models
    MODELS = {
        'bge-m3': ModelInfo(
            id='bge-m3',
            name='BGE-M3 Embeddings',
            provider='ollama',
            type=ModelType.EMBEDDING,
            capabilities=[ModelCapability.EMBEDDING],
            size_gb=1.5,
            vram_required_gb=1.5,
            context_window=8192,
            embedding_dimensions=1024,
            max_sequence_length=8192,
            quality_score=0.95,
            description='Multilingual embedding model optimized for code',
            recommended_for=['embeddings'],
        ),

        'qwen2.5-coder:7b-instruct-q4_K_M': ModelInfo(
            id='qwen2.5-coder:7b-instruct-q4_K_M',
            name='Qwen2.5-Coder 7B Instruct (4-bit)',
            provider='ollama',
            type=ModelType.CHAT,
            capabilities=[
                ModelCapability.CHAT,
                ModelCapability.CODE_GENERATION,
                ModelCapability.SUMMARIZATION,
            ],
            size_gb=4.5,
            vram_required_gb=4.5,
            context_window=32768,
            tokens_per_second=20.0,
            quality_score=0.80,
            description='Fast 7B model for chat and code generation',
            recommended_for=['chat', 'summarization'],
        ),

        'qwen2.5-coder:14b-instruct-q4_K_M': ModelInfo(
            id='qwen2.5-coder:14b-instruct-q4_K_M',
            name='Qwen2.5-Coder 14B Instruct (4-bit)',
            provider='ollama',
            type=ModelType.CHAT,
            capabilities=[
                ModelCapability.CHAT,
                ModelCapability.CODE_GENERATION,
                ModelCapability.PLANNING,
                ModelCapability.SUMMARIZATION,
            ],
            size_gb=9.0,
            vram_required_gb=9.0,
            context_window=32768,
            tokens_per_second=15.0,
            quality_score=0.92,
            description='High-quality 14B model for complex code generation and planning',
            recommended_for=['planning', 'coding', 'complex_tasks'],
        ),
    }

    @classmethod
    def get_model(cls, model_id: str) -> Optional[ModelInfo]:
        """Get model information by ID"""
        return cls.MODELS.get(model_id)

    @classmethod
    def get_models_by_capability(
        cls,
        capability: ModelCapability
    ) -> List[ModelInfo]:
        """Get all models with specific capability"""
        return [
            model for model in cls.MODELS.values()
            if capability in model.capabilities
        ]

    @classmethod
    def get_models_by_type(cls, model_type: ModelType) -> List[ModelInfo]:
        """Get all models of specific type"""
        return [
            model for model in cls.MODELS.values()
            if model.type == model_type
        ]

    @classmethod
    def find_alternative_models(
        cls,
        model_id: str,
        max_vram_gb: float
    ) -> List[ModelInfo]:
        """Find alternative models that fit in VRAM"""
        current = cls.get_model(model_id)
        if not current:
            return []

        # Find models with same capabilities but smaller
        alternatives = [
            model for model in cls.MODELS.values()
            if (
                model.id != model_id
                and model.type == current.type
                and all(cap in model.capabilities for cap in current.capabilities)
                and model.vram_required_gb <= max_vram_gb
            )
        ]

        # Sort by quality score (descending)
        alternatives.sort(
            key=lambda m: m.quality_score or 0,
            reverse=True
        )

        return alternatives
```

---

## 🧠 VRAM Management

### VRAM Monitor

```python
# backend/src/services/llm/vram_monitor.py

import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import GPUtil
import logging

logger = logging.getLogger(__name__)

@dataclass
class VRAMSnapshot:
    """VRAM usage snapshot"""
    timestamp: datetime
    total_gb: float
    used_gb: float
    free_gb: float
    utilization_percent: float

    @property
    def available_percent(self) -> float:
        return 100 - self.utilization_percent

class VRAMMonitor:
    """Real-time VRAM monitoring"""

    def __init__(
        self,
        warning_threshold: float = 0.85,
        critical_threshold: float = 0.95,
        check_interval_seconds: float = 1.0,
    ):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.check_interval = check_interval_seconds

        self._monitoring = False
        self._monitor_task: Optional[asyncio.Task] = None
        self._callbacks: Dict[str, List[Callable]] = {
            'warning': [],
            'critical': [],
            'normal': [],
        }

        self._last_state = 'normal'
        self._history: List[VRAMSnapshot] = []
        self._max_history = 3600  # Keep 1 hour of history

    def get_current_snapshot(self) -> VRAMSnapshot:
        """Get current VRAM snapshot"""
        gpus = GPUtil.getGPUs()
        if not gpus:
            return VRAMSnapshot(
                timestamp=datetime.utcnow(),
                total_gb=0,
                used_gb=0,
                free_gb=0,
                utilization_percent=0,
            )

        gpu = gpus[0]
        total_gb = gpu.memoryTotal / 1024
        free_gb = gpu.memoryFree / 1024
        used_gb = total_gb - free_gb
        utilization = (used_gb / total_gb) * 100 if total_gb > 0 else 0

        return VRAMSnapshot(
            timestamp=datetime.utcnow(),
            total_gb=round(total_gb, 2),
            used_gb=round(used_gb, 2),
            free_gb=round(free_gb, 2),
            utilization_percent=round(utilization, 1),
        )

    def register_callback(
        self,
        event: str,
        callback: Callable[[VRAMSnapshot], None]
    ):
        """Register callback for VRAM events"""
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    async def start_monitoring(self):
        """Start background VRAM monitoring"""
        if self._monitoring:
            return

        self._monitoring = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("VRAM monitoring started")

    async def stop_monitoring(self):
        """Stop background monitoring"""
        self._monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("VRAM monitoring stopped")

    async def _monitor_loop(self):
        """Background monitoring loop"""
        while self._monitoring:
            try:
                snapshot = self.get_current_snapshot()

                # Add to history
                self._history.append(snapshot)
                if len(self._history) > self._max_history:
                    self._history.pop(0)

                # Determine state
                utilization = snapshot.utilization_percent / 100

                if utilization >= self.critical_threshold:
                    new_state = 'critical'
                elif utilization >= self.warning_threshold:
                    new_state = 'warning'
                else:
                    new_state = 'normal'

                # Trigger callbacks if state changed
                if new_state != self._last_state:
                    logger.info(
                        f"VRAM state changed: {self._last_state} -> {new_state} "
                        f"({snapshot.used_gb:.2f}GB / {snapshot.total_gb:.2f}GB)"
                    )

                    for callback in self._callbacks[new_state]:
                        try:
                            callback(snapshot)
                        except Exception as e:
                            logger.error(f"VRAM callback error: {e}")

                    self._last_state = new_state

                # Wait before next check
                await asyncio.sleep(self.check_interval)

            except Exception as e:
                logger.error(f"VRAM monitoring error: {e}")
                await asyncio.sleep(self.check_interval)

    def get_usage_stats(self, minutes: int = 5) -> Dict:
        """Get usage statistics for last N minutes"""
        if not self._history:
            return {
                'avg_utilization': 0,
                'max_utilization': 0,
                'min_utilization': 0,
            }

        # Get snapshots from last N minutes
        cutoff = datetime.utcnow().timestamp() - (minutes * 60)
        recent = [
            s for s in self._history
            if s.timestamp.timestamp() >= cutoff
        ]

        if not recent:
            recent = [self._history[-1]]

        utilizations = [s.utilization_percent for s in recent]

        return {
            'avg_utilization': round(sum(utilizations) / len(utilizations), 1),
            'max_utilization': round(max(utilizations), 1),
            'min_utilization': round(min(utilizations), 1),
            'samples': len(recent),
        }
```

---

## 🔄 Model Swapping Strategy

### Model Swapper Implementation

```python
# backend/src/services/llm/model_swapper.py

import asyncio
from typing import Dict, Optional, Set
from datetime import datetime, timedelta
import logging
from .vram_monitor import VRAMMonitor
from .model_registry import ModelRegistry, ModelInfo

logger = logging.getLogger(__name__)

class ModelSwapper:
    """Intelligent model swapping for VRAM optimization"""

    def __init__(
        self,
        vram_monitor: VRAMMonitor,
        ollama_client,
    ):
        self.vram_monitor = vram_monitor
        self.ollama = ollama_client

        # Track loaded models
        self._loaded_models: Dict[str, datetime] = {}

        # Track model usage (for LRU)
        self._model_usage: Dict[str, datetime] = {}

        # Permanent models (never unload)
        self._permanent_models: Set[str] = set()

        # Lock for swapping operations
        self._swap_lock = asyncio.Lock()

    def mark_permanent(self, model_id: str):
        """Mark model as permanent (never unload)"""
        self._permanent_models.add(model_id)
        logger.info(f"Model {model_id} marked as permanent")

    async def ensure_model_loaded(
        self,
        model_id: str,
        priority: str = 'normal'
    ) -> bool:
        """
        Ensure model is loaded, swap if necessary

        Args:
            model_id: Model to load
            priority: 'high' (block until loaded) or 'normal'

        Returns:
            True if model is loaded, False if failed
        """
        async with self._swap_lock:
            # Check if already loaded
            if model_id in self._loaded_models:
                # Update usage timestamp
                self._model_usage[model_id] = datetime.utcnow()
                logger.debug(f"Model {model_id} already loaded")
                return True

            # Get model info
            model_info = ModelRegistry.get_model(model_id)
            if not model_info:
                logger.error(f"Unknown model: {model_id}")
                return False

            # Check if we have enough VRAM
            snapshot = self.vram_monitor.get_current_snapshot()
            required_vram = model_info.vram_required_gb

            if snapshot.free_gb >= required_vram:
                # Enough VRAM, load directly
                logger.info(f"Loading {model_id} ({required_vram}GB required, {snapshot.free_gb}GB available)")
                success = await self._load_model(model_id)

                if success:
                    self._loaded_models[model_id] = datetime.utcnow()
                    self._model_usage[model_id] = datetime.utcnow()

                return success

            else:
                # Need to unload models to make space
                logger.info(
                    f"Insufficient VRAM for {model_id} "
                    f"({required_vram}GB required, {snapshot.free_gb}GB available)"
                )

                # Unload least recently used models
                freed_vram = await self._free_vram(required_vram)

                if freed_vram >= required_vram:
                    # Now load the model
                    success = await self._load_model(model_id)

                    if success:
                        self._loaded_models[model_id] = datetime.utcnow()
                        self._model_usage[model_id] = datetime.utcnow()

                    return success
                else:
                    logger.error(
                        f"Cannot free enough VRAM for {model_id} "
                        f"(freed {freed_vram}GB, need {required_vram}GB)"
                    )
                    return False

    async def _load_model(self, model_id: str) -> bool:
        """Load model into memory"""
        try:
            logger.info(f"Loading model: {model_id}")
            start_time = datetime.utcnow()

            # Trigger Ollama to load model
            # (Ollama loads model on first use)
            await self.ollama.generate(
                model=model_id,
                prompt="",  # Empty prompt just to load
                stream=False,
            )

            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Model {model_id} loaded in {duration:.2f}s")

            return True

        except Exception as e:
            logger.error(f"Failed to load model {model_id}: {e}")
            return False

    async def _unload_model(self, model_id: str) -> float:
        """
        Unload model from memory

        Returns:
            VRAM freed in GB
        """
        if model_id not in self._loaded_models:
            return 0.0

        # Don't unload permanent models
        if model_id in self._permanent_models:
            logger.debug(f"Cannot unload permanent model: {model_id}")
            return 0.0

        try:
            logger.info(f"Unloading model: {model_id}")

            # Get model size
            model_info = ModelRegistry.get_model(model_id)
            vram_to_free = model_info.vram_required_gb if model_info else 0

            # Ollama doesn't have explicit unload API
            # We rely on OS to reclaim memory
            # In practice, loading another model will replace it

            # Remove from tracking
            del self._loaded_models[model_id]

            logger.info(f"Model {model_id} unloaded (freed ~{vram_to_free}GB)")

            return vram_to_free

        except Exception as e:
            logger.error(f"Failed to unload model {model_id}: {e}")
            return 0.0

    async def _free_vram(self, required_gb: float) -> float:
        """
        Free VRAM by unloading least recently used models

        Returns:
            Total VRAM freed in GB
        """
        # Sort loaded models by last usage (LRU)
        sorted_models = sorted(
            self._loaded_models.keys(),
            key=lambda m: self._model_usage.get(m, datetime.min)
        )

        total_freed = 0.0

        for model_id in sorted_models:
            if total_freed >= required_gb:
                break

            # Skip permanent models
            if model_id in self._permanent_models:
                continue

            freed = await self._unload_model(model_id)
            total_freed += freed

        # Wait a bit for memory to be reclaimed
        await asyncio.sleep(0.5)

        return total_freed

    def get_loaded_models(self) -> Dict[str, Dict]:
        """Get currently loaded models"""
        result = {}

        for model_id, loaded_at in self._loaded_models.items():
            last_used = self._model_usage.get(model_id)
            model_info = ModelRegistry.get_model(model_id)

            result[model_id] = {
                'loaded_at': loaded_at.isoformat(),
                'last_used': last_used.isoformat() if last_used else None,
                'vram_gb': model_info.vram_required_gb if model_info else 0,
                'permanent': model_id in self._permanent_models,
            }

        return result

    async def preload_models(self, model_ids: List[str]):
        """Preload models if VRAM available"""
        for model_id in model_ids:
            try:
                await self.ensure_model_loaded(model_id, priority='normal')
            except Exception as e:
                logger.warning(f"Failed to preload {model_id}: {e}")
```

### Swap Timing Optimization

```python
# backend/src/services/llm/swap_optimizer.py

from typing import Dict, List
from datetime import datetime, timedelta

class SwapOptimizer:
    """Optimize model swapping decisions"""

    def __init__(self):
        # Track swap history
        self._swap_history: List[Dict] = []

        # Track model usage patterns
        self._usage_patterns: Dict[str, List[datetime]] = {}

    def record_swap(
        self,
        from_model: str,
        to_model: str,
        duration_seconds: float
    ):
        """Record a model swap"""
        self._swap_history.append({
            'from': from_model,
            'to': to_model,
            'duration': duration_seconds,
            'timestamp': datetime.utcnow(),
        })

    def record_usage(self, model_id: str):
        """Record model usage"""
        if model_id not in self._usage_patterns:
            self._usage_patterns[model_id] = []

        self._usage_patterns[model_id].append(datetime.utcnow())

        # Keep only last 24 hours
        cutoff = datetime.utcnow() - timedelta(hours=24)
        self._usage_patterns[model_id] = [
            ts for ts in self._usage_patterns[model_id]
            if ts >= cutoff
        ]

    def predict_next_model(self, current_mode: str) -> str:
        """Predict which model will be needed next"""
        # Simple heuristic based on mode
        predictions = {
            'chat': 'qwen2.5-coder:7b-instruct-q4_K_M',
            'plan': 'qwen2.5-coder:14b-instruct-q4_K_M',
            'act': 'qwen2.5-coder:14b-instruct-q4_K_M',
        }

        return predictions.get(current_mode, 'qwen2.5-coder:7b-instruct-q4_K_M')

    def should_preload(
        self,
        model_id: str,
        available_vram_gb: float
    ) -> bool:
        """Determine if model should be preloaded"""
        # Get usage frequency
        usage_count = len(self._usage_patterns.get(model_id, []))

        # Preload if:
        # 1. Enough VRAM
        # 2. Used recently (in last hour)

        model_info = ModelRegistry.get_model(model_id)
        if not model_info:
            return False

        if model_info.vram_required_gb > available_vram_gb:
            return False

        if usage_count > 0:
            last_usage = max(self._usage_patterns[model_id])
            if datetime.utcnow() - last_usage < timedelta(hours=1):
                return True

        return False

    def get_swap_stats(self) -> Dict:
        """Get swap statistics"""
        if not self._swap_history:
            return {
                'total_swaps': 0,
                'avg_duration': 0,
                'max_duration': 0,
            }

        durations = [s['duration'] for s in self._swap_history]

        return {
            'total_swaps': len(self._swap_history),
            'avg_duration': sum(durations) / len(durations),
            'max_duration': max(durations),
            'min_duration': min(durations),
        }
```
---

## ✅ Model Validation System

### Configuration Validator

```python
# backend/src/services/llm/model_validator.py

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from .model_registry import ModelRegistry, ModelInfo
from .hardware_profile import HardwareProfile

@dataclass
class ValidationResult:
    """Model configuration validation result"""
    valid: bool
    level: str  # 'success', 'warning', 'error'
    message: str
    recommendations: List[str]
    details: Dict

    def to_dict(self) -> Dict:
        return {
            'valid': self.valid,
            'level': self.level,
            'message': self.message,
            'recommendations': self.recommendations,
            'details': self.details,
        }

class ModelValidator:
    """Validate model configurations"""

    @staticmethod
    def validate_configuration(
        config: Dict[str, str],
        hardware: HardwareProfile
    ) -> ValidationResult:
        """
        Comprehensive validation of model configuration

        Args:
            config: Model configuration dict
            hardware: Hardware profile

        Returns:
            ValidationResult with validation status and recommendations
        """

        # 1. Verify all models exist
        missing_models = []
        for task, model_id in config.items():
            if not ModelRegistry.get_model(model_id):
                missing_models.append(model_id)

        if missing_models:
            return ValidationResult(
                valid=False,
                level='error',
                message=f'Unknown models: {", ".join(missing_models)}',
                recommendations=[
                    'Verify model IDs are correct',
                    'Run "ollama list" to see available models',
                ],
                details={'missing_models': missing_models},
            )

        # 2. Calculate VRAM requirements
        vram_analysis = ModelValidator._analyze_vram_requirements(config, hardware)

        # 3. Check concurrent models
        concurrent_check = ModelValidator._check_concurrent_models(config, hardware)

        # 4. Check swappable models
        swappable_check = ModelValidator._check_swappable_models(config, hardware)

        # 5. Determine overall status
        if not concurrent_check['valid']:
            return ValidationResult(
                valid=False,
                level='error',
                message=concurrent_check['message'],
                recommendations=concurrent_check['recommendations'],
                details={
                    'vram_analysis': vram_analysis,
                    'concurrent_check': concurrent_check,
                },
            )

        if not swappable_check['valid']:
            return ValidationResult(
                valid=False,
                level='error',
                message=swappable_check['message'],
                recommendations=swappable_check['recommendations'],
                details={
                    'vram_analysis': vram_analysis,
                    'swappable_check': swappable_check,
                },
            )

        # 6. Check for warnings
        warnings = []

        if vram_analysis['concurrent_vram_gb'] > hardware.total_vram_gb * 0.75:
            warnings.append(
                f"High VRAM usage ({vram_analysis['concurrent_vram_gb']:.1f}GB / {hardware.total_vram_gb:.1f}GB)"
            )

        if vram_analysis['requires_swapping']:
            warnings.append(
                f"Model swapping required (~{vram_analysis['estimated_swap_time_seconds']}s delays)"
            )

        if hardware.total_vram_gb < 8:
            warnings.append(
                "GPU VRAM below recommended 8GB - may experience performance issues"
            )

        # 7. Generate recommendations
        recommendations = ModelValidator._generate_recommendations(
            config, hardware, vram_analysis
        )

        # Success with possible warnings
        if warnings:
            return ValidationResult(
                valid=True,
                level='warning',
                message='; '.join(warnings),
                recommendations=recommendations,
                details={
                    'vram_analysis': vram_analysis,
                    'concurrent_check': concurrent_check,
                    'swappable_check': swappable_check,
                },
            )
        else:
            return ValidationResult(
                valid=True,
                level='success',
                message=f"Configuration optimal ({vram_analysis['concurrent_vram_gb']:.1f}GB / {hardware.total_vram_gb:.1f}GB)",
                recommendations=recommendations,
                details={
                    'vram_analysis': vram_analysis,
                    'concurrent_check': concurrent_check,
                    'swappable_check': swappable_check,
                },
            )

    @staticmethod
    def _analyze_vram_requirements(
        config: Dict[str, str],
        hardware: HardwareProfile
    ) -> Dict:
        """Analyze VRAM requirements for configuration"""

        # Categorize models
        concurrent_models = {
            'embedding': config.get('embedding'),
            'chat': config.get('chat'),
        }

        swappable_models = {
            'planning': config.get('planning'),
            'coding': config.get('coding'),
        }

        # Calculate VRAM for concurrent models
        concurrent_vram = 0.0
        for task, model_id in concurrent_models.items():
            if model_id:
                model_info = ModelRegistry.get_model(model_id)
                if model_info:
                    concurrent_vram += model_info.vram_required_gb

        # Calculate VRAM for swappable models (max of any single one)
        swappable_vram = 0.0
        for task, model_id in swappable_models.items():
            if model_id:
                model_info = ModelRegistry.get_model(model_id)
                if model_info:
                    swappable_vram = max(swappable_vram, model_info.vram_required_gb)

        # Peak VRAM (concurrent + largest swappable)
        peak_vram = concurrent_vram + swappable_vram

        # Check if swapping needed
        requires_swapping = swappable_vram > 0 and (
            concurrent_vram + swappable_vram > hardware.total_vram_gb * 0.9
        )

        # Estimate swap time (empirical: ~2-3s for model swap)
        estimated_swap_time = 2.5 if requires_swapping else 0

        return {
            'concurrent_vram_gb': round(concurrent_vram, 2),
            'swappable_vram_gb': round(swappable_vram, 2),
            'peak_vram_gb': round(peak_vram, 2),
            'total_vram_gb': hardware.total_vram_gb,
            'max_safe_vram_gb': round(hardware.total_vram_gb * 0.9, 2),
            'requires_swapping': requires_swapping,
            'estimated_swap_time_seconds': estimated_swap_time,
            'utilization_percent': round((concurrent_vram / hardware.total_vram_gb) * 100, 1),
        }

    @staticmethod
    def _check_concurrent_models(
        config: Dict[str, str],
        hardware: HardwareProfile
    ) -> Dict:
        """Check if concurrent models fit in VRAM"""

        concurrent_models = ['embedding', 'chat']
        concurrent_vram = 0.0

        for task in concurrent_models:
            model_id = config.get(task)
            if model_id:
                model_info = ModelRegistry.get_model(model_id)
                if model_info:
                    concurrent_vram += model_info.vram_required_gb

        max_safe = hardware.total_vram_gb * 0.9

        if concurrent_vram > hardware.total_vram_gb:
            return {
                'valid': False,
                'message': f'Concurrent models require {concurrent_vram:.1f}GB but only {hardware.total_vram_gb:.1f}GB available',
                'recommendations': [
                    'Reduce to smaller models',
                    'Use 7b models instead of 14b',
                    'Ensure no other applications are using GPU',
                ],
            }

        elif concurrent_vram > max_safe:
            return {
                'valid': False,
                'message': f'Concurrent usage ({concurrent_vram:.1f}GB) exceeds safe limit ({max_safe:.1f}GB)',
                'recommendations': [
                    'Reduce to smaller models to leave VRAM buffer',
                    'System may crash or become unstable',
                ],
            }

        else:
            return {
                'valid': True,
                'message': f'Concurrent models fit comfortably ({concurrent_vram:.1f}GB / {hardware.total_vram_gb:.1f}GB)',
                'recommendations': [],
            }

    @staticmethod
    def _check_swappable_models(
        config: Dict[str, str],
        hardware: HardwareProfile
    ) -> Dict:
        """Check if swappable models can be loaded"""

        swappable_models = ['planning', 'coding']

        for task in swappable_models:
            model_id = config.get(task)
            if model_id:
                model_info = ModelRegistry.get_model(model_id)
                if model_info:
                    if model_info.vram_required_gb > hardware.total_vram_gb:
                        return {
                            'valid': False,
                            'message': f'{task.capitalize()} model ({model_id}) requires {model_info.vram_required_gb:.1f}GB but only {hardware.total_vram_gb:.1f}GB total',
                            'recommendations': [
                                f'Use smaller model for {task}',
                                f'Consider 7b instead of 14b',
                            ],
                        }

        return {
            'valid': True,
            'message': 'Swappable models can be loaded',
            'recommendations': [],
        }

    @staticmethod
    def _generate_recommendations(
        config: Dict[str, str],
        hardware: HardwareProfile,
        vram_analysis: Dict
    ) -> List[str]:
        """Generate configuration recommendations"""

        recommendations = []

        # Recommend based on VRAM
        if hardware.total_vram_gb >= 16:
            recommendations.append(
                'Your GPU can handle 14b models for all tasks without swapping'
            )
            if config.get('chat') != 'qwen2.5-coder:14b-instruct-q4_K_M':
                recommendations.append(
                    'Consider upgrading chat model to 14b for better quality'
                )

        elif hardware.total_vram_gb >= 8:
            recommendations.append(
                'Your configuration is optimal for 8GB VRAM'
            )
            if vram_analysis['requires_swapping']:
                recommendations.append(
                    'Planning/Coding will swap models (~2-3s delay) - this is normal'
                )

        else:
            recommendations.append(
                'Consider using 7b models for all tasks on 4-6GB GPU'
            )

        # Performance recommendations
        if vram_analysis['utilization_percent'] > 85:
            recommendations.append(
                'Close other GPU-intensive applications for best performance'
            )

        return recommendations

    @staticmethod
    def suggest_optimal_config(
        hardware: HardwareProfile,
        priority: str = 'balanced'
    ) -> Dict[str, str]:
        """
        Suggest optimal model configuration

        Args:
            hardware: Hardware profile
            priority: 'speed', 'quality', or 'balanced'

        Returns:
            Optimal model configuration
        """

        vram = hardware.total_vram_gb

        # High-end GPU (16GB+)
        if vram >= 16:
            return {
                'embedding': 'bge-m3',
                'chat': 'qwen2.5-coder:14b-instruct-q4_K_M',
                'planning': 'qwen2.5-coder:14b-instruct-q4_K_M',
                'coding': 'qwen2.5-coder:14b-instruct-q4_K_M',
            }

        # Mid-range GPU (8-16GB)
        elif vram >= 8:
            if priority == 'speed':
                # All 7b for speed
                return {
                    'embedding': 'bge-m3',
                    'chat': 'qwen2.5-coder:7b-instruct-q4_K_M',
                    'planning': 'qwen2.5-coder:7b-instruct-q4_K_M',
                    'coding': 'qwen2.5-coder:7b-instruct-q4_K_M',
                }
            elif priority == 'quality':
                # 14b for important tasks (with swapping)
                return {
                    'embedding': 'bge-m3',
                    'chat': 'qwen2.5-coder:14b-instruct-q4_K_M',
                    'planning': 'qwen2.5-coder:14b-instruct-q4_K_M',
                    'coding': 'qwen2.5-coder:14b-instruct-q4_K_M',
                }
            else:  # balanced (recommended)
                return {
                    'embedding': 'bge-m3',
                    'chat': 'qwen2.5-coder:7b-instruct-q4_K_M',
                    'planning': 'qwen2.5-coder:14b-instruct-q4_K_M',
                    'coding': 'qwen2.5-coder:14b-instruct-q4_K_M',
                }

        # Low-end GPU (4-8GB)
        else:
            return {
                'embedding': 'bge-m3',
                'chat': 'qwen2.5-coder:7b-instruct-q4_K_M',
                'planning': 'qwen2.5-coder:7b-instruct-q4_K_M',
                'coding': 'qwen2.5-coder:7b-instruct-q4_K_M',
            }
```

---

## 📊 Resource Monitoring

### Comprehensive Resource Monitor

```python
# backend/src/services/llm/resource_monitor.py

import asyncio
import psutil
import GPUtil
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class ResourceSnapshot:
    """Complete resource usage snapshot"""
    timestamp: datetime

    # GPU
    gpu_name: str
    vram_total_gb: float
    vram_used_gb: float
    vram_free_gb: float
    gpu_utilization_percent: float
    gpu_temperature_c: Optional[float]

    # CPU
    cpu_percent: float
    cpu_count: int
    cpu_freq_mhz: float

    # RAM
    ram_total_gb: float
    ram_used_gb: float
    ram_available_gb: float
    ram_percent: float

    # Process-specific
    process_cpu_percent: float
    process_memory_mb: float

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'gpu': {
                'name': self.gpu_name,
                'vram_total_gb': self.vram_total_gb,
                'vram_used_gb': self.vram_used_gb,
                'vram_free_gb': self.vram_free_gb,
                'utilization_percent': self.gpu_utilization_percent,
                'temperature_c': self.gpu_temperature_c,
            },
            'cpu': {
                'utilization_percent': self.cpu_percent,
                'count': self.cpu_count,
                'frequency_mhz': self.cpu_freq_mhz,
            },
            'ram': {
                'total_gb': self.ram_total_gb,
                'used_gb': self.ram_used_gb,
                'available_gb': self.ram_available_gb,
                'utilization_percent': self.ram_percent,
            },
            'process': {
                'cpu_percent': self.process_cpu_percent,
                'memory_mb': self.process_memory_mb,
            },
        }

class ResourceMonitor:
    """Monitor system and process resources"""

    def __init__(self):
        self.process = psutil.Process()
        self._history: List[ResourceSnapshot] = []
        self._max_history = 3600  # 1 hour

        self._monitoring = False
        self._monitor_task: Optional[asyncio.Task] = None

    def get_snapshot(self) -> ResourceSnapshot:
        """Get current resource snapshot"""

        # GPU info
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            gpu_name = gpu.name
            vram_total = gpu.memoryTotal / 1024
            vram_free = gpu.memoryFree / 1024
            vram_used = vram_total - vram_free
            gpu_util = gpu.load * 100
            gpu_temp = gpu.temperature
        else:
            gpu_name = "No GPU"
            vram_total = vram_free = vram_used = gpu_util = 0
            gpu_temp = None

        # CPU info
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        cpu_freq_mhz = cpu_freq.current if cpu_freq else 0

        # RAM info
        ram = psutil.virtual_memory()
        ram_total = ram.total / (1024 ** 3)
        ram_used = ram.used / (1024 ** 3)
        ram_available = ram.available / (1024 ** 3)
        ram_percent = ram.percent

        # Process info
        try:
            process_cpu = self.process.cpu_percent()
            process_mem = self.process.memory_info().rss / (1024 ** 2)
        except:
            process_cpu = 0
            process_mem = 0

        return ResourceSnapshot(
            timestamp=datetime.utcnow(),
            gpu_name=gpu_name,
            vram_total_gb=round(vram_total, 2),
            vram_used_gb=round(vram_used, 2),
            vram_free_gb=round(vram_free, 2),
            gpu_utilization_percent=round(gpu_util, 1),
            gpu_temperature_c=gpu_temp,
            cpu_percent=round(cpu_percent, 1),
            cpu_count=cpu_count,
            cpu_freq_mhz=round(cpu_freq_mhz, 0),
            ram_total_gb=round(ram_total, 2),
            ram_used_gb=round(ram_used, 2),
            ram_available_gb=round(ram_available, 2),
            ram_percent=round(ram_percent, 1),
            process_cpu_percent=round(process_cpu, 1),
            process_memory_mb=round(process_mem, 1),
        )

    async def start_monitoring(self, interval_seconds: float = 5.0):
        """Start background monitoring"""
        if self._monitoring:
            return

        self._monitoring = True
        self._monitor_task = asyncio.create_task(
            self._monitor_loop(interval_seconds)
        )
        logger.info("Resource monitoring started")

    async def stop_monitoring(self):
        """Stop background monitoring"""
        self._monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Resource monitoring stopped")

    async def _monitor_loop(self, interval: float):
        """Background monitoring loop"""
        while self._monitoring:
            try:
                snapshot = self.get_snapshot()

                # Add to history
                self._history.append(snapshot)
                if len(self._history) > self._max_history:
                    self._history.pop(0)

                # Check for issues
                self._check_resource_issues(snapshot)

                await asyncio.sleep(interval)

            except Exception as e:
                logger.error(f"Resource monitoring error: {e}")
                await asyncio.sleep(interval)

    def _check_resource_issues(self, snapshot: ResourceSnapshot):
        """Check for resource issues and log warnings"""

        # Check VRAM
        if snapshot.vram_total_gb > 0:
            vram_percent = (snapshot.vram_used_gb / snapshot.vram_total_gb) * 100

            if vram_percent > 95:
                logger.error(
                    f"CRITICAL: VRAM usage at {vram_percent:.1f}% "
                    f"({snapshot.vram_used_gb:.1f}GB / {snapshot.vram_total_gb:.1f}GB)"
                )
            elif vram_percent > 90:
                logger.warning(
                    f"High VRAM usage: {vram_percent:.1f}% "
                    f"({snapshot.vram_used_gb:.1f}GB / {snapshot.vram_total_gb:.1f}GB)"
                )

        # Check RAM
        if snapshot.ram_percent > 95:
            logger.error(
                f"CRITICAL: RAM usage at {snapshot.ram_percent:.1f}% "
                f"({snapshot.ram_used_gb:.1f}GB / {snapshot.ram_total_gb:.1f}GB)"
            )
        elif snapshot.ram_percent > 90:
            logger.warning(
                f"High RAM usage: {snapshot.ram_percent:.1f}% "
                f"({snapshot.ram_used_gb:.1f}GB / {snapshot.ram_total_gb:.1f}GB)"
            )

        # Check GPU temperature
        if snapshot.gpu_temperature_c:
            if snapshot.gpu_temperature_c > 85:
                logger.warning(
                    f"High GPU temperature: {snapshot.gpu_temperature_c}°C"
                )

    def get_statistics(self, minutes: int = 5) -> Dict:
        """Get resource statistics for last N minutes"""
        if not self._history:
            return {}

        # Get recent snapshots
        cutoff = datetime.utcnow().timestamp() - (minutes * 60)
        recent = [
            s for s in self._history
            if s.timestamp.timestamp() >= cutoff
        ]

        if not recent:
            recent = [self._history[-1]]

        # Calculate averages
        avg_vram = sum(s.vram_used_gb for s in recent) / len(recent)
        max_vram = max(s.vram_used_gb for s in recent)

        avg_cpu = sum(s.cpu_percent for s in recent) / len(recent)
        max_cpu = max(s.cpu_percent for s in recent)

        avg_ram = sum(s.ram_used_gb for s in recent) / len(recent)
        max_ram = max(s.ram_used_gb for s in recent)

        return {
            'period_minutes': minutes,
            'samples': len(recent),
            'vram': {
                'avg_used_gb': round(avg_vram, 2),
                'max_used_gb': round(max_vram, 2),
                'total_gb': recent[-1].vram_total_gb,
            },
            'cpu': {
                'avg_percent': round(avg_cpu, 1),
                'max_percent': round(max_cpu, 1),
            },
            'ram': {
                'avg_used_gb': round(avg_ram, 2),
                'max_used_gb': round(max_ram, 2),
                'total_gb': recent[-1].ram_total_gb,
            },
        }
```

---

## ⚡ Performance Optimization

### Model Loading Optimization

```python
# backend/src/services/llm/performance_optimizer.py

import asyncio
from typing import Dict, List, Optional
import time
import logging

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """Optimize model loading and inference performance"""

    def __init__(self):
        # Track operation timings
        self._timings: Dict[str, List[float]] = {
            'model_load': [],
            'model_swap': [],
            'inference': [],
            'embedding': [],
        }

        # Performance settings
        self._settings = {
            'concurrent_embeddings': 5,
            'batch_size': 32,
            'preload_enabled': True,
            'swap_prediction_enabled': True,
        }

    def record_timing(self, operation: str, duration_seconds: float):
        """Record operation timing"""
        if operation in self._timings:
            self._timings[operation].append(duration_seconds)

            # Keep only last 100 timings
            if len(self._timings[operation]) > 100:
                self._timings[operation].pop(0)

    def get_avg_timing(self, operation: str) -> float:
        """Get average timing for operation"""
        timings = self._timings.get(operation, [])
        if not timings:
            return 0.0
        return sum(timings) / len(timings)

    async def optimize_batch_embeddings(
        self,
        texts: List[str],
        embed_func,
        batch_size: Optional[int] = None
    ) -> List[List[float]]:
        """
        Optimize batch embedding generation

        Automatically adjusts batch size based on performance
        """
        if batch_size is None:
            batch_size = self._settings['batch_size']

        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            start = time.time()
            embeddings = await embed_func(batch)
            duration = time.time() - start

            all_embeddings.extend(embeddings)

            self.record_timing('embedding', duration / len(batch))

            # Adjust batch size if needed
            if duration > 5.0 and batch_size > 16:
                # Too slow, reduce batch size
                batch_size = max(16, batch_size // 2)
                logger.info(f"Reduced embedding batch size to {batch_size}")
            elif duration < 1.0 and batch_size < 64:
                # Very fast, can increase batch size
                batch_size = min(64, batch_size * 2)
                logger.info(f"Increased embedding batch size to {batch_size}")

        return all_embeddings

    async def optimize_model_loading(
        self,
        model_id: str,
        load_func
    ) -> bool:
        """Optimize model loading with retry and timing"""

        max_retries = 3

        for attempt in range(max_retries):
            try:
                start = time.time()

                result = await load_func(model_id)

                duration = time.time() - start
                self.record_timing('model_load', duration)

                logger.info(f"Model {model_id} loaded in {duration:.2f}s")

                return result

            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Model load attempt {attempt + 1} failed: {e}, retrying..."
                    )
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Model load failed after {max_retries} attempts")
                    raise

        return False

    def get_performance_report(self) -> Dict:
        """Get performance report"""
        return {
            'model_load': {
                'avg_seconds': round(self.get_avg_timing('model_load'), 2),
                'samples': len(self._timings['model_load']),
            },
            'model_swap': {
                'avg_seconds': round(self.get_avg_timing('model_swap'), 2),
                'samples': len(self._timings['model_swap']),
            },
            'inference': {
                'avg_seconds': round(self.get_avg_timing('inference'), 2),
                'samples': len(self._timings['inference']),
            },
            'embedding': {
                'avg_seconds_per_text': round(self.get_avg_timing('embedding'), 3),
                'samples': len(self._timings['embedding']),
            },
            'settings': self._settings,
        }

    def suggest_optimizations(self, hardware_profile) -> List[str]:
        """Suggest performance optimizations"""
        suggestions = []

        # Check model load times
        avg_load = self.get_avg_timing('model_load')
        if avg_load > 5.0:
            suggestions.append(
                f"Model loading is slow ({avg_load:.1f}s avg). "
                "Consider using smaller quantized models or upgrading SSD."
            )

        # Check swap times
        avg_swap = self.get_avg_timing('model_swap')
        if avg_swap > 4.0:
            suggestions.append(
                f"Model swapping is slow ({avg_swap:.1f}s avg). "
                "Consider upgrading to 16GB+ VRAM to avoid swapping."
            )

        # Check embedding performance
        avg_embed = self.get_avg_timing('embedding')
        if avg_embed > 0.5:
            suggestions.append(
                f"Embedding generation is slow ({avg_embed:.2f}s per text). "
                "Ensure GPU acceleration is enabled for bge-m3."
            )

        # Hardware-based suggestions
        if hardware_profile.total_vram_gb < 8:
            suggestions.append(
                "GPU VRAM below 8GB - consider using 7b models only"
            )

        if hardware_profile.total_ram_gb < 16:
            suggestions.append(
                "System RAM below 16GB - close other applications for best performance"
            )

        return suggestions
```

---

## ⚠️ Error Handling

### Model Management Error Handling

```python
# backend/src/services/llm/error_handler.py

from typing import Optional, Dict, Callable
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ModelErrorType(Enum):
    """Types of model management errors"""
    MODEL_NOT_FOUND = 'model_not_found'
    VRAM_OVERFLOW = 'vram_overflow'
    LOAD_TIMEOUT = 'load_timeout'
    SWAP_FAILED = 'swap_failed'
    INVALID_CONFIG = 'invalid_config'
    OLLAMA_UNAVAILABLE = 'ollama_unavailable'
    GPU_NOT_AVAILABLE = 'gpu_not_available'

class ModelManagementError(Exception):
    """Base exception for model management errors"""

    def __init__(
        self,
        error_type: ModelErrorType,
        message: str,
        details: Optional[Dict] = None,
        recovery_actions: Optional[list] = None
    ):
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        self.recovery_actions = recovery_actions or []
        super().__init__(message)

    def to_dict(self) -> Dict:
        return {
            'error_type': self.error_type.value,
            'message': self.message,
            'details': self.details,
            'recovery_actions': self.recovery_actions,
        }

class ModelErrorHandler:
    """Handle model management errors gracefully"""

    @staticmethod
    def handle_model_not_found(model_id: str) -> ModelManagementError:
        """Handle model not found error"""
        return ModelManagementError(
            error_type=ModelErrorType.MODEL_NOT_FOUND,
            message=f"Model '{model_id}' not found",
            details={'model_id': model_id},
            recovery_actions=[
                'Check if model is installed: ollama list',
                f'Pull model: ollama pull {model_id}',
                'Verify model ID is correct',
            ],
        )

    @staticmethod
    def handle_vram_overflow(
        required_gb: float,
        available_gb: float,
        model_id: str
    ) -> ModelManagementError:
        """Handle VRAM overflow error"""
        return ModelManagementError(
            error_type=ModelErrorType.VRAM_OVERFLOW,
            message=f"Insufficient VRAM: need {required_gb:.1f}GB, only {available_gb:.1f}GB available",
            details={
                'model_id': model_id,
                'required_gb': required_gb,
                'available_gb': available_gb,
            },
            recovery_actions=[
                'Close other GPU-intensive applications',
                'Use smaller model variant (e.g., 7b instead of 14b)',
                'Restart LocalPilot to free VRAM',
                'Check GPU usage: nvidia-smi',
            ],
        )

    @staticmethod
    def handle_swap_failed(
        from_model: str,
        to_model: str,
        reason: str
    ) -> ModelManagementError:
        """Handle model swap failure"""
        return ModelManagementError(
            error_type=ModelErrorType.SWAP_FAILED,
            message=f"Failed to swap from {from_model} to {to_model}: {reason}",
            details={
                'from_model': from_model,
                'to_model': to_model,
                'reason': reason,
            },
            recovery_actions=[
                'Retry operation',
                'Restart backend service',
                'Check Ollama is running',
            ],
        )

    @staticmethod
    def handle_ollama_unavailable() -> ModelManagementError:
        """Handle Ollama service unavailable"""
        return ModelManagementError(
            error_type=ModelErrorType.OLLAMA_UNAVAILABLE,
            message="Ollama service is not available",
            details={},
            recovery_actions=[
                'Start Ollama: ollama serve',
                'Check if Ollama is running: curl http://localhost:11434/api/tags',
                'Verify Ollama is installed correctly',
                'Check firewall settings',
            ],
        )

    @staticmethod
    async def with_retry(
        func: Callable,
        max_retries: int = 3,
        backoff_seconds: float = 2.0,
        error_handler: Optional[Callable] = None
    ):
        """Execute function with retry logic"""

        for attempt in range(max_retries):
            try:
                return await func()

            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {e}, retrying in {backoff_seconds}s..."
                    )
                    await asyncio.sleep(backoff_seconds * (2 ** attempt))
                else:
                    if error_handler:
                        error_handler(e)
                    raise
```

---

## ⚙️ Configuration Management

### Model Configuration Service

```python
# backend/src/services/llm/config_manager.py

from typing import Dict, Optional
from pathlib import Path
import json
import logging
from .model_validator import ModelValidator
from .hardware_profile import HardwareDetector

logger = logging.getLogger(__name__)

class ModelConfigManager:
    """Manage model configuration persistence and updates"""

    def __init__(self, config_path: str = '.localpilot/model_config.json'):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        self._config: Optional[Dict[str, str]] = None
        self._validated = False

    def load_config(self) -> Dict[str, str]:
        """Load configuration from disk"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self._config = json.load(f)
                logger.info(f"Loaded model config from {self.config_path}")
                return self._config
            except Exception as e:
                logger.error(f"Failed to load config: {e}")

        # Return default config
        hardware = HardwareDetector.detect()
        self._config = ModelValidator.suggest_optimal_config(hardware)
        logger.info("Using default optimal configuration")

        return self._config

    def save_config(self, config: Dict[str, str]) -> bool:
        """Save configuration to disk"""
        try:
            # Validate before saving
            hardware = HardwareDetector.detect()
            validation = ModelValidator.validate_configuration(config, hardware)

            if not validation.valid:
                logger.error(f"Cannot save invalid config: {validation.message}")
                return False

            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)

            self._config = config
            self._validated = True

            logger.info(f"Saved model config to {self.config_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def get_config(self) -> Dict[str, str]:
        """Get current configuration"""
        if self._config is None:
            self.load_config()
        return self._config

    def update_config(self, updates: Dict[str, str]) -> bool:
        """Update configuration with validation"""
        current = self.get_config()
        new_config = {**current, **updates}

        return self.save_config(new_config)

    def validate_current_config(self) -> Dict:
        """Validate current configuration"""
        config = self.get_config()
        hardware = HardwareDetector.detect()

        validation = ModelValidator.validate_configuration(config, hardware)

        return validation.to_dict()

    def reset_to_optimal(self) -> Dict[str, str]:
        """Reset to hardware-optimal configuration"""
        hardware = HardwareDetector.detect()
        optimal = ModelValidator.suggest_optimal_config(hardware)

        self.save_config(optimal)

        return optimal
```

---

## 📚 Related Documents

- `PROJECT_CHARTER.md` - Vision and timeline
- `TECHNICAL_ARCHITECTURE.md` - System architecture
- `INDEXING_SYSTEM_SPEC.md` - Indexing pipeline
- `DEVELOPMENT_GUIDE.md` - Setup and workflow
- `TESTING_STRATEGY.md` - Test specifications (PREVIOUS)
- `RAG_SYSTEM_SPEC.md` - RAG implementation (NEXT)
- `PHASE_1_IMPLEMENTATION.md` - Implementation roadmap

---

**END OF DOCUMENT**
