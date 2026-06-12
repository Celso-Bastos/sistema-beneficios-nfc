import json
import os
import sys

import psycopg


def fetch_scalar(cursor, query: str) -> int:
    cursor.execute(query)
    value = cursor.fetchone()[0]
    return int(value or 0)


def main() -> int:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL nao configurada.", file=sys.stderr)
        return 1

    try:
        with psycopg.connect(database_url, connect_timeout=10) as connection:
            with connection.cursor() as cursor:
                summary = {
                    "clientes_total": fetch_scalar(cursor, "select count(*) from clientes"),
                    "clientes_ativos": fetch_scalar(
                        cursor,
                        "select count(*) from clientes where ativo = true",
                    ),
                    "nfc_tags_total": fetch_scalar(cursor, "select count(*) from nfc_tags"),
                    "nfc_tags_ativas": fetch_scalar(
                        cursor,
                        "select count(*) from nfc_tags where status = 'ativa'",
                    ),
                    "leituras_total": fetch_scalar(
                        cursor,
                        "select count(*) from leituras_nfc",
                    ),
                    "leituras_sucesso": fetch_scalar(
                        cursor,
                        "select count(*) from leituras_nfc where sucesso = true",
                    ),
                    "leituras_falha": fetch_scalar(
                        cursor,
                        "select count(*) from leituras_nfc where sucesso = false",
                    ),
                    "audit_logs_total": fetch_scalar(
                        cursor,
                        "select count(*) from audit_logs",
                    ),
                }
    except psycopg.Error:
        print("Nao foi possivel exportar metricas agregadas do piloto.", file=sys.stderr)
        return 1

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
