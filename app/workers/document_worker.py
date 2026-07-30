from app.workers.tasks import process_chunking,process_embedding,process_ocr
from app.db.session import SessionLocal
from app.repositories.document_repository import DocumentRepository

db = SessionLocal()

def process_document(document_id):

    db = SessionLocal()
    try:
        document = DocumentRepository.get_by_id(db,document_id)
        process_ocr(db,document)

        process_chunking(db,document)

        process_embedding(db,document)

    finally:
        db.close()