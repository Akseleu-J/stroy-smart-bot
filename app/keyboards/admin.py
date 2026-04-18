from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.constants import PORTFOLIO_KEYS, PORTFOLIO_NAMES, SERVICE_NAMES


def kb_admin_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Бағаларды өзгерту",  callback_data="adm:prices")],
        [InlineKeyboardButton(text="📸 Портфолио — фото",    callback_data="adm:photos")],
        [InlineKeyboardButton(text="📝 Портфолио — мәтін",   callback_data="adm:texts")],
        [InlineKeyboardButton(text="📞 Контакт өзгерту",     callback_data="adm:contact")],
        [InlineKeyboardButton(text="📊 Статистика",           callback_data="adm:stats")],
        [InlineKeyboardButton(text="❌ Шығу",                 callback_data="adm:exit")],
    ])


def kb_admin_prices(prices: dict[str, int]) -> InlineKeyboardMarkup:
    rows = []
    for key, name in SERVICE_NAMES.items():
        rows.append([InlineKeyboardButton(
            text=f"{name}: {prices.get(key, 0):,} ₸/м³",
            callback_data=f"adm:setprice:{key}",
        )])
    rows.append([InlineKeyboardButton(text="◀️ Артқа", callback_data="adm:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_admin_photos(status: dict[str, bool]) -> InlineKeyboardMarkup:
    rows = []
    for key in PORTFOLIO_KEYS:
        icon = "✅" if status.get(key) else "❌"
        rows.append([InlineKeyboardButton(
            text=f"{icon} {PORTFOLIO_NAMES[key]}",
            callback_data=f"adm:photo:{key}",
        )])
    rows.append([InlineKeyboardButton(text="◀️ Артқа", callback_data="adm:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_admin_texts() -> InlineKeyboardMarkup:
    rows = []
    for key in PORTFOLIO_KEYS:
        rows.append([InlineKeyboardButton(
            text=f"✏️ {PORTFOLIO_NAMES[key]}",
            callback_data=f"adm:text:{key}",
        )])
    rows.append([InlineKeyboardButton(text="◀️ Артқа", callback_data="adm:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_admin_back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Артқа", callback_data="adm:back")]
    ])
