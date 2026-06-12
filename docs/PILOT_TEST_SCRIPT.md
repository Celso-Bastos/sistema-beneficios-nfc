# Roteiro de Teste do Piloto

## Fluxo A - Cadastro

1. Abrir o sistema.
2. Ir para `Clientes`.
3. Clicar em `Novo cliente`.
4. Cadastrar cliente ficticio ou cliente com consentimento.
5. Confirmar mensagem de sucesso.
6. Voltar para lista.
7. Confirmar que o cliente aparece.

## Fluxo B - Vinculo NFC

1. Ir para `Vincular NFC`.
2. Clicar no campo UID.
3. Aproximar a tag NFC.
4. Confirmar que o UID foi preenchido.
5. Selecionar cliente.
6. Clicar em vincular.
7. Confirmar mensagem de sucesso.

## Fluxo C - Consulta NFC

1. Ir para `Consultar NFC`.
2. Aproximar a tag NFC.
3. Confirmar que o cliente aparece.
4. Conferir nome e telefone.
5. Confirmar que CPF nao aparece.
6. Clicar em `Limpar e ler outra tag`.
7. Repetir com outra tag.

## Fluxo D - Erros

1. Consultar tag nao cadastrada.
2. Confirmar mensagem amigavel.
3. Tentar vincular UID vazio.
4. Tentar cadastrar cliente invalido.
5. Desconectar internet.
6. Observar mensagem de indisponibilidade.
7. Registrar incidentes no modelo oficial.
