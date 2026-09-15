
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.embeddings.repository import EmbeddingRepository
from app.embeddings.service import EmbeddingService
from app.redis.cache import RedisCache
from app.redis.keys import RedisKeys
import time

cache = RedisCache()

def update_progress(document_id, status, progress):
    cache.set(
        RedisKeys.status(document_id),
        {
            "status": status,
            "progress": progress,
        },
        expire=3600,
    )


def process_embeddings(db: Session,chunks):
    """
    Generate embeddings for document chunks
    and persist them into PostgreSQL using pgvector.
    """

    if not chunks:
        return 0

    update_progress(
        chunks[0].document_id,
        "EMBEDDING_STARTED",
        80,
    )

    embedding_service = EmbeddingService()
    repository = EmbeddingRepository(db)

    texts = [
        chunk.content
        for chunk in chunks
    ]

    vectors = embedding_service.generate_embeddings(texts)
    rows = []

    for chunk, vector in zip(chunks, vectors):
        rows.append(
            {
                "chunk_id": chunk.id,
                "model_name": settings.EMBEDDING_MODEL,
                "embedding": vector,
            }
        )

    repository.bulk_upsert(rows)

    update_progress(
        chunks[0].document_id,
        "EMBEDDING_COMPLETED",
        95,
    )

    return len(rows)


def process_ocr(document_id):
    update_progress(document_id, "OCR_STARTED", 10)
    time.sleep(3)
    update_progress(document_id, "OCR_COMPLETED", 40)


def process_chunking(document_id):
    update_progress(document_id, "CHUNKING", 60)
    time.sleep(2)
    update_progress(document_id, "CHUNKING_COMPLETED", 75)