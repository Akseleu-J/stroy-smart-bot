from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_PORTFOLIO_TEXTS, DEFAULT_PRICES
from app.database.models import (
    AppSettings, Booking, Calculation, Lead, Portfolio, Price, User,
)


class UserDAO:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get_or_create(self, telegram_id: int, name: str) -> User:
        r = await self._s.execute(select(User).where(User.telegram_id == telegram_id))
        user = r.scalar_one_or_none()
        if user is None:
            user = User(telegram_id=telegram_id, name=name)
            self._s.add(user)
            await self._s.flush()
        return user

    async def set_lang(self, telegram_id: int, lang: str) -> None:
        r = await self._s.execute(select(User).where(User.telegram_id == telegram_id))
        user = r.scalar_one_or_none()
        if user:
            user.lang = lang
            await self._s.flush()

    async def get_lang(self, telegram_id: int) -> str:
        r = await self._s.execute(
            select(User.lang).where(User.telegram_id == telegram_id)
        )
        return r.scalar_one_or_none() or "kz"

    async def count(self) -> int:
        r = await self._s.execute(select(func.count(User.id)))
        return r.scalar_one() or 0


class PriceDAO:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, service_type: str) -> int:
        r = await self._s.execute(
            select(Price.value).where(Price.service_type == service_type)
        )
        val = r.scalar_one_or_none()
        return int(val) if val is not None else DEFAULT_PRICES.get(service_type, 10_000)

    async def get_all(self) -> dict[str, int]:
        r = await self._s.execute(select(Price))
        rows = r.scalars().all()
        prices = dict(DEFAULT_PRICES)
        for row in rows:
            prices[row.service_type] = row.value
        return prices

    async def set(self, service_type: str, value: int) -> None:
        r = await self._s.execute(
            select(Price).where(Price.service_type == service_type)
        )
        price = r.scalar_one_or_none()
        if price is None:
            self._s.add(Price(service_type=service_type, value=value))
        else:
            price.value = value
        await self._s.flush()


class PortfolioDAO:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, ptype: str) -> Optional[Portfolio]:
        r = await self._s.execute(select(Portfolio).where(Portfolio.type == ptype))
        return r.scalar_one_or_none()

    async def get_all(self) -> list[Portfolio]:
        r = await self._s.execute(select(Portfolio))
        return list(r.scalars().all())

    async def get_text(self, ptype: str) -> str:
        port = await self.get(ptype)
        if port and port.text:
            return port.text
        return DEFAULT_PORTFOLIO_TEXTS.get(ptype, "")

    async def get_photo(self, ptype: str) -> Optional[str]:
        port = await self.get(ptype)
        return port.photo_id if port else None

    async def upsert(
        self,
        ptype: str,
        text: Optional[str] = None,
        photo_id: Optional[str] = None,
    ) -> None:
        r = await self._s.execute(select(Portfolio).where(Portfolio.type == ptype))
        port = r.scalar_one_or_none()
        if port is None:
            port = Portfolio(type=ptype)
            self._s.add(port)
        if text is not None:
            port.text = text
        if photo_id is not None:
            port.photo_id = photo_id
        await self._s.flush()


class CalculationDAO:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def create(
        self,
        user_id: int,
        service_type: str,
        volume: float,
        result_low: int,
        result_high: int,
    ) -> Calculation:
        calc = Calculation(
            user_id=user_id,
            service_type=service_type,
            volume=volume,
            result_low=result_low,
            result_high=result_high,
        )
        self._s.add(calc)
        await self._s.flush()
        return calc

    async def get_user_history(self, user_id: int, limit: int = 10) -> list[Calculation]:
        r = await self._s.execute(
            select(Calculation)
            .where(Calculation.user_id == user_id)
            .order_by(Calculation.created_at.desc())
            .limit(limit)
        )
        return list(r.scalars().all())

    async def count(self) -> int:
        r = await self._s.execute(select(func.count(Calculation.id)))
        return r.scalar_one() or 0

    async def count_period(self, since_days: int = 7) -> int:
        from datetime import datetime, timedelta, timezone
        since = datetime.now(timezone.utc) - timedelta(days=since_days)
        r = await self._s.execute(
            select(func.count(Calculation.id)).where(Calculation.created_at >= since)
        )
        return r.scalar_one() or 0


class LeadDAO:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def create(self, user_id: int) -> Lead:
        lead = Lead(user_id=user_id)
        self._s.add(lead)
        await self._s.flush()
        return lead

    async def count(self) -> int:
        r = await self._s.execute(select(func.count(Lead.id)))
        return r.scalar_one() or 0

    async def count_period(self, since_days: int = 7) -> int:
        from datetime import datetime, timedelta, timezone
        since = datetime.now(timezone.utc) - timedelta(days=since_days)
        r = await self._s.execute(
            select(func.count(Lead.id)).where(Lead.created_at >= since)
        )
        return r.scalar_one() or 0


class BookingDAO:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def create(self, user_id: int, date: str, time: str) -> Booking:
        booking = Booking(user_id=user_id, booking_date=date, booking_time=time)
        self._s.add(booking)
        await self._s.flush()
        return booking

    async def get_user_bookings(self, user_id: int) -> list[Booking]:
        r = await self._s.execute(
            select(Booking)
            .where(Booking.user_id == user_id)
            .order_by(Booking.created_at.desc())
            .limit(5)
        )
        return list(r.scalars().all())

    async def count_period(self, since_days: int = 7) -> int:
        from datetime import datetime, timedelta, timezone
        since = datetime.now(timezone.utc) - timedelta(days=since_days)
        r = await self._s.execute(
            select(func.count(Booking.id)).where(Booking.created_at >= since)
        )
        return r.scalar_one() or 0


class AppSettingsDAO:
    def __init__(self, session: AsyncSession) -> None:
        self._s = session

    async def get(self, key: str, default: str = "") -> str:
        r = await self._s.execute(
            select(AppSettings.value).where(AppSettings.key == key)
        )
        val = r.scalar_one_or_none()
        return val if val is not None else default

    async def set(self, key: str, value: str) -> None:
        r = await self._s.execute(
            select(AppSettings).where(AppSettings.key == key)
        )
        row = r.scalar_one_or_none()
        if row is None:
            self._s.add(AppSettings(key=key, value=value))
        else:
            row.value = value
        await self._s.flush()
