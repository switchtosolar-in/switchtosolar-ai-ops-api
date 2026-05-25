import psycopg
from psycopg.rows import dict_row

from app.core.config import settings


def get_connection():
    return psycopg.connect(
        settings.postgres_dsn,
        row_factory=dict_row,
    )


def check_postgres_connection() -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version() AS version;")
            row = cur.fetchone()

    return {
        "connected": True,
        "version": row["version"],
    }