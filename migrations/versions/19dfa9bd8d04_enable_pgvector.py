"""enable pgvector

Revision ID: 19dfa9bd8d04
Revises: 9b11550463cc
Create Date: 2026-07-31 15:53:30.970269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19dfa9bd8d04'
down_revision: Union[str, Sequence[str], None] = '9b11550463cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
