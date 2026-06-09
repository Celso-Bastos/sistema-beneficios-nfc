# Local NFC Reader

TODO: Preparar base futura para um app local em Python caso o leitor NFC nao funcione como teclado HID.

## Cenario Principal

Primeiro, o leitor NFC sera testado como teclado HID. Se funcionar, o UID sera digitado diretamente em um campo do frontend e esta pasta podera ficar sem implementacao inicial.

## Cenario Alternativo

Se o modo HID nao funcionar bem, esta area podera receber um app local Python para:

- ler UID do dispositivo NFC;
- normalizar o UID;
- enviar a leitura para o backend;
- registrar logs locais de diagnostico.

## Observacoes

TODO: Nao ha codigo funcional nesta fase.
TODO: Nao ha dependencias instaladas nesta fase.

