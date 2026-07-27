from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    return service.create_document(document)


@router.get("", response_model=list[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    return service.get_documents()


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    db: Session = Depends(get_db),
):
    service = DocumentService(db)
    return service.get_document(document_id)