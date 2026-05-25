# SwitchToSolar AI Ops API

Production-oriented Retrieval-Augmented Generation (RAG) backend built using FastAPI, PostgreSQL (pgvector), and OpenAI APIs.

This system powers context-aware AI workflows and operational AI services for the SwitchToSolar platform through retrieval-driven architectures, structured orchestration pipelines, and grounded response generation.

---

## Overview

The platform is designed around operational AI workflow patterns emphasizing:

- retrieval-driven AI architectures
- grounded response generation
- structured prompt orchestration
- operational safety controls
- observability and telemetry
- backend AI workflow separation
- controlled operational retrieval patterns

The system combines semantic retrieval pipelines with modular AI orchestration services to support AI-assisted platform workflows.

---

## Core Capabilities

- Semantic retrieval using vector embeddings
- Context-grounded AI response generation
- Structured prompt orchestration
- Retrieval confidence scoring
- Intent routing and workflow classification
- Operational AI workflow handling
- AI observability and telemetry logging
- Structured response metadata
- Backend AI service isolation
- Validation and reliability controls

---

## Architecture Overview

User Query
→ Intent Router
→ Retrieval Pipeline
→ Context Construction
→ Prompt Orchestration
→ LLM Execution
→ Structured Response Generation
→ Observability & Query Logging

The architecture separates:

- vector-based semantic retrieval
- operational workflow handling
- prompt orchestration
- runtime validation
- telemetry collection

to improve reliability, maintainability, and operational safety.

---

## Retrieval Pipeline

The retrieval layer uses PostgreSQL with pgvector for semantic similarity search.

Pipeline stages include:

1. Document ingestion
2. Chunking and preprocessing
3. Embedding generation
4. Vector similarity retrieval
5. Confidence filtering
6. Context injection into prompts
7. Source-grounded response generation

The system is designed to prioritize grounded responses over open-ended generation.

---

## Intent Routing

Requests are classified into workflow categories prior to LLM execution.

Supported workflow types:

- knowledge retrieval
- operational workflows
- unsupported requests

This routing layer helps isolate workflow behavior and prevents uncontrolled execution paths.

---

## AI Workflow Design

The platform uses structured orchestration pipelines combining:

- retrieval context
- scoped prompting
- response validation
- fallback handling
- timeout controls
- telemetry collection

The architecture emphasizes predictable AI workflow behavior and operational visibility.

---

## Observability & Telemetry

The platform captures operational metadata for AI workflow monitoring and diagnostics.

Tracked metadata includes:

- request identifiers
- workflow intent
- latency metrics
- retrieval metadata
- model usage
- confidence scoring
- response diagnostics
- execution status

This telemetry layer supports debugging, evaluation workflows, and iterative refinement.

---

## Reliability & Safety Controls

The system includes multiple operational safeguards:

- retrieval-grounded prompting
- controlled execution paths
- fallback response handling
- timeout management
- scoped workflow routing
- structured validation patterns
- protected backend service integration

Operational retrieval workflows avoid unrestricted AI-generated database execution patterns.

---

## API Endpoint

### POST /query

Example request:

```json
{
  "question": "How does the retrieval pipeline work?",
  "top_k": 3
}
Response:

{
"question": "...",
"answer": "...",
"intent": "knowledge",
"sources": [...],
"metadata": {
"request_id": "...",
"model": "...",
"chunks_used": 3,
"latency_ms": 4000,
"retrieval_confidence": "high",
"best_distance": 0.91
}
}

---

Tech Stack

- FastAPI (Python backend)
- PostgreSQL + pgvector (vector database)
- OpenAI API (LLM + embeddings)
- Docker (local DB setup)

Key Concepts Implemented

- Retrieval-Augmented Generation (RAG)
- Vector similarity search
- Prompt grounding
- Intent routing
- AI observability (logging + latency tracking)
- Retrieval confidence scoring



How to run Locally?

1. Start PostgreSQL:

docker-compose up -d
Activate env:
.venv\Scripts\activate
Start API:
uvicorn app.main:app --reload
Open docs:

http://127.0.0.1:8000/docs

---

# 2. Add Architecture Notes

Create:

docs/architecture.md

# Architecture Deep Dive

## RAG Flow

1. User question converted to embedding
2. pgvector similarity search returns top_k chunks
3. Prompt builder injects context into structured prompt
4. LLM generates grounded response
5. Response includes sources and metadata

## Intent Routing

- knowledge → RAG pipeline
- operations → placeholder (future MSSQL tools)
- unsupported → safe rejection

## Observability

Each query logs:

- request_id
- intent
- model_used
- latency_ms
- status

## Retrieval Quality

- best_distance → closest semantic match
- retrieval_confidence → high / medium / low
```
