# Dividas Tecnicas

## Autenticacao

O MVP ainda nao possui autenticacao ou autorizacao. Antes de uso em producao
real, todas as rotas que manipulam dados pessoais devem exigir usuario
autenticado e permissao adequada.

## CPF Unico Global

CPF e unico globalmente quando informado. Um cliente inativo nao libera o CPF
para novo cadastro. Futuramente pode ser criado um fluxo explicito de reativacao
ou revisao cadastral.

## Testes Automatizados

Os testes basicos nao dependem de Supabase ou credenciais reais. Testes de
integracao com PostgreSQL ainda devem ser adicionados para validar migrations,
constraints e comportamento real do banco.

## Politica Transacional

O service controla commit e rollback no CRUD de clientes. Operacoes futuras que
envolvam multiplas entidades, como cliente e NFC tag, devem manter uma unidade
transacional clara.

## Tratamento Global de Excecoes

A Fase 3 padroniza erros de banco no service de clientes, mas ainda nao existe
handler global para excecoes inesperadas da aplicacao.

## Auditoria

Quando houver autenticacao, sera necessario registrar auditoria por usuario para
operacoes sensiveis, especialmente alteracoes de dados pessoais.
