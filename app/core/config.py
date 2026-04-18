from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    DATABASE_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"
    ADMIN_IDS: List[int] = []
    ADMIN_CONTACT: str = "@admin"
    THROTTLE_RATE: float = 1.0
    PRICE_CACHE_TTL: int = 300

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        if isinstance(v, int):
            return [v]
        return v

    def default_prices(self) -> dict[str, int]:
        return {
            "foundation": 10_000,
            "columns":    12_000,
            "walls":       8_500,
        }


settings = Settings()
