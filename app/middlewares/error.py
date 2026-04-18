from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.core.logger import get_logger
from app.locales.translations import t

logger = get_logger(__name__)


class ErrorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as exc:
            logger.error("unhandled", error=str(exc), exc_info=True)
            try:
                if isinstance(event, Message):
                    await event.answer(t("kz", "error"))
                elif isinstance(event, CallbackQuery):
                    await event.message.answer(t("kz", "error"))
                    await event.answer()
            except Exception:
                pass
