"""add Room table second try

Revision ID: f4e244e7238c
Revises: 29a198c1d450
Create Date: 2025-04-02 19:35:46.057988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'f4e244e7238c'
down_revision: Union[str, None] = '29a198c1d450'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hotel_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_rooms_id'), 'rooms', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_rooms_id'), table_name='rooms')
    op.drop_table('rooms')
