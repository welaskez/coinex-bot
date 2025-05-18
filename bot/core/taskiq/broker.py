import taskiq_aiogram
from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker
from utils.coinex_api import CoinexAPI
from utils.redis import redis_client

from core.config import settings

broker = AioPikaBroker(url=str(settings.rmq.url))
scheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])

taskiq_aiogram.init(broker, dispatcher="main:dp", bot="main:bot")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    state.coinex_api = CoinexAPI(
        base_url=settings.coinex.base_url,
        headers={"X-Request-Id": settings.coinex.api_key},
    )
    state.redis = redis_client


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    await state.coinex_api.close()
    await state.redis.aclose()
