from datetime import UTC, datetime

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.database.session import engine

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/health/detailed")
def detailed_health_check() -> dict[str, str | dict[str, str]]:
    database_status = "not_configured"
    if engine is not None:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            database_status = "ok"
        except SQLAlchemyError:
            database_status = "unavailable"

    api_status = "ok" if database_status in {"ok", "not_configured"} else "degraded"

    return {
        "status": api_status,
        "api": {
            "status": "ok",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
        },
        "database": {
            "status": database_status,
        },
        "timestamp": datetime.now(UTC).isoformat(),
    }
