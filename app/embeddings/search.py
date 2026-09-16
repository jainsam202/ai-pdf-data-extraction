from sqlalchemy.orm import Session
from app.embeddings.repository import EmbeddingRepository
from app.embeddings.service import EmbeddingService
from app.embeddings.schemas import (
    SearchRequest,
    SearchResponse,
    SearchResult,
)


class SemanticSearchService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.repository = EmbeddingRepository(db)

    def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        query_embedding = (
            self.embedding_service
            .generate_embedding(
                request.query
            )
        )

        rows = self.repository.search_similar(
            query_embedding=query_embedding,
            top_k=request.top_k,
            document_id=request.document_id,
            min_score=request.min_score,
        )

        results = [
            SearchResult(
                chunk_id=row.chunk_id,
                document_id=row.document_id,
                content=row.content,
                score=float(row.score),
            )
            for row in rows
        ]

        return SearchResponse(
            query=request.query,
            results=results,
        )