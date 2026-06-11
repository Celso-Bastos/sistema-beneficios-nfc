from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.clientes import get_clientes_db
from app.api.nfc_tags import get_nfc_db
from app.database.base import Base
from app.main import app
from app.models.leitura_nfc import LeituraNFC
from app.schemas.nfc_tag import NFCTagCreate
from app.utils.normalizers import normalize_uid


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_clientes_db] = override_get_db
    app.dependency_overrides[get_nfc_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_normalize_uid_remove_espacos_e_uppercase() -> None:
    assert normalize_uid(" 04 a8\nb9 c1 ") == "04A8B9C1"


def test_schema_rejeita_uid_vazio() -> None:
    with pytest.raises(ValueError):
        NFCTagCreate(uid=" \n ")


def test_nfc_cadastro_vinculo_lookup_e_registro_leitura(client: TestClient) -> None:
    cliente_response = client.post(
        "/api/clientes",
        json={
            "nome": "Joao Silva",
            "cpf": "12345678900",
            "telefone": "(98) 99999-9999",
            "email": "joao@example.com",
        },
    )
    assert cliente_response.status_code == 201
    cliente = cliente_response.json()

    create_tag_response = client.post("/api/nfc-tags", json={"uid": "04 a8 b9 c1"})
    assert create_tag_response.status_code == 201
    tag = create_tag_response.json()
    assert tag["uid"] == "04A8B9C1"
    assert tag["status"] == "ativa"

    vincular_response = client.post(
        "/api/nfc-tags/vincular",
        json={"uid": "04A8B9C1", "cliente_id": cliente["id"]},
    )
    assert vincular_response.status_code == 200
    assert vincular_response.json() == {"message": "Tag vinculada com sucesso"}

    lookup_response = client.get("/api/nfc-tags/lookup/04 a8 b9 c1")
    assert lookup_response.status_code == 200
    lookup = lookup_response.json()
    assert lookup["uid"] == "04A8B9C1"
    assert lookup["cliente"]["id"] == cliente["id"]
    assert lookup["cliente"]["nome"] == "Joao Silva"
    assert lookup["cliente"]["telefone"] == "98999999999"
    assert "cpf" not in lookup["cliente"]

    leitura_response = client.post(
        "/api/nfc-tags/registrar-leitura",
        json={"uid": "04A8B9C1", "origem": "web"},
    )
    assert leitura_response.status_code == 200
    leitura = leitura_response.json()
    assert leitura["cliente"]["id"] == cliente["id"]
    assert "cpf" not in leitura["cliente"]

    with next(client.app.dependency_overrides[get_nfc_db]()) as db:
        leituras = list(db.scalars(select(LeituraNFC)).all())
        assert len(leituras) == 1
        assert leituras[0].uid == "04A8B9C1"
        assert leituras[0].sucesso is True


def test_nfc_tag_pode_ser_inativada(client: TestClient) -> None:
    create_tag_response = client.post("/api/nfc-tags", json={"uid": "ABC123"})
    assert create_tag_response.status_code == 201

    tag = create_tag_response.json()
    delete_response = client.delete(f"/api/nfc-tags/{tag['id']}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Tag NFC inativada com sucesso"}

    second_delete_response = client.delete(f"/api/nfc-tags/{tag['id']}")
    assert second_delete_response.status_code == 200
    assert second_delete_response.json() == {"message": "Tag NFC já estava inativa"}
