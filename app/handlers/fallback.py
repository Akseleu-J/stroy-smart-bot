from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dao import UserDAO
from app.keyboards.user import kb_main
from app.locales.translations import t

router = Router(name="fallback")


@router.message()
async def unknown(message: Message, session: AsyncSession) -> None:
    lang = await UserDAO(session).get_lang(message.from_user.id)
    await message.answer(
        "Кнопкаларды пайдаланыңыз / Используйте кнопки.\n/start",
        reply_markup=kb_main(lang),
    )
