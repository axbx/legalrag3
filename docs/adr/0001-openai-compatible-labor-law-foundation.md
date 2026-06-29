# ADR 0001: OpenAI-Compatible Provider and Labor-Law Scope

## Status

Accepted

## Context

The Legal RAG Assistant must be implemented as a real source-grounded legal
system, not as a demo chat. Runtime LLM behavior must use an OpenAI-compatible
API contract and must not silently fall back to fake or simplified providers.

The first production scope is limited by legal domain: labor law. This is a
domain scope choice, not a reduction in required system functionality. The
solution still needs ingestion, retrieval, claim verification, citation
verification, human review, audit trail, security controls, and evals.

## Decision

- Use an OpenAI-compatible chat-completions API as the first LLM provider
  contract.
- Configure provider access through environment variables:
  `OPENAI_COMPATIBLE_BASE_URL`, `OPENAI_COMPATIBLE_API_KEY`,
  `OPENAI_COMPATIBLE_CHAT_MODEL`, and `OPENAI_COMPATIBLE_TIMEOUT_SECONDS`.
- Do not include a fake runtime LLM provider in application code.
- Expose readiness as not ready when OpenAI-compatible provider credentials are
  missing.
- Treat `labor_law` as the initial legal scope while keeping architecture
  components broad enough for the full product requirements.

## Consequences

- Local development can start the API without secrets, but readiness will report
  the provider as not ready until real credentials and a model are configured.
- Tests may validate configuration and client construction without making LLM
  network calls.
- Future research, drafting, verification, and review flows must depend on this
  provider interface or a compatible successor, not on a fake provider branch.
