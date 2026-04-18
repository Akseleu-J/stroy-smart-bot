from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.database.dao import UserDAO
from app.keyboards.user import kb_lang, kb_main
from app.locales.translations import t

logger = get_logger(__name__)
router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    user = await UserDAO(session).get_or_create(
        telegram_id=message.from_user.id,
        name=message.from_user.first_name or "Қонақ",
    )
    lang = user.lang
    logger.info("start", user_id=user.telegram_id, lang=lang)
    await message.answer(
        t(lang, "welcome", name=user.name),
        reply_markup=kb_main(lang),
    )


@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    user = await UserDAO(session).get_or_create(
        telegram_id=callback.from_user.id,
        name=callback.from_user.first_name or "Қонақ",
    )
    lang = user.lang
    await callback.message.edit_text(t(lang, "main_menu"), reply_markup=kb_main(lang))
    await callback.answer()


@router.callback_query(F.data == "select_lang")
async def select_lang(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        t("kz", "select_lang"),
        reply_markup=kb_lang(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def set_lang(callback: CallbackQuery, session: AsyncSession) -> None:
    lang = callback.data.split(":")[1]
    dao  = UserDAO(session)
    await dao.set_lang(callback.from_user.id, lang)
    user = await dao.get_or_create(
        callback.from_user.id,
        callback.from_user.first_name or "Қонақ",
    )
    logger.info("lang_changed", user_id=callback.from_user.id, lang=lang)
    await callback.message.edit_text(
        t(lang, "lang_chosen") + "\n\n" + t(lang, "main_menu"),
        reply_markup=kb_main(lang),
    )
    await callback.answer(t(lang, "lang_chosen"))
