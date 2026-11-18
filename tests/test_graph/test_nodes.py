from unittest.mock import Mock
from langchain_core.documents import Document
from app.graph.nodes import retrieve_documents


def test_retrieve_documents():
    retriever = Mock()
    retriever.invoke.return_value = [
        Document(
            page_content="Revenue was ₹10 crore.",
            metadata={
                "chunk_id": 1,
                "document_id": 10,
                "score": 0.92,
            },
        )
    ]

    state = {
        "question": "What was the revenue?",
    }

    result = retrieve_documents(
        state,
        retriever,
    )

    assert len(result["documents"]) == 1
    assert result["retrieval_attempts"] == 1

    retriever.invoke.assert_called_once_with(
        "What was the revenue?"
    )
