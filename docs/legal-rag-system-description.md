# Technical System Description: Legal RAG Assistant

## 1. Purpose

Legal RAG Assistant is a retrieval-augmented generation system for legal work. Its purpose is to answer legal questions, analyze legal documents, and help prepare legal drafts using a controlled corpus of legal sources rather than relying only on the language model's internal knowledge.

The system description in this document is intended to be an input source for later implementation by an agent. It defines product boundaries, core workflows, architecture, data model, quality requirements, and an implementation backlog.

## 2. Target Users

- Lawyers and legal consultants who need fast source-backed analysis.
- In-house legal teams that work with internal policies, contracts, and legal knowledge bases.
- Compliance specialists who need traceable answers based on statutes, regulations, guidance, and company documents.
- Product or operations teams that need legal triage before escalation to counsel.

## 3. Core Principles

1. **Source-grounded answers.** Every substantive legal conclusion should be backed by cited retrieved sources.
2. **Jurisdiction awareness.** The assistant must ask for or infer the applicable jurisdiction and date context before producing legal analysis.
3. **No hidden legal authority.** The model must distinguish binding law, persuasive authority, internal documents, templates, and generated reasoning.
4. **Uncertainty disclosure.** If the corpus is incomplete, sources conflict, or retrieval confidence is low, the assistant must say so and recommend human review.
5. **Auditability.** The system must preserve source IDs, chunks, prompts, model versions, and output metadata for review.
6. **Privacy by default.** User uploads and confidential legal materials must be isolated by tenant and access policy.

## 4. Non-Goals for the MVP

- Replacing a licensed attorney or providing final legal advice without human review.
- Full e-discovery processing, litigation hold, or matter management.
- Automatic filing with courts or regulators.
- Guaranteed real-time law updates without an ingestion/update pipeline.
- Autonomous execution of legal actions or external communications.

## 5. MVP Use Cases

### 5.1 Legal Q&A

A user asks a legal question. The system identifies missing context, retrieves relevant materials, and returns a structured answer with citations.

Required output structure:

- short answer;
- assumptions and jurisdiction/date context;
- analysis with citations;
- risks and exceptions;
- recommended next steps;
- disclaimer that human legal review may be required.

### 5.2 Document Review

A user uploads or selects a contract, policy, pleading, memo, or regulation. The system extracts issues, compares text against legal or policy sources, and produces a review report.

Required output structure:

- document summary;
- key clauses or sections;
- detected issues and risk levels;
- source-backed explanation;
- proposed edits or negotiation points;
- open questions for counsel.

### 5.3 Drafting Assistance

A user requests a clause, letter, memo, checklist, or policy. The system retrieves relevant templates and rules, then drafts a document section with citations and editable assumptions.

Required output structure:

- draft text;
- drafting assumptions;
- source references;
- optional alternatives;
- review checklist.

### 5.4 Corpus Exploration

A user asks what the legal knowledge base contains on a topic. The system returns source clusters, representative documents, and gaps.

Required output structure:

- topic overview;
- source groups;
- important documents;
- coverage gaps;
- suggested ingestion updates.

## 6. High-Level Architecture

```text
User Interface
  -> API Gateway / Backend
    -> Authentication and Tenant Context
    -> Conversation Orchestrator
      -> Query Understanding
      -> Retrieval Planner
      -> Hybrid Retrieval
        -> Keyword Index
        -> Vector Index
        -> Metadata Filters
      -> Reranker
      -> Context Builder
      -> LLM Answer Generator
      -> Citation Verifier
      -> Safety and Policy Checks
    -> Audit Log
    -> Response Store

Document Ingestion Pipeline
  -> Upload / Connector
  -> File Normalization
  -> OCR if needed
  -> Text Extraction
  -> Metadata Extraction
  -> Chunking
  -> Embedding
  -> Indexing
  -> Quality Report
```

## 7. Main Components

### 7.1 User Interface

The UI should support:

- chat-based legal questions;
- document upload and document selection;
- visible citations linked to source snippets;
- jurisdiction, date, and matter controls;
- answer export to Markdown or PDF;
- feedback actions such as correct, incomplete, wrong citation, and needs lawyer review.

### 7.2 API Gateway / Backend

The backend should expose stable endpoints for:

- conversations and messages;
- document upload and ingestion status;
- search and source preview;
- generated answer requests;
- feedback and audit retrieval;
- admin corpus management.

### 7.3 Authentication, Authorization, and Tenancy

Minimum requirements:

- user authentication;
- tenant or workspace isolation;
- document-level access checks before retrieval;
- role separation for user, reviewer, and admin;
- audit trail for document access and answer generation.

### 7.4 Ingestion Pipeline

The ingestion pipeline converts legal materials into retrieval-ready records.

Input formats:

- PDF;
- DOCX;
- TXT/Markdown;
- HTML;
- CSV metadata exports;
- future connectors for document management systems or public legal sources.

Pipeline stages:

1. store the raw file;
2. extract text and page anchors;
3. run OCR when extracted text quality is low;
4. detect document type, jurisdiction, dates, parties, and source category;
5. split text into chunks while preserving legal structure;
6. create embeddings;
7. index chunks in vector and keyword stores;
8. produce an ingestion quality report.

### 7.5 Retrieval

Retrieval should be hybrid:

- keyword search for exact terms, statutes, citations, clause names, and defined terms;
- vector search for semantic similarity;
- metadata filtering for jurisdiction, source type, tenant, matter, effective date, and confidentiality;
- reranking to prioritize authoritative and contextually relevant chunks.

Retrieval output must include:

- document ID;
- chunk ID;
- source title;
- page or section anchor;
- source type;
- jurisdiction;
- effective date or publication date;
- confidence or rank score.

