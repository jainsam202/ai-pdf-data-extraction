from uuid import UUID
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)
    min_score: float = Field(default=0.50, ge=-1.0, le=1.0)
    document_id: UUID | None = None


class SearchResult(BaseModel):
    chunk_id: UUID
    document_id: UUID
    content: str
    score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
