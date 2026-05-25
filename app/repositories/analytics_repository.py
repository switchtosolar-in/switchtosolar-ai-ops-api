from app.db.postgres import get_connection


def get_ai_analytics_summary(days: int = 30) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    COUNT(*) AS total_requests,
                    COUNT(*) FILTER (WHERE intent_type = 'knowledge') AS knowledge_requests,
                    COUNT(*) FILTER (WHERE intent_type = 'operations') AS operations_requests,
                    COUNT(*) FILTER (WHERE intent_type = 'unsupported') AS unsupported_requests,
                    COUNT(*) FILTER (WHERE status = 'error') AS error_requests,
                    COALESCE(ROUND(AVG(latency_ms)), 0) AS avg_latency_ms
                FROM query_logs
                WHERE created_at >= NOW() - (%s || ' days')::INTERVAL;
                """,
                (days,),
            )
            summary = cur.fetchone()

            cur.execute(
                """
                SELECT
                    operation_tool,
                    COUNT(*) AS total
                FROM query_logs
                WHERE created_at >= NOW() - (%s || ' days')::INTERVAL
                  AND intent_type = 'operations'
                  AND operation_tool IS NOT NULL
                GROUP BY operation_tool
                ORDER BY total DESC
                LIMIT 10;
                """,
                (days,),
            )
            tools = cur.fetchall()

    return {
        "days": days,
        "total_requests": int(summary["total_requests"] or 0),
        "knowledge_requests": int(summary["knowledge_requests"] or 0),
        "operations_requests": int(summary["operations_requests"] or 0),
        "unsupported_requests": int(summary["unsupported_requests"] or 0),
        "error_requests": int(summary["error_requests"] or 0),
        "avg_latency_ms": int(summary["avg_latency_ms"] or 0),
        "top_operations_tools": [
            {
                "operation_tool": row["operation_tool"],
                "total": int(row["total"] or 0),
            }
            for row in tools
        ],
    }