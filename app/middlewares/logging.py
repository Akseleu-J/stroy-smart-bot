from typing import Any, Awaitable, Callable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.core.logger import new_trace_id

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        trace_id = new_trace_id()
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(trace_id=trace_id)

        uid  = None
        kind = "unknown"
        if isinstance(event, Message):
            uid  = event.from_user.id
            kind = f"msg:{event.text or event.content_type}"
        elif isinstance(event, CallbackQuery):
            uid  = event.from_user.id
            kind = f"cb:{event.data}"

        logger.info("in",  kind=kind, uid=uid)
        result = await handler(event, data)
        logger.info("out", kind=kind, uid=uid)
        return result
