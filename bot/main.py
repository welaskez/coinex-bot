import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatType, ParseMode
from core.config import settings
from core.models import session_pool
from core.taskiq import broker
from filters import ChatTypeFilter
from middlewares import DatabaseMiddleware, UserServiceMiddleware
from routers import router
from utils.log import setup_logging

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(
        link_preview_is_disabled=True,
        parse_mode=ParseMode.HTML,
    ),
)
dp = Dispatcher()


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    if not broker.is_worker_process:
        await broker.startup()


async def on_shutdown(bot: Bot, dispatcher: Dispatcher) -> None:
    if not broker.is_worker_process:
        await broker.shutdown()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.startup.register(on_shutdown)
    dp.update.middleware(DatabaseMiddleware(session_pool=session_pool))
    dp.update.middleware(UserServiceMiddleware())
    dp.message.filter(ChatTypeFilter(chat_types=[ChatType.PRIVATE]))
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logging(level=settings.log.level)
    asyncio.run(main())
