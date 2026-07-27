from fastapi import APIRouter

from app.redis.client import redis_client

router = APIRouter(
    prefix="/redis",
    tags=["Redis"],
)


@router.get("/ping")
def ping():

    redis_client.set("hello", "world")

    value = redis_client.get("hello")

    return {
        "value": value
    }