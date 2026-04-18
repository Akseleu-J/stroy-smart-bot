from typing import Optional

from aiogram import Bot

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

_bot: Optional[Bot] = None


def set_bot(bot: Bot) -> None:
    global _bot
    _bot = bot


class NotificationService:
    """Отправляет уведомления администраторам в реальном времени."""

    @staticmethod
    async def new_lead(
        username: Optional[str],
        name: str,
        telegram_id: int,
    ) -> None:
        if not _bot:
            return
        who  = f"@{username}" if username else name
        text = (
            "🔔 <b>Жаңа лид / Новый лид</b>\n\n"
            f"👤 {who}\n"
            f"🆔 <code>{telegram_id}</code>\n\n"
            "📞 Клиент консультация сұрады."
        )
        await NotificationService._send(text)

    @staticmethod
    async def new_booking(
        username: Optional[str],
        name: str,
        telegram_id: int,
        date: str,
        time: str,
    ) -> None:
        if not _bot:
            return
        who  = f"@{username}" if username else name
        text = (
            "📅 <b>Жаңа жазылу / Новая запись</b>\n\n"
            f"👤 {who}\n"
            f"🆔 <code>{telegram_id}</code>\n"
            f"📆 Күн: <b>{date}</b>\n"
            f"🕐 Уақыт: <b>{time}</b>"
        )
        await NotificationService._send(text)

    @staticmethod
    async def weekly_report(text: str) -> None:
        if not _bot:
            return
        await NotificationService._send(text)

    @staticmethod
    async def _send(text: str) -> None:
        for admin_id in settings.ADMIN_IDS:
            try:
                await _bot.send_message(admin_id, text, parse_mode="HTML")
            except Exception as e:
                logger.error("notify_fail", admin_id=admin_id, error=str(e))
