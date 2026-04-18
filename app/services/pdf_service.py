from app.core.logger import get_logger
from app.services.estimation import EstimationResult

logger = get_logger(__name__)


class PDFService:
    async def generate_quote(self, result: EstimationResult, user_name: str) -> bytes:
        logger.info("pdf_stub", service=result.service_type, volume=result.volume)
        return b""
