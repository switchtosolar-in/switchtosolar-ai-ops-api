from fastapi import APIRouter, Query

from app.services.analytics_service import get_analytics_summary

router = APIRouter()


@router.get("/summary")
def analytics_summary(days: int = Query(default=30, ge=1, le=365)):
    return get_analytics_summary(days=days)