"""make nfc tag cliente nullable

Revision ID: 0002_nfc_tag_cliente_nullable
Revises: 0001_initial_database
Create Date: 2026-06-11
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_nfc_tag_cliente_nullable"
down_revision = "0001_initial_database"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "nfc_tags",
        "cliente_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "nfc_tags",
        "cliente_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False,
    )
