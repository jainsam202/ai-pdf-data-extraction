import json
from app.kafka.retry import retry
from app.kafka.dlq import publish_dlq
from confluent_kafka import KafkaException
from app.core.logging import logger
from app.kafka.config import get_consumer
from app.kafka.topics import KafkaTopics
from app.workers.document_worker import process_document


consumer = get_consumer(
    KafkaTopics.DOCUMENT_UPLOAD
)

def start_document_consumer():
    logger.info("Document Consumer Started")
    try:
        while True:
            try:
                message = consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    logger.error(message.error())
                    continue

                payload = json.loads(message.value().decode("utf-8"))
                logger.info(f"Received Event: {payload}")
                logger.info(f"Processing document {payload['document_id']}")

                try:
                    retry(
                        lambda: process_document(payload["document_id"])
                    )

                    logger.info(f"Completed document {payload['document_id']}")
                    consumer.commit(message)

                except Exception:
                    logger.exception(f"Failed processing document {payload['document_id']}")

                    publish_dlq(payload)
                    consumer.commit(message)

            except KafkaException as ex:
                logger.exception(ex)

            except Exception as ex:
                logger.exception(ex)

    except KeyboardInterrupt:
        logger.info("Stopping Document Consumer")
    finally:
        consumer.close()
        logger.info("Document Consumer Closed")