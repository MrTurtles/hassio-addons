"""household and settings

Revision ID: 0001_household
Revises:
Create Date: 2026-11-22
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_household"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "households",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("locale", sa.String(length=16), nullable=False),
        sa.Column("default_servings", sa.Integer(), nullable=False),
        sa.Column("week_starts_on", sa.Integer(), nullable=False),
        sa.Column("unit_system", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "default_servings >= 1 AND default_servings <= 24",
            name="ck_household_servings",
        ),
        sa.CheckConstraint(
            "week_starts_on >= 1 AND week_starts_on <= 7",
            name="ck_household_week_start",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "household_settings",
        sa.Column("household_id", sa.Uuid(), nullable=False),
        sa.Column("subtract_pantry", sa.Boolean(), nullable=False),
        sa.Column("auto_shopping", sa.Boolean(), nullable=False),
        sa.Column("preserve_checked", sa.Boolean(), nullable=False),
        sa.Column("preserve_manual", sa.Boolean(), nullable=False),
        sa.Column("auto_consume_pantry", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["household_id"], ["households.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("household_id"),
    )


def downgrade() -> None:
    op.drop_table("household_settings")
    op.drop_table("households")
