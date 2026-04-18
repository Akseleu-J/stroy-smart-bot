from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.database.dao import LeadDAO
from app.database.models import User
from app.services.notification_service import NotificationService
from app.services.sheets_service import GoogleSheetsService

logger = get_logger(__name__)


class LeadService:
    def __init__(self, session: AsyncSession) -> None:
        self._leads  = LeadDAO(session)
        self._sheets = GoogleSheetsService()

    async def register_lead(self, user: User, username: str | None = None) -> None:
        lead = await self._leads.create(user.id)
        logger.info("lead_created", user_id=user.telegram_id, lead_id=lead.id)
        await NotificationService.new_lead(username, user.name, user.telegram_id)
        await self._sheets.push_lead(telegram_id=user.telegram_id, name=user.name)
