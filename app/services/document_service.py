from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate


class DocumentService:

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def create_document(self, document: DocumentCreate):
        return self.repository.create(document)

    def get_documents(self):
        return self.repository.get_all()

    def get_document(self, document_id):
        return self.repository.get_by_id(document_id)