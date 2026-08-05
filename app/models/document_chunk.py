import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, Text, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id")
    )

    page_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    chunk_index: Mapped[int]

    content: Mapped[str] = mapped_column(Text)

    content_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    
    embedding = relationship(
        "DocumentEmbedding",
        back_populates="chunk",
        uselist=False,
        cascade="all, delete",
    )