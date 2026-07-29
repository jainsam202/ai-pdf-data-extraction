from app.redis.client import redis_client


def already_processed(event_id):

    key = f"event:{event_id}"

    if redis_client.exists(key):
        return True

    redis_client.set(
        key,
        "processed",
        ex=86400,
    )

    return False