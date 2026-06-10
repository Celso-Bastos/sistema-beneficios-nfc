# Modelo de Banco de Dados

## Objetivo

Esta modelagem cria a base de persistencia da Fase 2 do MVP
sistema-beneficios-nfc. O foco e preparar PostgreSQL/Supabase, SQLAlchemy e
Alembic para as entidades iniciais, sem implementar regras de negocio ou CRUDs.

## Tabelas

### clientes

Armazena os clientes que poderao ter tags NFC vinculadas.

| Campo | Tipo | Obrigatorio | Observacao |
| --- | --- | --- | --- |
| id | UUID | Sim | Chave primaria |
| nome | string | Sim | Nome do cliente |
| cpf | string | Nao | Unico e indexado |
| telefone | string | Nao | Telefone do cliente |
| email | string | Nao | Email do cliente |
| ativo | boolean | Sim | Padrao `true` |
| created_at | datetime com timezone | Sim | Criacao do registro |
| updated_at | datetime com timezone | Sim | Atualizacao do registro |

### nfc_tags

Armazena tags NFC vinculadas a clientes.

| Campo | Tipo | Obrigatorio | Observacao |
| --- | --- | --- | --- |
| id | UUID | Sim | Chave primaria |
| uid | string | Sim | Unico e indexado |
| cliente_id | UUID | Sim | FK para `clientes.id` |
| status | string | Sim | Padrao `ativa` |
| created_at | datetime com timezone | Sim | Criacao do registro |
| updated_at | datetime com timezone | Sim | Atualizacao do registro |

### leituras_nfc

Registra leituras de UID NFC realizadas pelo sistema.

| Campo | Tipo | Obrigatorio | Observacao |
| --- | --- | --- | --- |
| id | UUID | Sim | Chave primaria |
| uid | string | Sim | Indexado |
| cliente_id | UUID | Nao | FK opcional para `clientes.id` |
| origem | string | Nao | Origem da leitura |
| sucesso | boolean | Sim | Padrao `true` |
| created_at | datetime com timezone | Sim | Criacao do registro |

## Relacionamentos

- Um cliente possui varias NFC tags.
- Uma NFC tag pertence a um cliente.
- Uma leitura NFC pode pertencer a um cliente.

## UID NFC

O leitor NFC funciona como HID Keyboard, entao o UID chega ao frontend como
texto digitado e deve ser tratado pelo backend como string, nao como numero.
Futuramente o UID deve ser normalizado para uppercase e sem espacos antes de
persistir ou consultar.

## Seguranca

- `DATABASE_URL` deve vir de variavel de ambiente.
- Nao versione arquivos `.env` com credenciais reais.
- Nao exponha `DATABASE_URL`, senha ou stack trace em respostas da API.
- Nao use service role key da Supabase nesta fase.
- Nao use secret key da Supabase no frontend.

## Migrations

Rodar migrations:

```bash
alembic upgrade head
```

Criar nova migration futuramente:

```bash
alembic revision --autogenerate -m "mensagem"
```

## Teste de Conexao

Com a API rodando, testar:

```text
GET /database/status
```

Sem `DATABASE_URL`, a resposta esperada e HTTP 503 com:

```json
{
  "status": "error",
  "message": "DATABASE_URL is not configured"
}
```

Com `DATABASE_URL` valida, a resposta esperada e:

```json
{
  "status": "ok",
  "database": "connected"
}
```
