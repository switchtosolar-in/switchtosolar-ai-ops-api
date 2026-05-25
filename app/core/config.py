from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "switchtosolar-ai-ops-api"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_DB: str = "switchtosolar_ai_ops"
    POSTGRES_USER: str = "s2s_ai_user"
    POSTGRES_PASSWORD: str = "s2s_ai_password"

    OPENAI_API_KEY: str = ""
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"

    MSSQL_SERVER: str = ""
    MSSQL_DATABASE: str = ""
    MSSQL_USER: str = ""
    MSSQL_PASSWORD: str = ""
    MSSQL_DRIVER: str = "ODBC Driver 18 for SQL Server"
    MSSQL_ENCRYPT: str = "yes"
    MSSQL_TRUST_SERVER_CERTIFICATE: str = "no"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def postgres_dsn(self) -> str:
        return (
            f"host={self.POSTGRES_HOST} "
            f"port={self.POSTGRES_PORT} "
            f"dbname={self.POSTGRES_DB} "
            f"user={self.POSTGRES_USER} "
            f"password={self.POSTGRES_PASSWORD}"
        )

    @property
    def mssql_connection_string(self) -> str:
        return (
            f"DRIVER={{{self.MSSQL_DRIVER}}};"
            f"SERVER={self.MSSQL_SERVER};"
            f"DATABASE={self.MSSQL_DATABASE};"
            f"UID={self.MSSQL_USER};"
            f"PWD={self.MSSQL_PASSWORD};"
            f"Encrypt={self.MSSQL_ENCRYPT};"
            f"TrustServerCertificate={self.MSSQL_TRUST_SERVER_CERTIFICATE};"
            "Connection Timeout=5;"
        )


settings = Settings()