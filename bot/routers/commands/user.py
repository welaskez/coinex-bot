from aiogram import Router, types
from aiogram.filters import CommandStart
from core import message_texts
from core.config import settings
from core.schemas.user import UserCreate
from services.user import UserService

router = Router(name=__name__)


@router.message(CommandStart())
async def start_cmd(message: types.Message, user_service: UserService):
    user = await user_service.get_by_tg_id(tg_id=message.from_user.id)
    if not user:
        await user_service.create(UserCreate(tg_id=message.from_user.id))

    await message.answer(text=message_texts.START.format(channel=settings.channel_id))
