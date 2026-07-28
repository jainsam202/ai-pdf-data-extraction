from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class DocumentUploadedEvent(BaseModel):
    document_id: UUID

    filename: str

    file_path: str

    event_type: str = "DOCUMENT_UPLOADED"

    timestamp: datetime = datetime.utcnow()