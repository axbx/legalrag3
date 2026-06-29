# legalrag3

Minimal workspace for experimenting with the MVP solo agentic workflow.

## Legal RAG Assistant Requirements

The primary technical requirements for the Legal RAG Assistant are in
`docs/legal-rag-system-description.md`. This document is the source input for
future agent-driven implementation tasks.

## API Foundation

The backend skeleton lives in `apps/api`. Runtime LLM features are configured
through an OpenAI-compatible `/v1/chat/completions` API; there is no fake
runtime LLM provider.

Run local API tests from the repository root:

```bash
python3 -m pytest
```

Start the API directly:

```bash
PYTHONPATH=apps/api uvicorn app.main:app --reload
```

Required LLM settings are documented in `.env.example`. `/health` only checks
that the API process is alive; `/api/v1/readiness` reports `503` until
`OPENAI_COMPATIBLE_API_KEY` and `OPENAI_COMPATIBLE_CHAT_MODEL` are configured.

## Hello World

Open `index.html` in a browser to view the first static page.

## Linear API Helper

Routine Linear updates should use `scripts/linear_cli.py`. See
`docs/linear-api-usage.md` for setup and examples.
