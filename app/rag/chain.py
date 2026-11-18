from typing import List
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from app.rag.prompts import RAG_PROMPT


def create_rag_chain(llm, retriever):

    def rag_chain(question: str):

        documents = retriever.invoke(question)
        context = format_documents(documents)
        messages = RAG_PROMPT.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        response = llm.invoke(messages)
        sources = [
            {
                "chunk_id": document.metadata.get("chunk_id"),
                "document_id": document.metadata.get("document_id"),
                "score": document.metadata.get("score"),
            }
            for document in documents
        ]

        return {
            "answer": response.content,
            "sources": sources,
        }

    return rag_chain


def format_documents(documents: list[Document]) -> str:

    if not documents:
        return ""

    return "\n\n".join(
        f"Document Chunk {index}\n{document.page_content}"
        for index, document in enumerate(documents, start=1)
    )
