from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logger import get_logger
from app.database.dao import AppSettingsDAO, PortfolioDAO, PriceDAO
from app.keyboards.admin import (
    kb_admin_back, kb_admin_main, kb_admin_photos,
    kb_admin_prices, kb_admin_texts,
)
from app.services.admin_service import AdminService
from app.services.analytics_service import AnalyticsService
from app.utils.validators import ContactInput, PriceInput

logger = get_logger(__name__)
router = Router(name="admin")


class AdminStates(StatesGroup):
    main          = State()
    edit_price    = State()
    edit_contact  = State()
    waiting_photo = State()
    waiting_text  = State()


def _is_admin(uid: int) -> bool:
    return uid in settings.ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer("⛔ Қол жетімді емес")
        return
    await state.set_state(AdminStates.main)
    logger.info("admin_enter", uid=message.from_user.id)
    await message.answer("🔐 <b>Админ панелі</b>", reply_markup=kb_admin_main())


@router.callback_query(F.data == "adm:back")
async def adm_back(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        return
    await state.set_state(AdminStates.main)
    await callback.message.edit_text("🔐 <b>Админ панелі</b>", reply_markup=kb_admin_main())
    await callback.answer()


@router.callback_query(F.data == "adm:exit")
async def adm_exit(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        return
    await state.clear()
    await callback.message.edit_text("✅ Шықтыңыз. /start")
    await callback.answer()


@router.callback_query(F.data == "adm:stats")
async def adm_stats(callback: CallbackQuery, session: AsyncSession) -> None:
    if not _is_admin(callback.from_user.id):
        return
    svc   = AnalyticsService(session)
    stats = await svc.get_stats()
    w     = await svc.get_weekly_stats()
    text  = (
        svc.format_stats(stats) + "\n\n"
        "<b>Осы аптада / За эту неделю:</b>\n"
        f"📈 Смета: <b>{w['calcs_week']}</b>\n"
        f"📞 Лид: <b>{w['leads_week']}</b>\n"
        f"📅 Жазылу: <b>{w['bookings_week']}</b>"
    )
    await callback.message.edit_text(text, reply_markup=kb_admin_back())
    await callback.answer()


@router.callback_query(F.data == "adm:prices")
async def adm_prices(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(callback.from_user.id):
        return
    await state.set_state(AdminStates.main)
    prices = await AdminService(session).get_all_prices()
    await callback.message.edit_text(
        "<b>💰 Бағаларды өзгерту</b>",
        reply_markup=kb_admin_prices(prices),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:setprice:"))
async def adm_setprice_ask(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(callback.from_user.id):
        return
    key    = callback.data.split(":")[2]
    prices = await AdminService(session).get_all_prices()
    cur    = prices.get(key, 0)
    await state.update_data(editing_price_key=key)
    await state.set_state(AdminStates.edit_price)
    await callback.message.edit_text(
        f"Ағымдағы: <b>{cur:,} ₸/м³</b>\n\nЖаңа бағаны енгізіңіз:",
        reply_markup=kb_admin_back(),
    )
    await callback.answer()


@router.message(AdminStates.edit_price)
async def adm_setprice_val(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(message.from_user.id):
        return
    try:
        inp = PriceInput(raw=message.text or "")
    except ValidationError:
        await message.answer("❌ Дұрыс сан енгізіңіз")
        return
    d        = await state.get_data()
    key      = d.get("editing_price_key", "")
    svc      = AdminService(session)
    old, new = await svc.set_price(key, inp.value)
    prices   = await svc.get_all_prices()
    await state.set_state(AdminStates.main)
    logger.info("price_updated", key=key, old=old, new=new)
    await message.answer(
        f"✅ {old:,} ₸ → <b>{new:,} ₸/м³</b>",
        reply_markup=kb_admin_prices(prices),
    )


@router.callback_query(F.data == "adm:contact")
async def adm_contact_ask(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(callback.from_user.id):
        return
    cur = await AdminService(session).get_contact()
    await state.set_state(AdminStates.edit_contact)
    await callback.message.edit_text(
        f"Ағымдағы: <b>{cur}</b>\n\nЖаңа username:",
        reply_markup=kb_admin_back(),
    )
    await callback.answer()


@router.message(AdminStates.edit_contact)
async def adm_contact_val(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(message.from_user.id):
        return
    try:
        inp = ContactInput(raw=message.text or "")
    except ValidationError:
        await message.answer("❌ Дұрыс username енгізіңіз")
        return
    svc      = AdminService(session)
    old, new = await svc.set_contact(inp.value)
    await state.set_state(AdminStates.main)
    logger.info("contact_updated", old=old, new=new)
    await message.answer(f"✅ {old} → <b>{new}</b>", reply_markup=kb_admin_main())


@router.callback_query(F.data == "adm:photos")
async def adm_photos(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(callback.from_user.id):
        return
    await state.set_state(AdminStates.main)
    status = await AdminService(session).get_portfolio_status()
    await callback.message.edit_text(
        "<b>📸 Портфолио — фото</b>\n✅ бар · ❌ жоқ",
        reply_markup=kb_admin_photos(status),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:photo:"))
async def adm_photo_ask(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(callback.from_user.id):
        return
    key    = callback.data.split(":")[2]
    status = await AdminService(session).get_portfolio_status()
    icon   = "✅ Бар" if status.get(key) else "❌ Жоқ"
    await state.update_data(editing_photo_key=key)
    await state.set_state(AdminStates.waiting_photo)
    await callback.message.edit_text(
        f"Ағымдағы фото: {icon}\n\nЖаңа фотосурет жіберіңіз:",
        reply_markup=kb_admin_back(),
    )
    await callback.answer()


@router.message(AdminStates.waiting_photo, F.photo)
async def adm_photo_receive(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(message.from_user.id):
        return
    d      = await state.get_data()
    key    = d.get("editing_photo_key", "")
    fid    = message.photo[-1].file_id
    svc    = AdminService(session)
    await svc.set_photo(key, fid)
    status = await svc.get_portfolio_status()
    await state.set_state(AdminStates.main)
    logger.info("photo_updated", key=key)
    await message.answer("✅ Фото жаңартылды!", reply_markup=kb_admin_photos(status))


@router.message(AdminStates.waiting_photo)
async def adm_photo_wrong(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return
    await message.answer("❌ Фотосурет жіберіңіз")


@router.callback_query(F.data == "adm:texts")
async def adm_texts(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        return
    await state.set_state(AdminStates.main)
    await callback.message.edit_text(
        "<b>📝 Портфолио — мәтін</b>",
        reply_markup=kb_admin_texts(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:text:"))
async def adm_text_ask(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(callback.from_user.id):
        return
    key     = callback.data.split(":")[2]
    cur_txt = await PortfolioDAO(session).get_text(key)
    await state.update_data(editing_text_key=key)
    await state.set_state(AdminStates.waiting_text)
    await callback.message.edit_text(
        f"Ағымдағы мәтін:\n<i>{cur_txt[:150]}...</i>\n\nЖаңа мәтінді енгізіңіз:",
        reply_markup=kb_admin_back(),
    )
    await callback.answer()


@router.message(AdminStates.waiting_text)
async def adm_text_receive(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if not _is_admin(message.from_user.id):
        return
    d   = await state.get_data()
    key = d.get("editing_text_key", "")
    await AdminService(session).set_portfolio_text(key, message.text or "")
    await state.set_state(AdminStates.main)
    logger.info("text_updated", key=key)
    await message.answer("✅ Мәтін жаңартылды!", reply_markup=kb_admin_main())
