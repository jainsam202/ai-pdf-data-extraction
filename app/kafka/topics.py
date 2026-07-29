from app.config.settings import settings


class KafkaTopics:

    DOCUMENT_UPLOAD = settings.KAFKA_UPLOAD_TOPIC

    OCR_COMPLETED = "ocr.completed"

    CHUNK_COMPLETED = "chunk.completed"

    EMBEDDING_COMPLETED = "embedding.completed"

    DOCUMENT_DLQ = "document.dlq"