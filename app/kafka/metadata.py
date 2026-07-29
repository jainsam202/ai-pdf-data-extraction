from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel


class EventMetadata(BaseModel):

    event_id: str = str(uuid4())

    correlation_id: str = str(uuid4())

    version: str = "1.0"

    source: str = "fastapi"

    created_at: datetime = datetime.utcnow()