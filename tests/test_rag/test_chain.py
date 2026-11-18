from unittest.mock import Mock

from langchain_core.documents import Document

from app.rag.chain import create_rag_chain


def test_rag_chain():

    retriever = Mock()

    retriever.invoke.return_value = [
        Document(
            page_content="The company generated revenue of ₹10 crore.",
            metadata={
                "chunk_id": 1,
                "document_id": 5,
                "score": 0.92,
            },
        )
    ]

    llm = Mock()

    llm.invoke.return_value = Mock(
        content="The company generated revenue of ₹10 crore."
    )

    chain = create_rag_chain(
        llm=llm,
        retriever=retriever,
    )

    result = chain("What was the company's revenue?")

    assert result["answer"] == (
        "The company generated revenue of ₹10 crore."
    )

    assert result["sources"][0]["chunk_id"] == 1