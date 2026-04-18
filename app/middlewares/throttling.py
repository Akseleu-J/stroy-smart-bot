import time
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.core.config import settings
from app.core.logger import get_logger
from app.locales.translations import t

logger = get_logger(__name__)
_last: dict[int, float] = {}


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._rate = settings.THROTTLE_RATE

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        uid = event.from_user.id
        now = time.monotonic()
        if now - _last.get(uid, 0.0) < self._rate:
            logger.info("throttled", user_id=uid)
            await event.answer(t("kz", "throttle"))
            return

        _last[uid] = now
        return await handler(event, data)
