from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

connect_args = (
    {"connect_timeout": 5}
    if settings.sqlalchemy_database_url.startswith("postgresql")
    else {}
)

try:
    engine = (
        create_engine(
            settings.sqlalchemy_database_url,
            pool_pre_ping=True,
            connect_args=connect_args,
        )
        if settings.DATABASE_URL
        else None
    )
except (ArgumentError, SQLAlchemyError):
    engine = None

SessionLocal = (
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
    if engine is not None
    else None
)


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
