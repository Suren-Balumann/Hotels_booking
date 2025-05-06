"""add facilities tables

Revision ID: dce532c413b9
Revises: bb5fd1a7c737
Create Date: 2025-05-05 16:40:30.259064

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "dce532c413b9"
down_revision: Union[str, None] = "bb5fd1a7c737"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_facilities_id"), "facilities", ["id"], unique=False)
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_rooms_facilities_id"), "rooms_facilities", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_rooms_facilities_id"), table_name="rooms_facilities")
    op.drop_table("rooms_facilities")
    op.drop_index(op.f("ix_facilities_id"), table_name="facilities")
    op.drop_table("facilities")
