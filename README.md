# Pequenas Cidades NFC

TODO: Evoluir este monorepo como MVP para um sistema NFC simples, focado em cadastro de clientes, vinculo de tags NFC e consulta por UID.

## Objetivo do MVP

Preparar uma base limpa para validar:

- leitura de UID de tag NFC;
- cadastro de cliente;
- vinculo entre UID NFC e cliente;
- consulta de cliente pelo UID;
- base futura para descontos e historico de leituras.

## Arquitetura Planejada

- Frontend web: React ou Next.js, com hospedagem futura na Vercel.
- Backend/API: Python FastAPI, com hospedagem futura no Render.
- Banco de dados: PostgreSQL, com preferencia inicial por Supabase.
- Leitor NFC: primeiro validar modo teclado HID; se nao funcionar, preparar app local em Python.

## Como o Projeto Sera Evoluido

TODO: Comecar pela validacao do leitor NFC em campo de texto no frontend.
TODO: Definir modelo inicial do banco antes de implementar rotas reais.
TODO: Criar API FastAPI somente apos fechar os contratos principais.
TODO: Criar telas simples somente apos validar cadastro, vinculo e consulta por UID.
TODO: Adicionar autenticacao apenas em fase posterior.

## Areas do Monorepo

- `frontend/`: base futura da interface web.
- `backend/`: base futura da API FastAPI.
- `local-nfc-reader/`: base futura para leitura local caso HID nao funcione.
- `database/`: rascunhos de schema e migrations.
- `docs/`: planejamento, arquitetura, fluxos e roadmap.
- `scripts/`: scripts auxiliares futuros.
- `config/`: exemplos de configuracao para deploy futuro.

