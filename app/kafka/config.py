from confluent_kafka import Consumer, Producer

from app.config.settings import settings


def get_producer() -> Producer:
    return Producer(
        {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "client.id": "pdf-api",
        }
    )


def get_consumer(topic: str) -> Consumer:
    consumer = Consumer(
        {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group.id": settings.KAFKA_GROUP,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        }
    )

    consumer.subscribe([topic])

    return consumer