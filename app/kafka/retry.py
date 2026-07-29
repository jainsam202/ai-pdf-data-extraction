MAX_RETRIES = 3

import time

from app.core.logging import logger


def retry(operation):

    for attempt in range(1, 4):

        try:

            return operation()

        except Exception as ex:

            logger.warning(
                f"Retry {attempt} failed: {ex}"
            )

            time.sleep(2)

    raise Exception("Maximum retries exceeded")