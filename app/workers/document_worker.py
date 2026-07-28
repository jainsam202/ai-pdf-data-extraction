from app.workers.tasks import (
    fake_chunking,
    fake_embedding,
    fake_ocr,
    update_progress,
)
from app.core.logging import logger


def process_document(document_id):
    logger.info(f"Started processing {document_id}")
    
    try:
        fake_ocr(document_id)

        fake_chunking(document_id)

        fake_embedding(document_id)
    except Exception:
        update_progress(document_id, "FAILED", 0)