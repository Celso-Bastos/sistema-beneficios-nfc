from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.clientes import router as clientes_router
from app.api.database import router as database_router
from app.api.health import router as health_router
from app.api.nfc_tags import router as nfc_tags_router
from app.core.config import settings
from app.core.exception_handlers import (
    http_exception_handler,
    sqlalchemy_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging import configure_logging
from app.core.middleware import OperationalMiddleware

configure_logging()
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(OperationalMiddleware)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "service": settings.APP_NAME,
        "status": "running",
        "version": settings.APP_VERSION,
    }


app.include_router(health_router)
app.include_router(database_router)
app.include_router(clientes_router)
app.include_router(nfc_tags_router)
