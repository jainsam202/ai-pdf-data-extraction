from uuid import UUID
from pydantic import BaseModel, Field


class RAGQuery(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    document_id: UUID | None = None


class RAGSource(BaseModel):
    chunk_id: UUID | None = None
    document_id: UUID | None = None
    score: float | None = None


class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSource]
