from typing import TypedDict
from uuid import UUID
from langchain_core.documents import Document


class GraphState(TypedDict, total=False):
    question: str
    rewritten_question: str
    document_id: UUID | None
    documents: list[Document]
    context: str
    answer: str
    sources: list[dict]
    retrieval_attempts: int
    relevant: bool