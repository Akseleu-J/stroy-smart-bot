from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.config import settings
from app.core.constants import BOOKING_TIME_SLOTS
from app.locales.translations import t


def kb_main(lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_services"),  callback_data="services")],
        [InlineKeyboardButton(text=t(lang, "btn_portfolio"), callback_data="portfolio")],
        [InlineKeyboardButton(text=t(lang, "btn_calc"),      callback_data="calc")],
        [InlineKeyboardButton(text=t(lang, "btn_booking"),   callback_data="booking")],
        [InlineKeyboardButton(text=t(lang, "btn_history"),   callback_data="history")],
        [InlineKeyboardButton(text=t(lang, "btn_contact"),   callback_data="contact")],
        [InlineKeyboardButton(text=t(lang, "btn_lang"),      callback_data="select_lang")],
    ])


def kb_services(lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪨 Фундамент",  callback_data="svc:foundation")],
        [InlineKeyboardButton(text="🏛️ Колонналар", callback_data="svc:columns")],
        [InlineKeyboardButton(text="🧱 Қабырғалар", callback_data="svc:walls")],
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="back_main")],
    ])


def kb_portfolio(lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪨 Бетон жұмыстары",   callback_data="port:concrete")],
        [InlineKeyboardButton(text="🧱 Кірпіш қалау",      callback_data="port:brick")],
        [InlineKeyboardButton(text="🎨 Отделка жұмыстары", callback_data="port:finish")],
        [InlineKeyboardButton(text=t(lang, "back"),         callback_data="back_main")],
    ])


def kb_calc_type(lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪨 Фундамент",   callback_data="ctype:foundation")],
        [InlineKeyboardButton(text="🏛️ Колонналар",  callback_data="ctype:columns")],
        [InlineKeyboardButton(text="🧱 Қабырғалар",  callback_data="ctype:walls")],
        [InlineKeyboardButton(text=t(lang, "cancel"), callback_data="back_main")],
    ])


def kb_after_calc(lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_contact"), callback_data="contact")],
        [InlineKeyboardButton(text="🔄 Қайта есептеу",    callback_data="calc")],
        [InlineKeyboardButton(text=t(lang, "back"),        callback_data="back_main")],
    ])


def kb_service_detail(lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_calc"),    callback_data="calc")],
        [InlineKeyboardButton(text=t(lang, "btn_contact"), callback_data="contact")],
        [InlineKeyboardButton(text=t(lang, "back"),        callback_data="services")],
    ])


def kb_portfolio_detail(lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_contact"), callback_data="contact")],
        [InlineKeyboardButton(text=t(lang, "back"),        callback_data="portfolio")],
    ])


def kb_contact(contact: str, lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t(lang, "contact_btn"),
            url=f"https://t.me/{contact.lstrip('@')}",
        )],
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="back_main")],
    ])


def kb_lang() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="lang:kz")],
        [InlineKeyboardButton(text="🇷🇺 Русский",  callback_data="lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English",  callback_data="lang:en")],
    ])


def kb_booking_dates(lang: str = "kz") -> InlineKeyboardMarkup:
    """Показывает ближайшие 7 дней для бронирования."""
    today = date.today()
    rows  = []
    for i in range(1, 8):
        d     = today + timedelta(days=i)
        label = d.strftime("%d.%m.%Y (%A)")
        rows.append([InlineKeyboardButton(
            text=label,
            callback_data=f"bdate:{d.isoformat()}",
        )])
    rows.append([InlineKeyboardButton(text=t(lang, "cancel"), callback_data="back_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_booking_times(selected_date: str, lang: str = "kz") -> InlineKeyboardMarkup:
    """Показывает доступные слоты времени."""
    rows = []
    row  = []
    for slot in BOOKING_TIME_SLOTS:
        row.append(InlineKeyboardButton(
            text=slot,
            callback_data=f"btime:{selected_date}:{slot}",
        ))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text=t(lang, "back"), callback_data="booking")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_booking_confirm(lang: str = "kz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "confirm"), callback_data="book:confirm")],
        [InlineKeyboardButton(text=t(lang, "cancel"),  callback_data="booking")],
    ])
