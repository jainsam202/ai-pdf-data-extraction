import time
from app.workers.progress import update_progress

def process_ocr(document_id):
    update_progress(document_id, "OCR_STARTED", 10)
    time.sleep(3)
    update_progress(document_id, "OCR_COMPLETED", 40)


def process_chunking(document_id):
    update_progress(document_id, "CHUNKING", 60)
    time.sleep(2)
    update_progress(document_id, "CHUNKING_COMPLETED", 75)


def process_embedding(document_id):
    update_progress(document_id, "EMBEDDING", 90)
    time.sleep(2)
    update_progress(document_id, "READY", 100)