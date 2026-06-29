from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


client = TestClient(app)


def test_health_reports_service_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "Legal RAG Assistant API"
    assert body["status"] == "ok"
    assert body["legal_scope"] == "labor_law"


def test_readiness_requires_openai_compatible_configuration(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_COMPATIBLE_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_COMPATIBLE_CHAT_MODEL", raising=False)
    get_settings.cache_clear()

    response = client.get("/api/v1/readiness")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["llm"]["provider"] == "openai-compatible"
    assert body["llm"]["ready"] is False
    assert body["llm"]["missing"] == [
        "OPENAI_COMPATIBLE_API_KEY",
        "OPENAI_COMPATIBLE_CHAT_MODEL",
    ]


def test_readiness_accepts_configured_openai_compatible_provider(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_COMPATIBLE_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_COMPATIBLE_CHAT_MODEL", "test-model")
    monkeypatch.setenv("OPENAI_COMPATIBLE_BASE_URL", "https://llm.example.test/v1/")
    get_settings.cache_clear()

    response = client.get("/api/v1/readiness")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["llm"]["base_url"] == "https://llm.example.test/v1"
    assert body["llm"]["chat_model"] == "test-model"
    assert body["llm"]["api_key_configured"] is True
    assert body["llm"]["missing"] == []
