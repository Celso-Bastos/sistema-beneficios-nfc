import pytest
from pydantic import ValidationError

from app.schemas.cliente import ClienteCreate, ClienteUpdate


def test_nome_com_menos_de_dois_caracteres_falha() -> None:
    with pytest.raises(ValidationError):
        ClienteCreate(nome="A")


def test_cpf_com_pontuacao_normaliza_para_digitos() -> None:
    cliente = ClienteCreate(nome="Joao", cpf="123.456.789-00")

    assert cliente.cpf == "12345678900"


def test_cpf_com_tamanho_invalido_falha() -> None:
    with pytest.raises(ValidationError):
        ClienteCreate(nome="Joao", cpf="123")


def test_telefone_com_mascara_normaliza_para_digitos() -> None:
    cliente = ClienteCreate(nome="Joao", telefone="+55 (98) 99999-9999")

    assert cliente.telefone == "5598999999999"


def test_email_normaliza_para_lowercase() -> None:
    cliente = ClienteCreate(nome="Joao", email=" TESTE@EXAMPLE.COM ")

    assert cliente.email == "teste@example.com"


def test_cliente_update_vazio_e_permitido_no_schema() -> None:
    update = ClienteUpdate()

    assert update.model_dump(exclude_unset=True) == {}
