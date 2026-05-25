from typing import Any

from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=3, ge=1, le=10)

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Question cannot be blank.")

        return cleaned


class SourceItem(BaseModel):
    document_title: str
    chunk_index: int
    distance: float


class QueryMetadata(BaseModel):
    request_id: str
    model: str
    chunks_used: int
    latency_ms: int
    retrieval_confidence: str | None = None
    best_distance: float | None = None

    # Operations metadata
    data_source: str | None = None
    operation_tool: str | None = None
    operation_data: dict[str, Any] | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    intent: str
    sources: list[SourceItem]
    metadata: QueryMetadata