"""create school settings table

Revision ID: 7259138838ba
Revises: 712a68a99db0
Create Date: 2026-08-22 17:50:48.530487
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7259138838ba"
down_revision: Union[str, Sequence[str], None] = "712a68a99db0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "school_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("school_name", sa.String(150), nullable=False),
        sa.Column("opening_time", sa.Time(), nullable=False),
        sa.Column("closing_time", sa.Time(), nullable=False),
        sa.Column("default_lesson_duration", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("buffer_minutes", sa.Integer(), nullable=False, server_default="15"),
        sa.Column("cancellation_hours", sa.Integer(), nullable=False, server_default="24"),
        sa.Column("timezone", sa.String(100), nullable=False, server_default="Australia/Sydney"),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )


def downgrade() -> None:
    op.drop_table("school_settings")