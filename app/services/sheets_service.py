from app.core.logger import get_logger

logger = get_logger(__name__)


class GoogleSheetsService:
    async def push_lead(self, telegram_id: int, name: str) -> None:
        logger.info("sheets_stub", telegram_id=telegram_id, name=name)
