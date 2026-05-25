from fastapi import HTTPException


def service_unavailable(message: str = "AI service temporarily unavailable. Please try again.") -> HTTPException:
    return HTTPException(
        status_code=503,
        detail=message,
    )


def bad_request(message: str) -> HTTPException:
    return HTTPException(
        status_code=400,
        detail=message,
    )