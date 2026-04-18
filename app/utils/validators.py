from pydantic import BaseModel, field_validator


class VolumeInput(BaseModel):
    raw: str

    @field_validator("raw")
    @classmethod
    def check(cls, v: str) -> str:
        n = v.strip().replace(",", ".")
        try:
            val = float(n)
        except ValueError:
            raise ValueError("invalid")
        if val <= 0 or val > 100_000:
            raise ValueError("out_of_range")
        return n

    @property
    def value(self) -> float:
        return float(self.raw.replace(",", "."))


class PriceInput(BaseModel):
    raw: str

    @field_validator("raw")
    @classmethod
    def check(cls, v: str) -> str:
        n = v.strip().replace(" ", "").replace(",", "")
        try:
            val = int(n)
        except ValueError:
            raise ValueError("invalid")
        if val <= 0:
            raise ValueError("invalid")
        return n

    @property
    def value(self) -> int:
        return int(self.raw.replace(" ", "").replace(",", ""))


class ContactInput(BaseModel):
    raw: str

    @field_validator("raw")
    @classmethod
    def check(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("empty")
        return s if s.startswith("@") else "@" + s

    @property
    def value(self) -> str:
        r = self.raw.strip()
        return r if r.startswith("@") else "@" + r
