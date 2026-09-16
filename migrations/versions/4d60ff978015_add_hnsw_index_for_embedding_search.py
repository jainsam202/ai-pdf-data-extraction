from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d60ff978015'
down_revision: Union[str, Sequence[str], None] = '1f58d0911de2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS
        ix_document_embeddings_embedding_hnsw
        ON document_embeddings
        USING hnsw (embedding vector_cosine_ops)
        """
    )    
    

def downgrade():
    op.execute(
        """
        DROP INDEX IF EXISTS
        ix_document_embeddings_embedding_hnsw
        """
    )
