from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.database.models import Base

_engine: AsyncEngine | None = None
_factory: async_sessionmaker | None = None


async def init_db() -> None:
    global _engine, _factory
    _engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )
    _factory = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None


def get_factory() -> async_sessionmaker:
    if _factory is None:
        raise RuntimeError("БД инициализацияланбаған")
    return _factory
