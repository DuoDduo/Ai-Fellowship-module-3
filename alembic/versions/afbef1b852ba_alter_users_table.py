"""alter users table

Revision ID: afbef1b852ba
Revises: 
Create Date: 2025-10-23 11:57:06.962932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afbef1b852ba'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
               ALTER TABLE users ADD COLUMN user_type VARCHAR(100);
               """)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(""" ALTER TABLE users
               DROP COLUMN user_type""")
    pass
