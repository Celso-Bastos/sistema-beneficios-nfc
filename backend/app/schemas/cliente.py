from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.utils.normalizers import normalize_cpf, normalize_phone, normalize_text


class ClienteBase(BaseModel):
    nome: str | None = None
    cpf: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, value: str | None) -> str | None:
        normalized = normalize_text(value)
        if value is not None and normalized is None:
            raise ValueError("nome nao pode ser vazio")
        if normalized is not None and len(normalized) < 2:
            raise ValueError("nome deve ter pelo menos 2 caracteres")

        return normalized

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str | None) -> str | None:
        normalized = normalize_cpf(value)
        if value is not None and normalized is None:
            raise ValueError("cpf nao pode ser vazio")
        if normalized is None:
            return None
        if not normalized.isdigit() or len(normalized) != 11:
            raise ValueError("cpf deve conter 11 digitos")

        return normalized

    @field_validator("telefone")
    @classmethod
    def validate_telefone(cls, value: str | None) -> str | None:
        normalized = normalize_phone(value)
        if value is not None and normalized is None:
            raise ValueError("telefone nao pode ser vazio")
        if normalized is None:
            return None
        if not normalized.isdigit():
            raise ValueError("telefone deve conter apenas digitos")

        return normalized

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        normalized = normalize_text(value)
        if value is not None and normalized is None:
            raise ValueError("email nao pode ser vazio")
        if normalized is None:
            return None

        return normalized.lower()


class ClienteCreate(ClienteBase):
    nome: str = Field(..., min_length=2)


class ClienteUpdate(ClienteBase):
    pass


class ClienteResponse(BaseModel):
    id: UUID
    nome: str
    cpf: str | None
    telefone: str | None
    email: EmailStr | None
    ativo: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClienteListResponse(BaseModel):
    items: list[ClienteResponse]
    limit: int
    offset: int
    total: int
