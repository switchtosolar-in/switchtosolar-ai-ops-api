from app.services.embedding_service import create_embedding

from app.repositories.document_repository import (
    delete_all_documents,
    insert_document,
    insert_document_chunk,
    count_documents,
    count_chunks,
)
from app.services.document_loader import load_markdown_files
from app.services.chunking_service import chunk_document


def ingest_knowledge_base(directory_path: str = "knowledge_base") -> dict:
    """
    Loads markdown docs, chunks them, and stores them in PostgreSQL.
    """
    documents = load_markdown_files(directory_path)

    delete_all_documents()

    documents_ingested = 0
    chunks_created = 0

    for document in documents:
        document_id = insert_document(
            title=document["title"],
            source_path=document["source_path"],
        )
        documents_ingested += 1

        chunks = chunk_document(document)

        for chunk in chunks:
            embedding = create_embedding(chunk["chunk_text"])

            insert_document_chunk(
                document_id=document_id,
                chunk_index=chunk["chunk_index"],
                chunk_text=chunk["chunk_text"],
                embedding=embedding,
            )

            chunks_created += 1

    return {
        "status": "success",
        "documents_ingested": documents_ingested,
        "chunks_created": chunks_created,
        "documents_in_db": count_documents(),
        "chunks_in_db": count_chunks(),
    }