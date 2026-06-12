# Plano do Piloto Controlado

## Objetivo

Validar em campo se o MVP sistema-beneficios-nfc permite cadastrar clientes,
vincular tags NFC e identificar clientes pelo leitor NFC HID Keyboard com fluxo
simples para balcao.

## Escopo

Sera testado:

- cadastro de cliente;
- vinculo UID NFC -> cliente;
- consulta de cliente por UID;
- clareza das mensagens de erro;
- velocidade percebida no atendimento;
- uso por operador nao tecnico.

Nao sera testado:

- beneficios;
- cashback;
- pagamentos;
- dashboard avancado;
- IA/RPA;
- multiempresa;
- app mobile ou app local.

## Local Sugerido

Um estabelecimento pequeno, com atendimento em balcao e ambiente controlado.

## Quantidade Minima

- 1 estabelecimento.
- 1 computador ou notebook.
- 1 leitor NFC USB validado como HID Keyboard.
- 20 tags NFC.
- 20 clientes de teste ou clientes com consentimento.

## Duracao Sugerida

- 1 a 3 dias para teste inicial.
- Ate 7 dias para validacao real.

## Papeis

- Operador: usa o sistema no atendimento.
- Responsavel tecnico: acompanha erros, logs e incidentes.
- Responsavel pelo negocio: avalia valor, fluxo e decisao de produto.

## Criterios de Sucesso

- Cadastro de cliente em menos de 1 minuto.
- Vinculo NFC em menos de 30 segundos.
- Consulta NFC em menos de 2 segundos.
- Operador usa sem ajuda tecnica constante.
- Menos de 5% de falhas de leitura.
- Nenhum dado sensivel exposto indevidamente.

## Criterios de Reprovacao

- Operador nao consegue executar o fluxo sem suporte constante.
- Consulta NFC demora demais para uso em balcao.
- Falhas de leitura acima de 5%.
- Dados pessoais aparecem onde nao deveriam.
- Sistema fica indisponivel durante o teste.
