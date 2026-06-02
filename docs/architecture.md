# Architecture Overview

This document explains the architecture of the SwitchToSolar AI Ops API.

The goal of this service is to provide a dedicated AI backend for retrieval-grounded answers, operational AI workflows, semantic retrieval, and AI observability.

This service is intentionally separate from the main SwitchToSolar product backend because AI workflows have different responsibilities from core business APIs.

---

## 1. System Purpose

SwitchToSolar AI Ops API is designed to support internal AI-assisted workflows such as:

- answering questions using platform knowledge
- retrieving relevant knowledge base documents
- routing questions into the correct workflow
- supporting controlled operational AI patterns
- logging AI query metadata for debugging and observability

The system is not designed as a generic chatbot.

It is designed as an AI systems layer that combines retrieval, routing, prompt construction, LLM execution, and logging.

---

## 2. High-Level Runtime Flow

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

## 3. Main Architectural Layers

The service is organized into clear backend layers.

### API Layer

Location:

```text
app/api/routes/
```

Responsibilities:

- expose FastAPI endpoints
- validate request/response models
- keep route handlers thin
- delegate business logic to services

Example routes:

- query route
- document route
- analytics route
- health route

The API layer should not contain retrieval logic, prompt construction logic, or database query logic.

---

### Service Layer

Location:

```text
app/services/
```

Responsibilities:

- orchestrate RAG workflows
- perform retrieval
- build prompts
- classify question intent
- call LLM services
- coordinate operational workflows

Important service responsibilities include:

- RAG orchestration
- embedding generation
- chunk retrieval
- prompt construction
- intent routing
- operational tool routing
- LLM execution

This layer contains the main AI workflow logic.

---

### Repository Layer

Location:

```text
app/repositories/
```

Responsibilities:

- isolate database access
- store and retrieve document chunks
- write query logs
- read analytics data
- provide controlled operational data access

The repository pattern helps keep database logic separate from AI orchestration logic.

This is especially important for operational AI workflows because AI should not directly generate or execute arbitrary database queries.

---

### Database Layer

Location:

```text
app/db/
```

Responsibilities:

- manage PostgreSQL connection logic
- support pgvector-based retrieval
- manage MSSQL connection logic for operational data
- keep database configuration centralized

The AI Ops API uses PostgreSQL + pgvector for semantic retrieval and includes an MSSQL integration layer for controlled operational retrieval patterns.

---

### Knowledge Base

Location:

```text
knowledge_base/
```

Responsibilities:

- store platform knowledge documents
- act as the source corpus for RAG ingestion
- provide grounding material for AI answers

Example knowledge files:

- AI Advisor Design
- AI Explainer Design
- Lead Workflow
- Azure Architecture
- SwitchToSolar Overview

These documents are used as retrieval source material, not as public-facing architecture documentation.

---

## 4. Knowledge Retrieval Flow

Knowledge-based questions use the RAG pipeline.

```text
Question
   |
   v
Embedding Generation
   |
   v
pgvector Similarity Search
   |
   v
Relevant Chunks
   |
   v
Prompt Builder
   |
   v
OpenAI API
   |
   v
Answer + Sources + Metadata
```

The purpose of this flow is to ground answers in retrieved platform knowledge rather than relying only on model memory.

---

## 5. Operational AI Flow

Operational questions follow a different design.

The system is designed to avoid unrestricted AI-generated SQL.

Instead, operational questions should follow this pattern:

```text
Operational Question
        |
        v
Intent / Tool Router
        |
        v
Allowed Tool Selection
        |
        v
Service Layer
        |
        v
Repository Function
        |
        v
Controlled Data Result
        |
        v
Response Formatting
```

This approach keeps operational data access predictable and easier to audit.

The model may help classify or explain, but database access remains controlled by application code.

---

## 6. Why Intent Routing Exists

Not every question should go through the same path.

The system separates questions into categories:

### Knowledge Questions

Questions that can be answered from the knowledge base.

Example:

```text
How does the AI Advisor work?
```

Execution path:

```text
RAG pipeline
```

---

### Operational Questions

Questions that require platform metrics or operational data.

Example:

```text
How many leads are currently overdue?
```

Execution path:

```text
Controlled operational tools
```

---

### Unsupported Questions

Questions outside the platform scope.

Example:

```text
What is the weather today?
```

Execution path:

```text
Safe unsupported response
```

Intent routing keeps the system focused and avoids forcing every question into a single retrieval pattern.

---

## 7. Observability Design

AI workflows need visibility because model behavior can be non-deterministic.

The AI Ops API captures useful metadata such as:

- request ID
- question
- intent type
- retrieved chunks
- similarity scores
- model used
- latency
- operation tool
- response status
- error state

This metadata supports:

- debugging
- analytics
- evaluation
- prompt improvement
- retrieval quality review

Observability is treated as part of the AI workflow, not an afterthought.

---

## 8. Design Principles

The architecture follows a few core principles.

### Keep Routes Thin

Routes should receive requests and delegate workflow execution to services.

### Separate AI Orchestration from Data Access

Services orchestrate AI workflows.

Repositories own database access.

### Ground Answers with Retrieval

Knowledge responses should use retrieved context where possible.

### Avoid Unrestricted Operational Execution

Operational AI should use controlled tools and repository methods instead of AI-generated SQL.

### Log Metadata for Debugging

AI requests should produce traceable metadata so failures and weak answers can be investigated later.

---

## 9. What This Architecture Demonstrates

This architecture demonstrates practical applied AI systems engineering patterns:

- FastAPI service design
- Retrieval-Augmented Generation
- pgvector-based semantic retrieval
- prompt orchestration
- intent routing
- controlled operational AI design
- service/repository separation
- AI observability
- production-oriented backend structure

The main idea is simple:

AI should not be treated as only a model call.

It should be designed as a governed backend workflow with retrieval, routing, controlled data access, and observability.
