from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.database.dao import BookingDAO
from app.database.models import User
from app.services.notification_service import NotificationService

logger = get_logger(__name__)


class BookingService:
    def __init__(self, session: AsyncSession) -> None:
        self._dao = BookingDAO(session)

    async def create_booking(
        self,
        user: User,
        date: str,
        time: str,
        username: str | None = None,
    ) -> None:
        booking = await self._dao.create(user.id, date, time)
        logger.info("booking_created", user_id=user.telegram_id, date=date, time=time)
        await NotificationService.new_booking(
            username, user.name, user.telegram_id, date, time
        )

    async def get_user_bookings(self, user_id: int) -> list:
        return await self._dao.get_user_bookings(user_id)
