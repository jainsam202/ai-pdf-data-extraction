from sqlalchemy.orm import Session
from app.kafka.metadata import EventMetadata
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate
from app.redis.cache import RedisCache
from app.redis.keys import RedisKeys
from app.kafka.document_producer import DocumentProducer
from app.kafka.events import DocumentUploadedEvent

cache = RedisCache()


class DocumentService:

    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)

    def create_document(self, document: DocumentCreate):
        return self.repository.create(document)

    def get_documents(self):
        return self.repository.get_all()
  
    def get_document(self, document_id):
        key = RedisKeys.document(document_id)
        cached = cache.get(key)
        if cached:
            return cached

        document = self.repository.get_by_id(document_id)

        if document:
            document_data = {
                "id": str(document.id),
                "filename": document.filename,
                "file_path": document.file_path,
                "file_size": document.file_size,
                "status": document.status,
            }
            cache.set(key,document_data,expire=600)
            return document_data

        return document

    def start_processing(self, document):
        if isinstance(document, dict):
            document = self.repository.get_by_id(document["id"])
        if document is None:
            raise ValueError("Document not found")

        event = DocumentUploadedEvent(
            metadata=EventMetadata(),
            document_id=document.id,
            filename=document.filename,
            file_path=document.file_path,
        )

        DocumentProducer.publish_upload(event)

        return {
            "message": "Document queued successfully",
            "document_id": str(document.id),
        }