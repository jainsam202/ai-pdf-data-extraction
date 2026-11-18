from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, Field
from app.kafka.metadata import EventMetadata

class DocumentUploadedEvent(BaseModel):
    metadata: EventMetadata = Field(default_factory=EventMetadata)
    document_id: UUID
    filename: str
    file_path: str
    event_type: str = "DOCUMENT_UPLOADED"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))