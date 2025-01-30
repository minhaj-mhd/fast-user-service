import redis
from core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def publish_event(event_name: str, data: dict):
    redis_client.publish(event_name, str(data))