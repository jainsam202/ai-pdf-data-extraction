
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class EventMetadata(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    version: str = "1.0"
    source: str = "fastapi"
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
