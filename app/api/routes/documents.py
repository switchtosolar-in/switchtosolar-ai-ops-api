from fastapi import APIRouter

from app.services.document_loader import load_markdown_files
from app.services.chunking_service import chunk_document
from app.services.ingestion_service import ingest_knowledge_base
from app.repositories.document_repository import count_documents, count_chunks

router = APIRouter()


@router.get("/preview-chunks")
def preview_chunks():
    documents = load_markdown_files("knowledge_base")

    all_chunks = []

    for document in documents:
        chunks = chunk_document(document)
        all_chunks.extend(chunks)

    return {
        "documents_found": len(documents),
        "chunks_created": len(all_chunks),
        "sample_chunks": all_chunks[:5],
    }


@router.post("/ingest")
def ingest_documents():
    return ingest_knowledge_base("knowledge_base")


@router.get("/stats")
def document_stats():
    return {
        "documents_in_db": count_documents(),
        "chunks_in_db": count_chunks(),
    }