
from app.redis.cache import RedisCache
from app.redis.keys import RedisKeys

document_id = "5465fcac-18a5-4c43-bf43-52d5b0422beb"

cache = RedisCache()
key = RedisKeys.document(document_id)

cache.delete(key)

print(f"Deleted Redis cache entry: {key}")
