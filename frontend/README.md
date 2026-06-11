# Frontend

Frontend MVP do projeto sistema-beneficios-nfc.

Esta fase valida o uso em navegador para cadastro de clientes, listagem de tags
NFC, vinculo UID -> cliente e consulta de cliente por UID digitado pelo leitor
NFC HID Keyboard.

## Stack

- Next.js
- React
- TypeScript
- CSS simples
- `fetch` nativo

O frontend fala apenas com a API FastAPI. Nao usa Supabase client no browser.

## Configurar ambiente

Crie um arquivo local `.env.local` apenas na sua maquina, sem versionar:

```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Para deploy, use a URL do backend no Render:

```bash
NEXT_PUBLIC_API_URL=https://sua-api.onrender.com
```

## Instalar

```bash
npm install
```

## Rodar localmente

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Telas

- `/` - inicio do MVP
- `/clientes` - lista de clientes
- `/clientes/novo` - cadastro de cliente
- `/nfc` - lista de NFC tags
- `/nfc/vincular` - vincular UID NFC a cliente
- `/nfc/consultar` - consultar cliente por UID

## Fluxo de teste com leitor NFC HID

1. Configure `NEXT_PUBLIC_API_URL` apontando para a API FastAPI.
2. Inicie o backend.
3. Rode `npm run dev`.
4. Abra `/clientes/novo` e cadastre um cliente ficticio.
5. Abra `/nfc/vincular`.
6. Clique no campo UID e aproxime a tag NFC do leitor.
7. Selecione o cliente e vincule.
8. Abra `/nfc/consultar`.
9. Aproxime a mesma tag NFC.
10. O cliente deve aparecer na tela sem exibir CPF.

## LGPD e seguranca

- Use somente dados ficticios em testes.
- Nao armazene CPF, telefone ou dados pessoais em `localStorage`.
- Nao exponha CPF na consulta NFC.
- Nao use `SUPABASE_SECRET_KEY` ou service role key no frontend.
- Nao chame Supabase diretamente do browser nesta fase.
- Nao registre dados pessoais no console.
