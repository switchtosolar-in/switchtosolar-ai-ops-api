from app.db.postgres import get_connection


def delete_all_documents() -> None:
    """
    Clears existing documents and chunks.

    For this project stage, ingestion is simple:
    every ingest refreshes the knowledge base.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM document_chunks;")
            cur.execute("DELETE FROM documents;")
        conn.commit()


def insert_document(title: str, source_path: str) -> int:
    """
    Inserts a document row and returns its ID.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO documents (title, source_path)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (title, source_path),
            )
            row = cur.fetchone()
        conn.commit()

    return row["id"]


def insert_document_chunk(
    document_id: int,
    chunk_index: int,
    chunk_text: str,
    embedding: list[float] | None = None,
) -> int:
    """
    Inserts a document chunk with optional embedding.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO document_chunks (
                    document_id,
                    chunk_index,
                    chunk_text,
                    embedding
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    document_id,
                    chunk_index,
                    chunk_text,
                    embedding,
                ),
            )
            row = cur.fetchone()
        conn.commit()

    return row["id"]


def count_documents() -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS count FROM documents;")
            row = cur.fetchone()

    return row["count"]


def count_chunks() -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS count FROM document_chunks;")
            row = cur.fetchone()

    return row["count"]