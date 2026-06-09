# Fluxos NFC

## Fluxo NFC em Modo HID Keyboard

1. Usuario posiciona a tag NFC no leitor.
2. O leitor se comporta como teclado.
3. O UID e digitado automaticamente em um campo do frontend.
4. O frontend envia o UID para a API.
5. A API consulta a tag NFC.
6. A API retorna o cliente vinculado, se existir.

TODO: Validar se o leitor adiciona Enter automaticamente apos o UID.
TODO: Validar formato do UID enviado pelo leitor.
TODO: Definir normalizacao de UID antes da implementacao.

## Fluxo NFC com App Local Python

1. App local Python se comunica com o leitor NFC.
2. App local captura o UID.
3. App local normaliza o UID.
4. App local envia a leitura para a API.
5. API consulta ou registra a leitura.
6. Frontend exibe o resultado quando aplicavel.

TODO: Usar este fluxo apenas se o modo HID nao for suficiente.
TODO: Definir como o frontend recebera feedback do app local, se necessario.

