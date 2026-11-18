from unittest.mock import Mock

from langchain_core.documents import Document

from app.embeddings.model import EmbeddingModel
from app.embeddings.repository import EmbeddingRepository
from app.embeddings.retriever import PgVectorRetriever


def test_pgvector_retriever():

    embedding_model = Mock(spec=EmbeddingModel)
    embedding_model.embed_query.return_value = [0.1] * 384

    embedding_repository = Mock(spec=EmbeddingRepository)
    embedding_repository.search_similar.return_value = [
        Mock(
            chunk_id=1,
            document_id=10,
            content="This is relevant document content.",
            score=0.91,
        )
    ]

    retriever = PgVectorRetriever(
        embedding_model=embedding_model,
        embedding_repository=embedding_repository,
        top_k=5,
        min_score=0.50,
    )

    documents = retriever.invoke(
        "What is this document about?"
    )

    assert len(documents) == 1

    assert isinstance(
        documents[0],
        Document,
    )

    assert documents[0].page_content == (
        "This is relevant document content."
    )

    assert documents[0].metadata == {
        "chunk_id": 1,
        "document_id": 10,
        "score": 0.91,
    }

    embedding_model.embed_query.assert_called_once_with(
        "What is this document about?"
    )

    embedding_repository.search_similar.assert_called_once_with(
        query_embedding=[0.1] * 384,
        top_k=5,
        min_score=0.50,
        document_id=None,
    )