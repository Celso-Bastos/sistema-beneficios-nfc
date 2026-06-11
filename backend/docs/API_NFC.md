# API NFC

## Objetivo

Rotas da Fase 4 para cadastro, vinculo, consulta e registro de leituras NFC no
MVP sistema-beneficios-nfc.

O leitor NFC funciona como HID Keyboard. O backend recebe apenas o UID como
texto digitado pelo frontend. Nao ha integracao USB, serial ou aplicativo local.

## Normalizacao de UID

Todo UID recebido e:

- trimado;
- convertido para uppercase;
- salvo sem espacos ou quebras de linha;
- rejeitado quando vazio.

Exemplo:

```text
04 a8 b9 c1 -> 04A8B9C1
```

## Cadastro de Tag NFC

```http
POST /api/nfc-tags
Content-Type: application/json
```

Payload:

```json
{
  "uid": "04 a8 b9 c1"
}
```

Resposta `201`:

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "uid": "04A8B9C1",
  "status": "ativa"
}
```

## Listar Tags NFC

```http
GET /api/nfc-tags?limit=50&offset=0
```

Resposta `200`:

```json
{
  "items": [],
  "limit": 50,
  "offset": 0,
  "total": 0
}
```

## Buscar Tag por UID

```http
GET /api/nfc-tags/{uid}
```

O UID da URL tambem e normalizado antes da consulta.

## Inativar Tag NFC

```http
DELETE /api/nfc-tags/{id}
```

Soft delete. A tag nao e removida fisicamente; o status passa para `inativa`.

## Vincular Tag a Cliente

```http
POST /api/nfc-tags/vincular
Content-Type: application/json
```

Payload:

```json
{
  "uid": "04A8B9C1",
  "cliente_id": "00000000-0000-0000-0000-000000000000"
}
```

Regras:

- cliente deve existir;
- tag NFC deve existir;
- tag ativa nao pode estar vinculada a outro cliente.

Resposta `200`:

```json
{
  "message": "Tag vinculada com sucesso"
}
```

## Consulta Principal por UID

```http
GET /api/nfc-tags/lookup/{uid}
```

Fluxo:

```text
UID -> NFC Tag -> Cliente
```

Resposta `200`:

```json
{
  "uid": "04A8B9C1",
  "cliente": {
    "id": "00000000-0000-0000-0000-000000000000",
    "nome": "Joao Silva",
    "telefone": "98999999999"
  }
}
```

Se a tag nao existir, estiver inativa ou nao estiver vinculada:

```json
{
  "detail": "Tag NFC não encontrada"
}
```

## Registrar Leitura NFC

```http
POST /api/nfc-tags/registrar-leitura
Content-Type: application/json
```

Payload:

```json
{
  "uid": "04A8B9C1",
  "origem": "web"
}
```

A API busca a tag, busca o cliente vinculado, registra a leitura em
`leituras_nfc` e retorna o cliente.

Resposta `200`:

```json
{
  "cliente": {
    "id": "00000000-0000-0000-0000-000000000000",
    "nome": "Joao Silva",
    "telefone": "98999999999"
  }
}
```

## LGPD e Seguranca

Endpoints NFC nao retornam CPF por padrao. As respostas do fluxo NFC retornam
somente `id`, `nome` e `telefone` do cliente.

Nao exponha `DATABASE_URL`, SQL interno, senhas ou stack traces em respostas da
API.
