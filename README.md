# switchtosolar-ai-ops-api

🔷 Title

# SwitchToSolar AI Ops API

A production-style Retrieval-Augmented Generation (RAG) backend built using FastAPI, PostgreSQL (pgvector), and OpenAI.

This system powers intelligent, context-aware AI responses for the SwitchToSolar platform.

🔷 What this project does

## 🚀 Features

- Semantic search over knowledge base using vector embeddings
- Context-grounded AI responses (no hallucination design)
- Intent classification (knowledge / operations / unsupported)
- Retrieval confidence scoring
- Query observability (latency, model usage, logs)
- Production-style API with validation and error handling
  🔷 Architecture

## 🧠 Architecture Overview

User Query
→ Intent Router
→ Retrieval (pgvector similarity search)
→ Prompt Builder (grounded context)
→ LLM (OpenAI)
→ Structured Response (answer + sources + metadata)
→ Query Logging (PostgreSQL)
🔷 API Endpoints

## 🔌 API Endpoints

### POST /query

Request:
{
"question": "How does AI Advisor avoid hallucination?",
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

🔷 Tech Stack

- FastAPI (Python backend)
- PostgreSQL + pgvector (vector database)
- OpenAI API (LLM + embeddings)
- Docker (local DB setup)

🔷 Key Concepts Implemented

- Retrieval-Augmented Generation (RAG)
- Vector similarity search
- Prompt grounding
- Intent routing
- AI observability (logging + latency tracking)
- Retrieval confidence scoring

🔷 How to run Locally

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
