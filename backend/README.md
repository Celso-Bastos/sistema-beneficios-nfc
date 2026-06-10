# Backend

API FastAPI do MVP sistema-beneficios-nfc.

As Fases 1 e 2 validam estrutura do backend, execucao local, deploy no Render,
rotas de saude, configuracao por variaveis de ambiente e base inicial de
persistencia com PostgreSQL/Supabase, SQLAlchemy e Alembic. Ainda nao ha CRUD,
autenticacao, descontos, dashboard, frontend ou regras de negocio.

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

## Render

Start Command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
