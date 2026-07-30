from app.workers.tasks import fake_chunking,fake_embedding,update_progress
from app.ocr.service import OCRService
from app.core.logging import logger


def process_document(document_id):
    logger.info(f"Started processing {document_id}")

    try:
        # Load document from database
        document = ...

        # Perform real OCR
        text = OCRService.extract(document.file_path)
        document.extracted_text = text

        # Later we'll save this text to the database
        # document.extracted_text = text

        fake_chunking(document_id)
    
        fake_embedding(document_id)

    except Exception:
        update_progress(document_id, "FAILED", 0)