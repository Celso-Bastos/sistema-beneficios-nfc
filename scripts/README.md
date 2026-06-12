# Scripts

Scripts auxiliares opcionais para preparacao e avaliacao do piloto.

## Regras de Seguranca

- Nao inserir `DATABASE_URL` real no codigo.
- Nao commitar `.env`.
- Nao usar dados reais sem consentimento.
- Nao exportar CPF, telefone ou email completos.
- Rodar apenas em ambiente controlado.

## Scripts Disponiveis

### create_fake_pilot_data.py

Gera clientes ficticios para teste via API FastAPI.

Por padrao, apenas mostra os dados que seriam enviados:

```bash
python scripts/create_fake_pilot_data.py --api-url http://127.0.0.1:8000
```

Para enviar de fato, o script exige confirmacao interativa:

```bash
python scripts/create_fake_pilot_data.py --api-url http://127.0.0.1:8000 --send
```

### export_pilot_summary.py

Exporta somente metricas agregadas do banco, sem dados pessoais:

```bash
set DATABASE_URL=postgresql://usuario:senha@host:5432/database
python scripts/export_pilot_summary.py
```

O resultado sai em JSON no terminal.
