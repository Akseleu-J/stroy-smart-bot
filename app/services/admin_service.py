from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import PORTFOLIO_KEYS
from app.database.dao import AppSettingsDAO, PortfolioDAO, PriceDAO
from app.services.cache_service import CacheService


class AdminService:
    def __init__(self, session: AsyncSession) -> None:
        self._prices    = PriceDAO(session)
        self._portfolio = PortfolioDAO(session)
        self._settings  = AppSettingsDAO(session)

    async def get_all_prices(self) -> dict[str, int]:
        cached = await CacheService.get_prices()
        if cached:
            return cached
        prices = await self._prices.get_all()
        await CacheService.set_prices(prices)
        return prices

    async def set_price(self, service_type: str, value: int) -> tuple[int, int]:
        old = await self._prices.get(service_type)
        await self._prices.set(service_type, value)
        await CacheService.invalidate_prices()
        return old, value

    async def get_contact(self) -> str:
        return await self._settings.get("contact", settings.ADMIN_CONTACT)

    async def set_contact(self, contact: str) -> tuple[str, str]:
        old = await self.get_contact()
        await self._settings.set("contact", contact)
        return old, contact

    async def get_portfolio_status(self) -> dict[str, bool]:
        rows = await self._portfolio.get_all()
        m = {r.type: bool(r.photo_id) for r in rows}
        return {k: m.get(k, False) for k in PORTFOLIO_KEYS}

    async def set_photo(self, ptype: str, photo_id: str) -> None:
        await self._portfolio.upsert(ptype, photo_id=photo_id)

    async def set_portfolio_text(self, ptype: str, text: str) -> None:
        await self._portfolio.upsert(ptype, text=text)
