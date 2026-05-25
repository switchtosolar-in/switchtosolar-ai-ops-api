from app.db.postgres import get_connection
from app.services.embedding_service import create_embedding


DEFAULT_TOP_K = 3
CANDIDATE_LIMIT = 8


def _get_confidence_level(best_distance: float | None) -> str:
    if best_distance is None:
        return "none"

    if best_distance <= 0.95:
        return "high"

    if best_distance <= 1.20:
        return "medium"

    return "low"


def _get_dynamic_max_distance(best_distance: float | None) -> float:
    """
    Dynamically chooses how much context to keep.

    If best match is strong, keep only close matches.
    If best match is medium, allow moderate matches.
    If best match is weak, effectively reject all.
    """
    if best_distance is None:
        return 0.0

    if best_distance <= 0.95:
        return best_distance + 0.30

    if best_distance <= 1.20:
        return 1.20

    return 0.0


def retrieve_relevant_chunks(
    question: str,
    top_k: int = DEFAULT_TOP_K,
) -> dict:
    """
    Retrieves relevant chunks using pgvector and applies confidence-aware filtering.

    Returns:
    {
        "chunks": [...],
        "confidence": "high|medium|low|none",
        "best_distance": 0.91
    }
    """
    question_embedding = create_embedding(question)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    dc.id AS chunk_id,
                    dc.chunk_index,
                    dc.chunk_text,
                    d.title AS document_title,
                    d.source_path,
                    dc.embedding <-> %s::vector AS distance
                FROM document_chunks dc
                JOIN documents d ON d.id = dc.document_id
                WHERE dc.embedding IS NOT NULL
                ORDER BY dc.embedding <-> %s::vector
                LIMIT %s;
                """,
                (
                    question_embedding,
                    question_embedding,
                    CANDIDATE_LIMIT,
                ),
            )

            rows = cur.fetchall()

    candidates = [
        {
            "chunk_id": row["chunk_id"],
            "chunk_index": row["chunk_index"],
            "chunk_text": row["chunk_text"],
            "document_title": row["document_title"],
            "source_path": row["source_path"],
            "distance": float(row["distance"]),
        }
        for row in rows
    ]

    best_distance = candidates[0]["distance"] if candidates else None
    confidence = _get_confidence_level(best_distance)
    max_distance = _get_dynamic_max_distance(best_distance)

    if confidence == "low" or confidence == "none":
        return {
            "chunks": [],
            "confidence": confidence,
            "best_distance": best_distance,
        }

    filtered_chunks = [
        chunk for chunk in candidates
        if chunk["distance"] <= max_distance
    ][:top_k]

    return {
        "chunks": filtered_chunks,
        "confidence": confidence,
        "best_distance": best_distance,
    }