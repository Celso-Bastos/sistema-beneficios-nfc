# Modelo de Dados Draft

TODO: Este documento descreve entidades planejadas, sem criar banco real.

## clientes

Representa a pessoa cadastrada no sistema.

Campos futuros possiveis:

- id;
- nome;
- telefone;
- documento opcional;
- data de cadastro;
- status.

## nfc_tags

Representa uma tag NFC fisica.

Campos futuros possiveis:

- id;
- uid;
- cliente_id;
- status;
- data de cadastro;
- data de vinculo.

## empresas

Representa empresas participantes ou unidades operacionais.

Campos futuros possiveis:

- id;
- nome;
- cidade;
- status.

## usuarios

Representa usuarios internos do sistema.

Campos futuros possiveis:

- id;
- nome;
- email;
- empresa_id;
- perfil.

TODO: Nao implementar autenticacao nesta fase.

## leituras_nfc

Representa historico futuro de leituras NFC.

Campos futuros possiveis:

- id;
- uid;
- cliente_id;
- empresa_id;
- usuario_id;
- data da leitura;
- origem da leitura;
- observacao.

