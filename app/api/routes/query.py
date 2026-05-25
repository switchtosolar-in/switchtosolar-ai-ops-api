from fastapi import APIRouter
from pydantic import BaseModel

from app.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.prompt_builder import build_prompt
from app.services.rag_service import answer_question

router = APIRouter()


class RetrievalPreviewRequest(BaseModel):
    question: str
    top_k: int = 3


@router.post("", response_model=QueryResponse)
def query(payload: QueryRequest):
    try:
        return answer_question(
            question=payload.question,
            top_k=payload.top_k,
        )
    except Exception as error:
        print("QUERY ERROR:", repr(error))
        from app.core.errors import service_unavailable
        raise service_unavailable()


@router.post("/retrieval-preview")
def retrieval_preview(payload: RetrievalPreviewRequest):
    chunks = retrieve_relevant_chunks(
        question=payload.question,
        top_k=payload.top_k,
    )

    return {
        "question": payload.question,
        "chunks_found": len(chunks),
        "chunks": chunks,
    }


@router.post("/prompt-preview")
def prompt_preview(payload: RetrievalPreviewRequest):
    chunks = retrieve_relevant_chunks(
        question=payload.question,
        top_k=payload.top_k,
    )

    prompt = build_prompt(
        question=payload.question,
        chunks=chunks,
    )

    return {
        "question": payload.question,
        "chunks_found": len(chunks),
        "prompt": prompt,
    }