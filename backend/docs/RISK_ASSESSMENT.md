# Relatorio de Risco

## Critico

- Nao ha autenticacao/autorizacao. O piloto deve operar em ambiente controlado
  ate que controle de acesso seja implementado.

## Alto

- Rate limit em memoria nao e distribuido. Em multiplas instancias, cada
  instancia tera seu proprio contador.
- Testes automatizados usam SQLite em memoria para fluxo basico, nao PostgreSQL
  real.

## Medio

- Nao ha mascaramento de CPF em endpoints administrativos de clientes.
- Nao ha auditoria por usuario porque ainda nao existe autenticacao.
- Nao ha tracing distribuido externo; rastreabilidade atual depende de logs e
  `X-Request-ID`.

## Baixo

- Logs usam stdout estruturado, suficiente para Render, mas ainda sem painel
  dedicado.
- Cobertura de testes foca fluxos principais; cenarios de concorrencia ainda
  nao foram cobertos.

## Riscos Aceitos no MVP

- Sem funcionalidades de beneficios, cashback ou dashboard avancado nesta fase.
- Sem Supabase client no frontend.
- Sem app local para NFC, pois o leitor opera como HID Keyboard.
