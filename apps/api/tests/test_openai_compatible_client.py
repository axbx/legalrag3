import pytest

from app.core.config import OpenAICompatibleSettings
from app.llm.openai_compatible import (
    OpenAICompatibleClient,
    OpenAICompatibleConfigurationError,
)


def test_openai_compatible_client_rejects_missing_runtime_configuration() -> None:
    settings = OpenAICompatibleSettings(
        api_key=None,
        chat_model=None,
    )

    with pytest.raises(OpenAICompatibleConfigurationError) as exc_info:
        OpenAICompatibleClient(settings)

    message = str(exc_info.value)
    assert "OPENAI_COMPATIBLE_API_KEY" in message
    assert "OPENAI_COMPATIBLE_CHAT_MODEL" in message


def test_openai_compatible_client_accepts_complete_runtime_configuration() -> None:
    settings = OpenAICompatibleSettings(
        base_url="https://llm.example.test/v1/",
        api_key="test-key",
        chat_model="test-model",
    )

    client = OpenAICompatibleClient(settings)

    assert client is not None
    assert settings.base_url == "https://llm.example.test/v1"
