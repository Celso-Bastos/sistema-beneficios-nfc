# Backend

API FastAPI do MVP sistema-beneficios-nfc.

As Fases 1, 2 e 3 validam estrutura do backend, execucao local, deploy no
Render, rotas de saude, configuracao por variaveis de ambiente, base inicial de
persistencia com PostgreSQL/Supabase, SQLAlchemy e Alembic, e CRUD minimo de
Clientes. Ainda nao ha autenticacao, descontos, dashboard, frontend ou regras
de negocio de beneficios.

## Instalar

```bash
pip install -r requirements.txt
```

## Rodar localmente

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `GET /`
- `GET /health`
- `GET /database/status`
- `POST /api/clientes`
- `GET /api/clientes`
- `GET /api/clientes/{cliente_id}`
- `PUT /api/clientes/{cliente_id}`
- `DELETE /api/clientes/{cliente_id}`

## Variaveis de ambiente

Use `.env.example` como referencia. Nao crie ou versione arquivos `.env`
com credenciais reais.

Para conectar ao Supabase PostgreSQL, configure `DATABASE_URL` no ambiente:

```bash
DATABASE_URL=postgresql://usuario:senha@host:5432/database
```

O valor acima e apenas o formato esperado. Nao coloque credenciais reais em
arquivos versionados.

## Migrations

Rodar migration:

```bash
alembic upgrade head
```

Criar nova migration futuramente:

```bash
alembic revision --autogenerate -m "mensagem"
```

## Testar banco

```text
GET /database/status
```

Sem `DATABASE_URL`, o endpoint retorna HTTP 503 com mensagem controlada. Com
`DATABASE_URL` valida, retorna:

```json
{
  "status": "ok",
  "database": "connected"
}
```

Mais detalhes da modelagem estao em `docs/DATABASE_MODEL.md`.

## Clientes

Criar cliente:

```bash
curl -X POST http://127.0.0.1:8000/api/clientes \
  -H "Content-Type: application/json" \
  -d "{\"nome\":\"Joao da Silva\",\"cpf\":\"123.456.789-00\",\"telefone\":\"+55 (98) 99999-9999\",\"email\":\"joao@email.com\"}"
```

Listar clientes:

```bash
curl http://127.0.0.1:8000/api/clientes
```

Buscar cliente:

```bash
curl http://127.0.0.1:8000/api/clientes/{cliente_id}
```

Atualizar cliente:

```bash
curl -X PUT http://127.0.0.1:8000/api/clientes/{cliente_id} \
  -H "Content-Type: application/json" \
  -d "{\"nome\":\"Joao Atualizado\",\"telefone\":\"98988888888\"}"
```

Inativar cliente:

```bash
curl -X DELETE http://127.0.0.1:8000/api/clientes/{cliente_id}
```

As mesmas rotas podem ser testadas no navegador, quando forem `GET`, ou em
clientes HTTP como Postman e Insomnia. A documentacao detalhada esta em
`docs/API_CLIENTES.md`.

O CPF, quando informado, e unico globalmente. Inativar um cliente nao libera o
CPF para novo cadastro; uma reativacao podera ser implementada futuramente.

## LGPD e Seguranca

CPF, telefone e email sao dados pessoais sensiveis para o MVP. Use apenas
dados ficticios em testes, nao gere seeds com dados reais e nao registre CPF ou
telefone em logs ou mensagens de erro.

TODO: autenticacao e autorizacao serao obrigatorias antes de qualquer uso em
producao real.

Dividas tecnicas conhecidas estao documentadas em `docs/TECH_DEBT.md`.

## Render

Start Command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
