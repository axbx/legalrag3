from __future__ import annotations

from typing import Any, Literal

import httpx
from pydantic import BaseModel, Field

from app.core.config import OpenAICompatibleSettings


class OpenAICompatibleError(RuntimeError):
    """Base error for OpenAI-compatible provider failures."""


class OpenAICompatibleConfigurationError(OpenAICompatibleError):
    """Raised when required provider settings are not configured."""


class OpenAICompatibleAPIError(OpenAICompatibleError):
    """Raised when the provider returns an error response."""


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str


class ChatCompletionResult(BaseModel):
    content: str
    model: str | None
    raw_response: dict[str, Any]


class OpenAICompatibleClient:
    """HTTP client for OpenAI-compatible chat completion APIs.

    The product runtime has no fake provider path. Tests may validate payloads
    and configuration locally, but generated answers must come from the
    configured OpenAI-compatible endpoint.
    """

    def __init__(self, settings: OpenAICompatibleSettings) -> None:
        missing = settings.missing_required_values()
        if missing:
            joined = ", ".join(missing)
            raise OpenAICompatibleConfigurationError(f"Missing OpenAI-compatible settings: {joined}")
        self._settings = settings

    async def create_chat_completion(
        self,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.0,
        max_tokens: int | None = None,
        extra_body: dict[str, Any] | None = None,
    ) -> ChatCompletionResult:
        body: dict[str, Any] = {
            "model": self._settings.chat_model,
            "messages": [message.model_dump() for message in messages],
            "temperature": temperature,
        }
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if extra_body:
            body.update(extra_body)

        async with httpx.AsyncClient(timeout=self._settings.timeout_seconds) as client:
            response = await client.post(
                f"{self._settings.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._settings.api_key}",
                    "Content-Type": "application/json",
                },
                json=body,
            )

        if response.status_code >= 400:
            raise OpenAICompatibleAPIError(
                f"OpenAI-compatible API returned HTTP {response.status_code}: {response.text}"
            )

        payload = response.json()
        try:
            choice = payload["choices"][0]
            message = choice["message"]
            content = message["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise OpenAICompatibleAPIError("OpenAI-compatible API response did not include message content") from exc

        if not isinstance(content, str):
            raise OpenAICompatibleAPIError("OpenAI-compatible API message content must be a string")

        return ChatCompletionResult(
            content=content,
            model=payload.get("model"),
            raw_response=payload,
        )
