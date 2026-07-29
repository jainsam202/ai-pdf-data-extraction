from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.kafka.metadata import EventMetadata

class DocumentUploadedEvent(BaseModel):
    metadata: EventMetadata
    document_id: UUID
    filename: str
    file_path: str
    event_type: str = "DOCUMENT_UPLOADED"
    timestamp: datetime = datetime.utcnow()