import asyncio
from functools import wraps
from typing import Any, Callable, Type

from aiohttp import ClientError, ClientSession


def retry(
    exceptions: tuple[Type[BaseException]] = (ClientError, asyncio.TimeoutError),
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            _retries = retries
            _delay = delay

            while _retries > 0:
                try:
                    return await func(*args, **kwargs)
                except exceptions:
                    _retries -= 1
                    if _retries == 0:
                        raise
                    await asyncio.sleep(_delay)
                    _delay *= backoff

        return wrapper

    return decorator


class HttpClient:
    def __init__(self, base_url: str, headers: dict[str, str] | None = None) -> None:
        self._base_url = base_url
        self._headers = {"Content-Type": "application/json"}
        if headers:
            self._headers.update(headers)
        self._session = ClientSession(base_url=self._base_url, headers=self._headers)

    async def get(self, url: str) -> dict:
        async with self._session.get(url=url) as response:
            response.raise_for_status()
            return await response.json()

    async def post(self, url: str, body: dict[str, Any] | None = None) -> dict:
        async with self._session.post(url=url, data=body) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self) -> None:
        await self._session.close()
