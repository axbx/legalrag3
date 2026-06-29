from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from app.core.config import get_settings

router = APIRouter(tags=["health"])


class LLMProviderStatus(BaseModel):
    provider: str
    base_url: str
    chat_model: str | None
    api_key_configured: bool
    ready: bool
    missing: list[str]


class HealthResponse(BaseModel):
    service: str
    environment: str
    status: str
    legal_scope: str


class ReadinessResponse(HealthResponse):
    llm: LLMProviderStatus


def _llm_status() -> LLMProviderStatus:
    settings = get_settings()
    missing = list(settings.llm.missing_required_values())
    return LLMProviderStatus(
        provider="openai-compatible",
        base_url=settings.llm.base_url,
        chat_model=settings.llm.chat_model,
        api_key_configured=bool(settings.llm.api_key),
        ready=not missing,
        missing=missing,
    )


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        service=settings.app_name,
        environment=settings.environment,
        status="ok",
        legal_scope=settings.legal_scope,
    )


@router.get("/api/v1/readiness", response_model=ReadinessResponse)
def readiness(response: Response) -> ReadinessResponse:
    settings = get_settings()
    llm_status = _llm_status()
    ready = llm_status.ready
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadinessResponse(
        service=settings.app_name,
        environment=settings.environment,
        status="ready" if ready else "not_ready",
        legal_scope=settings.legal_scope,
        llm=llm_status,
    )
