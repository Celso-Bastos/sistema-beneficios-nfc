from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.normalizers import normalize_text, normalize_uid


class NFCTagCreate(BaseModel):
    uid: str = Field(..., min_length=1)

    @field_validator("uid")
    @classmethod
    def validate_uid(cls, value: str) -> str:
        normalized = normalize_uid(value)
        if normalized is None:
            raise ValueError("uid nao pode ser vazio")

        return normalized


class NFCTagVincular(BaseModel):
    uid: str = Field(..., min_length=1)
    cliente_id: UUID

    @field_validator("uid")
    @classmethod
    def validate_uid(cls, value: str) -> str:
        normalized = normalize_uid(value)
        if normalized is None:
            raise ValueError("uid nao pode ser vazio")

        return normalized


class NFCLeituraCreate(BaseModel):
    uid: str = Field(..., min_length=1)
    origem: str | None = None

    @field_validator("uid")
    @classmethod
    def validate_uid(cls, value: str) -> str:
        normalized = normalize_uid(value)
        if normalized is None:
            raise ValueError("uid nao pode ser vazio")

        return normalized

    @field_validator("origem")
    @classmethod
    def validate_origem(cls, value: str | None) -> str | None:
        return normalize_text(value)


class NFCTagResponse(BaseModel):
    id: UUID
    uid: str
    cliente_id: UUID | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NFCTagMinimalResponse(BaseModel):
    id: UUID
    uid: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class NFCTagListResponse(BaseModel):
    items: list[NFCTagResponse]
    limit: int
    offset: int
    total: int


class NFCClienteResponse(BaseModel):
    id: UUID
    nome: str
    telefone: str | None

    model_config = ConfigDict(from_attributes=True)


class NFCLookupResponse(BaseModel):
    uid: str
    cliente: NFCClienteResponse


class NFCLeituraResponse(BaseModel):
    cliente: NFCClienteResponse


class NFCMessageResponse(BaseModel):
    message: str
