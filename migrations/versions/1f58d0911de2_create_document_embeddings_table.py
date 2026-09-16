from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "1f58d0911de2"
down_revision: Union[str, Sequence[str], None] = "19dfa9bd8d04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create document_embeddings table."""

    op.create_table(
        "document_embeddings",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "chunk_id",
            UUID(as_uuid=True),
            sa.ForeignKey(
                "document_chunks.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "model_name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "embedding",
            Vector(384),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Drop document_embeddings table."""

    op.drop_table("document_embeddings")