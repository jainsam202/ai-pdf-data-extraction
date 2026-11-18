from app.embeddings.model import EmbeddingModel
from app.embeddings.repository import EmbeddingRepository
from app.embeddings.retriever import PgVectorRetriever


def create_pgvector_retriever(
    embedding_model: EmbeddingModel,
    embedding_repository: EmbeddingRepository,
    top_k: int = 5,
    min_score: float = 0.50,
    document_id: int | None = None,
) -> PgVectorRetriever:

    return PgVectorRetriever(
        embedding_model=embedding_model,
        embedding_repository=embedding_repository,
        top_k=top_k,
        min_score=min_score,
        document_id=document_id,
    )