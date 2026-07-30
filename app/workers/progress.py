from app.redis.cache import RedisCache
from app.redis.keys import RedisKeys

cache = RedisCache()


def update_progress(document_id, status, progress):

    cache.set(
        RedisKeys.status(document_id),
        {
            "status": status,
            "progress": progress,
        },
        expire=3600,
    )