"""create initial database

Revision ID: 0001_initial_database
Revises:
Create Date: 2026-06-10
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial_database"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "clientes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("cpf", sa.String(length=14), nullable=True),
        sa.Column("telefone", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("ativo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_clientes_cpf"), "clientes", ["cpf"], unique=True)

    op.create_table(
        "nfc_tags",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("uid", sa.String(length=128), nullable=False),
        sa.Column("cliente_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default="ativa",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["cliente_id"], ["clientes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_nfc_tags_uid"), "nfc_tags", ["uid"], unique=True)

    op.create_table(
        "leituras_nfc",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("uid", sa.String(length=128), nullable=False),
        sa.Column("cliente_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("origem", sa.String(length=100), nullable=True),
        sa.Column("sucesso", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["cliente_id"], ["clientes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_leituras_nfc_uid"),
        "leituras_nfc",
        ["uid"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_leituras_nfc_uid"), table_name="leituras_nfc")
    op.drop_table("leituras_nfc")
    op.drop_index(op.f("ix_nfc_tags_uid"), table_name="nfc_tags")
    op.drop_table("nfc_tags")
    op.drop_index(op.f("ix_clientes_cpf"), table_name="clientes")
    op.drop_table("clientes")
