from app.core.logging import logger
from app.db.session import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.workers.tasks import process_embeddings, update_progress
from app.ocr.service import OCRService
from app.chunking.service import ChunkService


def process_document(document_id):
    logger.info(
        f"Started processing document {document_id}"
    )

    db = SessionLocal()

    try:
        update_progress(
            document_id,
            "PROCESSING",
            0,
        )

        # --------------------------------------------------
        # 1. Load document
        # --------------------------------------------------

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if document is None:
            raise ValueError(
                f"Document {document_id} not found"
            )

        # --------------------------------------------------
        # 2. OCR
        # --------------------------------------------------

        update_progress(
            document_id,
            "OCR_STARTED",
            10,
        )

        text = OCRService.extract(
            document.file_path
        )

        document.extracted_text = text

        db.commit()
        db.refresh(document)

        update_progress(
            document_id,
            "OCR_COMPLETED",
            40,
        )

        # --------------------------------------------------
        # 3. Chunking
        # --------------------------------------------------

        update_progress(
            document_id,
            "CHUNKING_STARTED",
            50,
        )

        chunk_service = ChunkService(db)

        chunk_count = chunk_service.process(
            document.id,
            document.extracted_text,
        )

        update_progress(
            document_id,
            "CHUNKING_COMPLETED",
            75,
        )

        logger.info(
            f"Created {chunk_count} chunks "
            f"for document {document_id}"
        )

        # --------------------------------------------------
        # 4. Load chunks
        # --------------------------------------------------

        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id
                == document.id
            )
            .order_by(
                DocumentChunk.chunk_index
            )
            .all()
        )

        # --------------------------------------------------
        # 5. Generate and store embeddings
        # --------------------------------------------------

        embedding_count = process_embeddings(
            db,
            chunks,
        )

        logger.info(
            f"Created {embedding_count} embeddings "
            f"for document {document_id}"
        )

        # --------------------------------------------------
        # 6. Mark document ready
        # --------------------------------------------------

        update_progress(
            document_id,
            "READY",
            100,
        )

        logger.info(
            f"Finished processing document "
            f"{document_id}"
        )

    except Exception as exc:

        logger.exception(
            f"Document processing failed "
            f"for {document_id}: {exc}"
        )

        db.rollback()

        update_progress(
            document_id,
            "FAILED",
            0,
        )

        raise

    finally:
        db.close()