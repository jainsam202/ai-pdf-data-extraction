from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from app.redis.cache import RedisCache
from app.redis.keys import RedisKeys

from app.db.dependencies import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])

DBSession =Annotated[Session, Depends(get_db)]
cache = RedisCache()

@router.post("", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: DBSession,
):
    service = DocumentService(db)
    return service.create_document(document)


@router.get("", response_model=list[DocumentResponse])
def get_documents(
    db: DBSession,
):
    service = DocumentService(db)
    return service.get_documents()


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    db: DBSession,
):
    service = DocumentService(db)
    return service.get_document(document_id)


@router.post("/{document_id}/process")
def process_document(
    document_id: UUID,
    db: DBSession
):

    service = DocumentService(db)

    document = service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return service.start_processing(document)
 
    
@router.get("/{document_id}/status")
def status(document_id: str):

    return cache.get(
        RedisKeys.status(document_id)
    )