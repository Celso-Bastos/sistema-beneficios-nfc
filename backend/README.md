# Backend

API minima em FastAPI para a Fase 1 do MVP sistema-beneficios-nfc.

Esta fase valida estrutura do backend, execucao local, deploy no Render,
rota de saude e preparacao segura para variaveis de ambiente. Nao ha banco
de dados, autenticacao, regras de negocio, NFC, dashboard ou frontend.

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

## Variaveis de ambiente

Use `.env.example` como referencia. Nao crie ou versione arquivos `.env`
com credenciais reais.

## Render

Start Command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
