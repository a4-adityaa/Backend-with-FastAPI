"""adding extra columns to post2 table

Revision ID: f8bae896211c
Revises: 7a716f1eca7f
Create Date: 2026-11-12 06:53:43.847869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8bae896211c'
down_revision: Union[str, Sequence[str], None] = '7a716f1eca7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post2', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('post2', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post2', 'publsihed')
    op.drop_column('post2', 'created_at')
    pass
