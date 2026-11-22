import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.household import Household, HouseholdSettings
from app.schemas.settings import SettingsRead, SettingsUpdate


def seed_household(session: Session) -> Household:
    existing = session.scalar(select(Household))
    if existing is not None:
        return existing
    now = datetime.now(UTC)
    household = Household(
        id=uuid.uuid4(),
        name="Huishouden",
        timezone="Europe/Amsterdam",
        locale="nl",
        default_servings=2,
        week_starts_on=1,
        unit_system="metric",
        created_at=now,
        updated_at=now,
    )
    session.add(household)
    session.add(HouseholdSettings(household_id=household.id))
    session.commit()
    return household


def read_settings(session: Session) -> SettingsRead:
    household, preferences = _load(session)
    return _to_read(household, preferences)


def update_settings(session: Session, payload: SettingsUpdate) -> SettingsRead:
    household, preferences = _load(session)
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in changes.items():
        if hasattr(household, field):
            setattr(household, field, value)
        else:
            setattr(preferences, field, value)
    if changes:
        household.updated_at = datetime.now(UTC)
        session.commit()
        session.refresh(household)
        session.refresh(preferences)
    return _to_read(household, preferences)


def household_count(session: Session) -> int:
    return int(session.scalar(select(func.count()).select_from(Household)) or 0)


def _load(session: Session) -> tuple[Household, HouseholdSettings]:
    household = session.scalar(select(Household))
    if household is None:
        household = seed_household(session)
    preferences = session.get(HouseholdSettings, household.id)
    if preferences is None:
        preferences = HouseholdSettings(household_id=household.id)
        session.add(preferences)
        session.commit()
    return household, preferences


def _to_read(household: Household, preferences: HouseholdSettings) -> SettingsRead:
    return SettingsRead(
        name=household.name,
        default_servings=household.default_servings,
        timezone=household.timezone,
        locale=household.locale,
        unit_system=household.unit_system,
        week_starts_on=household.week_starts_on,
        subtract_pantry=preferences.subtract_pantry,
        auto_shopping=preferences.auto_shopping,
        preserve_checked=preferences.preserve_checked,
        preserve_manual=preferences.preserve_manual,
        auto_consume_pantry=preferences.auto_consume_pantry,
    )
