from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.models.leitura_nfc import LeituraNFC
from app.models.nfc_tag import NFCTag


class NFCTagRepository:
    def create(self, db: Session, uid: str) -> NFCTag:
        nfc_tag = NFCTag(uid=uid, status="ativa")
        db.add(nfc_tag)
        return nfc_tag

    def get_by_id(self, db: Session, nfc_tag_id: UUID) -> NFCTag | None:
        return db.get(NFCTag, nfc_tag_id)

    def get_by_uid(self, db: Session, uid: str) -> NFCTag | None:
        statement = select(NFCTag).where(NFCTag.uid == uid)
        return db.scalar(statement)

    def list(self, db: Session, limit: int, offset: int) -> list[NFCTag]:
        statement = select(NFCTag).order_by(NFCTag.created_at.desc())
        return list(db.scalars(statement.offset(offset).limit(limit)).all())

    def count(self, db: Session) -> int:
        statement = select(func.count()).select_from(NFCTag)
        return int(db.scalar(statement) or 0)

    def get_cliente_by_id(self, db: Session, cliente_id: UUID) -> Cliente | None:
        return db.get(Cliente, cliente_id)

    def vincular(self, nfc_tag: NFCTag, cliente_id: UUID) -> NFCTag:
        nfc_tag.cliente_id = cliente_id
        nfc_tag.status = "ativa"
        return nfc_tag

    def soft_delete(self, nfc_tag: NFCTag) -> None:
        nfc_tag.status = "inativa"

    def create_leitura(
        self,
        db: Session,
        uid: str,
        cliente_id: UUID | None,
        sucesso: bool,
        origem: str | None,
    ) -> LeituraNFC:
        leitura = LeituraNFC(
            uid=uid,
            cliente_id=cliente_id,
            sucesso=sucesso,
            origem=origem,
        )
        db.add(leitura)
        return leitura
