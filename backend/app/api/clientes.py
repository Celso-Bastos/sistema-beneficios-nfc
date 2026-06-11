from uuid import UUID

from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import DatabaseSessionNotConfigured, get_db
from app.core.rate_limit import rate_limit
from app.schemas.cliente import (
    ClienteCreate,
    ClienteListResponse,
    ClienteResponse,
    ClienteUpdate,
)
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/api/clientes", tags=["clientes"])
service = ClienteService()


def get_clientes_db() -> Generator[Session, None, None]:
    try:
        yield from get_db()
    except DatabaseSessionNotConfigured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de banco de dados temporariamente indisponível",
        ) from None


@router.post(
    "",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cliente(
    payload: ClienteCreate,
    _: None = Depends(rate_limit),
    db: Session = Depends(get_clientes_db),
) -> ClienteResponse:
    return service.create(db, payload)


@router.get("", response_model=ClienteListResponse)
def list_clientes(
    ativo: bool | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_clientes_db),
) -> ClienteListResponse:
    clientes, total = service.list(db, ativo=ativo, limit=limit, offset=offset)
    return ClienteListResponse(
        items=clientes,
        limit=limit,
        offset=offset,
        total=total,
    )


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(
    cliente_id: UUID,
    db: Session = Depends(get_clientes_db),
) -> ClienteResponse:
    return service.get_by_id(db, cliente_id)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: UUID,
    payload: ClienteUpdate,
    db: Session = Depends(get_clientes_db),
) -> ClienteResponse:
    return service.update(db, cliente_id, payload)


@router.delete("/{cliente_id}")
def delete_cliente(
    cliente_id: UUID,
    db: Session = Depends(get_clientes_db),
) -> dict[str, str]:
    was_deactivated = service.soft_delete(db, cliente_id)
    if not was_deactivated:
        return {"message": "Cliente já estava inativo"}

    return {"message": "Cliente inativado com sucesso"}
