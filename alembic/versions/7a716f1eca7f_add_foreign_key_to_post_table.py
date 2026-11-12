"""add foreign key to post table

Revision ID: 7a716f1eca7f
Revises: 4ea5aa8febbd
Create Date: 2026-11-12 06:23:03.476165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a716f1eca7f'
down_revision: Union[str, Sequence[str], None] = '4ea5aa8febbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post2',sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='post2', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk', table_name='post2')
    op.drop_column('post2', 'owener_id')
    pass
