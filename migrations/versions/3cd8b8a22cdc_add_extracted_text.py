from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "3cd8b8a22cdc"
down_revision: Union[str, Sequence[str], None] = "eb477e7cb314"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add extracted_text to documents."""
    op.add_column(
        "documents",
        sa.Column(
            "extracted_text",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove extracted_text from documents."""
    op.drop_column("documents", "extracted_text")