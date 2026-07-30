import time

from app.redis.cache import RedisCache
from app.redis.keys import RedisKeys

cache = RedisCache()


def update_progress(document_id):

    cache.set(
        RedisKeys.status(document_id),
        {
            "status": "OCR_COMPLETED",
            "progress": 40,
        },
        expire=3600,
    )


def fake_ocr(document_id):

    update_progress(document_id, "OCR_STARTED", 10)

    time.sleep(3)

    update_progress(document_id, "OCR_COMPLETED", 40)


def fake_chunking(document_id):

    update_progress(document_id, "CHUNKING", 60)

    time.sleep(2)

    update_progress(document_id, "CHUNKING_COMPLETED", 75)


def fake_embedding(document_id):

    update_progress(document_id, "EMBEDDING", 90)

    time.sleep(2)

    update_progress(document_id, "READY", 100)