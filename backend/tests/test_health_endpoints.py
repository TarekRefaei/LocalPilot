"""
Tests for health check and configuration endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app
from app.api import health

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for GET /health endpoint."""

    def test_health_returns_200(self):
        """Health endpoint should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_structure(self):
        """Health response should have required fields."""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "version" in data
        assert "uptime_seconds" in data
        assert "services" in data
        assert "resources" in data
        assert "timestamp" in data

    def test_health_status_is_healthy(self):
        """Health status should be 'healthy'."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_version_matches_config(self):
        """Health version should match app version."""
        response = client.get("/health")
        data = response.json()
        assert data["version"] == "0.1.0"

    def test_health_services_structure(self):
        """Services should have status and details."""
        response = client.get("/health")
        data = response.json()
        services = data["services"]

        assert "ollama" in services
        assert "vector_db" in services

        for service_name, service_data in services.items():
            assert "status" in service_data
            assert service_data["status"] in ["connected", "ready", "error"]

    def test_health_resources_structure(self):
        """Resources should have VRAM and RAM info."""
        response = client.get("/health")
        data = response.json()
        resources = data["resources"]

        assert "vram_usage_gb" in resources
        assert "vram_total_gb" in resources
        assert "ram_usage_gb" in resources
        assert "ram_total_gb" in resources

        # All should be numbers
        assert isinstance(resources["vram_usage_gb"], (int, float))
        assert isinstance(resources["vram_total_gb"], (int, float))
        assert isinstance(resources["ram_usage_gb"], (int, float))
        assert isinstance(resources["ram_total_gb"], (int, float))

    def test_health_uptime_increases(self):
        """Uptime should increase with time."""
        response1 = client.get("/health")
        uptime1 = response1.json()["uptime_seconds"]

        # Small delay
        import time

        time.sleep(0.1)

        response2 = client.get("/health")
        uptime2 = response2.json()["uptime_seconds"]

        assert uptime2 >= uptime1


class TestOllamaHealthEndpoint:
    """Tests for GET /health/ollama endpoint."""

    def test_ollama_health_returns_200(self):
        """Ollama health endpoint should return 200 OK."""
        response = client.get("/health/ollama")
        assert response.status_code == 200

    def test_ollama_health_response_structure(self):
        """Ollama health response should have required fields."""
        response = client.get("/health/ollama")
        data = response.json()

        assert "status" in data
        assert "host" in data
        assert "version" in data
        assert "models" in data

    def test_ollama_status_is_connected(self):
        """Ollama status should be 'connected'."""
        response = client.get("/health/ollama")
        data = response.json()
        assert data["status"] == "connected"

    def test_ollama_models_structure(self):
        """Models should have name, size_gb, and loaded fields."""
        response = client.get("/health/ollama")
        data = response.json()
        models = data["models"]

        assert len(models) > 0

        for model in models:
            assert "name" in model
            assert "size_gb" in model
            assert "loaded" in model
            assert isinstance(model["loaded"], bool)


class TestConfigEndpoint:
    """Tests for GET /config endpoint."""

    def test_config_returns_200(self):
        """Config endpoint should return 200 OK."""
        response = client.get("/config")
        assert response.status_code == 200

    def test_config_response_structure(self):
        """Config response should have required fields."""
        response = client.get("/config")
        data = response.json()

        assert "app_name" in data
        assert "app_version" in data
        assert "debug" in data
        assert "host" in data
        assert "port" in data
        assert "ollama_host" in data
        assert "log_level" in data
        assert "timestamp" in data

    def test_config_values(self):
        """Config should return correct values."""
        response = client.get("/config")
        data = response.json()

        assert data["app_name"] == "LocalPilot Backend"
        assert data["app_version"] == "0.1.0"
        assert isinstance(data["debug"], bool)
        assert data["host"] == "127.0.0.1"
        assert data["port"] == 8765
        assert "localhost" in data["ollama_host"]
