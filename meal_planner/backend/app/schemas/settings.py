from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, field_validator


class SettingsRead(BaseModel):
    name: str
    default_servings: int
    timezone: str
    locale: str
    unit_system: str
    week_starts_on: int
    subtract_pantry: bool
    auto_shopping: bool
    preserve_checked: bool
    preserve_manual: bool
    auto_consume_pantry: bool


class SettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    default_servings: int | None = None
    timezone: str | None = None
    subtract_pantry: bool | None = None
    auto_shopping: bool | None = None
    preserve_checked: bool | None = None
    preserve_manual: bool | None = None
    auto_consume_pantry: bool | None = None

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned or len(cleaned) > 80:
            raise ValueError("De naam moet tussen 1 en 80 tekens zijn.")
        return cleaned

    @field_validator("timezone")
    @classmethod
    def known_timezone(cls, value: str | None) -> str | None:
        if value is None:
            return None
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError("Onbekende tijdzone.") from exc
        return value

    @field_validator("default_servings")
    @classmethod
    def servings_range(cls, value: int | None) -> int | None:
        if value is None:
            return None
        if value < 1 or value > 24:
            raise ValueError("Het aantal personen moet tussen 1 en 24 liggen.")
        return value
