import logging
from typing import Annotated

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from core import message_texts
from core.config import settings
from core.taskiq import broker
from taskiq import Context, TaskiqDepends
from utils.coinex_api import CoinexAPI

logger = logging.getLogger(name=__name__)


@broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def publish_usdt_rub_price(
    context: Annotated[Context, TaskiqDepends()],
    bot: Bot = TaskiqDepends(),
) -> None:
    coinex_api: CoinexAPI = context.state.coinex_api

    response = await coinex_api.get_usdt_rub_price()

    message = await bot.send_message(
        chat_id=settings.channel_id,
        text=message_texts.PRICE.format(price=response.ask_rate),
        disable_notification=True,
    )
    try:
        await bot.delete_message(
            chat_id=settings.channel_id,
            message_id=message.message_id - 1,
        )
    except TelegramBadRequest as ex:
        logger.error(ex, exc_info=ex)
