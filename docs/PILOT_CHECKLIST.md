# Checklist Pre-Piloto

## Infraestrutura

- [ ] Backend Render online.
- [ ] Frontend Vercel online.
- [ ] Banco Supabase acessivel.
- [ ] Variaveis de ambiente configuradas.
- [ ] CORS configurado para a URL do frontend.
- [ ] `GET /health` OK.
- [ ] `GET /health/detailed` OK.
- [ ] `alembic upgrade head` executado no banco do piloto.

## Equipamentos

- [ ] Computador ou notebook.
- [ ] Navegador atualizado.
- [ ] Leitor NFC USB.
- [ ] Tags NFC.
- [ ] Internet estavel.
- [ ] Bloco de Notas ou editor simples para testar o leitor.

## Teste do Leitor

- [ ] Abrir Bloco de Notas.
- [ ] Aproximar uma tag.
- [ ] Confirmar UID digitado automaticamente.
- [ ] Repetir com 3 tags diferentes.
- [ ] Confirmar que cada tag gera UID esperado.

## Sistema

- [ ] Abrir frontend.
- [ ] Criar cliente de teste.
- [ ] Vincular tag.
- [ ] Consultar tag.
- [ ] Ler outra tag.
- [ ] Confirmar mensagens de erro com tag nao cadastrada.

## Seguranca e LGPD

- [ ] Nao usar CPF real sem autorizacao.
- [ ] Nao usar telefone real sem autorizacao.
- [ ] Usar dados ficticios sempre que possivel.
- [ ] Nao deixar painel aberto sem supervisao.
- [ ] Nao compartilhar links administrativos publicamente.
- [ ] Nao registrar CPF/telefone em planilhas de incidente sem consentimento.
