from __future__ import annotations

import os
from functools import lru_cache
from typing import Mapping

from pydantic import BaseModel, Field, field_validator


def _env_value(environ: Mapping[str, str], name: str, default: str | None = None) -> str | None:
    value = environ.get(name)
    if value is None or value == "":
        return default
    return value


class OpenAICompatibleSettings(BaseModel):
    base_url: str = Field(default="https://api.openai.com/v1")
    api_key: str | None = Field(default=None)
    chat_model: str | None = Field(default=None)
    timeout_seconds: float = Field(default=60.0)

    @field_validator("base_url")
    @classmethod
    def normalize_base_url(cls, value: str) -> str:
        normalized = value.rstrip("/")
        if not normalized.startswith(("https://", "http://")):
            raise ValueError("OPENAI_COMPATIBLE_BASE_URL must be an http(s) URL")
        return normalized

    @field_validator("timeout_seconds")
    @classmethod
    def validate_timeout(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("OPENAI_COMPATIBLE_TIMEOUT_SECONDS must be positive")
        return value

    def missing_required_values(self) -> tuple[str, ...]:
        missing: list[str] = []
        if not self.api_key:
            missing.append("OPENAI_COMPATIBLE_API_KEY")
        if not self.chat_model:
            missing.append("OPENAI_COMPATIBLE_CHAT_MODEL")
        return tuple(missing)

    @property
    def is_configured(self) -> bool:
        return not self.missing_required_values()


class Settings(BaseModel):
    app_name: str = Field(default="Legal RAG Assistant API")
    environment: str = Field(default="local")
    legal_scope: str = Field(default="labor_law")
    database_url: str | None = Field(default=None)
    llm: OpenAICompatibleSettings = Field(default_factory=OpenAICompatibleSettings)

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "Settings":
        source = environ or os.environ
        timeout = _env_value(source, "OPENAI_COMPATIBLE_TIMEOUT_SECONDS", "60")

        return cls(
            app_name=_env_value(source, "APP_NAME", "Legal RAG Assistant API"),
            environment=_env_value(source, "APP_ENV", "local"),
            legal_scope=_env_value(source, "LEGAL_SCOPE", "labor_law"),
            database_url=_env_value(source, "DATABASE_URL"),
            llm=OpenAICompatibleSettings(
                base_url=_env_value(
                    source,
                    "OPENAI_COMPATIBLE_BASE_URL",
                    "https://api.openai.com/v1",
                ),
                api_key=_env_value(source, "OPENAI_COMPATIBLE_API_KEY"),
                chat_model=_env_value(source, "OPENAI_COMPATIBLE_CHAT_MODEL"),
                timeout_seconds=float(timeout or "60"),
            ),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
