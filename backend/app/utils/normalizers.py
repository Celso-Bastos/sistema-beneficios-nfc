import re


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def normalize_cpf(value: str | None) -> str | None:
    normalized = normalize_text(value)
    if normalized is None:
        return None

    return normalized.replace(".", "").replace("-", "")


def normalize_phone(value: str | None) -> str | None:
    normalized = normalize_text(value)
    if normalized is None:
        return None

    return re.sub(r"[\s()+-]", "", normalized)
