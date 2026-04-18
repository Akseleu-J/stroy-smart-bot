from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dao import BookingDAO, CalculationDAO, LeadDAO, UserDAO


class AnalyticsService:
    def __init__(self, session: AsyncSession) -> None:
        self._users    = UserDAO(session)
        self._calcs    = CalculationDAO(session)
        self._leads    = LeadDAO(session)
        self._bookings = BookingDAO(session)

    async def get_stats(self) -> dict:
        return {
            "users":    await self._users.count(),
            "calcs":    await self._calcs.count(),
            "contacts": await self._leads.count(),
            "bookings": await self._bookings.count_period(9999),
        }

    async def get_weekly_stats(self) -> dict:
        return {
            "calcs_week":    await self._calcs.count_period(7),
            "leads_week":    await self._leads.count_period(7),
            "bookings_week": await self._bookings.count_period(7),
        }

    def format_stats(self, stats: dict) -> str:
        return (
            "<b>📊 Статистика</b>\n\n"
            f"🚀 Барлық пайдаланушылар: <b>{stats['users']}</b>\n"
            f"📈 Смета есептелді:       <b>{stats['calcs']}</b>\n"
            f"📞 Консультация сұрады:   <b>{stats['contacts']}</b>\n"
            f"📅 Жазылулар:             <b>{stats['bookings']}</b>"
        )

    def format_weekly_report(self, stats: dict) -> str:
        return (
            "📊 <b>Апталық есеп / Еженедельный отчёт</b>\n\n"
            f"📈 Смета: <b>{stats['calcs_week']}</b>\n"
            f"📞 Лидтер: <b>{stats['leads_week']}</b>\n"
            f"📅 Жазылулар: <b>{stats['bookings_week']}</b>"
        )