### 7.6 Context Builder

The context builder should construct the LLM prompt from:

- user question;
- conversation state;
- jurisdiction/date/matter context;
- top retrieved chunks;
- source metadata;
- required answer format;
- safety instructions.

It must avoid overloading context with duplicate chunks and should preserve enough surrounding text for citation verification.

### 7.7 LLM Answer Generator

The generator should:

- answer only from retrieved sources when the task requires legal authority;
- mark unsupported statements as assumptions or general information;
- include citations next to specific claims;
- ask a clarifying question when critical context is missing;
- avoid fabricating statutes, cases, citations, parties, dates, or quotes.

### 7.8 Citation Verifier

The citation verifier should validate that:

- each citation points to a retrieved chunk;
- cited chunks actually support the claim;
- quoted text is present in the source;
- answer claims without support are marked or removed;
- citation links resolve to the correct page or section.

For the MVP, verification may be implemented as deterministic checks plus an LLM self-check pass. Later versions should add more robust entailment and quote validation.

### 7.9 Safety and Legal Policy Layer

The policy layer should detect and handle:

- requests to bypass law, commit fraud, hide evidence, or evade regulators;
- requests for definitive legal advice when facts or jurisdiction are missing;
- conflicts between sources;
- privileged or confidential information exposure;
- personal data and sensitive data in uploaded documents.

The assistant should provide safe alternatives, such as recommending lawful compliance steps or human counsel review.

## 8. Data Model

### 8.1 Document

Recommended fields:

- `id`;
- `tenant_id`;
- `title`;
- `source_uri`;
- `source_type`;
- `jurisdiction`;
- `language`;
- `publication_date`;
- `effective_date`;
- `version`;
- `confidentiality_level`;
- `created_at`;
- `updated_at`.

### 8.2 Chunk

Recommended fields:

- `id`;
- `document_id`;
- `tenant_id`;
- `text`;
- `section_path`;
- `page_start`;
- `page_end`;
- `token_count`;
- `embedding_id`;
- `metadata`.

### 8.3 Conversation and Message

Recommended fields:

- `conversation_id`;
- `tenant_id`;
- `user_id`;
- `matter_id`;
- `jurisdiction`;
- `created_at`;
- `message_id`;
- `role`;
- `content`;
- `retrieval_trace_id`;
- `model`;
- `prompt_version`.

### 8.4 Retrieval Trace

Recommended fields:

- `trace_id`;
- `query`;
- `filters`;
- `retrieved_chunk_ids`;
- `reranked_chunk_ids`;
- `scores`;
- `selected_context_chunk_ids`;
- `created_at`.

### 8.5 Answer Citation

Recommended fields:

- `answer_id`;
- `claim_id`;
- `document_id`;
- `chunk_id`;
- `page`;
- `section_path`;
- `support_status`.

## 9. Prompting Requirements

System prompt requirements:

- define the assistant as a legal RAG assistant, not a lawyer;
- require jurisdiction/date clarification when missing;
- require source-grounded answers;
- prohibit fabricated citations;
- require uncertainty disclosure;
- require concise but complete structure;
- require refusal or redirection for unlawful requests.

Per-task prompt templates should exist for:

- legal Q&A;
- document review;
- drafting;
- corpus exploration;
- citation verification.

Prompt templates should be versioned and included in audit metadata.

## 10. Quality Metrics

### 10.1 Retrieval Metrics

- recall at K for known-answer test sets;
- precision at K;
- metadata filter accuracy;
- duplicate chunk rate;
- stale source rate.

### 10.2 Answer Metrics

- citation support rate;
- hallucinated citation rate;
- unsupported claim rate;
- jurisdiction/date handling accuracy;
- refusal correctness for unsafe requests;
- human reviewer usefulness score.

### 10.3 Operational Metrics

- ingestion success rate;
- ingestion latency;
- answer latency;
- retrieval latency;
- model cost per answer;
- feedback rate;
- error rate.

## 11. Suggested MVP Implementation Plan

### Phase 1: Repository and Documentation Foundation

- Keep this system description as the implementation source of truth.
- Add architecture decision records when technology choices are made.
- Define initial prompt templates and evaluation examples.

### Phase 2: Minimal Ingestion and Retrieval

- Implement document upload for text and PDF files.
- Extract text and create chunks with source anchors.
- Add a local or hosted vector store.
- Add keyword search or database full-text search.
- Return source previews from search.

### Phase 3: RAG Answering

- Add conversation API.
- Add retrieval planner and context builder.
- Integrate an LLM answer generator.
- Render citations in responses.
- Store retrieval traces and answer metadata.

### Phase 4: Verification and Evaluation

- Add citation validation checks.
- Create a small legal QA benchmark set.
- Track retrieval and answer metrics.
- Add reviewer feedback capture.

### Phase 5: Security and Multi-Tenant Hardening

- Add tenant isolation tests.
- Add role-based access control.
- Add audit log views.
- Add retention and deletion policies.

## 12. Open Questions for Product and Legal Review

1. Which jurisdictions must the MVP support first?
2. Which source corpus is authoritative for the first release?
3. Are user uploads stored permanently, per matter, or only temporarily?
4. What confidentiality model is required for privileged documents?
5. Which LLM provider and model classes are acceptable for legal data?
6. What is the required human-review workflow before external use?
7. Should the assistant support Russian, English, or both in the MVP?
8. Which output formats are required first: chat only, Markdown, PDF, DOCX, or all?

## 13. Acceptance Criteria for DEV-4

- A technical system description exists in the repository.
- The description is specific enough for a future implementation agent to derive issues and tasks.
- The description covers purpose, users, use cases, architecture, components, data model, prompts, metrics, phases, and open questions.
- The document does not change production application behavior.
