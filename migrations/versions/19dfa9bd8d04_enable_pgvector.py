from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "19dfa9bd8d04"
down_revision: Union[str, Sequence[str], None] = "9b11550463cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enable pgvector extension."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    """Disable pgvector extension."""
    op.execute("DROP EXTENSION IF EXISTS vector")