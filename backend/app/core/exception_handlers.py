import logging

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger("app.errors")


def _response(request: Request, status_code: int, message: str) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    headers = {"X-Request-ID": request_id} if request_id else None
    return JSONResponse(
        status_code=status_code,
        content={"error": True, "message": message},
        headers=headers,
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "Erro na requisição"
    return _response(request, exc.status_code, message)


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return _response(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Dados inválidos",
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(
        "database_error",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "method": request.method,
            "path": request.url.path,
        },
    )
    return _response(
        request,
        status.HTTP_503_SERVICE_UNAVAILABLE,
        "Serviço de banco de dados temporariamente indisponível",
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "unhandled_error",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "method": request.method,
            "path": request.url.path,
        },
    )
    return _response(
        request,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Erro interno",
    )
