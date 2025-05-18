import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from redis.asyncio import Redis


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
        self,
        redis: Redis,
        window_size: int = 7,
        window_seconds: int = 10,
        mute_seconds: int = 30,
        key_ttl: int = 120,
    ):
        self.redis = redis
        self.window_size = window_size
        self.window_seconds = window_seconds
        self.mute_seconds = mute_seconds
        self.key_ttl = key_ttl

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user = f"user:{event.from_user.id}"

        if await self.redis.exists(f"{user}:muted"):
            return await event.answer("Stop spam.")

        current_time = time.time()

        await self.redis.lpush(user, current_time)
        await self.redis.ltrim(user, 0, self.window_size - 1)
        await self.redis.expire(user, self.key_ttl)

        timestamps = await self.redis.lrange(user, 0, -1)

        if len(timestamps) >= self.window_size:
            oldest_time = float(timestamps[-1])
            if current_time - oldest_time <= self.window_seconds:
                await self.redis.set(name=f"{user}:muted", value=1, ex=self.mute_seconds)
                return await event.answer(f"Stop spam, mute for {self.mute_seconds} seconds.")

        return await handler(event, data)
