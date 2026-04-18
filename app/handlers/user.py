from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SERVICE_DESCRIPTIONS, SERVICE_NAMES
from app.core.logger import get_logger
from app.database.dao import (
    AppSettingsDAO, CalculationDAO, PortfolioDAO, PriceDAO, UserDAO,
)
from app.keyboards.user import (
    kb_after_calc, kb_booking_confirm, kb_booking_dates,
    kb_booking_times, kb_calc_type, kb_contact,
    kb_main, kb_portfolio, kb_portfolio_detail,
    kb_service_detail, kb_services,
)
from app.locales.translations import t
from app.services.booking_service import BookingService
from app.services.estimation import EstimationService
from app.services.lead_service import LeadService
from app.utils.validators import VolumeInput

logger = get_logger(__name__)
router = Router(name="user")


class CalcStates(StatesGroup):
    waiting_service = State()
    waiting_volume  = State()


class BookingStates(StatesGroup):
    waiting_date = State()
    waiting_time = State()
    confirming   = State()


async def _lang(uid: int, session: AsyncSession) -> str:
    return await UserDAO(session).get_lang(uid)


# ── Услуги ───────────────────────────────────────────────────────

@router.callback_query(F.data == "services")
async def show_services(callback: CallbackQuery, session: AsyncSession) -> None:
    lang = await _lang(callback.from_user.id, session)
    await callback.message.edit_text(
        t(lang, "services_title"),
        reply_markup=kb_services(lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("svc:"))
async def show_service_detail(callback: CallbackQuery, session: AsyncSession) -> None:
    key   = callback.data.split(":")[1]
    lang  = await _lang(callback.from_user.id, session)
    price = await PriceDAO(session).get(key)
    desc  = SERVICE_DESCRIPTIONS.get(key, {}).get(lang if lang in ("kz", "ru") else "kz", "")
    name  = SERVICE_NAMES.get(key, key)
    text  = (
        f"<b>{name}</b>\n\n"
        f"{desc}\n\n"
        f"<b>Баға / Цена:</b> {price:,} ₸/м³\n"
        "<b>Кепілдік / Гарантия:</b> 5 жыл"
    )
    await callback.message.edit_text(text, reply_markup=kb_service_detail(lang))
    await callback.answer()


# ── Портфолио ────────────────────────────────────────────────────

@router.callback_query(F.data == "portfolio")
async def show_portfolio(callback: CallbackQuery, session: AsyncSession) -> None:
    lang = await _lang(callback.from_user.id, session)
    await callback.message.edit_text(
        t(lang, "portfolio_title"),
        reply_markup=kb_portfolio(lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("port:"))
async def show_portfolio_detail(callback: CallbackQuery, session: AsyncSession) -> None:
    key      = callback.data.split(":")[1]
    lang     = await _lang(callback.from_user.id, session)
    dao      = PortfolioDAO(session)
    text     = await dao.get_text(key)
    photo_id = await dao.get_photo(key)

    if photo_id:
        await callback.message.answer_photo(
            photo=photo_id,
            caption=text,
            reply_markup=kb_portfolio_detail(lang),
        )
        try:
            await callback.message.delete()
        except Exception:
            pass
    else:
        await callback.message.edit_text(
            text + t(lang, "photo_soon"),
            reply_markup=kb_portfolio_detail(lang),
        )
    await callback.answer()


# ── Смета (AI калькулятор) ────────────────────────────────────────

@router.callback_query(F.data == "calc")
async def calc_start(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    lang = await _lang(callback.from_user.id, session)
    await state.set_state(CalcStates.waiting_service)
    await callback.message.edit_text(
        t(lang, "calc_start"),
        reply_markup=kb_calc_type(lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ctype:"), CalcStates.waiting_service)
async def calc_choose_type(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    key  = callback.data.split(":")[1]
    lang = await _lang(callback.from_user.id, session)
    name = SERVICE_NAMES.get(key, key)
    await state.update_data(service_type=key, service_name=name)
    await state.set_state(CalcStates.waiting_volume)
    await callback.message.edit_text(
        t(lang, "calc_enter_vol", name=name),
        reply_markup=None,
    )
    await callback.answer()


@router.message(CalcStates.waiting_volume)
async def calc_result(message: Message, state: FSMContext, session: AsyncSession) -> None:
    lang = await _lang(message.from_user.id, session)
    try:
        inp = VolumeInput(raw=message.text or "")
    except ValidationError:
        await message.answer(t(lang, "calc_error"))
        return

    data         = await state.get_data()
    service_type = data.get("service_type", "foundation")
    await state.clear()

    result = await EstimationService(session).estimate(service_type, inp.value)
    user   = await UserDAO(session).get_or_create(
        telegram_id=message.from_user.id,
        name=message.from_user.first_name or "Қонақ",
    )
    await CalculationDAO(session).create(
        user_id=user.id,
        service_type=service_type,
        volume=inp.value,
        result_low=result.result_low,
        result_high=result.result_high,
    )
    logger.info(
        "calc_done",
        user_id=user.telegram_id,
        service=service_type,
        volume=inp.value,
        low=result.result_low,
        high=result.result_high,
    )
    await message.answer(result.format_text(), reply_markup=kb_after_calc(lang))


# ── История расчётов ──────────────────────────────────────────────

@router.callback_query(F.data == "history")
async def show_history(callback: CallbackQuery, session: AsyncSession) -> None:
    lang = await _lang(callback.from_user.id, session)
    user = await UserDAO(session).get_or_create(
        telegram_id=callback.from_user.id,
        name=callback.from_user.first_name or "Қонақ",
    )
    calcs = await CalculationDAO(session).get_user_history(user.id)

    if not calcs:
        await callback.message.edit_text(
            t(lang, "history_empty"),
            reply_markup=__import__(
                "app.keyboards.user", fromlist=["kb_main"]
            ).kb_main(lang),
        )
        await callback.answer()
        return

    text = t(lang, "history_title")
    for c in calcs:
        date_str = c.created_at.strftime("%d.%m.%Y")
        svc_name = SERVICE_NAMES.get(c.service_type, c.service_type)
        text += t(
            lang, "history_item",
            service=svc_name,
            volume=c.volume,
            low=c.result_low,
            high=c.result_high,
            date=date_str,
        )

    from app.keyboards.user import kb_main as _kb_main
    await callback.message.edit_text(text, reply_markup=_kb_main(lang))
    await callback.answer()


# ── Бронирование консультации ─────────────────────────────────────

@router.callback_query(F.data == "booking")
async def booking_start(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    lang = await _lang(callback.from_user.id, session)
    await state.set_state(BookingStates.waiting_date)
    await callback.message.answer(
        t(lang, "booking_start"),
        reply_markup=kb_booking_dates(lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("bdate:"), BookingStates.waiting_date)
async def booking_choose_date(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    selected_date = callback.data.split(":")[1]
    lang          = await _lang(callback.from_user.id, session)
    await state.update_data(booking_date=selected_date)
    await state.set_state(BookingStates.waiting_time)
    await callback.message.edit_text(
        t(lang, "booking_time"),
        reply_markup=kb_booking_times(selected_date, lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("btime:"), BookingStates.waiting_time)
async def booking_choose_time(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    parts = callback.data.split(":")
    selected_date = parts[1]
    selected_time = parts[2]
    lang          = await _lang(callback.from_user.id, session)

    await state.update_data(booking_date=selected_date, booking_time=selected_time)
    await state.set_state(BookingStates.confirming)
    await callback.message.edit_text(
        t(lang, "booking_confirm", date=selected_date, time=selected_time),
        reply_markup=kb_booking_confirm(lang),
    )
    await callback.answer()


@router.callback_query(F.data == "book:confirm", BookingStates.confirming)
async def booking_confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data()
    date = data.get("booking_date", "")
    time = data.get("booking_time", "")
    lang = await _lang(callback.from_user.id, session)

    user = await UserDAO(session).get_or_create(
        telegram_id=callback.from_user.id,
        name=callback.from_user.first_name or "Қонақ",
    )
    await BookingService(session).create_booking(
        user=user,
        date=date,
        time=time,
        username=callback.from_user.username,
    )
    await state.clear()

    from app.keyboards.user import kb_main as _kb_main
    await callback.message.edit_text(
        t(lang, "booking_done", date=date, time=time),
        reply_markup=_kb_main(lang),
    )
    await callback.answer("✅")


# ── Контакт / Консультация ────────────────────────────────────────

@router.callback_query(F.data == "contact")
async def show_contact(callback: CallbackQuery, session: AsyncSession) -> None:
    lang = await _lang(callback.from_user.id, session)
    user = await UserDAO(session).get_or_create(
        telegram_id=callback.from_user.id,
        name=callback.from_user.first_name or "Қонақ",
    )
    await LeadService(session).register_lead(user, username=callback.from_user.username)

    contact = await AppSettingsDAO(session).get("contact")
    if not contact:
        from app.core.config import settings
        contact = settings.ADMIN_CONTACT

    await callback.message.edit_text(
        t(lang, "contact_title"),
        reply_markup=kb_contact(contact, lang),
    )
    await callback.answer()
