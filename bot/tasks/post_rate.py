import logging
from typing import Annotated

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiohttp import ClientResponseError
from core import message_texts
from core.config import settings
from core.taskiq import broker
from redis.asyncio import Redis
from taskiq import Context, TaskiqDepends
from utils.coinex_api import CoinexAPI

logger = logging.getLogger(name=__name__)


@broker.task(schedule=[{"cron": "0 * * * *"}])
async def publish_usdt_rub_price(
    context: Annotated[Context, TaskiqDepends()],
    bot: Annotated[Bot, TaskiqDepends()],
) -> None:
    coinex_api: CoinexAPI = context.state.coinex_api
    redis: Redis = context.state.redis

    try:
        response = await coinex_api.get_rate(symbol="usdtrub")
    except ClientResponseError as ex:
        logger.error(msg="Error while fetching price", exc_info=ex)
        return

    message = await bot.send_message(
        chat_id=settings.channel_id,
        text=message_texts.PRICE.format(price=response.ask_rate),
        disable_notification=True,
    )

    old_message_id = await redis.get("old_message_id")
    if old_message_id:
        try:
            await bot.delete_message(
                chat_id=settings.channel_id,
                message_id=old_message_id,
            )
        except TelegramBadRequest as ex:
            logger.error(msg="Error while deleting old msg", exc_info=ex)

    await redis.set(name="old_message_id", value=message.message_id)
