"""
Планировщик задач (APScheduler).
Каждое воскресенье в 20:00 отправляет еженедельный отчёт администраторам.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.logger import get_logger
from app.database.engine import get_factory
from app.services.analytics_service import AnalyticsService
from app.services.notification_service import NotificationService

logger = get_logger(__name__)

_scheduler: AsyncIOScheduler | None = None


async def _send_weekly_report() -> None:
    """Собирает статистику за неделю и отправляет всем администраторам."""
    try:
        async with get_factory()() as session:
            async with session.begin():
                svc   = AnalyticsService(session)
                stats = await svc.get_weekly_stats()
                text  = svc.format_weekly_report(stats)
        await NotificationService.weekly_report(text)
        logger.info("weekly_report_sent")
    except Exception as e:
        logger.error("weekly_report_error", error=str(e))


def start_scheduler() -> None:
    global _scheduler
    _scheduler = AsyncIOScheduler(timezone="Asia/Almaty")
    _scheduler.add_job(
        _send_weekly_report,
        trigger=CronTrigger(day_of_week="sun", hour=20, minute=0),
        id="weekly_report",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("scheduler_started")


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler:
        _scheduler.shutdown(wait=False)
        _scheduler = None
        logger.info("scheduler_stopped")
