import json

from app.redis.client import redis_client


class RedisCache:

    def set(self, key, value, expire=3600):

        redis_client.set(
            key,
            json.dumps(value),
            ex=expire,
        )

    def get(self, key):

        value = redis_client.get(key)

        if value is None:
            return None

        return json.loads(value)

    def delete(self, key):

        redis_client.delete(key)