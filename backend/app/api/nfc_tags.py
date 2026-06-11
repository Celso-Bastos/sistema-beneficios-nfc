from collections.abc import Generator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import DatabaseSessionNotConfigured, get_db
from app.schemas.nfc_tag import (
    NFCLeituraCreate,
    NFCLeituraResponse,
    NFCLookupResponse,
    NFCMessageResponse,
    NFCTagCreate,
    NFCTagListResponse,
    NFCTagMinimalResponse,
    NFCTagResponse,
    NFCTagVincular,
)
from app.services.nfc_tag_service import NFCTagService

router = APIRouter(prefix="/api/nfc-tags", tags=["nfc-tags"])
service = NFCTagService()


def get_nfc_db() -> Generator[Session, None, None]:
    try:
        yield from get_db()
    except DatabaseSessionNotConfigured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de banco de dados temporariamente indisponível",
        ) from None


@router.post(
    "",
    response_model=NFCTagMinimalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_nfc_tag(
    payload: NFCTagCreate,
    db: Session = Depends(get_nfc_db),
) -> NFCTagMinimalResponse:
    return service.create(db, payload)


@router.get("", response_model=NFCTagListResponse)
def list_nfc_tags(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_nfc_db),
) -> NFCTagListResponse:
    nfc_tags, total = service.list(db, limit=limit, offset=offset)
    return NFCTagListResponse(
        items=nfc_tags,
        limit=limit,
        offset=offset,
        total=total,
    )


@router.post("/vincular", response_model=NFCMessageResponse)
def vincular_nfc_tag(
    payload: NFCTagVincular,
    db: Session = Depends(get_nfc_db),
) -> dict[str, str]:
    service.vincular(db, payload)
    return {"message": "Tag vinculada com sucesso"}


@router.get("/lookup/{uid}", response_model=NFCLookupResponse)
def lookup_nfc_tag(
    uid: str,
    db: Session = Depends(get_nfc_db),
) -> NFCLookupResponse:
    nfc_tag = service.lookup(db, uid)
    return NFCLookupResponse(uid=nfc_tag.uid, cliente=nfc_tag.cliente)


@router.post("/registrar-leitura", response_model=NFCLeituraResponse)
def registrar_leitura(
    payload: NFCLeituraCreate,
    db: Session = Depends(get_nfc_db),
) -> NFCLeituraResponse:
    nfc_tag = service.registrar_leitura(db, payload)
    return NFCLeituraResponse(cliente=nfc_tag.cliente)


@router.get("/{uid}", response_model=NFCTagResponse)
def get_nfc_tag_by_uid(
    uid: str,
    db: Session = Depends(get_nfc_db),
) -> NFCTagResponse:
    return service.get_by_uid(db, uid)


@router.delete("/{nfc_tag_id}", response_model=NFCMessageResponse)
def delete_nfc_tag(
    nfc_tag_id: UUID,
    db: Session = Depends(get_nfc_db),
) -> dict[str, str]:
    was_deactivated = service.soft_delete(db, nfc_tag_id)
    if not was_deactivated:
        return {"message": "Tag NFC já estava inativa"}

    return {"message": "Tag NFC inativada com sucesso"}
