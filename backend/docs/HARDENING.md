# Hardening do MVP

## Objetivo

Preparar o sistema-beneficios-nfc para piloto real com foco em seguranca,
observabilidade, estabilidade e qualidade operacional.

## Tratamento Global de Erros

A API possui handlers globais para:

- `HTTPException`
- erros de validacao
- erros SQLAlchemy
- excecoes inesperadas

As respostas evitam stack traces, SQL interno e detalhes sensiveis:

```json
{
  "error": true,
  "message": "Erro interno"
}
```

## Logs Estruturados

Cada requisicao gera log JSON com:

- `request_id`
- metodo HTTP
- path
- status
- tempo de execucao em ms

Nao registrar CPF, telefone, email, `DATABASE_URL`, SQL ou secrets.

## Request ID

Toda requisicao recebe ou reutiliza o header `X-Request-ID`. O mesmo valor e
retornado na resposta para rastreabilidade operacional.

## Rate Limit

Foi adicionada protecao em memoria para endpoints criticos:

- `POST /api/clientes`
- `POST /api/nfc-tags/vincular`
- `GET /api/nfc-tags/lookup/{uid}`

Padrao atual: 100 requisicoes por minuto por IP.

## Health Check Detalhado

Endpoint:

```text
GET /health/detailed
```

Retorna status da API, banco, versao e timestamp, sem segredos.

## Auditoria

Tabela `audit_logs` registra eventos operacionais sem dados pessoais completos:

- cliente criado
- cliente alterado
- cliente inativado
- NFC criada
- NFC vinculada

Campos: `id`, `event_type`, `entity`, `entity_id`, `created_at`.

## Headers de Seguranca

Todas as respostas recebem:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: no-referrer`
- `Cache-Control: no-store`

## Timeouts

O backend configura timeout de conexao com PostgreSQL. O frontend usa timeout
de 10 segundos para chamadas HTTP.

## LGPD

Cuidados aplicados:

- CPF nao e retornado nos endpoints NFC de lookup/leitura.
- Logs estruturados nao registram payloads nem dados pessoais.
- Auditoria registra apenas tipo de evento, entidade e ID.
- Documentacao orienta uso de dados ficticios em testes.

## Monitoramento

Para operacao piloto, acompanhar:

- quantidade de respostas 5xx;
- tempo medio dos endpoints NFC;
- volume de 429 por IP;
- falhas em `/health/detailed`;
- eventos registrados em `audit_logs`.
