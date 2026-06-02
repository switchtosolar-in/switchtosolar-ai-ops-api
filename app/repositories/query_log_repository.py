"""
Query log repository for AI Ops observability.

This file records metadata for AI Ops requests, including RAG queries,
operational tool usage, latency, model information, retrieval metadata,
and error states.

The goal is to make AI behavior traceable instead of treating responses
as one-off model outputs.
"""


import json
from typing import Any

from app.db.postgres import get_connection


def insert_query_log(
    request_id: str,
    question: str,
    answer: str,
    intent_type: str,
    retrieved_chunk_ids: list[int],
    similarity_scores: list[float],
    model_used: str,
    latency_ms: int,
    status: str,
    error_message: str | None = None,
    data_source: str | None = None,
    operation_tool: str | None = None,
    operation_data: dict[str, Any] | None = None,
) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO query_logs (
                    request_id,
                    question,
                    answer,
                    intent_type,
                    retrieved_chunk_ids,
                    similarity_scores,
                    model_used,
                    latency_ms,
                    status,
                    error_message,
                    data_source,
                    operation_tool,
                    operation_data
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    request_id,
                    question,
                    answer,
                    intent_type,
                    json.dumps(retrieved_chunk_ids),
                    json.dumps(similarity_scores),
                    model_used,
                    latency_ms,
                    status,
                    error_message,
                    data_source,
                    operation_tool,
                    json.dumps(operation_data) if operation_data is not None else None,
                ),
            )
            row = cur.fetchone()
        conn.commit()

    return row["id"]