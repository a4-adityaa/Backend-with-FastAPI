"""add a new column to post2 table

Revision ID: 50f50137cdce
Revises: ffc60455b31b
Create Date: 2026-11-12 05:53:16.002783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50f50137cdce'
down_revision: Union[str, Sequence[str], None] = 'ffc60455b31b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post2', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post2', 'content')
    pass
