from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.embeddings.schemas import (
    SearchRequest,
    SearchResponse,
)
from app.embeddings.search import (
    SemanticSearchService,
)

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post(
    "/semantic",
    response_model=SearchResponse,
)
def semantic_search(
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    service = SemanticSearchService(db)

    return service.search(request)