from app.kafka.producer import publish
from app.kafka.topics import KafkaTopics


def publish_dlq(event):

    publish(
        topic=KafkaTopics.DOCUMENT_DLQ,
        value=event,
    )