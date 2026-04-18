from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import MARGIN_HIGH, MARGIN_LOW, SERVICE_NAMES
from app.database.dao import PriceDAO
from app.services.cache_service import CacheService


@dataclass
class EstimationResult:
    service_type: str
    service_name: str
    volume: float
    price_per_m3: int
    result_low: int
    result_high: int

    def format_text(self) -> str:
        return (
            "<b>📊 Смета нәтижесі / Результат сметы</b>\n\n"
            f"🔧 {self.service_name}\n"
            f"📐 {self.volume} м³\n"
            f"💰 {self.price_per_m3:,} ₸/м³\n\n"
            "━━━━━━━━━━━━━━━\n"
            f"<b>{self.result_low:,} ₸ — {self.result_high:,} ₸</b>\n"
            "━━━━━━━━━━━━━━━\n\n"
            "<i>Нақты баға брифингтен кейін анықталады.</i>"
        )


class EstimationService:
    """
    Бизнес-логика расчёта сметы.
    Использует Redis-кэш для цен, при промахе — читает из БД.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._dao   = PriceDAO(session)
        self._cache = CacheService()

    async def get_price(self, service_type: str) -> int:
        cached = await CacheService.get_prices()
        if cached and service_type in cached:
            return cached[service_type]
        return await self._dao.get(service_type)

    async def estimate(self, service_type: str, volume: float) -> EstimationResult:
        price_per_m3 = await self.get_price(service_type)
        base         = volume * price_per_m3
        return EstimationResult(
            service_type=service_type,
            service_name=SERVICE_NAMES.get(service_type, service_type),
            volume=volume,
            price_per_m3=price_per_m3,
            result_low=int(base * MARGIN_LOW),
            result_high=int(base * MARGIN_HIGH),
        )
