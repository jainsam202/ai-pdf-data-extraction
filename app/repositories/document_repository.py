from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentCreate


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, document: DocumentCreate) -> Document:

        db_document = Document(
            filename=document.filename,
            file_path=document.file_path,
            file_size=document.file_size,
        )

        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)

        return db_document

    def get_all(self):
        return self.db.query(Document).all()

    def get_by_id(self, document_id):
        return (
            self.db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )