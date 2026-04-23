import redis.asyncio as aioredis
from config import settings

redis_client = aioredis.Redis(
    host=settings.REDIS_HOST,
    port = settings.REDIS_PORT,
    db = settings.REDIS_DB,
    decode_responses = True
)

async def get_redis():
    return redis_client