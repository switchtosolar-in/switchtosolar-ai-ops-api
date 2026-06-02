# SwitchToSolar AI Ops API

SwitchToSolar AI Ops API is a FastAPI-based backend service for retrieval-grounded AI workflows, semantic search, operational AI tooling, and AI observability.

It is part of the SwitchToSolar platform and is designed as a dedicated AI systems layer separate from the main product backend. The service handles knowledge retrieval, intent routing, prompt construction, LLM execution, and query logging for internal AI-assisted workflows.

---

## Purpose

This project focuses on the backend systems required to make AI workflows more grounded, observable, and operationally useful beyond a simple prompt-response integration.

The main goals are:

- Retrieve relevant platform knowledge before generating answers
- Separate knowledge questions from operational questions
- Keep AI workflows routed through controlled backend services
- Capture metadata for debugging, evaluation, and observability
- Support future operational AI tooling without exposing unrestricted database access

---

## Core Capabilities

- Retrieval-Augmented Generation (RAG)
- Semantic retrieval using PostgreSQL + pgvector
- Knowledge base ingestion and chunk retrieval
- Intent routing for knowledge, operations, and unsupported questions
- Prompt construction using retrieved context
- OpenAI API integration
- Query logging and response metadata
- Operational AI workflow foundation
- FastAPI route separation
- Repository-based data access patterns

---

## Architecture Overview

```text
Admin / Platform Question
        |
        v
FastAPI Query Endpoint
        |
        v
Intent Router
        |
        +--------------------+--------------------+
        |                    |                    |
        v                    v                    v
Knowledge Query       Operational Query     Unsupported Query
        |                    |                    |
        v                    v                    v
RAG Pipeline          Controlled Tools       Safe Response
        |                    |
        v                    v
PostgreSQL + pgvector  Repository Layer
        |                    |
        +---------+----------+
                  |
                  v
Prompt Builder
                  |
                  v
OpenAI API
                  |
                  v
Response + Sources + Metadata
                  |
                  v
Query Logging / Observability
```

---

## RAG Pipeline

The RAG pipeline is used for knowledge-based questions about the SwitchToSolar platform.

Flow:

1. A question is received by the FastAPI query endpoint.
2. The intent router classifies the question.
3. Knowledge questions are routed into the retrieval pipeline.
4. The question is converted into an embedding.
5. PostgreSQL + pgvector retrieves semantically relevant chunks.
6. Retrieved chunks are passed into the prompt builder.
7. The LLM generates a grounded response using retrieved context.
8. The response returns with sources and metadata.
9. Query metadata is logged for observability.

The documents used for retrieval are stored in the `knowledge_base/` directory.

---

## Operational AI Design

The system is designed to support operational AI workflows without giving the model unrestricted database access.

Operational questions are routed through controlled service and repository layers instead of allowing AI-generated SQL.

This design supports:

- Predictable execution
- Safer data access
- Clearer auditability
- Easier debugging
- Separation between AI reasoning and data retrieval

---

## Observability

The API captures metadata that helps inspect and debug AI behavior.

Examples of tracked metadata include:

- Request ID
- Intent type
- Retrieved chunks
- Similarity scores
- Model used
- Latency
- Operation tool
- Response status
- Error state

This makes the AI workflow easier to monitor and improve over time.

---

## Repository Structure

```text
app/
├── api/routes/          # FastAPI route handlers for query, documents, analytics, and health checks
├── services/            # Core AI workflow logic: RAG, retrieval, embeddings, routing, prompts, and LLM calls
├── repositories/        # Database access layer for documents, query logs, analytics, and operations
├── schemas/             # Request and response models
├── db/                  # PostgreSQL, pgvector, and MSSQL connection logic
├── core/                # Configuration and shared error handling
├── utils/               # Shared helper utilities
└── main.py              # FastAPI application entrypoint

knowledge_base/
├── ai-advisor-design.md
├── ai-explainer-design.md
├── azure-architecture.md
├── lead-workflow.md
└── switchtosolar-overview.md

tests/
└── Python tests for operational logic and service behavior
```

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- pgvector
- OpenAI APIs
- Docker
- MSSQL integration layer
- pytest

---

## Running Locally

Start the local PostgreSQL service:

```bash
docker-compose up -d
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## What This Project Demonstrates

This repository demonstrates practical backend AI systems engineering, including:

- RAG architecture
- Semantic retrieval
- pgvector-based vector search
- Prompt orchestration
- Intent routing
- Controlled operational AI design
- AI observability
- Service/repository separation
- FastAPI backend design
- Production-oriented AI workflow patterns

---

## Project Context

This service is part of SwitchToSolar, a rooftop solar platform built to help users understand solar feasibility, generate solar reports, and connect with installers.

The AI Ops API focuses specifically on internal AI workflows, retrieval-grounded platform knowledge, operational assistance, and AI observability.
