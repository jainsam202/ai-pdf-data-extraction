from sqlalchemy.orm import Session

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
            cache.set(
                key,
                {
                    "id": str(document.id),
                    "filename": document.filename,
                    "status": document.status,
                },
                expire=600,
            )

        return document

    def start_processing(self, document):

        event = DocumentUploadedEvent(
            document_id=document.id,
            filename=document.filename,
            file_path=document.file_path,
        )

        DocumentProducer.publish_upload(event)

        return {
            "message": "Document queued successfully"
        }