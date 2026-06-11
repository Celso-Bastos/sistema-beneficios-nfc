from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.repositories.audit_repository import AuditRepository
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteService:
    def __init__(
        self,
        repository: ClienteRepository | None = None,
        audit_repository: AuditRepository | None = None,
    ) -> None:
        self.repository = repository or ClienteRepository()
        self.audit_repository = audit_repository or AuditRepository()

    def create(self, db: Session, payload: ClienteCreate) -> Cliente:
        data = payload.model_dump()
        self._validate_cpf_available(db, data.get("cpf"))

        try:
            cliente = self.repository.create(db, data)
            db.flush()
            self.audit_repository.create(
                db,
                event_type="cliente_criado",
                entity="cliente",
                entity_id=str(cliente.id),
            )
            db.commit()
            db.refresh(cliente)
            return cliente
        except IntegrityError:
            db.rollback()
            raise self._duplicated_cpf() from None
        except SQLAlchemyError:
            db.rollback()
            raise self._database_unavailable() from None

    def list(
        self,
        db: Session,
        ativo: bool | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Cliente], int]:
        try:
            clientes = self.repository.list(db, ativo=ativo, limit=limit, offset=offset)
            total = self.repository.count(db, ativo=ativo)
            return clientes, total
        except SQLAlchemyError:
            raise self._database_unavailable() from None

    def get_by_id(self, db: Session, cliente_id: UUID) -> Cliente:
        try:
            cliente = self.repository.get_by_id(db, cliente_id)
            if cliente is None:
                raise self._not_found()

            return cliente
        except HTTPException:
            raise
        except SQLAlchemyError:
            raise self._database_unavailable() from None

    def update(self, db: Session, cliente_id: UUID, payload: ClienteUpdate) -> Cliente:
        cliente = self.get_by_id(db, cliente_id)
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Informe pelo menos um campo para atualização",
            )

        if "cpf" in data:
            self._validate_cpf_available(db, data["cpf"], current_id=cliente.id)

        try:
            cliente = self.repository.update(db, cliente, data)
            self.audit_repository.create(
                db,
                event_type="cliente_alterado",
                entity="cliente",
                entity_id=str(cliente.id),
            )
            db.commit()
            db.refresh(cliente)
            return cliente
        except IntegrityError:
            db.rollback()
            raise self._duplicated_cpf() from None
        except SQLAlchemyError:
            db.rollback()
            raise self._database_unavailable() from None

    def soft_delete(self, db: Session, cliente_id: UUID) -> bool:
        cliente = self.get_by_id(db, cliente_id)
        if not cliente.ativo:
            return False

        try:
            self.repository.soft_delete(cliente)
            self.audit_repository.create(
                db,
                event_type="cliente_inativado",
                entity="cliente",
                entity_id=str(cliente.id),
            )
            db.commit()
            return True
        except SQLAlchemyError:
            db.rollback()
            raise self._database_unavailable() from None

    def _validate_cpf_available(
        self,
        db: Session,
        cpf: str | None,
        current_id: UUID | None = None,
    ) -> None:
        if cpf is None:
            return

        try:
            existing = self.repository.get_by_cpf(db, cpf)
        except SQLAlchemyError:
            raise self._database_unavailable() from None

        if existing is None:
            return
        if current_id is not None and existing.id == current_id:
            return

        raise self._duplicated_cpf()

    @staticmethod
    def _duplicated_cpf() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um cliente cadastrado com este CPF",
        )

    @staticmethod
    def _database_unavailable() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de banco de dados temporariamente indisponível",
        )

    @staticmethod
    def _not_found() -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado",
        )
