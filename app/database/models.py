from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id:          Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int]      = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    name:        Mapped[str]      = mapped_column(String(255), nullable=False)
    role:        Mapped[str]      = mapped_column(String(50), default="user", nullable=False)
    lang:        Mapped[str]      = mapped_column(String(10), default="kz", nullable=False)
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    calculations: Mapped[list["Calculation"]] = relationship(back_populates="user", lazy="noload")
    leads:        Mapped[list["Lead"]]        = relationship(back_populates="user", lazy="noload")
    bookings:     Mapped[list["Booking"]]     = relationship(back_populates="user", lazy="noload")


class Calculation(Base):
    __tablename__ = "calculations"

    id:           Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:      Mapped[int]      = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    service_type: Mapped[str]      = mapped_column(String(50), nullable=False)
    volume:       Mapped[float]    = mapped_column(Float, nullable=False)
    result_low:   Mapped[int]      = mapped_column(Integer, nullable=False)
    result_high:  Mapped[int]      = mapped_column(Integer, nullable=False)
    created_at:   Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="calculations")


class Price(Base):
    __tablename__ = "prices"

    id:           Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_type: Mapped[str]      = mapped_column(String(50), unique=True, nullable=False)
    value:        Mapped[int]      = mapped_column(Integer, nullable=False)
    updated_at:   Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Portfolio(Base):
    __tablename__ = "portfolio"

    id:         Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    type:       Mapped[str]           = mapped_column(String(50), unique=True, nullable=False)
    text:       Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    photo_id:   Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    updated_at: Mapped[datetime]      = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Lead(Base):
    __tablename__ = "leads"

    id:         Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:    Mapped[int]      = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="leads")


class Booking(Base):
    __tablename__ = "bookings"

    id:           Mapped[int]      = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:      Mapped[int]      = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    booking_date: Mapped[str]      = mapped_column(String(20), nullable=False)
    booking_time: Mapped[str]      = mapped_column(String(10), nullable=False)
    status:       Mapped[str]      = mapped_column(String(20), default="confirmed", nullable=False)
    created_at:   Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="bookings")


class AppSettings(Base):
    __tablename__ = "app_settings"

    id:    Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key:   Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
