from core.config import settings
from redis.asyncio import ConnectionPool, Redis

connection_pool = ConnectionPool.from_url(url=f"redis://{settings.redis.host}:{settings.redis.port}/")
redis_client = Redis(
    connection_pool=connection_pool,
    decode_responses=settings.redis.decode_responses,
)
