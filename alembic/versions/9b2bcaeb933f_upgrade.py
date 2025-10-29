"""upgrade

Revision ID: 9b2bcaeb933f
Revises: afbef1b852ba
Create Date: 2025-10-27 12:05:06.259288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b2bcaeb933f'
down_revision: Union[str, Sequence[str], None] = 'afbef1b852ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
               ALTER TABLE users ADD COLUMN user_id VARCHAR(100);
               """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(""" ALTER TABLE users
               DROP COLUMN user_type""")
    pass

