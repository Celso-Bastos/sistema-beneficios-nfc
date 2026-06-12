import argparse
import json
import sys
import urllib.error
import urllib.request


FAKE_CLIENTES = [
    {
        "nome": "Cliente Ficticio 01",
        "cpf": "00000000001",
        "telefone": "11900000001",
        "email": "cliente.ficticio01@example.com",
    },
    {
        "nome": "Cliente Ficticio 02",
        "cpf": "00000000002",
        "telefone": "11900000002",
        "email": "cliente.ficticio02@example.com",
    },
    {
        "nome": "Cliente Ficticio 03",
        "cpf": "00000000003",
        "telefone": "11900000003",
        "email": "cliente.ficticio03@example.com",
    },
]


def post_json(api_url: str, path: str, payload: dict) -> dict:
    request = urllib.request.Request(
        f"{api_url.rstrip('/')}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera clientes ficticios para piloto controlado."
    )
    parser.add_argument("--api-url", required=True, help="URL base da API FastAPI.")
    parser.add_argument(
        "--send",
        action="store_true",
        help="Envia os dados ficticios para a API apos confirmacao.",
    )
    args = parser.parse_args()

    print(json.dumps(FAKE_CLIENTES, indent=2, ensure_ascii=False))

    if not args.send:
        print("Modo dry-run. Use --send para enviar apos revisar os dados.")
        return 0

    confirmation = input("Digite CRIAR para enviar clientes ficticios: ")
    if confirmation != "CRIAR":
        print("Operacao cancelada.")
        return 1

    for cliente in FAKE_CLIENTES:
        try:
            created = post_json(args.api_url, "/api/clientes", cliente)
            print(f"Cliente ficticio criado: {created['id']}")
        except urllib.error.HTTPError as exc:
            print(f"Falha HTTP controlada ao criar cliente ficticio: {exc.code}")
        except urllib.error.URLError:
            print("API indisponivel. Verifique a URL e tente novamente.")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
