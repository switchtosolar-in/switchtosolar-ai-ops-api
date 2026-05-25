from app.repositories.analytics_repository import get_ai_analytics_summary


def get_analytics_summary(days: int = 30) -> dict:
    safe_days = max(1, min(days, 365))
    return get_ai_analytics_summary(days=safe_days)