from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import ConfigDict, Field, PrivateAttr

from app.embeddings.model import EmbeddingModel
from app.embeddings.repository import EmbeddingRepository


class PgVectorRetriever(BaseRetriever):
    """
    LangChain retriever backed by PostgreSQL + pgvector.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    embedding_model: EmbeddingModel = Field(exclude=True)
    embedding_repository: EmbeddingRepository = Field(exclude=True)

    top_k: int = 5
    min_score: float = 0.50
    document_id: Optional[int] = None

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager=None,
    ) -> List[Document]:

        query_embedding = self.embedding_model.embed_query(query)

        results = self.embedding_repository.search_similar(
            query_embedding=query_embedding,
            top_k=self.top_k,
            min_score=self.min_score,
            document_id=self.document_id,
        )

        documents = []

        for result in results:
            metadata = {
                "chunk_id": result.chunk_id,
                "document_id": result.document_id,
                "score": result.score,
            }

            documents.append(
                Document(
                    page_content=result.content,
                    metadata=metadata,
                )
            )

        return documents