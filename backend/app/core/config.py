"""
Configuration management for LocalPilot backend.
Supports environment variables and .env files.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    app_name: str = "LocalPilot Backend"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server
    host: str = "127.0.0.1"
    port: int = 8765
    reload: bool = False

    # WebSocket
    ws_heartbeat_interval_ms: int = 30000
    ws_heartbeat_timeout_ms: int = 10000
    ws_handshake_timeout_ms: int = 5000

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # "json" or "text"

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_timeout_seconds: int = 120

    # Vector DB
    vector_db_path: str = "./data/chroma"

    # Act/execution safety settings
    act_apply_safety: str = "strict"
    act_autoapprove_safe_creates: bool = True
    act_autoapprove_config_files: bool = False
    act_approval_timeout_seconds: int = 300

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
