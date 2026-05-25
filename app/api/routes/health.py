from fastapi import APIRouter

from app.core.config import settings
from app.db.postgres import check_postgres_connection

router = APIRouter()


@router.get("")
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/db")
def database_health_check():
    db_status = check_postgres_connection()

    return {
        "status": "ok",
        "database": db_status,
    }