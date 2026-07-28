from app.kafka.events import DocumentUploadedEvent
from app.kafka.producer import publish
from app.kafka.topics import KafkaTopics


class DocumentProducer:

    @staticmethod
    def publish_upload(
        event: DocumentUploadedEvent,
    ):

        publish(
            topic=KafkaTopics.DOCUMENT_UPLOAD,
            key=str(event.document_id),
            value=event.model_dump(mode="json"),
        )