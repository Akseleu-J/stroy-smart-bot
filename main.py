import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from app.core.logger import configure_logging, get_logger
from app.database.engine import close_db, init_db
from app.handlers import admin, common, fallback, user
from app.middlewares.db_session import DBSessionMiddleware
from app.middlewares.error import ErrorMiddleware
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.throttling import ThrottlingMiddleware
from app.services.cache_service import close_redis, init_redis
from app.services.notification_service import set_bot
from app.services.scheduler import start_scheduler, stop_scheduler

logger = get_logger(__name__)


async def main() -> None:
    configure_logging()
    logger.info("startup")

    # ── БД ───────────────────────────────────────────────────────
    await init_db()
    logger.info("db_ready")

    # ── Redis (кэш цен, опционально) ─────────────────────────────
    await init_redis()

    # ── Бот и диспетчер ──────────────────────────────────────────
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Регистрируем бот для уведомлений
    set_bot(bot)

    # FSM storage — MemoryStorage (стабильно без Redis)
    # Для продакшн с Redis:
    #   from aiogram.fsm.storage.redis import RedisStorage
    #   storage = RedisStorage.from_url(settings.REDIS_URL)
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    # ── Middleware (порядок важен) ─────────────────────────────────
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.message.middleware(ErrorMiddleware())
    dp.callback_query.middleware(ErrorMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(DBSessionMiddleware())
    dp.callback_query.middleware(DBSessionMiddleware())

    # ── Роутеры (порядок важен: admin раньше user) ────────────────
    dp.include_router(admin.router)
    dp.include_router(common.router)
    dp.include_router(user.router)
    dp.include_router(fallback.router)

    # ── Планировщик еженедельных отчётов ─────────────────────────
    start_scheduler()

    # ── Старт polling ─────────────────────────────────────────────
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("polling_start")

    try:
        await dp.start_polling(bot)
    finally:
        logger.info("shutdown")
        stop_scheduler()
        await close_redis()
        await close_db()
        await bot.session.close()
        logger.info("shutdown_complete")


if __name__ == "__main__":
    asyncio.run(main())
