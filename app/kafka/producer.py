import json
from typing import Any

from confluent_kafka import Producer

from app.core.logging import logger
from app.kafka.config import get_producer

producer: Producer = get_producer()


def delivery_report(err, msg):
    """
    Callback invoked by Kafka after the broker
    acknowledges the message.
    """

    if err:
        logger.error(f"Delivery failed: {err}")
    else:
        logger.info(
            "Delivered to "
            f"{msg.topic()} "
            f"Partition={msg.partition()} "
            f"Offset={msg.offset()}"
        )


def publish(
    topic: str,
    value: dict[str, Any],
    key: str | None = None,
):
    """
    Generic publish function.
    """

    producer.produce(
        topic=topic,
        key=key,
        value=json.dumps(value),
        callback=delivery_report,
    )

    producer.flush()