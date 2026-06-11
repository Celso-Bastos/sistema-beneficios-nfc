from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente


class ClienteRepository:
    def create(self, db: Session, data: dict) -> Cliente:
        cliente = Cliente(**data)
        db.add(cliente)
        return cliente

    def get_by_id(self, db: Session, cliente_id: UUID) -> Cliente | None:
        return db.get(Cliente, cliente_id)

    def get_by_cpf(self, db: Session, cpf: str) -> Cliente | None:
        statement = select(Cliente).where(Cliente.cpf == cpf)
        return db.scalar(statement)

    def list(
        self,
        db: Session,
        ativo: bool | None,
        limit: int,
        offset: int,
    ) -> list[Cliente]:
        statement = select(Cliente).order_by(Cliente.created_at.desc())
        if ativo is not None:
            statement = statement.where(Cliente.ativo == ativo)

        return list(db.scalars(statement.offset(offset).limit(limit)).all())

    def count(self, db: Session, ativo: bool | None) -> int:
        statement = select(func.count()).select_from(Cliente)
        if ativo is not None:
            statement = statement.where(Cliente.ativo == ativo)

        return int(db.scalar(statement) or 0)

    def update(self, db: Session, cliente: Cliente, data: dict) -> Cliente:
        for field, value in data.items():
            setattr(cliente, field, value)

        return cliente

    def soft_delete(self, cliente: Cliente) -> None:
        cliente.ativo = False
