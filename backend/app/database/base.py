from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


import app.models.cliente  # noqa: E402,F401
import app.models.leitura_nfc  # noqa: E402,F401
import app.models.nfc_tag  # noqa: E402,F401
