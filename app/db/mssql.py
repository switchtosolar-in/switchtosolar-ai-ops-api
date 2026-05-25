import pyodbc

from app.core.config import settings


def get_mssql_connection():
    print("Opening MSSQL connection...")
    conn = pyodbc.connect(
        settings.mssql_connection_string,
        timeout=5,
    )
    print("MSSQL connection opened.")
    return conn


def check_mssql_connection() -> dict:
    with get_mssql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DB_NAME() AS database_name, SYSUTCDATETIME() AS server_time;")
        row = cursor.fetchone()

    return {
        "connected": True,
        "database": row.database_name,
        "server_time": str(row.server_time),
    }