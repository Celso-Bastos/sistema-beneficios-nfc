# API de Clientes

## Objetivo

Rotas da Fase 3 para cadastro, consulta, atualizacao e inativacao logica de
clientes do MVP sistema-beneficios-nfc. Esta fase nao implementa NFC tags,
leituras, autenticacao, descontos ou frontend.

## Base URL

```text
/api/clientes
```

## Criar Cliente

```http
POST /api/clientes
Content-Type: application/json
```

Payload:

```json
{
  "nome": "Joao da Silva",
  "cpf": "123.456.789-00",
  "telefone": "+55 (98) 99999-9999",
  "email": "joao@email.com"
}
```

Resposta `201`:

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "nome": "Joao da Silva",
  "cpf": "12345678900",
  "telefone": "5598999999999",
  "email": "joao@email.com",
  "ativo": true,
  "created_at": "2026-06-10T12:00:00Z",
  "updated_at": "2026-06-10T12:00:00Z"
}
```

## Listar Clientes

```http
GET /api/clientes?ativo=true&limit=50&offset=0
```

Query params:

- `ativo`: opcional, boolean.
- `limit`: opcional, default `50`, maximo `100`.
- `offset`: opcional, default `0`.

Resposta `200`:

```json
{
  "items": [],
  "limit": 50,
  "offset": 0,
  "total": 0
}
```

## Buscar Cliente por ID

```http
GET /api/clientes/{cliente_id}
```

Se encontrado, retorna `200` com o cliente.

Se nao encontrado, retorna `404`:

```json
{
  "detail": "Cliente não encontrado"
}
```

## Atualizar Cliente

```http
PUT /api/clientes/{cliente_id}
Content-Type: application/json
```

Payload parcial:

```json
{
  "nome": "Joao Atualizado",
  "telefone": "98988888888"
}
```

Resposta `200`: cliente atualizado.

## Inativar Cliente

```http
DELETE /api/clientes/{cliente_id}
```

Nao remove fisicamente o registro. Define `ativo = false`.

Resposta `200` quando o cliente estava ativo:

```json
{
  "message": "Cliente inativado com sucesso"
}
```

Resposta `200` quando o cliente ja estava inativo:

```json
{
  "message": "Cliente já estava inativo"
}
```

Se o cliente nao existir, retorna `404`.

## Validacoes e Normalizacao

- `nome` e obrigatorio na criacao e deve ter pelo menos 2 caracteres.
- `nome` e trimado.
- `cpf` e opcional, mas quando informado deve ter 11 digitos.
- `cpf` e salvo somente com numeros.
- `cpf` e unico globalmente quando informado.
- Soft delete nao libera CPF para novo cadastro.
- `telefone` e opcional e salvo somente com numeros.
- `email` e opcional, validado, trimado e convertido para lowercase.
- Strings vazias nao sao aceitas como valores validos.

Um cliente inativo com CPF ja cadastrado deve ser reativado ou atualizado em
fluxo futuro. A Fase 3 nao implementa reativacao.

## Erros

CPF duplicado:

```json
{
  "detail": "Já existe um cliente cadastrado com este CPF"
}
```

Cliente inexistente:

```json
{
  "detail": "Cliente não encontrado"
}
```

Erros de validacao retornam HTTP `422` no formato padrao do FastAPI.

## Fluxo Esperado no MVP

1. Cadastrar cliente.
2. Listar clientes ativos.
3. Buscar cliente por ID.
4. Atualizar dados cadastrais.
5. Inativar cliente quando necessario.
6. Na proxima fase, vincular NFC tags ao cliente existente.

## LGPD e Seguranca

CPF, telefone e email sao dados pessoais. Use apenas dados ficticios nos testes
do MVP. Nao registre CPF ou telefone em logs, mensagens de erro ou seeds.
