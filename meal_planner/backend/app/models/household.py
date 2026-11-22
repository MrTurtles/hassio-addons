import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Household(Base):
    __tablename__ = "households"
    __table_args__ = (
        CheckConstraint(
            "default_servings >= 1 AND default_servings <= 24",
            name="ck_household_servings",
        ),
        CheckConstraint(
            "week_starts_on >= 1 AND week_starts_on <= 7",
            name="ck_household_week_start",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(80))
    timezone: Mapped[str] = mapped_column(String(64))
    locale: Mapped[str] = mapped_column(String(16), default="nl")
    default_servings: Mapped[int] = mapped_column(Integer)
    week_starts_on: Mapped[int] = mapped_column(Integer, default=1)
    unit_system: Mapped[str] = mapped_column(String(16), default="metric")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class HouseholdSettings(Base):
    __tablename__ = "household_settings"

    household_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("households.id", ondelete="CASCADE"), primary_key=True
    )
    subtract_pantry: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_shopping: Mapped[bool] = mapped_column(Boolean, default=True)
    preserve_checked: Mapped[bool] = mapped_column(Boolean, default=True)
    preserve_manual: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_consume_pantry: Mapped[bool] = mapped_column(Boolean, default=False)
