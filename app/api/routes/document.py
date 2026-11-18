from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,UploadFile, File
from uuid import UUID
from sqlalchemy.orm import Session
from app.redis.cache import RedisCache
from app.redis.keys import RedisKeys
from pathlib import Path
from uuid import uuid4
from app.db.dependencies import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])

DBSession =Annotated[Session, Depends(get_db)]
cache = RedisCache()



@router.post("/upload", response_model=DocumentResponse, status_code=201, responses={400: {"description": "Invalid file or unsupported file type"}})
def upload_document(db: DBSession,file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    upload_dir = Path("uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid4()}.pdf"
    file_path = upload_dir / stored_name

    try:
        header = file.file.read(5)
        file.file.seek(0)

        if header != b"%PDF-":
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid PDF.",
            )

        size = 0

        with file_path.open("wb") as destination:
            while True:
                chunk = file.file.read(1024 * 1024)
                if not chunk:
                    break

                destination.write(chunk)
                size += len(chunk)

        document = DocumentCreate(
            filename=Path(file.filename).name,
            file_path=str(file_path),
            file_size=size,
        )

        return DocumentService(db).create_document(document)

    except HTTPException:
        file_path.unlink(missing_ok=True)
        raise

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

    finally:
        file.file.close()



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