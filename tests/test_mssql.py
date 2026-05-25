import pyodbc
from app.core.config import settings

print("SERVER:", settings.MSSQL_SERVER)
print("DATABASE:", settings.MSSQL_DATABASE)
print("USER:", settings.MSSQL_USER)
print("DRIVER:", settings.MSSQL_DRIVER)

conn = pyodbc.connect(settings.mssql_connection_string, timeout=5)
cursor = conn.cursor()
cursor.execute("SELECT DB_NAME() AS db_name, SYSUTCDATETIME() AS now_utc;")
row = cursor.fetchone()

print("CONNECTED:", row.db_name, row.now_utc)

conn.close()