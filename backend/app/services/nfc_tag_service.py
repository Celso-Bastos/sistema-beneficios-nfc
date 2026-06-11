from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.nfc_tag import NFCTag
from app.repositories.nfc_tag_repository import NFCTagRepository
from app.schemas.nfc_tag import NFCLeituraCreate, NFCTagCreate, NFCTagVincular
from app.utils.normalizers import normalize_uid


class NFCTagService:
    def __init__(self, repository: NFCTagRepository | None = None) -> None:
        self.repository = repository or NFCTagRepository()

    def create(self, db: Session, payload: NFCTagCreate) -> NFCTag:
        try:
            existing = self.repository.get_by_uid(db, payload.uid)
            if existing is not None:
                raise self._duplicated_uid()

            nfc_tag = self.repository.create(db, payload.uid)
            db.commit()
            db.refresh(nfc_tag)
            return nfc_tag
        except HTTPException:
            raise
        except IntegrityError:
            db.rollback()
            raise self._duplicated_uid() from None
        except SQLAlchemyError:
            db.rollback()
            raise self._database_unavailable() from None

    def list(self, db: Session, limit: int, offset: int) -> tuple[list[NFCTag], int]:
        try:
            nfc_tags = self.repository.list(db, limit=limit, offset=offset)
            total = self.repository.count(db)
            return nfc_tags, total
        except SQLAlchemyError:
            raise self._database_unavailable() from None

    def get_by_uid(self, db: Session, uid: str) -> NFCTag:
        normalized_uid = self._normalize_uid_or_422(uid)
        try:
            nfc_tag = self.repository.get_by_uid(db, normalized_uid)
            if nfc_tag is None:
                raise self._tag_not_found()

            return nfc_tag
        except HTTPException:
            raise
        except SQLAlchemyError:
            raise self._database_unavailable() from None

    def soft_delete(self, db: Session, nfc_tag_id: UUID) -> bool:
        try:
            nfc_tag = self.repository.get_by_id(db, nfc_tag_id)
            if nfc_tag is None:
                raise self._tag_not_found()
            if nfc_tag.status == "inativa":
                return False

            self.repository.soft_delete(nfc_tag)
            db.commit()
            return True
        except HTTPException:
            raise
        except SQLAlchemyError:
            db.rollback()
            raise self._database_unavailable() from None

    def vincular(self, db: Session, payload: NFCTagVincular) -> None:
        try:
            cliente = self.repository.get_cliente_by_id(db, payload.cliente_id)
            if cliente is None:
                raise self._cliente_not_found()

            nfc_tag = self.repository.get_by_uid(db, payload.uid)
            if nfc_tag is None:
                raise self._tag_not_found()
            if (
                nfc_tag.status == "ativa"
                and nfc_tag.cliente_id is not None
                and nfc_tag.cliente_id != payload.cliente_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Tag NFC já vinculada a outro cliente ativo",
                )

            self.repository.vincular(nfc_tag, payload.cliente_id)
            db.commit()
        except HTTPException:
            raise
        except SQLAlchemyError:
            db.rollback()
            raise self._database_unavailable() from None

    def lookup(self, db: Session, uid: str) -> NFCTag:
        nfc_tag = self.get_by_uid(db, uid)
        if nfc_tag.status != "ativa" or nfc_tag.cliente is None:
            raise self._tag_not_found()

        return nfc_tag

    def registrar_leitura(self, db: Session, payload: NFCLeituraCreate) -> NFCTag:
        try:
            nfc_tag = self.repository.get_by_uid(db, payload.uid)
            if nfc_tag is None or nfc_tag.status != "ativa" or nfc_tag.cliente is None:
                self.repository.create_leitura(
                    db,
                    uid=payload.uid,
                    cliente_id=None,
                    sucesso=False,
                    origem=payload.origem,
                )
                db.commit()
                raise self._tag_not_found()

            self.repository.create_leitura(
                db,
                uid=payload.uid,
                cliente_id=nfc_tag.cliente_id,
                sucesso=True,
                origem=payload.origem,
            )
            db.commit()
            db.refresh(nfc_tag)
            return nfc_tag
        except HTTPException:
            raise
        except SQLAlchemyError:
            db.rollback()
            raise self._database_unavailable() from None

    @staticmethod
    def _normalize_uid_or_422(uid: str) -> str:
        normalized_uid = normalize_uid(uid)
        if normalized_uid is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="UID não pode ser vazio",
            )

        return normalized_uid

    @staticmethod
    def _duplicated_uid() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag NFC já cadastrada",
        )

    @staticmethod
    def _tag_not_found() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag NFC não encontrada",
        )

    @staticmethod
    def _cliente_not_found() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado",
        )

    @staticmethod
    def _database_unavailable() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de banco de dados temporariamente indisponível",
        )
