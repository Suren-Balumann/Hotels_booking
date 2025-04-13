"""initital migration

Revision ID: 41fe6ac75908
Revises:
Create Date: 2025-04-05 21:50:27.090465

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "41fe6ac75908"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_hotels_id"), "hotels", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_hotels_id"), table_name="hotels")
    op.drop_table("hotels")
