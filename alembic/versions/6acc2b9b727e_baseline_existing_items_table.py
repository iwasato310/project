"""baseline existing items table

Revision ID: 6acc2b9b727e
Revises: 
Create Date: 2026-07-29 12:46:41.909546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6acc2b9b727e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial items table."""

    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_items_name"),
        "items",
        ["name"],
        unique=False,
    )


def downgrade() -> None:
    """Drop initial items table."""

    op.drop_index(
        op.f("ix_items_name"),
        table_name="items",
    )

    op.drop_table("items")
