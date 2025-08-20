"""add content column to posts table

Revision ID: 7ce6537bf52c
Revises: 4821072349ad
Create Date: 2025-08-19 21:39:52.833990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ce6537bf52c'
down_revision: Union[str, Sequence[str], None] = '4821072349ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
