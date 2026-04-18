"""
Мультиязычность: казахский / русский / английский.
Все строки интерфейса хранятся здесь.
"""
from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "kz": {
        "welcome": (
            "Сәлем, <b>{name}</b>! 👋\n\n"
            "Мен — <b>Dauren Qurylyss</b>\n"
            "компаниясының цифрлық көмекшісімін.\n\n"
            "🏗️ Монолитті құрылыс, фундамент,\n"
            "колонналар және қабырғалар.\n\n"
            "<b>Не қызықтырады?</b>"
        ),
        "main_menu":        "🏗️ <b>Dauren Qurylyss</b>\n\n<b>Не қызықтырады?</b>",
        "services_title":   "<b>🏗️ Біздің қызметтер</b>\n\nБарлық жұмыстарға 5 жыл кепілдік.\n\nҚандай қызмет қызықтырады?",
        "portfolio_title":  "<b>📸 Біздің жұмыстар</b>\n\nКатегория таңдаңыз:",
        "calc_start":       "<b>📈 AI Смета (Beta)</b>\n\nЖұмыс түрін таңдаңыз:",
        "calc_enter_vol":   "<b>{name}</b> таңдалды ✅\n\nКөлемді енгізіңіз <b>(м³)</b>:\n\n<i>Мысалы: 50 немесе 120.5</i>",
        "calc_error":       "❌ Дұрыс сан енгізіңіз\n<i>Мысалы: 50 немесе 120.5</i>",
        "contact_title":    "<b>📞 Консультация алу</b>\n\nМенеджеріміз <b>24 сағат ішінде</b> жауап береді.\n\n🕐 Жұмыс уақыты: 09:00 – 19:00\n📍 Алматы, Астана, Шымкент",
        "contact_btn":      "💬 Жазу",
        "history_empty":    "📋 Сіздің есептеулер тарихы бос.",
        "history_title":    "📋 <b>Есептеулер тарихы</b>\n\n",
        "history_item":     "🔧 {service} · {volume} м³\n💰 {low:,} – {high:,} ₸\n📅 {date}\n\n",
        "booking_start":    "<b>📅 Консультацияға жазылу</b>\n\nКүнді таңдаңыз:",
        "booking_time":     "Уақытты таңдаңыз:",
        "booking_confirm":  "<b>📅 Жазылу расталсын ба?</b>\n\n📆 Күн: <b>{date}</b>\n🕐 Уақыт: <b>{time}</b>",
        "booking_done":     "✅ Жазылу расталды!\n\n📆 <b>{date}</b> сағат <b>{time}</b>\nМенеджер сізге хабарласады.",
        "booking_cancel":   "❌ Жазылу болдырылмады.",
        "throttle":         "⏳ Тым жылдам. Бірнеше секунд күтіңіз.",
        "error":            "⚠️ Қате орын алды. Кейінірек қайталаңыз.",
        "photo_soon":       "\n\n<i>Фото жақында қосылады</i>",
        "back":             "◀️ Артқа",
        "cancel":           "❌ Болдырмау",
        "confirm":          "✅ Растау",
        "btn_services":     "🏗️ Қызметтер мен Бағалар",
        "btn_portfolio":    "📸 Біздің жұмыстар",
        "btn_calc":         "📈 AI Смета (Beta)",
        "btn_contact":      "📞 Консультация алу",
        "btn_history":      "📋 Менің тарихым",
        "btn_booking":      "📅 Жазылу",
        "btn_lang":         "🌐 Тіл / Язык / Language",
        "lang_chosen":      "✅ Тіл: Қазақша",
        "select_lang":      "🌐 Тіл таңдаңыз / Выберите язык / Choose language:",
    },
    "ru": {
        "welcome": (
            "Привет, <b>{name}</b>! 👋\n\n"
            "Я — цифровой помощник компании\n"
            "<b>Dauren Qurylyss</b>.\n\n"
            "🏗️ Монолитное строительство, фундамент,\n"
            "колонны и стены.\n\n"
            "<b>Что вас интересует?</b>"
        ),
        "main_menu":        "🏗️ <b>Dauren Qurylyss</b>\n\n<b>Что вас интересует?</b>",
        "services_title":   "<b>🏗️ Наши услуги</b>\n\nГарантия 5 лет на все работы.\n\nКакая услуга интересует?",
        "portfolio_title":  "<b>📸 Наши работы</b>\n\nВыберите категорию:",
        "calc_start":       "<b>📈 AI Смета (Beta)</b>\n\nВыберите тип работ:",
        "calc_enter_vol":   "<b>{name}</b> выбрано ✅\n\nВведите объём <b>(м³)</b>:\n\n<i>Например: 50 или 120.5</i>",
        "calc_error":       "❌ Введите корректное число\n<i>Например: 50 или 120.5</i>",
        "contact_title":    "<b>📞 Получить консультацию</b>\n\nМенеджер ответит <b>в течение 24 часов</b>.\n\n🕐 Режим работы: 09:00 – 19:00\n📍 Алматы, Астана, Шымкент",
        "contact_btn":      "💬 Написать",
        "history_empty":    "📋 История ваших расчётов пуста.",
        "history_title":    "📋 <b>История расчётов</b>\n\n",
        "history_item":     "🔧 {service} · {volume} м³\n💰 {low:,} – {high:,} ₸\n📅 {date}\n\n",
        "booking_start":    "<b>📅 Запись на консультацию</b>\n\nВыберите дату:",
        "booking_time":     "Выберите время:",
        "booking_confirm":  "<b>📅 Подтвердить запись?</b>\n\n📆 Дата: <b>{date}</b>\n🕐 Время: <b>{time}</b>",
        "booking_done":     "✅ Запись подтверждена!\n\n📆 <b>{date}</b> в <b>{time}</b>\nМенеджер свяжется с вами.",
        "booking_cancel":   "❌ Запись отменена.",
        "throttle":         "⏳ Слишком быстро. Подождите несколько секунд.",
        "error":            "⚠️ Произошла ошибка. Попробуйте позже.",
        "photo_soon":       "\n\n<i>Фото будет добавлено скоро</i>",
        "back":             "◀️ Назад",
        "cancel":           "❌ Отмена",
        "confirm":          "✅ Подтвердить",
        "btn_services":     "🏗️ Услуги и цены",
        "btn_portfolio":    "📸 Наши работы",
        "btn_calc":         "📈 AI Смета (Beta)",
        "btn_contact":      "📞 Консультация",
        "btn_history":      "📋 Моя история",
        "btn_booking":      "📅 Записаться",
        "btn_lang":         "🌐 Тіл / Язык / Language",
        "lang_chosen":      "✅ Язык: Русский",
        "select_lang":      "🌐 Тіл таңдаңыз / Выберите язык / Choose language:",
    },
    "en": {
        "welcome": (
            "Hello, <b>{name}</b>! 👋\n\n"
            "I'm the digital assistant of\n"
            "<b>Dauren Qurylyss</b> company.\n\n"
            "🏗️ Monolithic construction, foundation,\n"
            "columns and walls.\n\n"
            "<b>What are you interested in?</b>"
        ),
        "main_menu":        "🏗️ <b>Dauren Qurylyss</b>\n\n<b>What are you interested in?</b>",
        "services_title":   "<b>🏗️ Our Services</b>\n\n5-year warranty on all works.\n\nWhich service interests you?",
        "portfolio_title":  "<b>📸 Our Works</b>\n\nChoose category:",
        "calc_start":       "<b>📈 AI Estimate (Beta)</b>\n\nSelect work type:",
        "calc_enter_vol":   "<b>{name}</b> selected ✅\n\nEnter volume <b>(m³)</b>:\n\n<i>Example: 50 or 120.5</i>",
        "calc_error":       "❌ Enter a valid number\n<i>Example: 50 or 120.5</i>",
        "contact_title":    "<b>📞 Get Consultation</b>\n\nManager will reply <b>within 24 hours</b>.\n\n🕐 Working hours: 09:00 – 19:00\n📍 Almaty, Astana, Shymkent",
        "contact_btn":      "💬 Write",
        "history_empty":    "📋 Your calculation history is empty.",
        "history_title":    "📋 <b>Calculation History</b>\n\n",
        "history_item":     "🔧 {service} · {volume} m³\n💰 {low:,} – {high:,} ₸\n📅 {date}\n\n",
        "booking_start":    "<b>📅 Book a Consultation</b>\n\nSelect date:",
        "booking_time":     "Select time:",
        "booking_confirm":  "<b>📅 Confirm booking?</b>\n\n📆 Date: <b>{date}</b>\n🕐 Time: <b>{time}</b>",
        "booking_done":     "✅ Booking confirmed!\n\n📆 <b>{date}</b> at <b>{time}</b>\nManager will contact you.",
        "booking_cancel":   "❌ Booking cancelled.",
        "throttle":         "⏳ Too fast. Please wait a few seconds.",
        "error":            "⚠️ An error occurred. Please try again later.",
        "photo_soon":       "\n\n<i>Photo will be added soon</i>",
        "back":             "◀️ Back",
        "cancel":           "❌ Cancel",
        "confirm":          "✅ Confirm",
        "btn_services":     "🏗️ Services & Prices",
        "btn_portfolio":    "📸 Our Works",
        "btn_calc":         "📈 AI Estimate (Beta)",
        "btn_contact":      "📞 Consultation",
        "btn_history":      "📋 My History",
        "btn_booking":      "📅 Book",
        "btn_lang":         "🌐 Тіл / Язык / Language",
        "lang_chosen":      "✅ Language: English",
        "select_lang":      "🌐 Тіл таңдаңыз / Выберите язык / Choose language:",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    text = TRANSLATIONS.get(lang, TRANSLATIONS["kz"]).get(
        key,
        TRANSLATIONS["kz"].get(key, key)
    )
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text
