from uuid import UUID
from sqlalchemy.orm import Session
from langchain_core.documents import Document
from app.embeddings.repository import EmbeddingRepository
from app.embeddings.service import EmbeddingService


class PgVectorRetriever:
    def __init__(
        self,
        db: Session,
        document_id: UUID | None = None,
        top_k: int = 5,
        min_score: float = 0.50,
    ):
        self.embedding_service = EmbeddingService()
        self.repository = EmbeddingRepository(db)
        self.document_id = document_id
        self.top_k = top_k
        self.min_score = min_score

    def invoke(self, query: str) -> list[Document]:
        query_embedding = (
            self.embedding_service.generate_embedding(query)
        )

        rows = self.repository.search_similar(
            query_embedding=query_embedding,
            top_k=self.top_k,
            document_id=self.document_id,
            min_score=self.min_score,
        )

        return [
            Document(
                page_content=row.content,
                metadata={
                    "chunk_id": str(row.chunk_id),
                    "document_id": str(row.document_id),
                    "score": float(row.score),
                },
            )
            for row in rows
        ]
