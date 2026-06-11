from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.clientes import get_clientes_db
from app.main import app
from app.models.audit_log import AuditLog
from tests.utils import build_test_session


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine, TestingSessionLocal = build_test_session()

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_clientes_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    engine.dispose()


def test_clientes_crud_minimo(client: TestClient) -> None:
    create_response = client.post(
        "/api/clientes",
        json={
            "nome": " Joao da Silva ",
            "cpf": "123.456.789-00",
            "telefone": "+55 (98) 99999-9999",
            "email": "JOAO@EXAMPLE.COM",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["nome"] == "Joao da Silva"
    assert created["cpf"] == "12345678900"
    assert created["telefone"] == "5598999999999"
    assert created["email"] == "joao@example.com"
    assert created["ativo"] is True

    duplicate_response = client.post(
        "/api/clientes",
        json={"nome": "Outro Cliente", "cpf": "12345678900"},
    )
    assert duplicate_response.status_code == 409
    assert duplicate_response.json() == {
        "error": True,
        "message": "Já existe um cliente cadastrado com este CPF",
    }

    list_response = client.get("/api/clientes")
    assert list_response.status_code == 200
    listed = list_response.json()
    assert listed["total"] == 1
    assert listed["items"][0]["id"] == created["id"]

    get_response = client.get(f"/api/clientes/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]

    empty_update_response = client.put(f"/api/clientes/{created['id']}", json={})
    assert empty_update_response.status_code == 400
    assert empty_update_response.json() == {
        "error": True,
        "message": "Informe pelo menos um campo para atualização",
    }

    update_response = client.put(
        f"/api/clientes/{created['id']}",
        json={"nome": "Joao Atualizado", "telefone": "(98) 98888-8888"},
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["nome"] == "Joao Atualizado"
    assert updated["telefone"] == "98988888888"

    delete_response = client.delete(f"/api/clientes/{created['id']}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Cliente inativado com sucesso"}

    second_delete_response = client.delete(f"/api/clientes/{created['id']}")
    assert second_delete_response.status_code == 200
    assert second_delete_response.json() == {"message": "Cliente já estava inativo"}

    with next(client.app.dependency_overrides[get_clientes_db]()) as db:
        audit_events = [event for event in db.scalars(select(AuditLog.event_type)).all()]
        assert sorted(audit_events) == sorted([
            "cliente_criado",
            "cliente_alterado",
            "cliente_inativado",
        ])
